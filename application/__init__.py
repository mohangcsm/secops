from flask import Flask
import logging
from logging.handlers import RotatingFileHandler
from flask.logging import default_handler

app = Flask(__name__)
app.config.from_object('config.Config')
logfile = app.config['ACCESS_LOGFILE_NAME']

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logHandler = RotatingFileHandler(logfile,maxBytes =1000000, backupCount=5)
logger.addHandler(logHandler)
logger.removeHandler(default_handler)

import views
