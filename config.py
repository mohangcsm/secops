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
    ACCESS_LOGFILE_NAME = 'logs/access_log'
    ERROR_LOGFILE_NAME = 'logs/error_log'
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
    SECURITY_EMAIL = 'mohan.gcsm@gmail.com'
    APPSEC_USERS = REVIEW_APPROVERS = ['mohan.gcsm@gmail.com']
    DEFAULT_DOMAIN = "gmail.com"
    DEFAULT_USER = "appsec" #must be a valid JIRA user.
    PEER_REVIEW_ENABLED = False
    PEER_REVIEW_REQUIRED_FOR = [
        'new_web_app',
        'new_mobile_app',
        'new_rest_api',
        'existing_web_app',
        'existing_mobile_app',
        'existing_rest_api',
        'other'
    ]
    #-------other settings---------#


    #-external page links settings-#
    SEC_KB_LINK = "<>"
    APPSEC_TEAM_LINK = "<>"
    VRM_POLICY_LINK = "<>"
    SEC_AWARENESS_LINK = "<>"
    INFOSEC_POLICY_LINK = "<>"
    
    #-external page links settings-#


    #-------JIRA settings----------#
    JIRA_SETTINGS = {

        "JIRA_URL" : "<JIRA URL>",
        "JIRA_USER" : "<JIRA USERNAME>",
        "JIRA_PASS" : "<JIRA TOKEN not PASSWORD>",
        "JIRA_PROJECT" : "<JIRA PROJECT NAME>",

        "JIRA_TRANSITIONS" : [
            { # action ids with out peer review
                "TODO_TRANS" : 21, # move to To do from backlog action
                "SEND_FOR_REVIEW_TRANS" : None, # This should always be none
                "APPROVE_TRANS" : 5, #Resolve action
                "CLOSED_TRANS" : 101 # close or reject action,
            },
            { # action ids with peer review
                "TODO_TRANS" : 51, # move to To do from backlog action
                "SEND_FOR_REVIEW_TRANS" : 51, # Send for review action
                "REJECT_APPROVAL" : 61, # reject review action
                "APPROVE_TRANS" : 71, # approve action
                "CLOSED_TRANS" : 101 # close or reject action
               
            }
        ],
        "JIRA_COMPONENTS" : {
            "SECURITY_REVIEW" : "Security Review",
            "SECURITY_BUG" : "Security Bug"
        },

        "JIRA_FILTERS" : {
            "open_secreviews" : 10000,
            "open_secbugs" : 10001,
            "open_secreviews_2_weeks" : 10002,
            "open_secreviews_by_me" : 10003,
            "open_tickets" : 10006,
            "total_secreviews" : 10004,
            "total_secbugs" : 10005,
            "total_secreviews_2_weeks" : 10007
        },

        "STATUS_N_SEVERITY" : {
            "by_status" : ["Done", "Deployed", "Resolved", "Closed", "In Progress", "Under Review", "Waiting for customer", "To Do", "Open", "Reopened"],
            "by_severity" : ["Highest", "High", "Medium", "Low", "Lowest"]
        },

        "STATUS_CODES" : {
            "Done":"green", 
            "Deployed":"green", 
            "Resolved":"green", 
            "Closed" : "green",
            "In Progress":"blue", 
            "Verification":"orange", 
            "Under Review":"orange", 
            "Waiting for customer":"gray", 
            "To Do":"red", 
            "Open":"red", 
            "Reopened":"red",

            "Lowest":"green", 
            "Low":"lime", 
            "Medium":"orange", 
            "High":"red", 
            "Highest":"red"
        },

        "COLOR_CODES" : {
            "BACKGROUND" : {
                "red" : 'rgba(255, 99, 132, 0.2)',
                "green" : 'rgba(180, 206, 32, 0.2)',
                "blue" : 'rgba(54, 162, 235, 0.2)',
                "orange" : 'rgba(255, 94, 0, 0.2)',
                "gray" : 'rgba(85, 85, 85, 0.2)',
                "lime" : 'rgba(0, 200, 225, 0.2)'
            },
            "BORDER" : {
                "red" : 'rgba(255, 99, 132, 1)',
                "green" : 'rgba(180, 206, 32, 1)',
                "blue" : 'rgba(54, 162, 235, 1)',
                "orange" : 'rgba(255, 94, 0, 1)',
                "gray" : 'rgba(85, 85, 85, 1)',
                "lime" : 'rgba(0, 200, 225, 1)'
            }
        }
    }

    #-------allowed domains settings---------#    



class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
