#Class: CIS-221
#Group: 2
#Project: Key escrow system
#Group members: Anoop, Pranav, Lisa, Evan, Teny

#Imports library Flask, request, and jsonify
from flask import Flask, request, jsonify

#flask syntax
app = Flask(__name__)

#pyhton dictionary that stores keys and key id's in key: value pairs
keys = {}

#a temp variable that stores the key while the user is makeing a key id
key = "null"

#holds ip and only IP's on this list can ascess this key escrow
IP_whitelist = ['10.0.0.172', '10.0.0.210']


#activates when the 'get_key' url is used in a client
@app.route('/get_key', methods=['POST'])
def get_key():
        #checks request ip against ip whitelist    
        if request.remote_addr not in IP_whitelist:
                return jsonify("3"), 403
        else:
       #gets the key_id from the client
                key_id = request.get_json()
                #checks if the key id matches a key in the keys, if it does it returns the key if not it returns 1
                if key_id in keys:
                        return jsonify(keys[key_id]), 200
                else:
                        return jsonify('1'), 500


#activates when the 'store_key' url is used in a client
@app.route('/store_key', methods=['POST'])
def store_key():
        #checks request ip against ip whitelist
        if request.remote_addr not in IP_whitelist:
                return jsonify("3"), 403
        else:
       #gets the key_id from the client  
                key_id = request.get_json()
                #checks if the key id matches a key in the keys, if it does return 1 otherwise store the key id with the key already gotten from the 'store_key_value function in the python dictionary
                if key_id in keys:
                        return jsonify("1"), 500
                else:
                      keys[key_id] = key
                      return jsonify("2"), 200

#activates when the 'store_key_value' url is used in a client
@app.route('/store_key_value', methods=['POST'])
def store_key_value():
        #checks request ip against ip whitelist    
        if request.remote_addr not in IP_whitelist:
                return jsonify("3"), 403
        else:
       #gets the key from the client    
                key_value = request.get_json()
                #stores the key in the global value
                global key
                #checks to see if it was stored succsessfully, if yes then return 2 but if no then return 1
                key = key_value
                if key == key_value:
                        return jsonify('2')
                else:
                      return jsonify('1')


#flask syntax to start the sever will be running on port 5000
if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000)
