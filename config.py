import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    #-------domain settings---------#
    HTTPS_PORT = 443
    HTTP_PORT = 80
    INTERFACE = '0.0.0.0'

    SSL_CERTFILE = 'ssl/server.crt'
    SSL_KEYFILE = 'ssl/server.key'
    
    #-------domain settings---------#


    #-----application settings------#
    SECRET_KEY = '$uP36S3c63T'
    DEBUG = True
    UPLOAD_FOLDER = 'uploads'
    DEFAULT_FOLDER = 'static/default'
    #-----application settings------#

    #-------oauth settings---------#
    OAUTH_CLIENT = 'google'

    GOOGLE_CLIENT_ID = 'XXXXXXXXXXXXXXXX-XXXXXXXXXXXXXXXXqbtijnssm9nv34ou6.apps.googleusercontent.com'
    GOOGLE_CLIENT_SECRET = 'XXXXXXXXXXXXXXXX'
    
    REDIRECT_URI = '/oauth2callback'  # one of the Redirect URIs from Google APIs console

    BASE_URL='https://www.google.com/accounts/'
    AUTHORIZE_URL='https://accounts.google.com/o/oauth2/auth'
    REQUEST_TOKEN_URL=None
    REQUEST_TOKEN_PARAMS={'scope': 'https://www.googleapis.com/auth/userinfo.email',
                        'response_type': 'code'}
    ACCESS_TOKEN_URL='https://accounts.google.com/o/oauth2/token'
    ACCESS_TOKEN_METHOD='POST'
    ACCESS_TOKEN_PARAMS={'grant_type': 'authorization_code'}
    #-------oauth settings---------#

    #-------other settings---------#
    ALLOWED_DOMAINS = ['gmail.com']
    SECURITY_EMAIL = ['mohan.gcsm@gmail.com']
    APPSEC_USERS = ['mohan.gcsm@gmail.com']
    PEER_REVIEW_ENABLED = False
    PEER_REVIEW_REQUIRED_FOR = [
        'new_web_app',
        'new_mobile_app',
        'new_rest_api',
        'existing_web_app',
        'existing_mobile_app',
        'existing_rest_api'
    ]

    #-------JIRA settings----------#
    JIRA_SETTINGS = {
    
        "JIRA_URL" : "<JIRA URL>",
        "JIRA_USER" : "<JIRA USERNAME>",
        "JIRA_PASS" : "<JIRA TOKEN not PASSWORD>",
        "JIRA_PROJECT" : "<JIRA PROJECT NAME>",

        "JIRA_TRANSITIONS" : [
            { # action ids with out peer review
                "TODO_TRANS" : 711, # move to To do from backlog action
                "SEND_FOR_REVIEW_TRANS" : None, # This should always be none
                "APPROVE_TRANS" : 5, #Resolve action
                "CLOSED_TRANS" : 2 # close or reject action,
            },
            { # action ids with peer review
                "TODO_TRANS" : 51, # move to To do from backlog action
                "SEND_FOR_REVIEW_TRANS" : 151, # Send for review action
                "APPROVE_TRANS" : 141, # approve action
                "CLOSED_TRANS" : 131 # close or reject action
            }
        ]
    }
    
    #-------allowed domains settings---------#    


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
