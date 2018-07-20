import json
import oauth2 as oauth
import os
import urllib2 as urllib

# See assignment1.html instructions or README for how to get these credentials

api_key = os.environ['COURSERA_API_KEY']
api_secret = os.environ['COURSERA_API_SECRET']
access_token_key = os.environ['COURSERA_ACCESS_TOKEN_KEY']
access_token_secret = os.environ['COURSERA_ACCESS_TOKEN_SECRET']

_debug = 0

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=api_key, secret=api_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"


http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''
def twitterreq(url, method, parameters):
  req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url, 
                                             parameters=parameters)

  req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

  headers = req.to_header()

  if http_method == "POST":
    encoded_post_data = req.to_postdata()
  else:
    encoded_post_data = None
    url = req.to_url()

  opener = urllib.OpenerDirector()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)

  response = opener.open(url, encoded_post_data)

  return response

def fetchsamples(query):
  last_id = None
  url_template = "https://api.twitter.com/1.1/search/tweets.json?lang=en&count=100&max_id={}&q={}"
  while True:
    url = url_template.format(last_id, query)
    parameters = []
    response = twitterreq(url, "GET", parameters)
    response_body = response.read()
    try:
        statuses = json.loads(response_body)['statuses']
    except:
        raise RuntimeError("Unexpected response: " + response_body)
    for status in statuses:
      print json.dumps(status)
      if last_id:
          last_id = min(last_id, int(status['id']))
      else:
          last_id = status['id']

if __name__ == '__main__':
  fetchsamples("apachekafka")
