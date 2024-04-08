from rest_framework.exceptions import PermissionDenied


class HasPolicy():
    @property
    def _policy(self):
        raise Exception(f'Policy class not registered for model: "{self.__class__.__name__}" \n Set it as "_policy" attribute')
    
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
        