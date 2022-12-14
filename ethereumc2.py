import os
import base64
from Crypto.Cipher import AES
from web3 import Web3, HTTPProvider

#encrpyt


def encrypt(message, key):
    # generate a random IV
    iv = os.urandom(16)

    # create a new AES cipher
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # pad the message to be a multiple of 16 bytes
    padded_message = message + b' ' * (16 - len(message) % 16)

    # encrypt the padded message
    encrypted_message = cipher.encrypt(padded_message)

    # return the IV and the encrypted message
    return base64.b64encode(iv + encrypted_message)

# read the message to encrypt from the user
message = input("Enter a message to encrypt: ")

# encrypt the message with the key "password"
encrypted_message = encrypt(message.encode('utf-8'), b"passwordpasswordpasswordpassword")

# print the encrypted message
print("Encrypted message:", encrypted_message) 

w3 = Web3(HTTPProvider('http://127.0.0.1:8545'))

print(w3.isConnected())

#put encrypted message into hex from
hexstring = (encrypted_message.hex())


signed_txn = w3.eth.account.sign_transaction(dict(
    nonce=w3.eth.get_transaction_count("<from public key>"),
    maxFeePerGas=3000000000,
    maxPriorityFeePerGas=2000000000,
    gas=1000000,
    to='<to public key>',
    value=500000,
    data=(hexstring),
    type=2,
    chainId=1337,
  ),
  "<private key>",
)
txHash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
print(w3.toHex(txHash))

# Connect to local Ethereum node
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

#pull latest block 
block = w3.eth.getBlock('latest')
#print(block)

#parse transactions out of block
transactions = block['transactions']

#filter transactions to only those sent to the contract address public key of account to monitor>
contract_transactions = []
for tx in transactions:
    tx_data = w3.eth.getTransaction(tx)
    if tx_data['to'] == '<account to monitor public key>':
        contract_transactions.append(tx_data)

        #print output
encryptedpayload = (bytes.fromhex(tx_data['input'][2:]).decode('utf-8'))


#decrypt


def decrypt(encrypted_message, key):
    # decode the IV and encrypted message from the base64 encoded string
    iv_and_encrypted_message = base64.b64decode(encrypted_message)

    # extract the IV and encrypted message
    iv = iv_and_encrypted_message[:16]
    encrypted_message = iv_and_encrypted_message[16:]

    # create a new AES cipher
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # decrypt the message
    decrypted_message = cipher.decrypt(encrypted_message)

    # return the decrypted message
    return decrypted_message

# read the encrypted message to decrypt from the user
encrypted_message = encryptedpayload

# decrypt the message with the key "password" has to be 32 bytes long
decrypted_message = decrypt(encrypted_message, b"passwordpasswordpasswordpassword")

# print the decrypted message
print("Decrypted message:", decrypted_message.decode('utf-8'))