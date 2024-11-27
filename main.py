from cryptography.fernet import Fernet
import os
import json
import re
from datetime import datetime, timedelta

class passwordmanager:
    def __init__(self,password_file= "password.json"):
       self.key=None
       self.password_file = password_file 
       self.password_dict ={}

    def create_key(self, path):
        self.key= Fernet.generate_key()
        with open(path,"wb") as key_file:
            key_file.write(self.key)
            print(f"Key saved to {path}")
    
    def load_key(self,path):
        with open(path,'rb') as key_file:
            self.key = key_file.read()
    
    def encrypt_password(self,password):
        if self.key is None:
                raise ValueError(("Encryption key not loaded. Load or create a key first."))
        f=Fernet(self.key)
        encrypted_password = f.encrypt(password.encode()) 
        return encrypted_password
    
    def decrypt_password(self,encrypted_password):
        if self.key is None:
                raise ValueError(("decryption key not loaded. Load or create a key first."))
        f=Fernet(self.key)
        decrypted_password = f.decrypt(encrypted_password).decode()
        return decrypted_password
    
    def check_password_strength(self, password):
        if len(password) < 6:
            return False, "Password is too short"
        if not re.search(r'[A-Z]', password):
            return False, "Password should contain at least one uppercase letter"
        if not re.search(r'[0-9]', password):
            return False, "Password should contain at least one digit"
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "Password should contain at least one special character"
        return True, "Password is strong"
   

    def add_password(self,account,password):
        is_strong,message= self.check_password_strength(password)
        if not is_strong:
            print(f"password for {account} not added,due to :{message}")
            return
        encrypted_password = self.encrypt_password(password)
        self.password_dict[account] = {
            'password': encrypted_password.decode(),
            'created_at': datetime.now().isoformat()  # Store creation date
        }
        print(f"Password for {account} added.")
        
    
    def check_expiration(self, account, days_valid=1):
        password_data = self.password_dict.get(account)
        
        # Check if the account exists in the password dictionary
        if password_data is None:
            print(f"No password found for {account}")
            return
        
        # Calculate expiration based on creation date
        created_at = datetime.fromisoformat(password_data["created_at"])
        if datetime.now() > created_at + timedelta(days=days_valid):
            print(f"Password for {account} is expired, consider updating it.")
        else:
            print(f"Password for {account} is still valid.")

    
    
    def get_password(self,account):
        password_data = self.password_dict.get(account)
        if password_data is None:
            print(f"No password found for {account}")
            return None
        encrypted_password = password_data['password']
        return self.decrypt_password(encrypted_password.encode())
     
    def save_password(self):
        with open(self.password_file, 'w') as file:
            json.dump(self.password_dict, file)
        print(f"Passwords saved to {self.password_file}")

    
    def  load_passwords(self):
        if os.path.exists(self.password_file):
            with open (self.password_file,'r') as file:
                self.password_dict=json.load(file)
            print(f"Password loaded from {self.password_file}")
        else:
            print(f"No password file found at {self.password_file}")




pm = passwordmanager()

# Create a key and optionally save it to a file (replace 'keyfile.key' with a valid path if needed)
pm.create_key('keyfile.key')
pm.load_key('keyfile.key')

# Add passwords
pm.add_password('arishsethi10@gmail.com', 'pookie')
pm.add_password('Arish-sethi', 'Laddle2008!')

# Retrieve and print passwords
print(f"arishsethi10@gmail.com: {pm.get_password('arishsethi10@gmail.com')}")
print(f"Arish-sethi: {pm.get_password('Arish-sethi')}")

# Save passwords to a file
pm.save_password()

# Load passwords from the file
pm.load_passwords()

# Verify loaded passwords
print(f"pookie23 (after loading): {pm.get_password('arishsethi10@gmail.com')}")
print(f"laddle2008 (after loading): {pm.get_password('Arish-sethi')}")

pm.check_expiration('arishsethi10@gmail.com', days_valid=1)
pm.check_expiration('Arish-sethi', days_valid=1)

# Prompt the user for account to retrieve password
account_to_retrieve = input("Enter the account to retrieve the password for: ")

# Retrieve and print the password
print(f"Password for {account_to_retrieve}: {pm.get_password(account_to_retrieve)}")

