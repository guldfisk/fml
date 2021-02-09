from flask import Flask
from flask_api import FlaskAPI

from fml.server.session import SessionContainer
from fml.server.views import views


server_app: Flask = FlaskAPI(__name__)
SessionContainer.init(server_app)

server_app.register_blueprint(views)
