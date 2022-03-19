# Standard library modules

# Installed packages
import requests


class Playlist():

    def __init__(self, url, auth):
        self._url = url
        self._auth = auth

    def delete(self, playlist_id):
        """Delete an artist, song pair.

        Parameters
        ----------
        m_id: string
            The UUID of this song in the music database.

        Returns
        -------
        Does not return anything. The music delete operation
        always returns 200, HTTP success.
        """
        requests.delete(
            self._url + playlist_id,
            headers={'Authorization': self._auth}
        )
