import http.client
import urllib
import os

"""
Push notification service using https://pushover.net/
Used to let us know about print supplies and maybe critical errors

Usage:
pusher = PushoverSender(push_user, push_api)
pusher.send("hello from python")
"""

class PushoverSender:
    def __init__(self, user_key_path, api_key_path):
        self.user_key = self.get_key(os.path.join(os.path.dirname(__file__), user_key_path))
        self.api_key = self.get_key(os.path.join(os.path.dirname(__file__), api_key_path))
        
    def send(self, text):
        conn = http.client.HTTPSConnection("api.pushover.net:443")
        post_data = {'user': self.user_key, 'token': self.api_key, 'message': text}
        conn.request("POST", "/1/messages.json", urllib.parse.urlencode(post_data), {"Content-type": "application/x-www-form-urlencoded"})
        #print(conn.getresponse().read())

    def get_key(self, filepath):
        with open(filepath) as f:
            key = f.read().strip()
        return key