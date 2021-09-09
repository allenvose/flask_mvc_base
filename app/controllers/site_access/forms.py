# -*- encoding: utf-8 -*-
"""

"""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SelectField
from wtforms.validators import InputRequired, Email, DataRequired, Length, Regexp, EqualTo
from wtforms import TextField, PasswordField
from wtforms.validators import InputRequired, Email, DataRequired

from app.controllers.utils.custom_validators import sms_field_validator, user_exists_validator

## login and registration

class LoginForm(FlaskForm):
    username = StringField('User', id='user_name_create',
                        validators=[InputRequired(message='User ID is required'),
                        Length(max=35, message='Maximum of 35 characters allowed'),
                        Regexp('^[^@]*$', message='Only include the username portion of the email')])
            
    password = PasswordField('Password', id='pwd_create',
                        validators=[DataRequired(),
                        Length(min=8, max=35, message='Must be a minimum of 2 letters and less than 35'),
                        Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
                        message='Minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character:'
                        ),])

class  RegisterUserForm(FlaskForm):
    username = StringField('User', id='user_name_create',
                        validators=[InputRequired(message='User ID is required'),
                        Length(max=35, message='Maximum of 35 characters allowed'),
                        Regexp('^[^@]*$', message='Only include the username portion of the email'),
                        user_exists_validator()])
            
    password = PasswordField('Password', id='pwd_create',
                        validators=[DataRequired(),
                        Length(min=8, max=35, message='Must be a minimum of 2 letters and less than 35'),
                        Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
                        message='Minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character:'
                        ),])

    first_name = StringField('First Name', id='first_name_create',
                        validators=[InputRequired(message='First Name is required'),
                        Length(min=2, max=35, message='Must be a minimum of 2 letters and less than 35'),
                        Regexp('^[A-Za-z]+$', message='Alpha characters only permited')])
    last_name = StringField('Last Name', id='last_name_create',
                        validators=[InputRequired(message='Last Name is required'),
                        Length(min=2, max=35, message='Must be a minimum of 2 letters and less than 35'),
                        Regexp('^[A-Za-z]+$', message='Alpha characters only permited')])
    title = StringField('Title', id='title_create',
                        validators=[InputRequired(message='Title is required')])
    company_association = SelectField('Email',
                        validators=[DataRequired()],
                        choices=[('@siriusfederal.com', '@siriusfederal.com'), ('@cisco.com', '@cisco.com')])
    sms_capable_phone = StringField('Mobile', id='mobile_create',
                        validators=[DataRequired(), sms_field_validator()])
    confirm = PasswordField('Repeat Password', id='pwd_match',
                        validators=[DataRequired(), Length(min=8, max=35),
                        EqualTo('password', message='Passwords must match'), ])

class  RegisterCompanyForm(FlaskForm):
    company_name = StringField('Company Name', id='company_name',
                        validators=[InputRequired(message='User ID is required'),
                        Length(max=35, message='Maximum of 35 characters allowed'),
                        ])
            
    company_url = StringField('Company URL', id='company_url',
                        validators=[DataRequired(),
                        Length(min=8, max=35, message='Must be a minimum of 2 letters and less than 35'),
                        ])

    company_logo = StringField('Logo', id='company_logo',
                        validators=[InputRequired(message='User ID is required'),
                        Length(max=200, message='Maximum of 35 characters allowed'),
                        ])