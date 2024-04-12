from urllib.parse import urljoin, urlencode

class ClientRoute:
    def __init__(self, config):
        self.config = config
        self.url_paths = {}

    def update_paths(self, paths):
        self.url_paths.update(paths)

    def url(self, path=''):
        return 'https://' + urljoin(self.config['domain'], path)

    def reverse_path(self, name, data=None):
        path = self.url_paths.get(name)
        if not path:
            raise ValueError(f'No client URL path registered with name: {name}.')
        return path.format(**data) if data else path

    def reverse(self, name, data=None):
        return self.url(self.reverse_path(name, data))