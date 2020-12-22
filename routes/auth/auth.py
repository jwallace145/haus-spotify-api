from flask import Blueprint, redirect, request, session
from spotify_requests import spotify

auth_blueprint = Blueprint('auth_blueprint', __name__)


@auth_blueprint.route('/health', methods=['GET'])
def health():
    return {'healthy': True}


@auth_blueprint.route('/auth', methods=['GET'])
def auth():
    return redirect(spotify.AUTH_URL)


@auth_blueprint.route('/callback', methods=['GET'])
def callback():

    auth_token = request.args['code']
    auth_header = spotify.authorize(auth_token)
    session['auth_header'] = auth_header

    return {'successful': True}
