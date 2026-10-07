from ..base import BaseAuthContext


class UserAuthContext(BaseAuthContext):
	session_key = "user"
	route_url = "/"
	session_fields = ("name", "email", "id", "created_at", "bio", "lock", "code")