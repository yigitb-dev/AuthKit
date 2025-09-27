from .encryption import Encryption
from .storage import Storage
from .manager import Manager
from .oauth import OAuthClient

class Manager:

    
    def __init__(self, key=None, filename="passwords.json"):
        self.encryption = Encryption(key)
        self.storage = Storage(filename)
        self.manager = Manager(key, filename)
        self.oauth_client = OAuthClient()
    
    def register_user(self,username, password):
        data = self.storage.read()
        encrypted_password = self.encryption.encrypt(password)  
        data[username] = {"password": encrypted_password.decode()}
        self.storage.write(data)
    
    def get_password(self, username):
        data = self.storage.read()
        if username in data:
            encrypted_password = data[username]["password"].encode()
            return {
                self.encryption.decrypt(encrypted_password)
            }
        return None

    def login(self,username, password):
        stored = self.manager.get_password(username)
        if stored == password:
            return True
        return False
    
    