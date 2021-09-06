# -*- encoding: utf-8 -*-
"""

"""
import os
from decouple import config

class Config(object):
    #SETUP Flask Base Enviroment Variables and Defaults
    basedir    = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = 'S#perS3crEt_007'

class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_HTTPONLY  = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

    # PostgreSQL database
    # SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
    #     config( 'DB_ENGINE'   , default='postgresql'    ),
    #     config( 'DB_USERNAME' , default=''       ),
    #     config( 'DB_PASS'     , default='pass'          ),
    #     config( 'DB_HOST'     , default='localhost'     ),
    #     config( 'DB_PORT'     , default=5432            ),
    #     config( 'DB_NAME'     , default='' )
    # )
class DebugConfig(Config):
    DEBUG = True
    NEO4J_PASSWORD = 'test'
    NEO4J_USER = 'neo4j'
    NEO4J_HOST = 'neo4j'

# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug'     : DebugConfig
}
