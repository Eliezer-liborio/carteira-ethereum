from eth_account import Account
import bcrypt
from cryptography.fernet import Fernet
import os

# Gera a chave Fernet para criptografia
chave_fernet = Fernet.generate_key()
fernet = Fernet(chave_fernet)

def gerar_carteira():
    # Gerar conta Ethereum
    account = Account.create()
    endereco = account.address
    private_key = account._private_key.hex()
    mnemonic = ""  # Pode adicionar geração de mnemonic se quiser depois
    return endereco, private_key, mnemonic

def hash_frase(frase):
    return bcrypt.hashpw(frase.encode(), bcrypt.gensalt())

def criptografar_private_key(private_key):
    return fernet.encrypt(private_key.encode())

def salvar_em_arquivo(dados):
    # Cria ou atualiza o arquivo .cap
    caminho = 'carteiras.cap'
    with open(caminho, 'a') as f:
        f.write(dados + '\n')
