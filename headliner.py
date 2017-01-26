from flask import Flask
from flask.json import jsonify
from src.api.clusters import Clusters
from src.api.cors import crossdomain
import redis
import os

app = Flask(__name__)

#default to local redis defaults if heroku config var not available
r_conn = redis.from_url(os.getenv('REDIS_URL',"redis://localhost:6379/"))


@app.route('/')
@crossdomain(origin='*')
def get__fresh_clusters():
    return jsonify(Clusters(r_conn).get())

if __name__ == "__main__":
    app.run(host='0.0.0.0')
