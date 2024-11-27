import hashlib
import json
from time import time
from flask import Flask, jsonify, request
from uuid import uuid4

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        
        # Create the genesis block
        self.new_block(proof=1, previous_hash='0')

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1] if self.chain else '0'),
        }
        # Reset the current list of transactions
        self.current_transactions = []
        self.chain.append(block)  # Add the new block to the blockchain
        return block  # Return the newly created block

    def new_transaction(self, sender, recipient, amount):
        # Add a new transaction to the list of transactions
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] + 1  # Return the index of the block that will hold this transaction

    @property
    def last_block(self):
        # Return the last block in the chain
        return self.chain[-1]

    @staticmethod
    def hash(block):
        # Creates a SHA-256 hash of a Block
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
        
    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod 
    def valid_proof(last_proof, proof):
        # Validates the Proof by checking if hash(last_proof, proof) has 4 leading zeroes
        guess = f"{last_proof}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    # Get the last proof and find a new proof
    last_proof = blockchain.last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # Reward the miner by adding a transaction
    blockchain.new_transaction(
        sender="0",  # This signifies that this node has mined a new block
        recipient=node_identifier,
        amount=1,
    )
    # Create a new block by adding it to the chain
    previous_hash = blockchain.hash(blockchain.last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Mined",
        'index': block['index'],
        'transactions': block["transactions"],
        'proof': block['proof'],
        'previous_hash': block["previous_hash"]
    }
    return jsonify(response), 200

@app.route("/transactions/new", methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return "Missing values", 400

    # Create a new transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    response = {"message": f"Transaction will be added to Block {index}"}
    return jsonify(response),201   #it represents created

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        "chain": blockchain.chain,
        "length": len(blockchain.chain),
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)