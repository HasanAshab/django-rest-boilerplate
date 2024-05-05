from drf_standardized_errors.openapi import AutoSchema as BaseAutoSchema
from drf_spectacular.utils import OpenApiResponse
from api.common.renderers import ResponseStandardizer


class AutoSchema(BaseAutoSchema):
    def _get_response_for_code(
        self, serializer, status_code, media_types=None, direction="response"
    ):
        response_standardizer = ResponseStandardizer(self._view)
        response = super()._get_response_for_code(
            serializer, status_code, media_types, direction
        )
        if not response_standardizer.should_standardize():
            return response
        if isinstance(serializer, OpenApiResponse):
            serializer = serializer.response

        if not (content := response.get("content")):
            return response
        if "application/json" not in content:
            return response

        schema = content["application/json"]["schema"]

        reference = schema.get("$ref", schema.get("items", {}).get("$ref"))
        if not reference:
            return response

        if "ErrorResponse" in reference:
            return response

        formatted_schema = self.format_response_schema(schema)
        content["application/json"]["schema"] = formatted_schema
        return response

    def format_response_schema(self, schema):
        return {
            "type": "object",
            "properties": {
                "success": {"type": "boolean"},
                "message": {"type": "string"},
                "data": schema,
            },
        }
