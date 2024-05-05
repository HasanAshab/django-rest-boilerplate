from http.client import responses

# from django.conf import settings
from rest_framework.renderers import JSONRenderer as DefaultJSONRenderer

# from .response import ImmutableResponse


# class ResponseStandardizer:
#     def should_format(self, renderer_context):
#         response = renderer_context["response"]
#         pagination = getattr(
#             renderer_context["view"],
#             "pagination_class",
#             None,
#         )

#         if isinstance(response, ImmutableResponse):
#             return False

#         # if not settings.WRAP_PAGINATED_RESPONSE and pagination is not None:
#         if pagination is not None:
#             return False

#         return True

#     def standardize(self, data):


class StandardizedJSONRenderer(DefaultJSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if not renderer_context:
            return super().render(data, accepted_media_type, renderer_context)

        if self._should_modify_data(renderer_context):
            data = self.standardize_response_data(data, renderer_context)
        return super().render(data, accepted_media_type, renderer_context)

    def _get_wrapper_key(self, renderer_context):
        view = renderer_context["view"]
        # return getattr(view, "wrapper_key", settings.DEFFAULT_WRAPPER_KEY)
        return getattr(view, "wrapper_key", "data")

    def _is_successful_response(self, renderer_context):
        response = renderer_context["response"]
        return 199 < response.status_code < 400

    def _get_standard_message(self, renderer_context):
        response = renderer_context["response"]
        return responses[response.status_code]

    def standardize_response_data(self, data, renderer_context):
        wrapper_key = self._get_wrapper_key(renderer_context)
        is_successful = self._is_successful_response(renderer_context)
        standardized_data = {} if data is None else data.copy()

        if isinstance(standardized_data, str):
            standardized_data = {"message": standardized_data}
        elif is_successful:
            standardized_data = {wrapper_key: standardized_data}
        standardized_data["success"] = is_successful
        standardized_data["message"] = data.get(
            "message",
            self._get_standard_message(renderer_context),
        )

        return standardized_data
