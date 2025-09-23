from .encryption import Encryption
from .storage import Storage
from .manager import Manager
from .oauth import OAuthClient
from .twofa import TwoFA 

__all__ = ["Encryption", "Storage","Manager","OAuthClient","TwoFA"]

class AuthKit:
    def __init__(self):
        self.encryption = Encryption()
        self.storage = Storage()
        self.manager = Manager()
        self.oauth_client = OAuthClient()
        self.twofa = TwoFA()