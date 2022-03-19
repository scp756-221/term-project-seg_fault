# Standard library modules

# Installed packages
import requests


class Playlist():
    def __init__(self, url, auth):
        self._url = url
        self._auth = auth

    def update_add(self, u_id, play_id, music_id):
        req = requests.put(
            self._url + 'update_add/' + u_id + '/' + play_id,
            json={'music': music_id},
            headers={'Authorization':self._auth}
        )
        return req.status_code

    def update_delete(self, u_id, play_id, music_id):
        req = requests.put(
            self.url + 'update_delete' + u_id + '/' + play_id,
            json={'music':music_id},
            headers={'Authorization':self._auth}
        )
