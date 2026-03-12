#Retrieve the user’s Documents directory path.
#Decrypt the encryption key used by the ransomware.
#Recursively enumerate all files within the Documents folder.
#Open each file and read 100,000 bytes of data.
#Use RC4 with the decrypted key to decrypt the file contents.
#Write the decrypted data back to the same file.

from Crypto.Cipher import ARC4
import os

def decrypt_file(filename,key):
    try:
        with open(filename, 'rb') as file:
            encrypted_data = file.read()
            cipher = ARC4.new(key)
            
            decrypted_data = cipher.decrypt(encrypted_data)
            
        with open(filename, 'wb') as file:
            file.write(decrypted_data)
            
    except PermissionError:
        print(f"Permission Denied: {filename}")
        
        
        
def generate_key():
    
        encrypted_key = b"qwedadnsnfisadvyhbdksasfsdgsa"
        xor_key = b"WhatAreYouDoingHere?!"
       #i % len(xor_key) is used to ensure we start over once we've reached the end of xor_key
        key = bytes(encrypted_key[i] ^ xor_key[i % len(xor_key)] for i in range(len(encrypted_key))) #running a loop for the entire length of encrypted_key
        
        return key
        
        
if __name__ == "__main__":
    
    key = generate_key()
    path = os.path.expanduser("~/Documents")
    
    #Going through all the files and directories in Documents folder
    for root, dirs, files in os.walk(path):
        for file in files:
            if not file.endwith(('.exe', '.dll')):
                filepath = os.path.join(root,file)
                decrypt_file(filepath, key)
            
   

    print("Decryption completed successfully.")