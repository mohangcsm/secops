

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
        jira.transition_issue(result.key,TODO_TRANS)
        return result
    
    except Exception, ae:
        print ae
        return False

    return None

def get_open_secreviews(jira,JIRA_SETTINGS):

    JIRA_URL = JIRA_SETTINGS["JIRA_URL"]
    JIRA_PROJECT = JIRA_SETTINGS["JIRA_PROJECT"]
    JIRA_COMPONENTS = JIRA_SETTINGS["JIRA_COMPONENTS"]

    open_issues = jira.search_issues('component in ("'+JIRA_COMPONENTS["SECURITY_BUG"]+'","'+JIRA_COMPONENTS["SECURITY_REVIEW"]+'") AND status not in (Closed, Resolved, Done) AND project = "'+JIRA_PROJECT+'" ORDER BY created DESC')

    secreview_string = ""
    secbugs_string = ""

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
                # msg_string += '<td><a href="'+JIRA_URL+'/browse/'+key+'" target="_blank"><button type="button" class="btn btn-primary pull-right"> open ticket </button></a></td></tr>'
                secbugs_string += msg_string
                break
        
    return [secreview_string,secbugs_string]



def resolve_or_close_jira(jira,JIRA_TRANSITIONS,key,comments,action=None,approver=None):
    
    if not action:
        return None

    if action == "Approve":
        transaction_id = JIRA_TRANSITIONS['APPROVE_TRANS']
        fields = {'resolution':{'name': 'Done'}}


    if action == "Reject":
        transaction_id = JIRA_TRANSITIONS['CLOSED_TRANS']
        fields = {'resolution':{'name': 'Won\'t Do'}}

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


    





