import flask, time, sys, json, sqlite3, os, sys, random, string, hashlib, subprocess

from flask import render_template, session, jsonify, request, Response, flash
from flask import flash, current_app, redirect, url_for, send_from_directory
from flask_oauth import OAuth

from application import app
from jira import JIRA
from jira_functions import *

reload(sys)
sys.setdefaultencoding('utf8')

app.config.from_object(__name__)

JIRA_SETTINGS = app.config['JIRA_SETTINGS']

JIRA_URL = JIRA_SETTINGS['JIRA_URL']
JIRA_USER = JIRA_SETTINGS['JIRA_USER']
JIRA_PASS = JIRA_SETTINGS['JIRA_PASS']
JIRA_PROJECT = JIRA_SETTINGS['JIRA_PROJECT']

peer_review_enabled = app.config['PEER_REVIEW_ENABLED']
JIRA_TRANSITIONS = JIRA_SETTINGS['JIRA_TRANSITIONS'][peer_review_enabled]
PEER_REVIEW_REQUIRED_FOR = app.config['PEER_REVIEW_REQUIRED_FOR']
JIRA_COMPONENTS = JIRA_SETTINGS['JIRA_COMPONENTS']

jira = JIRA(JIRA_URL, basic_auth=(JIRA_USER,JIRA_PASS))

oauth = OAuth()
google = oauth.remote_app(
    app.config['OAUTH_CLIENT'],
    base_url=app.config['BASE_URL'],
    authorize_url=app.config['AUTHORIZE_URL'],
    request_token_url=app.config['REQUEST_TOKEN_URL'],
    request_token_params=app.config['REQUEST_TOKEN_PARAMS'],
    access_token_url=app.config['ACCESS_TOKEN_URL'],
    access_token_method=app.config['ACCESS_TOKEN_METHOD'],
    access_token_params=app.config['ACCESS_TOKEN_PARAMS'],
    consumer_key=app.config['GOOGLE_CLIENT_ID'],
    consumer_secret=app.config['GOOGLE_CLIENT_SECRET']
)

@app.route('/', methods=['GET'])
def index():
    if not session.get('access_token'):
        return render_template("login.html"), 403

    return render_template('index.html',message=" ",category=""), 200

@app.route('/new_secreview', methods=['GET'])
def new_secreview():
    access_token = session.get('access_token')
    if access_token is None:
        return render_template("login.html",message="Please login to continue",category="info"), 403


    return render_template('new_secreview.html',message="",category=""), 200   

@app.route('/create_secreview', methods=['GET','POST'])
def create_secreview():
    redirect_url = "/"

    access_token = session.get('access_token')
    if access_token is None:
        return render_template("login.html",message="Please login to continue",category="info"), 403

    args = request.form

    if not args or "requestingfor" not in args:
        return render_template('new_secreview.html',message="Please fill all details before submitting",category="warning"), 200

    requestingfor = args.get('requestingfor')

    Product_Title = requestingfor
    if requestingfor not in ("others"):
        Product_Title = "["+requestingfor+"] "+args.get('Product_Title')

    component = JIRA_COMPONENTS["SECURITY_REVIEW"]
    if requestingfor == "sec_bug":
        component = JIRA_COMPONENTS["SECURITY_BUG"]
        Product_Title = "["+requestingfor+"] "+args.get('Issue_Title')


    description = ""
    for key in args:
        if key != "requestingfor":
            value = args.get(key)
            if key in ('steps to reproduce','Recommendation'):
                value = "\n{code}"+value+"{code}"
            if key in ("Environment Details"):
                value = "\n"+value

            description +="*"+key+"* : "+value+"\n"
    description+="*Ticket Raised By* : "+session.get('email');

    description = "*requestingfor* : "+requestingfor+"\n"+description

    result = create_new_jira(jira,JIRA_SETTINGS,Product_Title,description,component,peer_review_enabled)

    if result.key:
        redirect_url = JIRA_URL+"/browse/"+result.key
        # return redirect(redirect_url), 302
        return render_template("index.html",message="Ticket raised successfully: "+result.key+".<br /><br /><a href='"+redirect_url+"' target='_blank'>click here to view the ticket.</a>")

    return render_template('new_secreview.html',
        message="JiraError: "+str(result)+"<br />Please contact @mohan.kk",
        category="warning"), 200

