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
#metrics.info('app_info', 'Music process')

db = {
    "name": "http://cmpt756db:30002/api/v1/datastore", ############
    "endpoint": [
        "read",
        "write",
        "delete",
        "update"
    ]
}
bp = Blueprint('playlist-server', __name__)



@bp.route('/<playlist_id>', methods=['GET'])
def get_playlist(playlist_id):
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    payload = {"objtype": "playlist", "objkey": playlist_id}

    # This version will return 500 for a fraction of its calls
    if random.randrange(100) < PERCENT_ERROR:
        return Response(json.dumps({"error": "get_playlist failed"}),
                        status=500,
                        mimetype='application/json')

    url = db['name'] + '/' + db['endpoint'][0]
    response = requests.get(
        url,
        params=payload,
        headers={'Authorization': headers['Authorization']})
    return (response.json())
    


# All database calls will have this prefix.  Prometheus metric
# calls will not---they will have route '/metrics'.  This is
# the conventional organization.
app.register_blueprint(bp, url_prefix='/api/v1/music/')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.error("missing port arg 1")
        sys.exit(-1)

    p = int(sys.argv[1])
    # Do not set debug=True---that will disable the Prometheus metrics
    app.run(host='0.0.0.0', port=p, threaded=True)
