from functools import wraps
from allauth.core import ratelimit
from api.common.response import (
    APIResponse,
)

def rate_limit(*, action, **rl_kwargs):
    def decorator(function):
        @wraps(function)
        def wrap(view, request, *args, **kwargs):
            if not ratelimit.consume(
                request,
                action=action,
                **rl_kwargs
            ):
                return APIResponse(status=429)
            return function(view, request, *args, **kwargs)

        return wrap

    return decorator
