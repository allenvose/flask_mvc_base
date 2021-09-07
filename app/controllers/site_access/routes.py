# -*- encoding: utf-8 -*-
"""

"""
from passlib.hash import sha256_crypt
from flask import Blueprint, jsonify, render_template, redirect, request, url_for
from flask_login import (current_user, login_required, login_user, logout_user)


from app.controllers.site_access.registration_controller import UserRegistrationSystem
from app.controllers.site_access.forms import LoginForm, RegistrationForm
from app.models.models import User

from app.controllers.utils.util import verify_pass

authorization = Blueprint(
    'authorization_routes',
    __name__,
    url_prefix='',
    #template_folder='/views/templates/',
    static_folder='/views/static')

def blueprint_init():
    return authorization

@authorization.route('/')
def route_default():
    return redirect(url_for('authorization_routes.login'))

## Login & Registration

@authorization.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and verify_pass( password, user.password):
            login_user(user)
            return redirect(url_for('authorization_routes.route_default'))
        return render_template( 'auth/login.html', msg='Wrong user or password', form=login_form)

    if not current_user.is_authenticated:
        return render_template( 'auth/login.html',
                                form=login_form, segment='index')
    return redirect(url_for('base_routes.index'))

@authorization.route('/register', methods=['GET', 'POST'])
def register():
    registration_form = RegistrationForm(request.form)
    if 'register' in request.form:
        if registration_form.validate_on_submit():
            registration_form.password.data = sha256_crypt.encrypt(registration_form.password.data)
            new_user = UserRegistrationSystem()
            registration_form.populate_obj(new_user)
            new_user.save()
    
    return render_template( 'authorization/register.html', form=registration_form, segment='index')
@authorization.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authorization_routes.login'))

## Errors
