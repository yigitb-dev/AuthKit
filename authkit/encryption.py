from cryptography.fernet import Fernet
import math

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
    
    def get_password_strength(password):

        # Initialize counters and lists
        uppercase_letters = 0
        lowercase_letters = 0
        special_chars = 0
        special_chars_list = ["!", "@", "#", "$", "%", "^", "&", "*"]
        common_patterns_list = ["1234", "qwerty", "azerty", "password"]
        numbers_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
        number_count = 0
        common_patterns_count = 0
        password_len = len(password)
        entropy_symbol_set_size = 0
        total_point = 0
        temp_var_password = ''

        # Analyze the password
        for char in password:
            if char.isupper():
                uppercase_letters += 1
                if uppercase_letters ==1:
                    entropy_symbol_set_size +=26
            if char in special_chars_list:
                special_chars += 1
                if special_chars==1:
                    entropy_symbol_set_size += len(special_chars_list)
            if char.islower():
                lowercase_letters += 1
                if lowercase_letters==1:
                    entropy_symbol_set_size +=26
            if char in numbers_list:
                number_count += 1
                if number_count==1:
                    entropy_symbol_set_size+=10


            temp_var_password += char

            # Check for common patterns
            for pattern in common_patterns_list:
                if temp_var_password == pattern:
                    common_patterns_count += 1

        # Evaluate password strength
        if password_len >= 8:
            total_point += 1

        if uppercase_letters >= 1 and lowercase_letters >= 1:
            total_point += 1

        if number_count >= 1:
            total_point += 1
        
        #Calculate entropy
        entropy = password_len*math.log2(entropy_symbol_set_size)

        if entropy >=50:
            total_point +=1
        elif entropy <= 28:
            total_point-=1

        total_point -= common_patterns_count

        return total_point # Weak: <=1 Moderate: 2-3 Strong: >=4







