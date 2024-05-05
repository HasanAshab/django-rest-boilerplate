from http.client import responses

# from django.conf import settings
from rest_framework.renderers import JSONRenderer as DefaultJSONRenderer

# from .response import ImmutableResponse


class ResponseStandardizer:
    def __init__(self, view):
        self.view = view

    def should_standardize(self):
        pagination = getattr(
            self.view,
            "pagination_class",
            None,
        )
        should_strandardize = getattr(
            self.view,
            "should_strandardize",
            None,
        )

        if should_strandardize is not None:
            return should_strandardize

        # if not settings.WRAP_PAGINATED_RESPONSE and pagination is not None:
        if pagination is not None:
            return False

        return True

    def get_wrapper_key(self):
        # return getattr(
        #     self.view,
        #     "wrapper_key",
        #     settings.DEFFAULT_WRAPPER_KEY
        # )
        return getattr(self.view, "wrapper_key", "data")

    def get_wrapping_excluded_fields(self):
        # return getattr(
        #     self.view,
        #     "wrapping_excluded_fields",
        #     settings.DEFFAULT_WRAPPING_EXCLUDED_FIELDS,
        # )
        return getattr(self.view, "wrapping_excluded_fields", ["links"])

    def get_standard_message(self, response):
        return responses[response.status_code]

    def is_successful_response(self, response):
        return 199 < response.status_code < 400

    def standardize(self, response):
        wrapper_key = self.get_wrapper_key()
        is_successful = self.is_successful_response(response)
        standardized_data = (
            {} if response.data is None else response.data.copy()
        )

        if isinstance(standardized_data, str):
            standardized_data = {"message": standardized_data}
        elif is_successful:
            unwrapped_data = {
                field: standardized_data.pop(field, None)
                for field in self.get_wrapping_excluded_fields()
                if field is not None
            }
            standardized_data = {
                **unwrapped_data,
                wrapper_key: standardized_data,
            }

        if "success" not in standardized_data:
            standardized_data["success"] = is_successful
        if "message" not in standardized_data:
            standardized_data["message"] = self.get_standard_message(response)

        return standardized_data


class StandardizedJSONRenderer(DefaultJSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if not renderer_context:
            return super().render(data, accepted_media_type, renderer_context)

        response_standardizer = ResponseStandardizer(renderer_context["view"])
        if response_standardizer.should_standardize():
            data = response_standardizer.standardize(
                renderer_context["response"]
            )

        return super().render(data, accepted_media_type, renderer_context)
