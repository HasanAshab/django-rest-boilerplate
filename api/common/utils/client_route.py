from urllib.parse import urljoin
from django.conf import settings


class ClientRouteManager:
    def __init__(self, config):
        self.config = config
        self.url_paths = {}

    def update_paths(self, paths):
        self.url_paths.update(paths)

    def base_url(self):
        return "https://" + self.config["domain"]

    def url(self, path=""):
        return urljoin(self.base_url(), path)

    def reverse_path(self, name, data=None):
        path = self.url_paths.get(name)
        if not path:
            raise ValueError(f'No client URL path registered with name: "{name}".')
        return path.format(**data) if data else path

    def reverse(self, name, data=None):
        return self.url(self.reverse_path(name, data))


client_route = ClientRouteManager({"domain": settings.CLIENT_DOMIAN})
