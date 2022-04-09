
"""
SFU CMPT 756
Sample application---playlist service.
"""

# Standard library modules
import logging
import sys
import time

# Installed packages
from flask import Blueprint
from flask import Flask
from flask import request
from flask import Response

import jwt

from prometheus_flask_exporter import PrometheusMetrics

import requests

import simplejson as json

# The application

app = Flask(__name__)

metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Playlist process')

bp = Blueprint('app', __name__)

db = {
    "name": "http://cmpt756db:30002/api/v1/datastore",
    "endpoint": [
        "read",
        "write",
        "delete",
        "update"
    ]
}


@bp.route('/', methods=['GET'])
@metrics.do_not_track()
def hello_world():
    return ("If you are reading this in a browser, your service is "
            "operational. Switch to curl/Postman/etc to interact using the "
            "other HTTP verbs.")


@bp.route('/health')
@metrics.do_not_track()
def health():
    return Response("", status=200, mimetype="application/json")


@bp.route('/readiness')
@metrics.do_not_track()
def readiness():
    return Response("", status=200, mimetype="application/json")
  

@bp.route('/add_songs/<playlist_id>', methods=['PUT'])
def add_songs_to_playlist(playlist_id):
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    try:
        content = request.get_json()
        new_songs = content['songs']
    except Exception:
        return json.dumps({"message": "error reading arguments"})
    payload = {"objtype": "playlist", "objkey": playlist_id}
    # read the original songs from db
    read_url = db['name'] + '/' + db['endpoint'][0]
    response = requests.get(
        read_url,
        params=payload,
        headers={'Authorization': headers['Authorization']})
    original_songs = response.json()['Items'][0]["songs"]
    updated_songs = new_songs
    if original_songs is not None:
        updated_songs += original_songs
    # update the song list to db
    url = db['name'] + '/' + db['endpoint'][3]
    response = requests.put(
        url,
        params=payload,
        json={"songs": updated_songs},
        headers={'Authorization': headers['Authorization']})
    return (response.json())


@bp.route('/', methods=['POST'])
def create_playlist():
    raise NotImplemented


@bp.route('/<playlist_id>', methods=['DELETE'])
def delete_playlist(playlist_id):
    raise NotImplemented

  
@bp.route('/<playlist_id>', methods=['GET'])
def get_playlist(playlist_id):
    raise NotImplemented


@bp.route('delete_songs/<playlist_id>', methods=['PUT'])
def delete_songs_to_playlist(playlist_id):
    raise NotImplemented


@bp.route('/', methods=['POST'])
def create_playlist():
    raise NotImplemented

    
# All database calls will have this prefix.  Prometheus metric
# calls will not---they will have route '/metrics'.  This is
# the conventional organization.
app.register_blueprint(bp, url_prefix='/api/v1/playlist/')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.error("Usage: app.py <service-port>")
        sys.exit(-1)

    p = int(sys.argv[1])
    # Do not set debug=True---that will disable the Prometheus metrics
    app.run(host='0.0.0.0', port=p, threaded=True)