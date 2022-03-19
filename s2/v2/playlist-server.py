# Standard library modules
import logging
import random
import sys

# Installed packages
from flask import Blueprint
from flask import Flask
from flask import request
from flask import Response

from prometheus_flask_exporter import PrometheusMetrics

import requests

import simplejson as json

# The application

# Integer value 0 <= v < 100, denoting proportion of
# calls to `get_song` to return 500 from
PERCENT_ERROR = 50

app = Flask(__name__)

metrics = PrometheusMetrics(app)

db = {
    "name": "http://cmpt756db:30002/api/v2/datastore",
    "endpoint": [
        "read",
        "write",
        "delete",
        "update"
    ]
}
bp = Blueprint('playlist-server', __name__)


@bp.route('/update_add/<user_id>/<playlist_id>', methods=['GET', 'PUT'])
def update_add(user_id, playlist_id):
    headers = request.headers
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='notdefine/json')
    try:
        content = request.get_json()
        music_id_add = content['music']
    except Exception:
        return json.dumps({"message":"error reading arguments"})

    payload = {"objtype":"user_id", "objkey": user_id}

    url = db['name'] + '/' + db['endpoint'][0]
    response = requests.get(
        url,
        params=payload,
        header={'Authorization':headers['Authorization']})
    if response.status_code != 200:
        response = {
            "Count": 0,
            "Items": []
        }
        return app.make_response((response, 404))
    playlist = response.json()['Items'][0]
    if playlist_id not in item['playlist']:
        response = {
            "Count": 0,
            "Items": []
        }
        return app.make_response((response, 404))
    payload = {"objtype":"playlist", "objkey": playlist_id}
    url = db['name'] + '/' + db['endpoint'][0]
    response = request.get(
        url,
        params=payload,
        header={'Authorization':headers['Authorization']})
    if response.status_code != 200:
            response = {
                "Count": 0,
                "Items": []
            }
        return app.make_response((response, 404))
    item = response.json()['Item'][0]
    musiclist = (item['music'] if 'music' in item else None)
    if musiclist is None:
        musiclist = {music_id_add}
    else:
        musiclist = musiclist.add(music_id_add)

    payload = {"objtype":"playlist", "objkey": playlist_id}

    url = db['name'] + '/' + db['endpoint'][3]
    response = requests.put(
        url,
        params=payload,
        json={"music": musiclist},
        headers={'Authorization':headers['Authorization']})
    return (response.json())


@bp.route()
def update_delete():



# All database calls will have this prefix.  Prometheus metric
# calls will not---they will have route '/metrics'.  This is
# the conventional organization.
app.register_blueprint(bp, url_prefix='/api/v2/playlist/')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.error("missing port arg 1")
        sys.exit(-1)

    p = int(sys.argv[1])
    # Do not set debug=True---that will disable the Prometheus metrics
    app.run(host='0.0.0.0', port=p, threaded=True)
