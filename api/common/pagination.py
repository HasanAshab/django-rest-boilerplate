from rest_framework.pagination import BasePagination as Pagination


class BasePagination(Pagination):
    page_size_query_param = 'page_size'
