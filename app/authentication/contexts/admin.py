from ..base import BaseAuthContext


class AdminAuthContext(BaseAuthContext):
	session_key = "admin"
	route_url = "/admin/"
	session_fields = ("name", "email", "id", "created_at")