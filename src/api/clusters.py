import os
import json
import traceback
import redis

class Clusters:
    def __init__(self, conn):
        self.r_conn = conn
    def get(self):
        clusters = self.r_conn.get("clusters_fresh")
        if clusters is not None:
            try:
                return json.loads(clusters)
            except ValueError:
                traceback.print_exc()
                return('error loading json data!')
        else:
            return('no data!')
