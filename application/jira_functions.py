
from flask import jsonify
from requests.auth import HTTPBasicAuth
import requests


def create_new_jira(jira,JIRA_SETTINGS,product_title="", description="",component="Security Review",peer_review_enabled=False):
    
    JIRA_PROJECT = JIRA_SETTINGS['JIRA_PROJECT']
    JIRA_COMPONENTS = JIRA_SETTINGS['JIRA_COMPONENTS']
    
    JIRA_TRANSITIONS = JIRA_SETTINGS['JIRA_TRANSITIONS'][peer_review_enabled]
    TODO_TRANS = JIRA_TRANSITIONS['TODO_TRANS']

    task = "Task"
    if component == JIRA_COMPONENTS["SECURITY_BUG"]:
        task = "Bug"

    fields = {
        "project": {
            "key": JIRA_PROJECT
        }, 
        "summary": product_title,
        "description": description, 
        "issuetype": {
            'name': task
        },
        "components":[{
            'name': component
        }]
    }

    try:
        result = jira.create_issue(fields = fields)
        # jira.transition_issue(result.key,TODO_TRANS) #already in TODO state for newly created issues
        return result
    
    except Exception, ae:
        print ae
        return False

    return None

def get_jira_issues(jira, JIRA_SETTINGS, jira_filter, assignee=None, reporter=None, user_email=None, since=None):
    JIRA_URL = JIRA_SETTINGS["JIRA_URL"]
    JIRA_PROJECT = JIRA_SETTINGS["JIRA_PROJECT"]
    JIRA_COMPONENTS = JIRA_SETTINGS["JIRA_COMPONENTS"]

    JIRA_FILTERS = JIRA_SETTINGS["JIRA_FILTERS"]

    jira_filter = 'filter='+str(jira_filter)
    if assignee:
        jira_filter = jira_filter+' AND assignee=\"'+str(assignee)+'\"'

    if reporter:
        jira_filter = jira_filter+' AND reporter=\"'+str(reporter)+'\"'

    if since:
        jira_filter = jira_filter+' AND createdDate >= '+str(since)

    # return jsonify(jira_filter)
    open_issues = jira.search_issues(jira_filter, maxResults=500)
    return jsonify(create_dashboard_stats(open_issues, JIRA_SETTINGS, user_email))


def create_dashboard_stats(open_issues, JIRA_SETTINGS, user_email):
    JIRA_URL = JIRA_SETTINGS["JIRA_URL"]
    JIRA_PROJECT = JIRA_SETTINGS["JIRA_PROJECT"]
    JIRA_COMPONENTS = JIRA_SETTINGS["JIRA_COMPONENTS"]

    return_obj = {}
    issue_statusses = {}
    issue_priorities = {}

    for open_issue in open_issues:
        key = str(open_issue.key)
        summary = str(open_issue.fields.summary)
        
        status = str(open_issue.fields.status.name)
        if status not in issue_statusses:
            issue_statusses[status] = []

        if key not in issue_statusses[status]:
            issue_statusses[status].append({key:summary})

        priority = str(open_issue.fields.priority.name)
        if priority not in issue_priorities:
            issue_priorities[priority] = []

        if key not in issue_priorities[priority]:
            issue_priorities[priority].append({key:summary})
        
    return_obj['by_status'] = issue_statusses
    return_obj['by_severity'] = issue_priorities

    return return_obj

def get_jira_states(JIRA_SETTINGS):
    JIRA_URL = JIRA_SETTINGS['JIRA_URL']
    JIRA_USER = JIRA_SETTINGS['JIRA_USER']
    JIRA_PASS = JIRA_SETTINGS['JIRA_PASS']
    JIRA_PROJECT = JIRA_SETTINGS['JIRA_PROJECT']

    STATUS_N_SEVERITY = JIRA_SETTINGS['STATUS_N_SEVERITY']
    STATUS_CODES = JIRA_SETTINGS['STATUS_CODES']
    COLOR_CODES = JIRA_SETTINGS['COLOR_CODES']

    jira_states = STATUS_N_SEVERITY
    states = requests.get(JIRA_URL+'rest/api/latest/project/'+JIRA_PROJECT+'/statuses', auth=HTTPBasicAuth(JIRA_USER, JIRA_PASS), verify=False).json()
    if 'errorMessages' not in states:
        for state in states:
            if state['name'] in ["Task","Bug"]:
                for status in state['statuses']:
                    if status['name'] not in jira_states['by_status']:
                        jira_states['by_status'].append(status['name'])

    states = requests.get(JIRA_URL+'rest/api/latest/priority', auth=HTTPBasicAuth(JIRA_USER, JIRA_PASS), verify=False).json()
    if 'errorMessages' not in states:
        for state in states:
            if state['name'] not in jira_states['by_severity']:
                jira_states['by_severity'].append(state['name'])

    jira_states['STATUS_CODES'] = STATUS_CODES
    jira_states['COLOR_CODES'] = COLOR_CODES

    return jsonify(jira_states)

