# utils.py
from bip_utils import Bip39MnemonicGenerator, Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
from eth_account import Account
import uuid
import os

def generate_wallet():
    mnemonic = Bip39MnemonicGenerator().FromWordsNumber(12)
    seed = Bip39SeedGenerator(mnemonic).Generate()
    bip44_wallet = Bip44.FromSeed(seed, Bip44Coins.ETHEREUM).Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
    private_key = bip44_wallet.PrivateKey().Raw().ToHex()
    address = Account.from_key(private_key).address
    return {
        "mnemonic": str(mnemonic),
        "private_key": private_key,
        "address": address
    }

def generate_token():
    return str(uuid.uuid4())
