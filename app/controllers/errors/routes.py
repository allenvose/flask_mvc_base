from flask import Blueprint, render_template

from app import login_manager

errors = Blueprint(
    'error_routes',
    __name__,
    url_prefix='',
    #template_folder='/views/templates/',
    static_folder='/views/static')

def blueprint_init():
    return errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('page-403.html'), 403

@errors.errorhandler(403)
def access_forbidden(error):
    return render_template('page-403.html'), 403

@errors.errorhandler(404)
def not_found_error(error):
    return render_template('page-404.html'), 404

@errors.errorhandler(500)
def internal_error(error):
    return render_template('page-500.html'), 500
