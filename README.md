[![Github Release Version](https://img.shields.io/badge/release-V1.0-blue.svg)](https://github.com/mohangcsm/secops)
[![Python Version](https://img.shields.io/badge/python-2.7-blue.svg)](https://github.com/mohangcsm/secops)

# SECOPS Framework for Centralised Product Security Operations.

SECOPS Framework has below functional benifits over a common bug/issue tracking system,

#### Goals
    - Helps Security Teams to gather initial information in a systematic way.
    - Allows to integrate various other security tools via REST Apis.
    - Bring audit capabilities to different types of security operations.

#### How to install SECOPS:

- `git clone https://github.com/mohangcsm/secops.git` or download the zip
- `pip install -r requirements.txt`

#### Running SECOPS:
- run `python run.py` to launch server

- SECOPS server can be accessed from http://server_ip or https://server_ip


#### Docker Installation
```
$ git clone https://github.com/mohangcsm/secops.git
$ cd secops
```
Update the **config.py** file with required values as mentioned below section, then build and run docker with below commands. (change port mapping as defined in the config file)

#### If you are planning to do continuous development:
    - Build a temporary image with all dependencies installed
    - Build the final image with preinstalled dependencies
    - run secops container from the final image

```
$ docker build -f Dockerfile --rm -t secops1 . 
$ docker build -f Dockerfile2 --rm -t secops .
$ docker run --rm -d -p 80:80 -p 443:443 secops 
```

#### If you are planning to use as it is:
```
$ docker build --rm -t secops . 
$ docker run --rm -d -p 80:80 -p 443:443 secops 
```

##### Things to do before running: 
- in **config.py**
    - update values for GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, SECRET_KEY, ALLOWED_DOMAIN etc
    - edit the port of the app (Default: 80)
    - update the `JIRA_SETTINGS` with jira url and credentials. use jira access token instead of password
    - update the `JIRA_TRANSTIONS` according to 1factor workflow
    - update `external page links settings` as required.
    - create a default user (appsec) in JIRA `or` update DEFAULT_USER in config with any one of the jira user

#####
- Update JIRA Project Configuration to integrate with SECOPS Framework
    - Create Workflow according to the requirement. Workflows required for 1-factor approval and 2-factor approval can be found in the `WORKFLOWS` folder
    - Create 2 jira componants with names `Security Reviews` and `Security Bugs`
    - create `JIRA filters` (with exact names) as mentioned in JIRA_SETTINGS

#####
##### Enabling Peer Review & approval process
- in **config.py** 
    - update the `PEER_REVIEW_ENABLED=True`
    - update the values in `PEER_REVIEW_REQUIRED_FOR` with type of reviews that you require 2nd level approval
    - update the `JIRA_TRANSTIONS` values according to 2factor workflow
#####
#### For HTTPS Support:
- Generate or procure an SSL certificate and keyfile
- move the certificate and key file to SECOPS server.
- update the Domain settings in `config.py` file (HTTPS port, certificate path, key file path etc)
- uncomment the `HTTPS` section in `run.py` file and make sure to comment out the `HTTP` section.
#####

#### Adding New type of Security Requests

- Edit the **application/static/request_options.json** json to add/modify new secreview options

    - First update the `base_options` section to update the dropdown list
        - to add a new entry into dropdown add the respective **KEY:VALUE** data into JSON object
        
        For example, to add **new type of review** category under **Others** section, use below
    ```
        "Others" : {
            "PRD Document Review" : "prd_review",
            "Architecture Review" : "arch_review",
            "Security Bug" : "sec_bug",
            "Others" : "others",
            "new type of review" : "new_type_of_review"
        }
    ```
    - Now add HTML entities into `request_options` section to show the relevent form when the option is selected
        - **label** : Any label you want to show before the input element. Update this as needed
        - **name** : This will be the parameter name with which the input will be posted to server
        - **innerHtml** : prefill data comes here. leave empty string here if prefilling is not needed
        - **placeholder** : placeholder to be shown for input text element
        - **elementType** : type of html element. must be one of `input/textarea`
        - **type** : ignore if elementType is **textarea**. if elementType is **input**  this must be one of `text/file/date`
    
        For example, to add a textarea under `new_type_of_review` form, add as below
    ```
        "new_type_of_review" : [
            {
                "label" : "Enter Name here",
                "name" : "name",
                "innerHtml" : "",
                "elementType" : "textarea"
            }
        ]
    ```
    - Similarly, update the JSON file with as many HTML elements as required. 
    - Validate the JSON format before closing the file.
    
#### Adding New Closing options for Security Reviews

- Edit the **application/static/options.json** json to add/modify closing options for secreviews

    For example, to add new closing option **Business Logic Validated** to `sec_bug` options, use as below.
    ```
    "sec_bug" : {
        "Fix Verified Dynamically" : "fix_verified",
        "Code Review Done" : "code_verified",
        "Business Logic Validated" : "bus_logic_valid"
    },
    ```
- In this newly added **KEY:VALUE** pair, value such as bus_logic_valid is **optional** and can be anything
- Validate the JSON format before closing the file.
##### TROUBLESHOOTS :

- READ FIRST : About Python 2 and 3 compatibility

    Some scripts and modules versions required here are written in python 2 and not ready yet for python 3
    so it is recommended to download and install both interpreters python 2 and also python 3 (for windows users don't forget to add their folder paths also in your environment variables)
    Then when calling python scripts in version 2 or 3 anyway (example with the package manager script PIP)
    
    you can run default python command like :
    
    `"python -m pip install ..." or "pip install ..."`
    
    To call only python 3 scripts choose  this  instead :
    
    `"py -m pip install ..." or "pip3 install ..."`

### Screenshots
#### Login and Home Page

![Login Page](https://github.com/mohangcsm/secops/raw/devdocs/screenshot/1.png)

![Home Page](https://github.com/mohangcsm/secops/raw/devdocs/screenshot/2.png)

#### New Security Review

![New Secreview](https://github.com/mohangcsm/secops/raw/devdocs/screenshot/3.png)

![Secreview Options](https://github.com/mohangcsm/secops/raw/devdocs/screenshot/4.png)

#### Closing Reviews and Bugs

![Close Tickets page](https://github.com/mohangcsm/secops/raw/devdocs/screenshot/5.png)

![Closing Options Page](https://github.com/mohangcsm/secops/raw/devdocs/screenshot/6.png)

#### Peer Review & Approval Page

![Send for Review Page](https://github.com/mohangcsm/secops/raw/devdocs/screenshot/7.png)


#### Core Softwares :
    - Python 2.7

### Lead Developer
    - Mohan Kallepalli (@mohankallepalli) 

### Credits
    - Myntra Security Team
    - Flipkart Security Team
    - Moengage Security Team

### Changelog
~~~
v1.2
    - 3rd party dependency library integrated
    - Additional request options added

v1.1
    - Security Metrics added with multiple dashboards.
    - Option for adding Security Policies and guidelines added in menu.
    - Security Code review UI controls added.
    - UI based followup controls for security reviews and security bugs.

v1.0
    - Unified Security review creation and Security Bug creation features added.
    - JSON based customisation for UI controls added.
    - Peer approval process added as a flag from configuration.
    - Auditing capabilities through JIRA workflow history.
~~~

### Roadmap
    - Executive summary mailer for Security Metrics.
    - API Integration with DAST, SAST and FOSS tools.

##### License: Apache 2.0
~~~~

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
~~~~