

class LoginView(BaseLoginView):
    @rate_limit(action="signup")
    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)

