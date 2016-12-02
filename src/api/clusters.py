import os
import json
import traceback
import redis

class Clusters:
    def __init__(self, conn):
        self.r_conn = conn
    def get(self):
        clusters = r_conn.get("clusters_fresh")
        if clusters is not None:
            return clusters
        else:
            return('no data!')
