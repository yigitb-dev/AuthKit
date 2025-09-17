import json
import os

class Storage:
    def __init__(self,filename="passwords.json"):
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