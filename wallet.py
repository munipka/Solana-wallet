from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.rpc.api import Client
from solana.transaction import Transaction
from solana.system_program import TransferParams, transfer

from database import save_address

import json

import config

solana_client = Client(config.SOLANA_CLIENT)


def create_wallet(user_id):
    try:
        kp = Keypair.generate()
        public_key = str(kp.public_key)
        secret_key = kp.secret_key.decode('latin-1')

        data = {
            'public_key': public_key,
            'secret_key': secret_key,
        }
        
        save_address(user_id, public_key)
        file_name = f'users/{user_id}.txt'
        with open(file_name, 'w') as f:
            json.dump(data, f)

        return public_key
    except Exception as e:
        print(e)


def load_wallet(user_id):
    try:
        file_name = f'users/{user_id}.txt'
        with open(file_name) as json_file:
            account = json.load(json_file)
            account['secret_key'] = account['secret_key'].encode("latin-1")
            return account

    except Exception as e:
        print(e)
        return None


def fund_account(user_id, amount):
    try:
        amount = int(1000000000 * amount)
        account = load_wallet(user_id)
        resp = solana_client.request_airdrop(
            account['public_key'], amount)

        transaction_id = resp['result']
        if transaction_id is not None:
            return transaction_id
        else:
            return None

    except Exception as e:
        print('error:', e)
        return None


def get_balance(user_id):
    try:
        account = load_wallet(user_id)
        resp = solana_client.get_balance(account['public_key'])
        balance = resp['result']['value'] / 1000000000
        data = {
            "publicKey": account['public_key'],
            "balance": str(balance),
        }
        return data
    except Exception as e:
        print('error:', e)
        return None


def send_sol(user_id, amount, receiver):
    try:
        account = load_wallet(user_id)
        sender = Keypair.from_secret_key(account['secret_key'])
        amount = int(1000000000 * amount)
        txn = Transaction().add(transfer(TransferParams(
            from_pubkey=sender.public_key, to_pubkey=PublicKey(receiver), lamports=amount)))
        resp = solana_client.send_transaction(txn, sender)

        transaction_id = resp['result']
        if transaction_id is not None:
            return transaction_id
        else:
            return None

    except Exception as e:
        print('error:', e)
        return None
