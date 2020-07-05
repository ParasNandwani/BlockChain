#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 17:46:49 2020

@author: parasn

Module1 Create BlockChain
"""

import datetime
import hashlib #to hash the blocks
import json
from flask import Flask ,jsonify
#jsonify to return response in postman



#Part 1-Building a BlockChain

class Blockchain:
    
    def __init__(self):#self will refer to object of current class to specify
        self.chain = []
        self.create_block(proof=1, previous_hash='0')
        
    def create_block(self,proof,previous_hash):        
          block={'index':len(self.chain)+1,
                 'timestamp':str(datetime.datetime.now()),
                 'proof':proof,
                 'previous_hash':previous_hash}
          
          self.chain.append(block)
          return block
      
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self,previous_proof):
        new_proof=1
        check_proof=False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2-previous_proof**2).encode()).hexdigest()
            if hash_operation[:4]=='0000':
                check_proof=True
            else:
                new_proof+=1
        return new_proof
    
    """
    Hashing block
    first we use json library dump to string and then encode
    """
    
    def hash(self,block):
        encoded_block=json.dumps(block,sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest();
    
    """
    Mining block or check block is  valid
    
    """
    
    def is_chain_valid(self,chain):
        previous_block=chain[0]
        block_index=1
        while block_index < len(chain):
            block=chain[block_index]
            #firts check to chek previous hash and block hash
            if  block['previous_hash'] != self.hash(previous_block):
                return False;
            #second check is to check proof of each block is valid
            previous_proof=previous_block['proof']
            proof=block['proof']
            hash_operation = hashlib.sha256(str(proof**2-previous_proof**2).encode()).hexdigest()
            if hash_operation[:4]!='0000':
                return False;
            previous_block=block
            block_index += 1
        return True            
            
    
    #two essntial thhing
    #1.each b lock has correct proof of work 
    #2.Check wether previous block has correct hash
           
#Part 2-Mining our bloackchain

#create  a web-app
app = Flask(__name__)

#Creating a blockchaion
blockchain = Blockchain()

# Mining a block
@app.route("/mine_block",methods=['GET'])
def mine_block():
    previous_block=blockchain.get_previous_block()
    previous_proof=previous_block['proof']
    proof=blockchain.proof_of_work(previous_proof)
    previious_hash=blockchain.hash(previous_block)
    block=blockchain.create_block(proof,previious_hash)
    response={'message':'just mined a block',
              'index':block['index']}
    return jsonify(response),200


@app.route("/gat_chain",methods=['GET'])
def get_chain():
    response={'chain':blockchain.chain,'size':len(blockchain.chain)}
    return jsonify(response),200


app.run(host='0.0.0.0',port=5000)
    


    