def get_open_tickets(jira,JIRA_SETTINGS):

    JIRA_URL = JIRA_SETTINGS["JIRA_URL"]
    JIRA_PROJECT = JIRA_SETTINGS["JIRA_PROJECT"]
    JIRA_COMPONENTS = JIRA_SETTINGS["JIRA_COMPONENTS"]
    JIRA_FILTERS = JIRA_SETTINGS["JIRA_FILTERS"]

    open_issues = jira.search_issues('filter='+str(JIRA_FILTERS['Open_Tickets']), maxResults=1000)

    return get_jira_issue_strings(open_issues, JIRA_SETTINGS);

def get_jira_issue_strings(open_issues, JIRA_SETTINGS):

    secreview_string = ""
    secbugs_string = ""

    JIRA_URL = JIRA_SETTINGS["JIRA_URL"]
    JIRA_PROJECT = JIRA_SETTINGS["JIRA_PROJECT"]
    JIRA_COMPONENTS = JIRA_SETTINGS["JIRA_COMPONENTS"]

    for open_issue in open_issues:
        status = str(open_issue.fields.status.name)
        icon = 'glyphicon glyphicon-hourglass icon_info blue" title="Open'
        if status == "In Progress" or status == "InDevelopment" :
            icon = 'glyphicon glyphicon-road icon_info green" title="In Progress'
        if status == "Waiting for customer":
            icon = 'glyphicon glyphicon-time icon_info orange" title="Waiting for customer'
        if status in ("Backlog","To Start","To Do","Open"):
            icon = 'glyphicon glyphicon-hourglass icon_info blue" title="Open'
        if status == "Under Review":
            icon = 'glyphicon glyphicon-fire icon_info red" title="Under Review'

        key = str(open_issue.key)
        print key
        assignee = str(open_issue.fields.assignee)
        summary = str(open_issue.fields.summary)

        description = str(open_issue.fields.description)
        descriptions = description.split("\n")

        requestingfor = ""
        for key_values in descriptions:
            key_values = key_values.split(" : ")
            if "*requestingfor*" in key_values:
                for value in key_values:
                    if "requestingfor" not in value:
                        requestingfor = value
                        break
                break


        msg_string = '<tr><td align="center"><span class="'+icon+'"></span>&nbsp;&nbsp;&nbsp;&nbsp;<span class="glyphicon glyphicon-user" title="'+assignee+'"></span></td>'
        msg_string += '<td class="summary">'+key+' - <a href="'+JIRA_URL+'/browse/'+key+'" target="_blank">'+summary+'</a></td>'
        
        components = open_issue.fields.components
        for component in components:
            if str(component.name) == JIRA_COMPONENTS["SECURITY_REVIEW"]:
                msg_string += '<td><a class="secreview" onclick="open_issue(\''+key+'\',\''+status+'\',\''+summary+'\',\''+requestingfor+'\')" href="#"><button type="button" class="btn btn-primary pull-right">Close Ticket</button></a></td></tr>'
                secreview_string += msg_string
                break

            if str(component.name) == JIRA_COMPONENTS["SECURITY_BUG"]:
                msg_string += '<td><a class="secreview" onclick="open_issue(\''+key+'\',\''+status+'\',\''+summary+'\',\''+requestingfor+'\')" href="#"><button type="button" class="btn btn-primary pull-right">Close Bug</button></a></td></tr>'
                secbugs_string += msg_string
                break
    
    return [secreview_string,secbugs_string]


def resolve_or_close_jira(jira,JIRA_TRANSITIONS,status,key,comments,action=None,approver=None):
    
    if not action:
        return None

    if action == "Approve":
        transaction_id = JIRA_TRANSITIONS['APPROVE_TRANS']
        fields = {'resolution':{'name': 'Done'}}

    if action == "Reject":
        fields = {'resolution':{'name': 'Won\'t Do'}}
        transaction_id = JIRA_TRANSITIONS['CLOSED_TRANS']

        if status == "Under review":
            transaction_id = JIRA_TRANSITIONS['REJECT_APPROVAL']
            fields = None

    if action == "Send for Review":
        transaction_id = JIRA_TRANSITIONS['SEND_FOR_REVIEW_TRANS']
        fields = None

    try:
        jira.add_comment(key,comments)
        result = jira.transition_issue(key, transaction_id, fields=fields)
        if approver:
            try:
                jira.assign_issue(key,approver)
            except Exception, ae:
                print ae
                pass

        return True

    except Exception, ae:
        print ae
        return False

    return None


    





