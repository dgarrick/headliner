import falcon
from src.api.staticfile import StaticFile
from src.api.clusters import Clusters

api = falcon.API()
api.add_route('/', StaticFile("src/static/index.html"))
api.add_route('/clusters', Clusters('src/resources/clusters.json'))
