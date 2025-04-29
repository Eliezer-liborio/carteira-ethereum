# sdk.py
from web3 import Web3
from eth_account.messages import encode_defunct
from eth_account import Account
import os

alchemy_url = "SEU_ENDERECO_ALCHEMY_url"
w3 = Web3(Web3.HTTPProvider(alchemy_url))

def get_nonce(address):
    return w3.eth.get_transaction_count(address)

def verify_signature(address, signature, message):
    msg = encode_defunct(text=message)
    recovered = Account.recover_message(msg, signature=signature)
    return recovered.lower() == address.lower()
