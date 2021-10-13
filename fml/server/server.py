from flask import Flask
from flask_api import FlaskAPI
from flask_cors import CORS

from fml.server.session import SessionContainer
from fml.server.views.alarms import alarm_views
from fml.server.views.ciwatch import ci_watch_views
from fml.server.views.todos.comments import todo_comments_view
from fml.server.views.todos.cud import todo_cud_views
from fml.server.views.todos.dependencies import todo_dependency_views
from fml.server.views.todos.priorities import todo_priority_views
from fml.server.views.todos.projects import todo_project_views
from fml.server.views.todos.stats import todo_stat_views
from fml.server.views.todos.tags import todo_tag_views


server_app: Flask = FlaskAPI(__name__)
CORS(server_app)
SessionContainer.init(server_app)

server_app.register_blueprint(alarm_views)
server_app.register_blueprint(todo_comments_view)
server_app.register_blueprint(todo_cud_views)
server_app.register_blueprint(todo_dependency_views)
server_app.register_blueprint(todo_priority_views)
server_app.register_blueprint(todo_project_views)
server_app.register_blueprint(todo_stat_views)
server_app.register_blueprint(todo_tag_views)
server_app.register_blueprint(ci_watch_views)