@app.route('/close_tickets', methods=['GET','POST'])
def close_tickets():
    access_token = session.get('access_token')
    if access_token is None:
        return render_template("login.html",message="Please login to continue",category="info"), 403

    appsec_user = session.get('appsec_user')
    if not appsec_user:
        return render_template("index.html",message="You are not authorized",category="danger"), 403        

    if request.method == 'GET':
        [secreview_string,secbugs_string] = get_open_secreviews(jira,JIRA_SETTINGS)
        return render_template('close_tickets.html',
            peer_review_enabled = str(peer_review_enabled).lower(),
            PEER_REVIEW_REQUIRED_FOR = PEER_REVIEW_REQUIRED_FOR,
            secreview_string = secreview_string,
            secbugs_string = secbugs_string,
            message="",
            category=""), 200

    if request.method == "POST" and  "action" in request.form:
        args = request.form
        category="success"
        return_code = 200

        ticket_id = args.get('ticket_id')
        issue = jira.issue(ticket_id)

        requestingfor = args.get('requestingfor')
        comments = args.get('comments')
        approver = args.get('approver')
        action = args.get('action')

        status = check_status(str(issue.fields.status.name),requestingfor)

        if not status:
            message = "Operation not allowed. Please retry after changing the JIRA state from Backlog/Todo/ToStart."
            category = "warning"
            return_code = 403
            return render_template('index.html',message=message, category=category), return_code


        if not ticket_id or not requestingfor:
            message = "Manadatory parameters missing. Please check and retry"
            category = "warning"
            return_code = 403
            return render_template('index.html',message=message, category=category), return_code

        peer_review_required = False
        for review_id in PEER_REVIEW_REQUIRED_FOR:
            if review_id in str(issue.fields.summary):
                peer_review_required = True

        not_allowed = (action == "Approve" and peer_review_required and  status == "In Progress")
        if not_allowed:
            message = "Can not approve without peer review. Please check and retry"
            category = "warning"
            return_code = 403
            return render_template('index.html',message=message, category=category), return_code

        comment_message = ""
        if comments:
            comment_message = "The following are the Callouts/Feedback/Comments from Appsec side\n";
            comment_message += "{code}"+comments+"{code}";


        if action == "Approve" or action == "Send for Review":
            checks = get_request_options(requestingfor)

            checks_message = "\n{code}"
            for arg in args:
                for check in checks:
                    if arg == check:
                        checks_message += check+"\n"
            checks_message.strip("\n")

            checks_message += "{code}"

            if action == "Approve":
                message = "Ticket Approved successfully"
                approve_message = "This is good to go from appsec side. The following checks have been verified."
                signing_message = "\nReview Approved by : @["+session['email']+"]"
            else:
                message = "Ticket sent for approver review"
                approve_message = "Initial review Completed. The following checks have been performed as part of the review."
                signing_message = "\nInitial Review Completed by : @["+session['email']+"]"

                if approver == "":
                    message = "Manadatory parameters 'approver' is missing. Please check and retry"
                    category = "warning"
                    return_code = 403
                    return render_template('index.html',message=message, category=category), return_code 

                # assign_to_approver(key,approver)

            comment_message = approve_message+checks_message+"\n"+comment_message+signing_message

        if action == "Reject":
            if not comments or comments == "":
                message = "Manadatory parameters 'comments' is missing. Please check and retry"
                category = "warning"
                return_code = 403
                return render_template('index.html',message=message, category=category), return_code 

            message = "Ticket Rejected successfully"
            reject_message = "For mote information pelase reach out to "+app.config['SECURITY_EMAIL']+" with review ID in subject line."
            comment_message = comment_message+"\n"+reject_message


        result = resolve_or_close_jira(jira,JIRA_TRANSITIONS,ticket_id,comment_message,action,approver)

        if not result:
            message = "Error occured. Please try again after checking Jira state"
            category = "warning"
            return_code = 403
            return render_template('index.html',message=message, category=category), return_code

        return render_template('index.html',message=message, category=category), return_code

    return redirect(url_for('index')), 403
        

