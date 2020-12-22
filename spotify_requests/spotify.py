import os
import urllib.parse
import sys
import json
import requests
import base64

# --------------- SPOTIFY BASE URL --------------- #

SPOTIFY_API_BASE_URL = 'https://api.spotify.com'
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

# --------------- USER AUTHORIZATION --------------- #

# spotify endpoints
SPOTIFY_AUTH_BASE_URL = "https://accounts.spotify.com/{}"
SPOTIFY_AUTH_URL = SPOTIFY_AUTH_BASE_URL.format('authorize')
SPOTIFY_TOKEN_URL = SPOTIFY_AUTH_BASE_URL.format('api/token')

# client keys
CLIENT_ID = os.getenv('HAUS_CLIENT_ID')
CLIENT_SECRET = os.getenv('HAUS_CLIENT_SECRET')

# server side parameter
CLIENT_SIDE_URL = "http://localhost"
PORT = 8080
REDIRECT_URI = "{}:{}/callback".format(CLIENT_SIDE_URL, PORT)
SCOPE = "playlist-modify-public playlist-modify-private user-read-recently-played user-top-read"
STATE = ""

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    "client_id": CLIENT_ID
}

URL_ARGS = "&".join(["{}={}".format(key, urllib.parse.quote(val))
                     for key, val in list(auth_query_parameters.items())])

AUTH_URL = "{}?{}".format(SPOTIFY_AUTH_URL, URL_ARGS)


def authorize(auth_token):

    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI
    }

    base64encoded = base64.b64encode(
        ("{}:{}".format(CLIENT_ID, CLIENT_SECRET)).encode())

    headers = {"Authorization": "Basic {}".format(base64encoded.decode())}

    post_request = requests.post(
        SPOTIFY_TOKEN_URL,
        data=code_payload,
        headers=headers
    )

    # tokens are returned to the app
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]

    # use the access token to access Spotify API
    auth_header = {"Authorization": "Bearer {}".format(access_token)}

    return auth_header
