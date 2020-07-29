from flask import Flask
import logging

app = Flask(__name__)
app.config.from_object('config.Config')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

import views
