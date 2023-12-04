from rest_framework.filters import SearchFilter


class ServiceNameSearchFilter(SearchFilter):
    """Filter partial match searches by search_param."""

    search_param = 'service_name'

    def get_search_fields(self, view, request):
        if request.query_params.get(self.search_param):
            return [self.search_param]
        return super().get_search_fields(view, request)
