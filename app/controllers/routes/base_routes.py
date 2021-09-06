# -*- encoding: utf-8 -*-
"""
"""


from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound

base = Blueprint(
    'base_routes',
    __name__,
    url_prefix='',
    #template_folder='/home/templates',
    #static_folder='/views/static'
)

def blueprint_init():
    return base


@base.route('/index')
@login_required
def index():

    return render_template('home/index.html', segment='index')

@base.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith( '.html' ):
            template += '.html'

        # Detect the current page
        segment = get_segment( request )

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template( 'home/'+template, segment='index' )

    except TemplateNotFound:
        return render_template('home/page-404.html', segement='index'), 404
    
    except:
        return render_template('home/page-500.html', segment='index'), 500

# Helper - Extract current page name from request 
def get_segment( request ): 

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment    

    except:
        return None  
