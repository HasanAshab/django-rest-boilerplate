from rest_framework.exceptions import (
    PermissionDenied,
)


class HasPolicy:
    @property
    def _policy(self):
        msg = f"Policy class instance not registered \
        for model: '{self.__class__.__name__}' \
        Set it as '_policy' attribute"

        raise Exception(msg)

    def can(self, action, *args, **kwargs):
        handler = getattr(self._policy, action)
        return handler(self, *args, **kwargs)

    def cannot(self, action, *args, **kwargs):
        return not self.can(action, *args, **kwargs)

    def assert_can(self, action, *args, **kwargs):
        if self.cannot(action, *args, **kwargs):
            raise PermissionDenied

    def assert_cannot(self, action, *args, **kwargs):
        if self.can(action, *args, **kwargs):
            raise PermissionDenied
