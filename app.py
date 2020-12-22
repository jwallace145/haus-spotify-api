import os

from flask import Flask

from routes.auth.auth import auth_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.getenv('APP_SETTINGS'))
    app.register_blueprint(auth_blueprint)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
