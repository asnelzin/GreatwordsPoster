import time
import string
import random
import urllib.parse
import hashlib
import hmac
import base64
import httplib2

UPDATE_URL = 'https://api.twitter.com/1.1/statuses/update.json'


class Keys:
    keys = {}

    def __init__(self, consumer_key, consumer_secret, token, token_secret):
        self.keys = {'oauth_consumer_key': consumer_key,
                     'oauth_consumer_secret': consumer_secret,
                     'oauth_token': token,
                     'oauth_token_secret': token_secret}


class Request(object):
    headers = {
        "Content-type": "application/x-www-form-urlencoded"
    }
    params = {}
    secrets = {}

    def __init__(self, keys, http_method, http_url, params):
        self.http_url = http_url
        self.http_method = http_method

        self.params = params
        self.params['oauth_consumer_key'] = keys.keys['oauth_consumer_key']
        self.params['oauth_token'] = keys.keys['oauth_token']
        self.params['oauth_signature_method'] = 'HMAC-SHA1'
        self.params['oauth_version'] = '1.0'
        self.params['oauth_nonce'] = ''.join([random.choice(string.digits) for i in range(8)])
        self.params['oauth_timestamp'] = str(int(time.time()))

        self.secrets['oauth_consumer_secret'] = keys.keys['oauth_consumer_secret']
        self.secrets['oauth_token_secret'] = keys.keys['oauth_token_secret']

    def _get_param_string(self):
        return '&'.join(['%s=%s' % (urllib.parse.quote(k, ''),
                urllib.parse.quote(v, '')) for k, v in sorted(self.params.items())])

    def sign_request(self):
        print(self._get_param_string())
        base_string = (self.http_method.upper() + '&' + urllib.parse.quote(self.http_url, '') + '&' +
                       urllib.parse.quote(self._get_param_string(), ''))
        signing_key = (urllib.parse.quote(self.secrets['oauth_consumer_secret'], '') + '&' +
                       urllib.parse.quote(self.secrets['oauth_token_secret'], ''))

        signature = hmac.new(signing_key.encode('utf-8'), base_string.encode('utf-8'), hashlib.sha1)
        self.params['oauth_signature'] = base64.b64encode(signature.digest())

    def get_header(self):
        return self.headers

    def get_data(self):
        return urllib.parse.urlencode(self.params)


def post_update(keys, status):
    #connection = http.client.HTTPConnection('twitter.com')
    params = {'status': status}
    r = Request(keys, 'POST', UPDATE_URL, params)
    r.sign_request()

    httplib2.debuglevel = 1
    h = httplib2.Http()
    response, content = h.request(UPDATE_URL,  r.http_method, r.get_data(), headers=r.get_header())
    print(response, content)





