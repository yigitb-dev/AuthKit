import requests
import urllib.parse

class OAuthClient:
    def __init__(self):
        self.OAuth_providers = {}
    
    def add_provider(self, name, client_id, client_secret, auth_url, token_url, redirect_uri):
        self.OAuth_providers[name] = {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_url": auth_url,
            "token_url": token_url,
            "redirect_uri": redirect_uri
                                        }
    
    def get_auth_url(self, provider_name, state):
        service =  self.OAuth_providers[provider_name]
        params = {
            "response_type": "code",
            "client_id": service["client_id"],
            "redirect_uri": service["redirect_uri"],
            "state": state,
            "scope": "read"
        }
        return f"{service['auth_url']}?{urllib.parse.urlencode(params)}" #Construct the full URL with parameters
    
    
    def get_token(self, provider_name, code):
        service =  self.OAuth_providers[provider_name]
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": service["redirect_uri"],
            "client_id": service["client_id"],
            "client_secret": service["client_secret"]
        }
        response = requests.post(service["token_url"], data=data)
        return response.json()