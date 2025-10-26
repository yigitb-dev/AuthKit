import json
import os
import hashlib
import secrets
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes


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
    
    #End2End Encryption
    def generate_key_pair(username):
        #Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )

        #Generate public key from private key
        public_key = private_key.public_key()

        #Serialize(convert to bytes)
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        #Save keys for user
        data = Storage.read()
        data[username] = {
            "public_key": public_pem.decode(),
            "private_key": private_pem.decode()
        }

        Storage.write(data)

        return public_pem
    
    #Sender Client-Side
    def e2e_encrypt(public_key,message):
            return  public_key.encrypt(message,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))

    def e2e_decryption():
        pass


    #Hashing Tools
    def calculate_hash(self,data):
        data_string = json.dumps(data,sort_keys=True)
        return hashlib.sha256(data_string).hexdigest()
    
    def verify_hash(self,data,expected_hash):
        calculated_hash = Storage.calculate_hash(data)
        if calculated_hash == expected_hash:
            return True
        return False
    

    #Password Reset
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
        


        
    
            