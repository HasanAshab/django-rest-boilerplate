# pagination.py
from rest_framework.pagination import CursorPagination
from api.common.pagination import DynamicLimitPagination


class UserCursorPagination(DynamicLimitPagination, CursorPagination):
    ordering = 'date_joined'