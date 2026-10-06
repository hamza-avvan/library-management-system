# DAO and Dependency Refactor Proposal

## Goal

Make database dependencies easy to follow, reduce hidden behavior, and keep responsibilities clear as the application grows. Preserve the existing Flask routes and application behavior while simplifying how the app creates and supplies database access.

This proposal focuses on architecture and safe migration. It does not claim a measured runtime speedup; its expected benefits are maintainability, safer SQL, and easier testing.

## Current State

The current dependency path is difficult to read because several layers and names overlap:

1. `app/__init__.py` imports the `DAO` class, then assigns an instance back to the same name.
2. `DAO` wraps a `DBDAO` instance.
3. `DBDAO` subclasses `DB`, shallow-copies itself for each repository, and stores repositories as `book`, `reservation`, `user`, and `admin`.
4. Each repository sets a mutable `table` attribute, and `DB.query()` replaces `@table` in SQL strings.
5. Controllers retrieve a global service object and pass the whole DAO container to managers. Managers then reach through paths such as `DAO.db.admin`.

The design works, but understanding a query's target table or a manager's dependencies requires following multiple levels of indirection. The class/instance name collision and uppercase `DAO` constructor arguments add avoidable confusion. Some repositories also interpolate values directly into SQL.

## Proposed Structure

```text
Flask composition root
  creates Database
  creates repositories using Database
  creates managers using only their required repositories
  registers blueprints

Controllers -> Managers -> Repositories -> Database -> MySQL
```

### Database adapter

Keep one small `Database` abstraction responsible for the Flask-MySQL connection, parameterized query execution, and transaction boundaries. Repositories receive the same adapter; there is no need to shallow-copy the adapter to select a table.

The database adapter should:

- execute SQL with bound parameters, never by formatting user values into SQL;
- expose explicit commit/rollback or a transaction context manager;
- avoid mutable table state and `@table` text replacement;
- keep connection setup in one location.

### Repositories

Use one repository per persistence responsibility, for example `BookRepository`, `UserRepository`, `AdminRepository`, and `ReservationRepository`. Each query names its table explicitly. Repository methods should be specific and understandable, such as `get_by_id`, `get_by_email`, `search`, and `update_profile`.

Avoid generic methods that construct SQL from arbitrary field names unless those identifiers are strictly allowlisted. SQL parameters protect values, but cannot parameterize table or column identifiers.

### Repository container and composition

If a container is useful, give it a descriptive name such as `Repositories` or `RepositoryRegistry`, with lower-case fields such as `books`, `users`, `admins`, and `reservations`. It should only group repository instances; it should not execute queries or select tables.

Use distinct names for classes and instances. For example, import `DAO` as a class (or rename it to `RepositoryRegistry`) and store its instance in a lower-case variable. Preferably remove the extra `DAO -> DBDAO -> DB` wrapper chain once repository construction is straightforward.

### Managers

Managers should depend on the repository interfaces they actually use, not on the whole container:

- `BookManager(book_repository)`
- `UserManager(user_repository)`
- `AdminManager(admin_repository)`
- `ReservationManager(reservation_repository)`

If an application workflow needs more than one repository, inject those specific repositories. Reservation logic must keep its inventory update and reservation insert within one transaction.

### Controllers and application initialization

Controllers should continue to handle HTTP concerns: request parsing, route decorators, session-derived identity, template/JSON responses, and redirects. They call managers and should not issue SQL.

Create database, repository, and manager instances in one composition root. Do not make every manager import a global DAO. The current `get_services()` global can be retained during an initial migration, but its fields should be clearly named and its initialization order should remain explicit. A Flask application factory may improve testability later, but it is optional and should not be bundled into the first DAO cleanup unless necessary to preserve import behavior.

## SQL and Transaction Safety

Parameterize every query value using the database driver's placeholders. Review all repository methods, especially book search/get/delete, user/admin lookups, inserts, and dynamic update/delete methods. Do not use `json.dumps` as SQL escaping.

The reservation write must be atomic:

1. Decrement inventory only when the book has available copies.
2. Insert the reservation.
3. Commit both changes together.
4. Roll back if either operation fails.

Keep unavailable inventory and duplicate reservation outcomes explicit. The controller should translate application outcomes to user-facing responses; the repository should not return HTTP messages.

## Migration Plan

1. **Clarify names and current wiring.** Rename class/instance variables so each imported type and constructed object has a distinct, descriptive name. Document the composition root.
2. **Introduce the simple database adapter API.** Add parameterized `execute` and explicit transaction handling without changing every query at once.
3. **Remove hidden table selection.** Update repositories to use explicit table names; eliminate `copy(self)`, mutable `table`, and `@table` replacement.
4. **Convert SQL safely.** Parameterize all values and replace generic dynamic update/delete construction with specific methods or identifier allowlists.
5. **Narrow manager dependencies.** Inject only the repositories each manager needs; update controller wiring while preserving routes and response behavior.
6. **Validate incrementally.** Run syntax/type/lint checks available in the repo, add focused tests for repository/manager behavior where practical, and report any checks requiring a live MySQL instance.

Each phase should be a small reviewable change. Do not combine unrelated frontend or authentication redesigns with this work.

## Acceptance Criteria

- The path from app startup to a manager's repository dependency is explicit and uses descriptive names.
- Managers receive only the dependencies they use; managers do not import or discover global DAO state.
- Repositories do not depend on a mutable table field or `@table` substitution.
- SQL values are bound parameters throughout the touched repositories.
- Dynamic SQL identifiers are fixed or allowlisted.
- Reservation inventory updates and inserts are atomic, with rollback on failure.
- Existing endpoints, templates, and response contracts remain unchanged unless a separately justified bug fix is required.
- Relevant static checks and tests pass; unavailable integration checks are identified clearly.
