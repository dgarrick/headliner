from flask import Flask, render_template
from src.api.clusters import Clusters
import redis

app = Flask(__name__)

@app.route('/')
def get_clusters():
    r_conn = redis.from_url(os.environ.get["REDIS_URL"])
    clusters = Clusters(r_conn).get()
    return render_template('clusters.html', clusters=clusters)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
