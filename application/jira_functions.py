
from flask import jsonify
from requests.auth import HTTPBasicAuth
import json, requests
from datetime import datetime, timedelta
from application import app

app.config.from_object(__name__)
JIRA_SETTINGS = app.config['JIRA_SETTINGS']
DEFAULT_USER = app.config['DEFAULT_USER']

JIRA_URL = JIRA_SETTINGS['JIRA_URL']
JIRA_USER = JIRA_SETTINGS['JIRA_USER']
JIRA_PASS = JIRA_SETTINGS['JIRA_PASS']

JIRA_PROJECT = JIRA_SETTINGS["JIRA_PROJECT"]

JIRA_COMPONENTS = JIRA_SETTINGS["JIRA_COMPONENTS"]
JIRA_FILTERS = JIRA_SETTINGS["JIRA_FILTERS"]
JIRA_TRANSITIONS = JIRA_SETTINGS['JIRA_TRANSITIONS']

# def get_issue(jira, ticket_id):
auth = HTTPBasicAuth(JIRA_USER, JIRA_PASS)
headers = {"Accept": "application/json","Content-Type": "application/json"}




def create_new_jira(jira,JIRA_SETTINGS,product_title="", description="",component="Security Review",peer_review_enabled=False,Issue_Severity="Medium"):
    
    TODO_TRANS = JIRA_TRANSITIONS[peer_review_enabled]['TODO_TRANS']

    task = "Task"
    if component == JIRA_COMPONENTS["SECURITY_BUG"]:
        task = "Bug"

    duedate = 21
    if Issue_Severity in ["Highest","P0 (Blocker)"]:
        duedate = 5
        Issue_Severity = 'P0 (Blocker)'

    if Issue_Severity in ["High","P1 (Critical)","Urgent"]:
        duedate = 14
	Issue_Severity = 'P1 (Critical)'

    if Issue_Severity in ["Medium","P2 (Major)"]:
        duedate = 21
	Issue_Severity = 'P2 (Major)'

    if Issue_Severity in ["Low", "Lowest", "P3 (Minor)", "P4 (Trivial)", "None"]:
        duedate = 28
	Issue_Severity = 'P3 (Minor)'

    duedate = datetime.now() + timedelta(duedate)

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
        }],
        "priority":{
            "name": Issue_Severity
        },
        "duedate" : duedate.strftime('%Y-%m-%d')
    }

    # return fields

    url = JIRA_URL+"rest/api/latest/issue"
    payload = json.dumps({'fields':fields})

    try:
        # result = jira.create_issue(fields = fields)
        result = requests.request(
           "POST",
           url,
           data=payload,
           headers=headers,
           auth=auth,
           verify=False
        ).json()
        # print result
        return result
    
    except Exception, ae:
        print ae
        return str(ae)
        # return False

    return None

def search_issues(jql="project="+JIRA_PROJECT, total=30):
    url = JIRA_URL+"rest/api/latest/search"

    query = {
      'jql': jql,
      'maxResults': total
    }

    open_issues = requests.request(
       "GET",
       url,
       headers=headers,
       params=query,
       auth=auth,
       verify=False
    ).json()

    return open_issues['issues']

def transition_issue(key=0, transaction_id=0, fields={}, comments=""):
    payload = json.dumps({
      "transition": { 
         "id": transaction_id 
      } 
    })
    
    if comments != "":
        payload = json.dumps({
           "update": { 
              "comment":[{ 
                 "add": { 
                    "body": comments
                  } 
              }] 
           }, 
          "transition": { 
             "id": transaction_id 
          } 
        })

    url = JIRA_URL+"rest/api/latest/issue/"+key+"/transitions"

    response = requests.request(
       "POST",
       url,
       data=payload,
       headers=headers,
       auth=auth,
       verify=False
    )

    return response


def get_jira_issues(jira, JIRA_SETTINGS, jira_filter, assignee=None, reporter=None, user_email=None, since=None):

    jira_filter = 'filter='+str(jira_filter)
    if assignee:
        jira_filter = jira_filter+' AND assignee=\"'+str(assignee)+'\"'

    if reporter:
        jira_filter = jira_filter+' AND reporter=\"'+str(reporter)+'\"'

    if since:
        jira_filter = jira_filter+' AND  createdDate >= '+str(since)


    open_issues = search_issues(jira_filter, 500)

    # open_issues = jira.search_issues(jira_filter, maxResults=500)
    return jsonify(create_dashboard_stats(open_issues, JIRA_SETTINGS, user_email))


def create_dashboard_stats(open_issues, JIRA_SETTINGS, user_email):
    return_obj = {}
    issue_statusses = {}
    issue_priorities = {}

    from pprint import pprint

    # print(open_issues)
    # return return_obj

    for open_issue in open_issues:
        print(type(open_issue))
        key = str(open_issue['key'])
        summary = str(open_issue['fields']['summary'])
        
        status = str(open_issue['fields']['status']['name'])
        if status not in issue_statusses:
            issue_statusses[status] = []

        if key not in issue_statusses[status]:
            issue_statusses[status].append({key:summary})

        priority = str(open_issue['fields']['priority']['name'])
        if priority not in issue_priorities:
            issue_priorities[priority] = []

        if key not in issue_priorities[priority]:
            issue_priorities[priority].append({key:summary})
        
    return_obj['by_status'] = issue_statusses
    return_obj['by_severity'] = issue_priorities

    return return_obj

