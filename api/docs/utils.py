from drf_spectacular.utils import OpenApiResponse
from api.docs.serializers import SuccessfulResponseSerializer


class SuccessfulApiResponse(OpenApiResponse):
    def __init__(self, description=None, examples=None):
        super().__init__(
            response=SuccessfulResponseSerializer,
            description=description,
            examples=examples,
        )
