from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError

def handler(exc, context):
    print(isinstance(exc, ValidationError))
    response = exception_handler(exc, context)
    if response is not None:
        response.data['status_code'] = response.status_code

    return response