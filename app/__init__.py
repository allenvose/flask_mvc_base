# -*- encoding: utf-8 -*-
"""

"""
from logging import basicConfig, DEBUG, getLogger, StreamHandler
from importlib import import_module
from flask import Flask
from flask_login import LoginManager
from flask_principal import Principal, Permission, RoleNeed
from app.controllers.utils.extensions.flask_2neo4j.driver import Flask_Python2Neo4J

login_manager = LoginManager()
login_manager.login_view = 'login'
db = Flask_Python2Neo4J()
principal = Principal()

def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    principal.init_app(app)

def register_controllers(app):
    controllers = ['site_access', 'site_base', 'errors']
    for controller in controllers:
        blueprint_module = import_module('app.controllers.{}.routes'.format(controller))
        app.register_blueprint(blueprint_module.blueprint_init())
    
def create_app(config):
    app = Flask(__name__, static_folder='views/static', template_folder='views/templates')
    app.config.from_object(config)
    register_extensions(app)
    register_controllers(app)
    #configure_database(app)
    print(app.url_map)
    return app
