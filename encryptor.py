#This is to encrypt a file, using RC4 and using MD5 on a given key

from Crypto.Cipher import ARC4 
from Crypto.Hash import MD5 


def encrypt_file(filename,key):
    
    with open(filename, 'rb') as f:
        All_Text = f.read()
        
        md5=MD5.new()
        md5.update(key.encode())
        derived_key = md5.digest()
        
        cipher = ARC4.new(derived_key)
        
        encryptedtext = cipher.encrypt(All_Text)
        
        #Writing the Encrypted data into a new file
        
        with open("Encrypted.txt", 'wb') as f:
            f.write(encryptedtext)
            
        print("File Encrypted Successfully!")
        

if __name__ == "__main__":
    filename = "test1.txt"
    key = "KeyUsedForSymmetricEncryption"
    
    encrypt_file(filename,key)
        



