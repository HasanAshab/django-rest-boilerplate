from knox.auth import TokenAuthentication as BaseTokenAuthentication

class TokenAuthentication(BaseTokenAuthentication):
    keyword = 'Bearer'