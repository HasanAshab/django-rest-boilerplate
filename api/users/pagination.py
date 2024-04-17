# pagination.py
from rest_framework.pagination import CursorPagination
from api.common.pagination import BasePagination


class UserCursorPagination(BasePagination, CursorPagination):
    ordering = "date_joined"
