import falcon

class StaticFile:
    def __init__(self, fname):
        self.file_name = fname
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        with open(self.file_name, 'rb') as f:
            resp.body = f.read()
