import os
import json
import traceback

class Clusters:
    def __init__(self, fname):
        self.file_name = fname
    def get(self):
        if os.path.isfile(self.file_name):
            try:
                with open(self.file_name) as json_data:
                    data = json.load(json_data)
                    return data
            except ValueError:
                traceback.print_exc()
                return('error loading json data!')
        else:
            return('no data!')
