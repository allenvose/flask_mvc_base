# -*- encoding: utf-8 -*-
"""

"""
from logging import basicConfig, DEBUG, getLogger, StreamHandler
from os import path
from importlib import import_module
from flask import Flask, url_for
from flask_login import LoginManager
from flask_principal import Principal, Permission, RoleNeed


#db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login'
principal = Principal()

def register_extensions(app):
    #db.init_app(app)
    login_manager.init_app(app)
    principal.init_app(app)

def register_controllers(app):
    controllers = ['authorization', 'base']
    for controller in controllers:
        blueprint_module = import_module('app.controllers.routes.{}_routes'.format(controller))
        app.register_blueprint(blueprint_module.blueprint_init())
    

def configure_database(app):

    @app.before_first_request
    def initialize_database():
        #db.create_all()
        pass

    @app.teardown_request
    def shutdown_session(exception=None):
        #db.session.remove()
        pass

def create_app(config):
    app = Flask(__name__, static_folder='views/static', template_folder='views/templates')
    app.config.from_object(config)
    register_extensions(app)
    register_controllers(app)
    #configure_database(app)
    print(app.url_map)
    return app
