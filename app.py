# -*- encoding: utf-8 -*-
"""

"""
from app.models.models import user_loader
from os import environ
from decouple import config
from sys import exit

from app.config import config_dict
from app import create_app

DEBUG = True
get_config_mode = 'Debug' if DEBUG else 'Production'
try:
    app_config = config_dict[get_config_mode.capitalize()]
except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')
app = create_app( app_config ) 
if DEBUG:
    app.logger.info('DEBUG       = ' + str(DEBUG)      )
    app.logger.info('Environment = ' + get_config_mode )
    #app.logger.info('DBMS        = ' + app_config.SQLALCHEMY_DATABASE_URI )
if __name__ == "__main__":
    app.run(host= '0.0.0.0', port=5000, use_reloader=True,
            use_debugger=False, passthrough_errors=False)