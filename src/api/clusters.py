import os
import json
import traceback

class Clusters:
    def __init__(self, fname):
        self.file_name = fname
    def on_get(self, req, resp):
        """handles get requests"""
        if os.path.isfile(self.file_name):
            try:
                with open(self.file_name) as json_data:
                    data = json.load(json_data)
                    resp.body = json.dumps(data)
            except ValueError:
                traceback.print_exc()
                resp.body = 'error loading json data!'

        else:
            resp.body = 'no data!'
