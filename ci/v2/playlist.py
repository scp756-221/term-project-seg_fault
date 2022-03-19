
# Standard library modules

# Installed packages
import requests


class Playlist():
    
    def __init__(self, url, auth):
        self._url = url
        self._auth = auth


    def read(self, playlist_id):
        
        r = requests.get(
            self._url + playlist_id,
            headers={'Authorization': self._auth}
            )
        if r.status_code != 200:
            return r.status_code, None, None

        item = r.json()['Items'][0]
        return r.status_code, item['Artist'], item['SongTitle']

