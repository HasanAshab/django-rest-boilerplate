from rest_framework.pagination import BasePagination


class DynamicLimitPagination(BasePagination):
    
    def paginate_queryset(self, queryset, request, view=None):
        self.page_size = int(request.query_params.get('limit', self.page_size))
        return super().paginate_queryset(queryset, request, view)