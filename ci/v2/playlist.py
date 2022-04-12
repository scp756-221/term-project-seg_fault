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
        return r.status_code, item['name'], item['songs']

    def add_songs_to_playlist(self, play_id, music_id):
        req = requests.put(
            self._url + 'add_songs/' + play_id,
            json={'songs': music_id},
            headers={'Authorization':self._auth}
        )
        return req.status_code

    def delete_songs_to_playlist(self, play_id, music_id):
        req = requests.put(
            self.url + 'delete_songs/' + play_id,
            json={'songs':music_id},
            headers={'Authorization':self._auth}
        )
        return req.status_code
    def delete(self, playlist_id):
        """Delete a playlist.

        Parameters
        ----------
        m_id: string
            The UUID of this playlist in the playlist database.

        Returns
        -------
        Does not return anything. The music delete operation
        always returns 200, HTTP success.
        """
        requests.delete(
            self._url + playlist_id,
            headers={'Authorization': self._auth}
        )
