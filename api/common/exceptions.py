from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response


def handler(exc, context):
    if isinstance(exc, ValidationError):
        errors = {}
        for field_name, field_errors in exc.detail.items():
            errors[field_name] = field_errors[0]
        return Response({ 'errors': errors }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    response = exception_handler(exc, context)
    if response is not None:
        response.data['status_code'] = response.status_code

    return response