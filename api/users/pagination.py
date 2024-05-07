from rest_framework.pagination import (
    CursorPagination,
)
from drf_pagination_meta_wrap.mixins import (
    WrapPaginationMetadataMixin,
)


class UserPagination(WrapPaginationMetadataMixin, CursorPagination):
    ordering = "date_joined"
