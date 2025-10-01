import json
import os
import hashlib
import secrets

class Storage:
    def __init__(self,filename="user_data.json"):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                json.dump({}, f)
        
    def read(self):
        with open(self.filename, 'r') as f:
            return json.load(f)
    
    def write(self, data):
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)
        
    
    def calculate_hash(self,data):
        data_string = json.dumps(data,sort_keys=True)
        return hashlib.sha256(data_string).hexdigest()
    
    def verify_hash(self,data,expected_hash):
        calculated_hash = Storage.calculate_hash(data)
        if calculated_hash == expected_hash:
            return True
        return False
    
    def generate_reset_token(self,username):
        token = secrets.token_urlsafe(16)
        data = Storage.read()
        data[username]["reset_token"] = token
        Storage.write(data)
        return token
    
    def verify_reset_token(self,username,to_verify):
        data = Storage.read()
        token = data[username]["reset_token"]
        if token == to_verify:
            return True
        return False
        


        
    
            