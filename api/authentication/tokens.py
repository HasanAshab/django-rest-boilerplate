from allauth.headless.tokens.sessions import SessionTokenStrategy
from knox.views import LoginView


class STokenStrategy(SessionTokenStrategy):
    def create_access_token(self, request):
        _, token = LoginView(request=request).create_token()
        return token