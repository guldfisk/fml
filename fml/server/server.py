from flask import Flask
from flask_api import FlaskAPI

from fml.server.session import SessionContainer
from fml.server.views.alarms import alarm_views
from fml.server.views.todos.cud import todo_cud_views
from fml.server.views.todos.dependencies import todo_dependency_views
from fml.server.views.todos.priorities import todo_priority_views
from fml.server.views.todos.projects import todo_project_views
from fml.server.views.todos.stats import todo_stat_views
from fml.server.views.todos.tags import todo_tag_views


server_app: Flask = FlaskAPI(__name__)
SessionContainer.init(server_app)

server_app.register_blueprint(alarm_views)
server_app.register_blueprint(todo_cud_views)
server_app.register_blueprint(todo_dependency_views)
server_app.register_blueprint(todo_priority_views)
server_app.register_blueprint(todo_project_views)
server_app.register_blueprint(todo_stat_views)
server_app.register_blueprint(todo_tag_views)