def get_jira_states(JIRA_SETTINGS, jira_type=None):

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

    if jira_type != "secbug":
        states = requests.get(JIRA_URL+'rest/api/latest/project/SEC/statuses', auth=HTTPBasicAuth(JIRA_USER, JIRA_PASS), verify=False).json()
        if 'errorMessages' not in states:
            for state in states:
                if state['name'] in ["Task","Bug"]:
                    for status in state['statuses']:
                        if status['name'] not in jira_states['by_status']:
                            jira_states['by_status'].append(status['name'])

        states = requests.get(JIRA_URL+'rest/api/latest/project/AS/statuses', auth=HTTPBasicAuth(JIRA_USER, JIRA_PASS), verify=False).json()
        if 'errorMessages' not in states:
            for state in states:
                if state['name'] in ["Bug"]:
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

def get_open_tickets(jira,JIRA_SETTINGS,user_email):

    open_issues = search_issues('filter='+str(JIRA_FILTERS['open_tickets']), 500)

    return get_jira_issue_strings(open_issues, JIRA_SETTINGS, user_email);

def get_open_ticket_by_id(jira,JIRA_SETTINGS,ticket_id,user_email):

    jql = 'key in ('+str(ticket_id).strip("[").strip("]")+')'
    
    open_issues = search_issues(jql, 10)
    
    return get_jira_issue_strings(open_issues, JIRA_SETTINGS, user_email);    

def get_jira_issue_strings(open_issues, JIRA_SETTINGS,user_email):

    secreview_string = ""
    secbugs_string = ""
    secreview_count = 0
    secbugs_count = 0

    for open_issue in open_issues:
        status = str(open_issue['fields']['status']['name'])
        icon = 'glyphicon glyphicon-hourglass icon_info blue" title="Open'
        if status == "In Progress" or status == "InDevelopment" :
            icon = 'glyphicon glyphicon-road icon_info green" title="In Progress'
        if status == "Waiting for customer":
            icon = 'glyphicon glyphicon-time icon_info orange" title="Waiting for customer'
        if status in ("Backlog","To Start","To Do","Open"):
            icon = 'glyphicon glyphicon-hourglass icon_info blue" title="Open'
        if status == "Under Review":
            icon = 'glyphicon glyphicon-fire icon_info red" title="Under Review'

        key = str(open_issue['key'])
        summary = str(open_issue['fields']['summary'])

        assignee = open_issue['fields']['assignee']
        if assignee:
            assignee = str(assignee['emailAddress'])
        else:
            assignee = user_email

        description = str(open_issue['fields']['description']).lower()
        descriptions = description.split("\n")

        requestingfor = ""
        for key_values in descriptions:
            key_values = key_values.split(" : ")
            if "requestingfor" in key_values or "*requestingfor*" in key_values:
                for value in key_values:
                    if "requestingfor" not in value:
                        requestingfor = value
                        break
                break


        requestingfor = requestingfor.rstrip().lstrip();

        due_date = str(open_issue['fields']['duedate'])
        
        due_days = "-9999"
        if due_date != "None":
            due_date = datetime.strptime(due_date, '%Y-%m-%d')
            due_days = str((datetime.now() - due_date).days)

        follow_days = 'Follow up ('+due_days+' days)'
        follow_class = "primary"

        if int(due_days) > 10:
            follow_class = "warning"

        if int(due_days) > 30:
            follow_class = "danger"

        if int(due_days) < 0:
            follow_class = "success"

        if int(due_days) == -9999:
            follow_class = "info"
            follow_days = "No Due date"

        follow_onclick = '"followup(\''+key+'\',\''+status+'\',\''+summary+'\',\''+requestingfor+'\',\''+due_days+'\',\''+follow_class+'\',\''+assignee+'\')"'
        if int(due_days) == -9999:
            follow_onclick = '#'

        msg_string = '<tr><td align="center"><span class="'+icon+'"></span>&nbsp;&nbsp;&nbsp;&nbsp;<span class="glyphicon glyphicon-user" title="'+assignee+'"></span></td>'
        msg_string += '<td class="summary">'+key+' - <a href="'+JIRA_URL+'browse/'+key+'" target="_blank">'+summary+'</a></td>'
        if follow_onclick != "#":
            msg_string += '<td><a onclick='+follow_onclick+' href="#"><button class="btn btn-'+follow_class+' btn-md"  data-toggle="modal" data-target="#followModal">'+follow_days+'</button></a></td>'
        else:
            msg_string += '<td><a onclick="alert(\'Due date is not set.\')" href="#"><button class="btn btn-'+follow_class+' btn-md"  >'+follow_days+'</button></a></td>'
                
        components = open_issue['fields']['components']
        components_found = False

        for component in components:
            if str(component['name']) == JIRA_COMPONENTS["SECURITY_REVIEW"]:
                msg_string += '<td><a class="secreview pull-right" onclick="open_issue(\''+key+'\',\''+status+'\',\''+summary+'\',\''+requestingfor+'\',\''+due_days+'\')" href="#"><button type="button" class="btn btn-primary">Close Ticket</button></a></td></tr>'
                secreview_string += msg_string
                components_found = True
                secreview_count += 1
                break

            if str(component['name']) == JIRA_COMPONENTS["SECURITY_BUG"]:
                msg_string += '<td><a class="secreview pull-right" onclick="open_issue(\''+key+'\',\''+status+'\',\''+summary+'\',\''+requestingfor+'\',\''+due_days+'\')" href="#"><button type="button" class="btn btn-primary">Close Bug</button></a></td></tr>'
                secbugs_string += msg_string
                components_found = True
                secbugs_count += 1
                break

        if not components_found:
            if key.startswith('SEC-'):
                msg_string += '<td><a class="secreview" onclick="open_issue(\''+key+'\',\''+status+'\',\''+summary+'\',\''+requestingfor+'\',\''+due_days+'\')" href="#"><button type="button" class="btn btn-primary pull-right">Close Ticket</button></a></td></tr>'
                secreview_string += msg_string
                secreview_count += 1

            if key.startswith('AS-'):
                msg_string += '<td><a class="secreview" onclick="open_issue(\''+key+'\',\''+status+'\',\''+summary+'\',\''+requestingfor+'\',\''+due_days+'\')" href="#"><button type="button" class="btn btn-primary pull-right">Close Bug</button></a></td></tr>'
                secbugs_string += msg_string
                secbugs_count += 1

    return [secreview_string,secbugs_string, secreview_count,secbugs_count]


