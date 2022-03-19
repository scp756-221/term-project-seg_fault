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


@bp.route('add_songs/<playlist_id>', methods=['PUT', 'GET'])
def add_songs_to_playlist(playlist_id):
    headers = request.headers
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    try:
        content = request.get_json()
        music = content['Music']
    except Exception:
        return json.dumps({"message": "error reading arguments"})
    payload = {"objtype": "playlist", "objkey": playlist_id}
    url = db['name'] + '/' + db['endpoint'][0]
    response = requests.get(
        url,
        params=payload,
        headers={'Authorization': headers['Authorization']})
    if response.status_code != 200:
        response = {
            "Count": 0,
            "Items": []
         }
        return app.make_response((response, 404))
    item = response.json()['Items']
    music_list = (item['songs']if 'songs' in item else None)
    if music_list is None:
        music_list = {music}
    else:
        music_list.add(music)
    url = db['name'] + '/' + db['endpoint'][3]
    response = requests.put(
        url,
        params=payload,
        json={"songs": music_list}
        headers={'Authorization': headers['Authorization']})
    return(response.json())

@bp.route('delete_songs/<playlist_id>', methods=['PUT', 'GET'])
def delete_songs_to_playlist(playlist_id):
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    try:
        content = request.get_json()
        music = content['Music']
    except Exception:
        return json.dumps({"message": "error reading arguments"})
    payload = {"objtype": "playlist", "objkey": playlist_id}
    url = db['name'] + '/' + db['endpoint'][0]
    response = requests.get(
        url,
        params=payload,
        headers={'Authorization': headers['Authorization']})
    if response.status_code != 200:
        response = {
            "Count": 0,
            "Items": []
         }
        return app.make_response((response, 404))
    item = response.json()['Items']
    music_list = (item['songs']if 'songs' in item else None)
    if music_list is None or music not in music_list:
        response = {
            "Count": 0,
            "Items": []
        }
        return app.make_response((response, 404))
    else:
        music_list.discard(music)
        # check if the set is empty 
        if not music_list:
            music_list = None
        url = db['name'] + '/' + db['endpoint'][3]
        response = requests.put(
            url,
            params=payload,
            json={"songs": music_list}
            headers={'Authorization': headers['Authorization']})
        return(response.json())

@bp.route('/', methods=['POST'])
def create_playlist():
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    try:
        content = request.get_json()
        playlist_name = content['name']
        init_songs = None
        if 'songs' in content:
            init_songs = content['songs']
    except Exception:
        return json.dumps({"message": "error reading arguments"})
    url = db['name'] + '/' + db['endpoint'][1]
    response = requests.post(
        url,
        json={"objtype": "playlist", "name": playlist_name, "songs": init_songs},
        headers={'Authorization': headers['Authorization']})
    return (response.json())


@bp.route('/<playlist_id>', methods=['DELETE'])
def delete_playlist(playlist_id):
    raise NotImplemented


@bp.route('/<playlist_id>', methods=['GET'])
def get_playlist(playlist_id):
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