@app.route('/security_base')
def security_base():
    return render_template('index.html',message="currently not available", category="warning"), 200

@app.route('/rfp_base')
def rfp_base():
    return render_template('index.html',message="currently not available", category="warning"), 200


@app.route('/code_review')
def code_review():
    args = re


@app.route('/options.json')
def options():
    return send_from_directory(app.static_folder, "options.json")

@app.route('/request_options.json')
def request_options():
    return send_from_directory(app.static_folder, "request_options.json")


############ support functions ############
with app.test_request_context('/'):
    def is_appsec_user(email):
        appsec_users = app.config['APPSEC_USERS']
        if email in appsec_users:
            return True

        return False

with app.test_request_context('/'):
    def get_request_options(requestingfor):
        with open(app.static_folder+'/options.json') as options_file:
            options_all = json.load(options_file)
            secreview_options = options_all['others']
            
            for key in options_all:
                if key == requestingfor:
                    secreview_options = options_all[key]
                    if 'other_options' in secreview_options and secreview_options['other_options']:
                        for other_key in options_all['others']:
                            secreview_options[other_key] = options_all['others'][other_key]
                        secreview_options.pop('other_options')

            return secreview_options


with app.test_request_context('/'):
    def check_status(status,requestingfor):
        if requestingfor != 'sec_bug' and status in ("Backlog","To Do", "ToStart"):
            return None
        return status


############ Do not modify these route/functions ############

@app.route('/login', methods=['GET'])
def login():
    callback=url_for('authorized', _external=True)
    return google.authorize(callback=callback)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route(app.config['REDIRECT_URI'])
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''

    from urllib2 import Request, urlopen, URLError
 
    headers = {'Authorization': 'OAuth '+access_token}
    req = Request('https://www.googleapis.com/oauth2/v1/userinfo', None, headers)
    try:
        res = urlopen(req)

    except URLError, e:
        print e
        if e.code == 401:
            # Unauthorized - bad token
            session.pop('access_token', None)
            return redirect(url_for('login'))

        return res.read()
 
    res = json.loads(res.read())
    res['access_token'] = access_token

    allowed_domain = False

    for domain in app.config['ALLOWED_DOMAINS']:
        if domain in res['email']:
            allowed_domain = True
            break

    if not allowed_domain:
        session.clear()
        return render_template('login.html',message="Email ids with this domain are not allowed.",category="danger"), 403

    session['email'] = res['email']
    session['picture'] = res['picture']
    session['type'] = 'user'
    session['loginType'] = 'oauth'
    session['verified'] = True
    session['oauth_uid'] = res['id']
    session['appsec_user'] = is_appsec_user(res['email'])

    if session['access_token']:
        return redirect(url_for('index'))

    return render_template('login.html',message="Something went wrong. Please try again.",category="danger"), 500


@google.tokengetter
def get_access_token():
    return session.get('access_token')

@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, "robots.txt")

@app.errorhandler(404)
def page_not_found(e):
    redirect = "login.html"

    access_token = session.get('access_token')
    if access_token:
        redirect = "index.html"

    return render_template(redirect,message="404 - Requested resource does not exist.",category="warning"), 404

@app.errorhandler(403)
def server_error_403(e):
    redirect = "login.html"
    
    access_token = session.get('access_token')
    if access_token:
        redirect = "index.html"

    return render_template(redirect,message="User not authorized to view this resource.",category="warning"), 403

# @app.errorhandler(Exception)
@app.errorhandler(500)
def server_error_500(e):
    redirect = "login.html"
    
    access_token = session.get('access_token')
    if access_token:
        redirect = "index.html"

    return render_template(redirect,message="Something went wrong ! Please try again.",category="danger"), 500
############ Do not modify these route/functions ############