def resolve_or_close_jira(jira,JIRA_TRANSITIONS,status,key,comments,action=None,approver=None):
    
    if not action:
        return [False, "Action parameter missing"]

    if status == "Open":
        return [False, "Issue is in Open Status"]

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
        result = transition_issue(key, transaction_id, fields=fields, comments=comments)
        msg = None
        if approver:
            try:
                assign_issue(key,approver)
            except Exception as ae:
                app.logger.warning(str(ae))
                msg = str(ae)
                return [False, msg]

        return [True,msg]

    except Exception as ae:
        app.logger.warning(str(ae))
        msg = str(ae)
        return [False, msg]

    return [None,msg]

def jira_followup(jira, key, comment, assignee='appsec'):
    return_obj = {}
    return_obj['key'] = key

    # accId = ""
    # accId = get_jira_accId(assignee)
    # if not key or not comment:
    #     return_obj['status'] = "error"
    #     return_obj['message'] = "key or comment missing"
    # else:
    if "@" not in assignee:
        assignee = assignee+"@"+app.config['ALLOWED_DOMAINS'][0]

    comment = "[~"+assignee+"]\n\n"+comment
    try:
        # jira.add_comment(key,comment)
        add_comment(key,comment)
        return_obj['status'] = "suucess"
        return_obj['message'] = "Followup comment added on Issue: "+key
        return_obj['assignee'] = assignee

    except Exception, ae:
        return_obj['status'] = "error"
        return_obj['message'] = ae

    return return_obj

def add_comment(key=0, comment=""):
    payload = json.dumps({"body": comment})

    url = JIRA_URL+"rest/api/latest/issue/"+key+"/comment"

    response = requests.request(
       "POST",
       url,
       data=payload,
       headers=headers,
       auth=auth,
       verify=False
    ).json()

    return response
    

def get_jira_accId(user):
    url = JIRA_URL+'rest/api/latest/user/search?query='+user

    user = requests.request(
        "GET",
        url,
        headers=headers,
        auth=auth,
        verify=False
    ).json()

    print user

    if(len(user)):
        user = user[0]
        accId = user['accountId']
    else:
        accId = get_jira_accId(DEFAULT_USER)

    return accId

def assign_issue(key, assignee):
    if "@" not in assignee:
        assignee = assignee+"@"+app.config['ALLOWED_DOMAINS'][0]

    payload = {'name': assignee}

    assignment_status = None
    try:
        url = JIRA_URL+'rest/api/latest/issue/'+key+'/assignee'
        
        assignment_status = requests.request(
           "PUT",
           url,
           data=payload,
           headers=headers,
           auth=auth,
           verify=False
        ).json()

        if assignment_status['status_code'] == 204:
            return "Success"

    except Exception, ae:
        return "Failed"


    return "Failed"

def link_issue(jira, key1, key2):

    url = JIRA_URL+"rest/api/latest/issueLink"
    payload = json.dumps({
      "inwardIssue": {
        "key": key1
      },
      "outwardIssue": {
        "key": key2
      },
      "type": {
        "name": "blocks"
      }
    })


    try:
        # link_status = jira.create_issue_link('blocks', key1, key2)
        link_status = requests.request(
           "POST",
           url,
           data=payload,
           headers=headers,
           auth=auth,
           verify=False
        )

        if link_status['status_code'] == 201:
            return "Success"

        return "Failed"

    except Exception, ae:
        return str(ae)

    return "Failed"
