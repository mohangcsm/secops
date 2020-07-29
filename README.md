
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


##### Things to do before running: 
- in **config.py**
    - update values for GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, SECRET_KEY, ALLOWED_DOMAIN etc
    - edit the port of the app (Default: 80)
    - update the `JIRA_SETTINGS` with jira url and credentials. use jira access token instead of password
    - update the `JIRA_TRANSTIONS` according to 1factor workflow
#####
- Update JIRA Project Configuration to integrate with SECOPS Framework
    - Create Workflow according to the requirement. Workflows required for 1-factor approval and 2-factor approval can be found in the `WORKFLOWS` folder
    - Create 2 jira componants with names `Security Reviews` and `Security Bugs`
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
- MoEngage Security Team

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