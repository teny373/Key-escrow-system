#Class: CIS-221
#Group: 2
#Project: Key escrow system
#Group members: Anoop, Pranav, Lisa, Evan, Teny


#imports library requests, and Fernet
import requests
from cryptography.fernet import Fernet

#urls to connect to the key escrow and request it to do things
url1 = 'http://10.0.0.177:5000/store_key'
url2 = 'http://10.0.0.177:5000/get_key'
url3 = 'http://10.0.0.177:5000/store_key_value'



def generate_key():
        # generated a key    
        key = Fernet.generate_key()
        #turns the key into utf-8 format
        key_str = key.decode('utf-8')
        #sends the key to the key escrow server
        response = requests.post(url3, json=key_str)
        #checks to see if the key was recieved based on the response or if your ip is authorized
        data = response.json()
        if data == '1':
                print("key not received")
        elif data =='2':
                print("key received")
        elif data == '3':
                print("not authorized")    

        #asks the user to make a key id for the key that was generated
        creation_key_id = input("please make a key id\n")
        #sends the user created key id to key escrow
        response = requests.post(url1, json=creation_key_id)
        #checks to see if the key id was recieved based on the response or if your ip is authorized
        data = response.json()
        if data == '1':
                print("key id already exists")
        elif data =='2':
                print("key id received")
        elif data == '3':
                print("not authorized")



def view_keys():
        #asks the user to enter a key id    
        key_id1 = input("key id: \n")
        #requests the key that matches the key id from the key escrow
        response = requests.post(url2, json=key_id1)
        #checks to see if key was found based on the response or if your ip is authorized
        data = response.json()
        if data == "1":
                print("key not found")
        elif data == '3':
                print("not authorized")
        else:
              #prints the key that was received  
              print("key found: ", data)

#takes key_id and requests a key from key escrow and returns the result
def get_key(key_id):    
        response = requests.post(url2, json=key_id)
        data = response.json()
        return data

def encrypt_file():
        #asks the user to input the key id for the key they want to use to encrypt    
        key_id = input("enter the key id for the key you want to use to encrypt:\n")
        #sends that key id to the get_key function and puts the response in key
        key = get_key(key_id)
        #checks the response(if response == 1 then key not found) or if your ip is authorized
        if key == "1":
                print("key not found")
        elif key == '3':
                print("not authorized")
        else:
                #after the key is found asks the user to input the file path for the for the file they want to encrypt    
                file_path = input("enter the file path for the file you want to encrypt")
                #trys to accsess that file however if an error happens it prints file not found
                try:
                        #opens the file and puts its content in file_content variable    
                        with open(file_path, 'r') as file:
                                file_content = file.read()
                        print("file content is: ")
                        print(file_content)
                        #uses fernet to encrypt the infrmation on the file using thekey previously retreaved
                        msg = file_content.encode()
                        fernet_key = Fernet(key)
                        cipher_text = fernet_key.encrypt(msg)
                        cipher_text_str = cipher_text.decode('utf-8')
                        print("cipher text is:")
                        print(cipher_text_str)
                        #asks user to input the file path fo where they want to put the encrypted information
                        encrypt_file_path = input("enter the file path for the file you")
                        #places that encrypted information in that file
                        with open(encrypt_file_path, 'w') as file1:
                                file1.write(cipher_text_str)
                except FileNotFoundError:
                        print("file not found")

def decrypt_file():
        #asks user what key was used to encrypt this information that you want to decrypt    
        key_id = input("enter the key that was used to decrypt this file:\n")
        #sends that key id to the get_key function and puts the response in key
        key = get_key(key_id)
        #checks the response(if response == 1 then key not found) or if your ip is authorized
        if key == "1":
                print("key not found")
        elif key == '3':
                print("not authorized")
        else:
                #after the key is found it asks the user to input the file path for the for the file they want to decrypt     
                file_path = input("enter the file path for the file you want to decrypt")
                 #trys to accsess that file however if an error happens it prints file not found
                try:
                        #opens the file and puts its content in file_content variable    
                        with open(file_path, 'rb') as file:
                                file_content = file.read()
                        print("file content is: ")
                        print(file_content)
                        #uses fernet to decrypt the information on the file using the key previously retreaved
                        fernet_key = Fernet(key)
                        decrypted_info = fernet_key.decrypt(file_content)
                        #prints the decrypted info
                        print("decrypted info:")
                        print(decrypted_info)
                except FileNotFoundError:
                        print("file not found")

#starts user input at '99' just to initialize the variable
user_input = '99'

#While loop for menu
while user_input != '5':
        #asks user toinput a vlue for the menu    
        user_input = input("please enter\n1 to generate key\n2 view keys\n3 to encrypt ")

        #if user inputs 1 it runs the generate_key() function
        if user_input == '1':
                generate_key()

        #if user inputs 2 it runs the view_keys() function
        elif user_input == '2':
                view_keys()
                
        #if user inputs 3 it runs the encrypt_file() function
        elif user_input == '3':
                encrypt_file()
                
        #if user inputs 4 it runs the decrypt_file() function
        elif user_input == '4':
                decrypt_file()
                
        #if user inputs 5 it ends the program
        elif user_input == '5':
                print("program end")
                break











