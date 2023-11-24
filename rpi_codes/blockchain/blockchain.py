from ast import Dict
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import binascii
from datetime import datetime
import collections
import hashlib
from Crypto.Hash import SHA256
# from blockchainUtill import *
import base64,json
from flask import Flask, jsonify, request #sudo apt-get install python3-flask

def sha256(message):
    return hashlib.sha256(message.encode('ascii')).hexdigest()


class IoTnode:
    def __init__(self):
        r_value=Random.new().read
        key= RSA.generate(2048,r_value)
        self.publicKey=key.public_key().export_key()
        self.private_key=key.export_key()
        self.hostName=""


class IoTNodeTransaction:
    def __init__(self, source, destination, data):
        self.data = data
        self.source = source
        self.destination = destination
        self.timestamp = datetime.now()


    def encrypt_transaction(self):
        encrypted_transaction=""
        private_key=iot_node.private_key
        file_out = open("private.pem", "wb")
        file_out.write(private_key)
        file_out.close()
        public_key=iot_node.publicKey
        file_out = open("public.pem", "wb")
        file_out.write(public_key)
        file_out.close()
        public_key = RSA.import_key(open("public.pem").read())
        session_key = get_random_bytes(16)
        cipher_rsa = PKCS1_OAEP.new(public_key) # Encrypt the Session Key with the public RSA key.
        enc_session_key = cipher_rsa.encrypt(session_key)
        cipher_aes = AES.new(session_key, AES.MODE_EAX)
        encoded_dict = str(self.compose_transaction()).encode('utf-8')
        cipherdata = cipher_aes.encrypt(encoded_dict)
        msg_to_sent = {"data": cipherdata,
                       "enc_session_key":enc_session_key,
                       "nonce":cipher_aes.nonce}
        encrypted_transaction=base64.b64encode(str(msg_to_sent).encode('utf-8'))
        return encrypted_transaction
    
    def decrypt_transaction(self,data):
        x=base64.b64decode(data)
        x=x.decode('utf-8')
        x=eval(x)
        data=x.get("data")
        enc_session_key=x.get("enc_session_key")
        nonce=x.get("nonce")
        private_key=RSA.import_key(open("private.pem").read())
        cipher_rsa= PKCS1_OAEP.new(private_key)
        session_key=cipher_rsa.decrypt(enc_session_key)
        cipher_aes=AES.new(session_key, AES.MODE_EAX, nonce)
        data=cipher_aes.decrypt(data)
        return data



    def compose_transaction(self):
        transaction_dic=""
        transaction_dic=collections.OrderedDict({
            "source":self.source,
            "destination":self.destination,
            "data":self.data,
            "timeStamp":self.timestamp
        })
        return transaction_dic


class BlockChain:
    def __init__(self):
        self.v_transactions = []
        self.previous_block_hash=""
        self.Nonce=""
    
    def create_block(self):
        global last_transaction_index,last_block_hash
        temp_transaction=iot_transactions[last_transaction_index]
        self.v_transactions.append(temp_transaction)
        last_transaction_index += 1
        self.previous_block_hash=last_block_hash
        self.Nonce=self.mine(self, 2)
        digest = hash(self)
        blocks.append(self)
        last_block_hash=digest
    
    def mine(self,block,mine_difficulty=1):
        assert mine_difficulty >=1
        prefix = '1' * mine_difficulty
        for c in range(1000):
            digest = sha256(str(hash(block)) + str(c))
            if digest.startswith(prefix):
                print("after " + str(c) + " iterations found nonce:  " + digest)
        return digest
    
    def fetch_blocks(self):
        out=[]
        print("Number of blocks in the chain:  ", len(blocks))
        for i in range (len(blocks)):
            block_temp = blocks[i]
            print ("block # ", i)
            res = {"block # ": i}
        
            for t in block_temp.v_transactions:
                count=0;
                count+=1
                print("Transaction no   ",count)
                res["transaction_no"]=count
                print("IoT source node        : ", iot_node.hostName)
                res["iot_source_node"]=iot_node.hostName





            out.append(res)
        jsonData=json.dumps(out)
        return jsonData
        


#region Flask
app = Flask(__name__)

iot_transactions=[]
blocks=[]
last_transaction_index = 0
last_block_hash=""

iot_node=IoTnode()
block= BlockChain()

@app.route('/send', methods=['GET'])
def send_encrypt_transaction():
    iot_node.hostName="aj9394@shu.ac.uk"
    humidity=14.0
    t=IoTNodeTransaction(source=iot_node.hostName, destination="IoTServer", data=humidity)
    encrypted_data=t.encrypt_transaction()
    iot_transactions.append(t)
    block.create_block()
    return jsonify(encrypted_data), 200

@app.route('/list_blocks', methods=['GET'])
def list_blocks():
    response=block.fetch_blocks()
    return response, 200


@app.route('/test',methods=['GET'])
def hello_world():
    msg="Blockchain.py is running on the Flask Framework"
    return jsonify(msg), 200

app.run(host='127.0.0.1', port=5009)
#endregion