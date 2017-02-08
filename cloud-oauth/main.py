###########################################
# Author: Peter Nguyen
# Date: 2/12/17
# CS496-400
# Description: Implementation of OAuth 2.0
# server side flow
###########################################

from google.appengine.ext import ndb
import webapp2
import json
import logging

class Home(webapp2.RequestHandler):
    def get(self):
        self.response.write("CS496-400 - OAuth 2.0 Implemntation - Author: Peter Nguyen")

class OauthHandler(webapp2.RequestHandler):
    def get(self):
        logging.debug('The contents of Get request: ' + repr(self.request.GET))

app = webapp2.WSGIApplication([
    ('/', Home),
    ('/oauth', OauthHandler)
], debug=True)
