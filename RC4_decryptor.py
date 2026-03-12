#This is to decrypt a file, that was encrypted using RC4 and the key was generated using MD5

from Crypto.Cipher import ARC4 
from Crypto.Hash import MD5 

def decrypt_file (filename, key):
    
    with open(filename, 'rb') as f:
        ciphertext = f.read()
        
        #Creating an instance of MD5 
        md5 = MD5.new()
        #Entering key into the algorithm
        md5.update(key.encode())
        #Final MD5 generated based on the given key
        derived_key = md5.digest()
        
# Let's say, the key is "Hi, I've encrypted your files", now we're applying the MD5 algorithm on this string to get a MD5 value.
        #Creating an instance of ARC4 algorithm
        cipher = ARC4.new(derived_key)
        
        plaintext = cipher.decrypt(ciphertext)
        
        
        #Writing the Decrypted data into a new file
        
        with open("Decrypted.txt", 'wb') as f:
            f.write(plaintext)
            
        print("File decrypted Successfully!")
        
        
if __name__ == "__main__":
    
    filename = 'Encrypted.txt'
    key = 'KeyUsedForSymmetricEncryption' 
    decrypt_file(filename,key)
