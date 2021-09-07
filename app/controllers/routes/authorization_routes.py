# -*- encoding: utf-8 -*-
"""
"""
from passlib.hash import sha256_crypt
from flask import Blueprint, jsonify, render_template, redirect, request, url_for
from flask_login import (current_user, login_required, login_user, logout_user)

from app import login_manager
from app.controllers.access_and_registrion.registration_controller import RegistrationSystem
from app.controllers.forms.authorization_forms import LoginForm, RegistrationForm
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
        
        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = User.query.filter_by(username=username).first()
        
        # Check the password
        if user and verify_pass( password, user.password):

            login_user(user)
            return redirect(url_for('authorization_routes.route_default'))

        # Something (user or pass) is not ok
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
            new_user = RegistrationSystem()
            registration_form.populate_obj(new_user)
            print(new_user)
            new_user.save()
            #test_model = CreateAccountModel.from_orm(create_account_form)
            #print(test_model)
            # system_account = db.repo.match(System_Account, create_account_form.username).first()
            # mobile_phone = db.repo.match(Phone, create_account_form.sms_number).first()
            # if system_account:
            #     if system_account.username == create_account_form.username:
            #         return render_template( 'accounts/register.html', 
            #                             msg='Username already registered, please login or request help',
            #                             success=False,
            #                             form=create_account_form)
            #     if system_account.email == create_account_form.email:
            #         return render_template( 'accounts/register.html', 
            #                             msg='Email already registered, please login or request help', 
            #                             success=False,
            #                             form=create_account_form)
            # if mobile_phone:
            #     if mobile_phone.phone_number == create_account_form.sms_number:
            #         return render_template( 'accounts/register.html', 
            #                             msg='Mobile number is already registered',
            #                             success=False,
            #                             form=create_account_form)

            # if system_account is None and mobile_phone is None:
            # # # else we can create the user
            #     hashed_pasword = sha256_crypt.encrypt(create_account_form.password)
            #     system_account = System_Account()
            #     system_account.username = username
            #     system_account.email = email
            #     system_account.hashed_password = hashed_pasword
            #     db.repo.save(system_account)
            #     print('User Created')
            #     return render_template( 'accounts/register.html', 
            #                     msg='User created please <a href="/login">login</a>', 
            #                     success=True,
            #                     form=create_account_form)
        # else:
        #     return render_template( 'accounts/login.html',
        #                             form=create_account_form,
        #                             success=False, segment='index')
   
    return render_template( 'authorization/register.html', form=registration_form, segment='index')
@authorization.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authorization_routes.login'))

## Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('page-403.html'), 403

@authorization.errorhandler(403)
def access_forbidden(error):
    return render_template('page-403.html'), 403

@authorization.errorhandler(404)
def not_found_error(error):
    return render_template('page-404.html'), 404

@authorization.errorhandler(500)
def internal_error(error):
    return render_template('page-500.html'), 500
