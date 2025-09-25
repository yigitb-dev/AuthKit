import base32_lib as bs32
import json
import pyotp

class TwoFA:
    def __init__(self,filename="user_data.json"):
        self.filename = filename
    
    def generate_twofa_secret(self,username):
        secret = bs32.random_base32()
        with open(self.filename, "a") as f:
            data = json.load(f)
            if username in data:
                data[username]["2fa_secret"] = secret
            else:
                return "User not found"
        
    def get_twofa_secret(self,username):
        with open(self.filename, "r")as f:
            data = json.load(f)
            if username in data:
                return data[username]["2fa_secret"]
            else:
                return "User not found"
    
    def generate_twofa_token(self,username):
        secret = self.get_twofa_secret(username)
        if secret == "User not found":
            return "User not found"
        totp = pyotp.TOTP(secret)
        return totp.now()
    
    def twofa_verified(self,username,token):
        secret = self.get_twofa_secret(username)
        if secret == "User not found":
            return "User not found"
        totp = pyotp.TOTP(secret)
        return totp.verify(token)
        
