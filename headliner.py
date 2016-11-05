from flask import Flask, render_template
from src.api.clusters import Clusters

app = Flask(__name__)

@app.route('/')
def get_clusters():
    clusters = Clusters('src/resources/clusters.json').get()
    return render_template('clusters.html', clusters=clusters)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
