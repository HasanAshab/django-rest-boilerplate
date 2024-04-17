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

    def can(self, action, obj):
        handler = getattr(self._policy, action)
        return handler(self, obj)

    def cannot(self, action, obj):
        return not self.can(action, obj)

    def assert_can(self, action, obj):
        if self.cannot(action, obj):
            raise PermissionDenied

    def assert_cannot(self, action, obj):
        if self.can(action, obj):
            raise PermissionDenied
