from flask import Flask, render_template, request, redirect, url_for, make_response
from bs4 import BeautifulSoup
from random import randint

import requests
import json

class Track(object):
    def __init__(self, song: str, artist: str):
        self.song = song
        self.artist = artist

    @staticmethod
    def from_dict(source):
        track = Track(source[u'song'], source[u'artist'])

        return track

    def to_dict(self):
        dest = {
            u'song': self.song,
            u'artist': self.artist
        }

        return dest

    def __repr__(self):
        return(u'Track(song={}, artist={})'.format(self.song, self.artist))


def get_playlist_from_apple_music(url):
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    }
    html = session.get(url, headers=headers).content
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all(class_='tracklist-item--song')

    track_list = []

    for item in items:
        song = item.find(class_='tracklist-item__text__headline')
        if song is None:
            continue

        artist = item.find(class_='table__row__link--secondary')
        if artist is None:
            continue

        song_name = song.get_text().strip()
        artist_name = artist.get_text().strip()

        track = Track(song_name, artist_name)
        track_list.append(track.to_dict())

    playlist_item = {
        'title': soup.find(class_='product-header__title').get_text(),
        'playlist': track_list
    }

    return playlist_item


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/load-playlist', methods=['POST'])
def load_playlist():
    playlist_url = request.args.get('url')
    playlist_item = get_playlist_from_apple_music(playlist_url)

    return json.dumps(playlist_item)

@app.route('/test')
def testhtml():
    return render_template('test.html')


if __name__ == '__main__':
    # openssl
    # ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    # ssl_context.load_cert_chain(certfile='newcert.pem', keyfile='newkey.pem', password='secret')
    # app.run(host="0.0.0.0", port=4443, ssl_context=ssl_context)

    app.run(host='0.0.0.0', port=6000, debug=True)

    # get_playlist_from_apple_music('https://music.apple.com/us/playlist/2019-top-100/pl.u-r2yJ1d4IJoX7g8')
