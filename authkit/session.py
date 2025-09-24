import base32_lib as bs32
import uuid
import json

class SessionManager:
    def __init__(self,database_path="user_data.json"):
        self.database_path = database_path
        try:
            with open(database_path,'a') as database:
                self.database = database
        except FileNotFoundError:
            return "Database non-existent"


    def create_session(self,username):
        session_id = uuid.uuid4()
        if username in self.database:
            self.database[username]["session_id"] = session_id
        else: 
            return "User not found"
    
    def session_valid(self,username,session_id):
        if username in self.database:
            if session_id and self.database[username]["session_id"] == session_id:
                return True
            else:
                return False
        
        else:
            return "User not found"
    
    def end_session(self,username):
        if username in self.database:
            self.database[username].pop("session_id", None)
        else:
            return "User not logged in"
        
