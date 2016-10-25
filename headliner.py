import falcon
from src.api.clusters import Clusters

api = falcon.API()
api.add_route('/clusters', Clusters('src/resources/clusters.json'))
