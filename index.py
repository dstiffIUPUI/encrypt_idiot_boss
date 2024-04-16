from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
import base64
import os

# Load the old private key
with open("old_private_key.pem", "rb") as key_file:
    old_private_key = serialization.load_pem_private_key(
        key_file.read(),
          password=None
    )

# Load the new public key
with open("new_public_key.pem", "rb") as key_file:
    new_public_key = serialization.load_pem_public_key(
        key_file.read(),
          
    )

# Specify the directory you want to use
directory = 'user_profiles'

# Loop over all files in the directory
for filename in os.listdir(directory):
    
    filepath = os.path.join(directory, filename)
    
   
    with open(filepath, 'rb') as file:
        encrypted_data = file.read()
        
        # Decrypt
        decrypted_data = old_private_key.decrypt(
            base64.b64decode(encrypted_data),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # Encrypt (i think it's supposed to be generally unreadable in this state.)
        encrypted_data = new_public_key.encrypt(
            decrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # new directory
        new_directory = 'new_user_profiles'
        os.makedirs(new_directory, exist_ok=True)
        new_filepath = os.path.join(new_directory, filename)
        with open(new_filepath, 'wb') as new_file:
            new_file.write(encrypted_data)
    
   