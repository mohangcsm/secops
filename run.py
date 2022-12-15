#!/usr/bin/python
# -*- coding: utf-8 -*-

from application import app

import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer


gevent.monkey.patch_all()


# ------- PRODUCTION CONFIG -------
if __name__ == '__main__':
    try:

        INTERFACE = app.config['INTERFACE']
        
        # ----------------- For HTTPS -------------------#
        HTTPS_PORT = app.config['HTTPS_PORT']
        SSL_CERTFILE = app.config['SSL_CERTFILE']
        SSL_KEYFILE = app.config['SSL_KEYFILE']

        server = WSGIServer((INTERFACE, HTTPS_PORT), app, certfile=SSL_CERTFILE, keyfile=SSL_KEYFILE,log=app.logger)
        if server:
            print "Server Started on: https://"+str(INTERFACE)+":"+str(HTTPS_PORT)+"/"


        # ---------------- For HTTP Only ----------------#
        # HTTP_PORT = app.config['HTTP_PORT']
        # server = WSGIServer((INTERFACE, HTTP_PORT), app,log=app.logger)

        # if server:
            # print "Server Started on: http://"+str(INTERFACE)+":"+str(HTTP_PORT)+"/"


        # -------Common for both HTTP and HTTPS----------#

    #     server.serve_forever()


    except KeyboardInterrupt:
        print "\nUser Abort Identified. Good Bye\n"

# ------- DEVELOPMENT CONFIG -------
# if __name__ == "__main__":
#     INTERFACE = app.config['INTERFACE']
#     PORT = app.config['HTTP_PORT']
#     DEBUG = app.config['DEBUG']
    
#     app.run(host=INTERFACE,port=PORT,debug=DEBUG)




