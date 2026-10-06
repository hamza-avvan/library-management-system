from __future__ import annotations
from dataclasses import dataclass

from app.extensions.mailer import Mailer
from app.extensions.scheduler import Scheduler
from app.database.dao import DAO


@dataclass(frozen=True)
class ApplicationServices:
    dao: DAO
    mailer: Mailer
    scheduler: Scheduler


_services: ApplicationServices | None = None


def configure_services(dao: DAO, mailer: Mailer, scheduler: Scheduler) -> None:
    global _services
    _services = ApplicationServices(dao=dao, mailer=mailer, scheduler=scheduler)


def get_services() -> ApplicationServices:
    if _services is None:
        raise RuntimeError("Application services have not been configured")
    return _services
