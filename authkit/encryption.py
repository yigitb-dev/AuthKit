from cryptography.fernet import Fernet

class Encryption:
    def __init__(self,key=None):
        if key is None:
            self.key = Fernet.generate_key()
        self.key = key
        self.fernet = Fernet(self.key)
    
    def encrypt(self, data):
        return self.fernet.encrypt(data.encode()).decode()
    

    def decrypt(self,key):
        return self.fernet.decrypt(key.encode()).decode()