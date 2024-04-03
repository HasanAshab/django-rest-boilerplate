# pagination.py
from rest_framework.pagination import CursorPagination
from api.common.pagination import DynamicLimitPagination


class UserCursorPagination(DynamicLimitPagination, CursorPagination):
    ordering = 'username'  # Specify the field you want to use for sorting
    