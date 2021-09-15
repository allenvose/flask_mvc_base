# -*- encoding: utf-8 -*-
"""

"""

from app.models.site_access import Company
from importlib import import_module
from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
from passlib.hash import sha256_crypt
from flask import Blueprint, jsonify, render_template, redirect, request, url_for
from flask_login import (current_user, login_required, login_user, logout_user)

from app.controllers.site_access.registration_controller import UserRegistration, CompanyRegistration
from app.controllers.site_access.forms import LoginForm, RegisterUserForm, RegisterCompanyForm

from app.controllers.utils.util import verify_pass
from app.controllers.utils.extensions.flask_mydash import FlaskDash
from app import db

df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 10, 2, 2, 4, 10],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)





authorization = Blueprint(
    'site_access_routes',
    __name__,
    url_prefix='',
    #template_folder='/views/templates/',
    #static_folder='/views/static'
    )

def blueprint_init():
    return authorization

authorization_dash = FlaskDash(
    name= 'test',
    server=False,
    include_assets_files  = False, 
    url_base_pathname='/register/user/', assets_folder='views/static')

def dash_init():
    return authorization_dash

authorization_dash.layout = html.Div(id='holder_for_check')
def get_layout():
    layout = html.Div([
        dcc.Dropdown(
            id='demo-dropdown',
            className='row',
            options=[
                {'label': 'Ping Host', 'value': 'NYC'},
                {'label': 'Run Away', 'value': 'MTL'},
                {'label': 'Restart Router', 'value': 'SF'}
            ],
            value='NYC'
        ),
        html.Div(id='dd-output-container')
    ])
    return layout



@authorization.route('/')
def route_default():
    return redirect(url_for('site_access_routes.login'))

## Login & Registration

@authorization.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:
        username = request.form['username']
        password = request.form['password']
        user = None #User.query.filter_by(username=username).first()
        if user and verify_pass( password, user.password):
            login_user(user)
            return redirect(url_for('site_access_routes.route_default'))
        return render_template( 'auth/login.html', msg='Wrong user or password', form=login_form)

    if not current_user.is_authenticated:
        return render_template( 'auth/login.html',
                                form=login_form, segment='index')
    return redirect(url_for('site_base_routes.index'))

@authorization.route('/register/user', methods=['GET', 'POST'])
def register_user():
    user_registration_data = RegisterUserForm(request.form)
    if 'register_user' in request.form:
        print(request.form)
        if user_registration_data.validate_on_submit():
            user_registration_data.password.data = sha256_crypt.encrypt(user_registration_data.password.data)
            new_user = UserRegistration()
            user_registration_data.populate_obj(new_user)
            new_user.save()
    
    return render_template( 'authorization/register_user.html', form=user_registration_data, segment='index' )

@authorization.route('/register/company', methods=['GET', 'POST'])
def edit_register_company():
    existing_companies = Company.get_name_url_logo()
    print(existing_companies)
    company_registration_data = RegisterCompanyForm(request.form)
    if 'register_company' in request.form:
        if company_registration_data.validate_on_submit():
            new_company = CompanyRegistration()
            company_registration_data.populate_obj(new_company)
            new_company.save()
            return render_template( 'company/register_company.html', form=company_registration_data, segment='index', mydash="Hello", existing_companies=existing_companies)
    authorization_dash.layout = get_layout
    @authorization_dash.callback(
        Output('dd-output-container', 'children'),
        [Input('demo-dropdown', 'value')])
    def update_output(value):
        if value == 'SF':
            value = 'You are screwed!'
        return 'You have selected "{}"'.format(value)

    return render_template( 'company/register_company.html', form=company_registration_data, segment='index',  existing_companies=existing_companies)


@authorization.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site_access_routes.login'))

## Errors
