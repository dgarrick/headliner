from flask import Flask
from flask.json import jsonify
from src.api.clusters import Clusters
from src.api.cors import crossdomain
import redis
import os

app = Flask(__name__, static_url_path='')

redis_host = os.environ.get('REDISHOST', 'localhost')
redis_port = int(os.environ.get('REDISPORT', 6379))
redis_client = redis.StrictRedis(host=redis_host, port=redis_port)


@app.route('/clusters')
@crossdomain(origin='*')
def get__fresh_clusters():
    return jsonify(Clusters(redis_client).get())


@app.route('/')
@crossdomain(origin='*')
def serve_page():
    return app.send_static_file('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
