from flask import Flask, render_template
from src.api.clusters import Clusters
import redis
import os

app = Flask(__name__)

#default to local redis defaults if heroku config var not available
r_conn = redis.from_url(os.getenv('REDIS_URL',"redis://localhost:6379/"))

@app.route('/')
def get__fresh_clusters():
    clusters = Clusters(r_conn).get()
    return render_template('clusters.html', clusters=clusters)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
