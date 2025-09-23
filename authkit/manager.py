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
    
    def add_password(self, service, username, password):
        data = self.storage.read()
        encrypted_password = self.encryption.encrypt(password)  
        data[service] = {"username": username, "password": encrypted_password.decode()}
        self.storage.write(data)
    
    def get_password(self, service):
        data = self.storage.read()
        if service in data:
            encrypted_password = data[service]["password"].encode()
            return {
                "username": data[service]["username"],
                "password": self.encryption.decrypt(encrypted_password)
            }
        return None

    def login(self, service, username, password):
        stored = self.manager.get_password(service)
        if stored and stored["username"] == username and stored["password"] == password:
            return True
        return False