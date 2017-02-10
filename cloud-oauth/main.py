###########################################
# Author: Peter Nguyen
# Date: 2/12/17
# CS496-400
# Description: Implementation of OAuth 2.0
# server side flow
###########################################

from google.appengine.ext import ndb
from google.appengine.api import urlfetch
from oauth2client import client
import webapp2
import json
import urllib
import logging
import string
import random

class Home(webapp2.RequestHandler):
    def get(self):
        # GET request for authorization from resource server
        state = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(30))
        responseType = 'code'
        clientID = '698547700374-pb73isaturrk4m4rcod8ajmo6kpuj6td.apps.googleusercontent.com'
        redirectURI = 'http://localhost:8080/oauth'
        scope = 'email'
        url = 'https://accounts.google.com/o/oauth2/v2/auth?' + "response_type=" + responseType + '&client_id=' + clientID + '&redirect_uri=' + redirectURI + '&scope=' + scope + '&state=' + state
        try:
            result = urlfetch.fetch(url)
            if result.status_code == 200:
                self.response.write(result.content)
            else:
                self.response.status_code = result.status_code
        except urlfetch.Error:
            logging.exception('Caught exception fetching url')

        self.response.write("CS496-400 - OAuth 2.0 Implementation - Author: Peter Nguyen")

class OauthHandler(webapp2.RequestHandler):
    def get(self):
        # Receive authorization code
        responseCode = self.request.GET['code']
        responseState = self.request.GET['state']

        # POST request for token
        try:
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            params = {
                'code': str(responseCode),
                'client_id': '698547700374-pb73isaturrk4m4rcod8ajmo6kpuj6td.apps.googleusercontent.com',
                'client_secret': 'scYrdsRwfvDl-d3uOJ-obRS0',
                'redirect_uri': 'http://localhost:8080/oauth',
                'grant_type': 'authorization_code'
            }
            result = urlfetch.fetch(
            	url='https://www.googleapis.com/oauth2/v4/token',
                payload=urllib.urlencode(params),
                method=urlfetch.POST,
                headers=headers)
    	except urlfetch.Error:
            logging.exception('Caught exception fetching url')

        # Receive access token
        response2 = json.loads(result.content)
        responseToken = response2['access_token']

        # GET request for data from the API
        try:
            headers = {'Authorization': 'Bearer ' + str(responseToken)}
            result2 = urlfetch.fetch(
            	url='https://www.googleapis.com/plus/v1/people/me',
                method=urlfetch.GET,
                headers=headers)
    	except urlfetch.Error:
            logging.exception('Caught exception fetching url')

        # Receive data from the resource server
        response3 = json.loads(result2.content)
        googleName = response3['displayName']
        googleUrl = response3['url']
        self.response.write('Google+ name: ')
        self.response.write(googleName)
        self.response.write('<br />Google+ url: ')
        self.response.write(googleUrl)
        self.response.write('<br />State variable received: ')
        self.response.write(responseState)

app = webapp2.WSGIApplication([
    ('/', Home),
    ('/oauth', OauthHandler),
], debug=True)
