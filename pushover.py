import http.client
import urllib

class PushoverSender:
    
    def __init__(self, user_key, api_key):
        self.user_key = user_key
        self.api_key = api_key
        
    def send(self, text):
        conn = http.client.HTTPSConnection("api.pushover.net:443")
        post_data = {'user': self.user_key, 'token': self.api_key, 'message': text}
        conn.request("POST", "/1/messages.json", urllib.parse.urlencode(post_data), {"Content-type": "application/x-www-form-urlencoded"})
        #print(conn.getresponse().read())
        