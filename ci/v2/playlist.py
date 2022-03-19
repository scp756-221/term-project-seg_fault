# Standard library modules

# Installed packages
import requests


class Playlist():
    def __init__(self, url, auth):
        self._url = url
        self._auth = auth

    def add_songs_to_playlist(self, play_id, music_id):
        req = requests.put(
            self._url + 'add_songs/' + play_id,
            json={'Music': music_id},
            headers={'Authorization':self._auth}
        )
        return req.status_code

    def delete_songs_to_playlist(self, play_id, music_id):
        req = requests.put(
            self.url + 'delete_songs/' + play_id,
            json={'Music':music_id},
            headers={'Authorization':self._auth}
        )
