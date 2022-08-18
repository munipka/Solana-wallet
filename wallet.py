import json

from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.rpc.api import Client
from solana.system_program import TransferParams, transfer
from solana.transaction import Transaction

import config
from database import save_wallet_keys, save_address, load_wallet_keys

solana_client = Client(config.SOLANA_CLIENT)


async def create_wallet(user_id):
    """creates a wallet in blockchain"""
    try:
        kp = Keypair.generate()
        public_key = str(kp.public_key)
        secret_key = kp.secret_key.decode('latin-1')

        data = {
            "public_key": public_key,
            "secret_key": secret_key,
        }
        await save_address(user_id, public_key)
        await save_wallet_keys(user_id, data)

        return public_key
    except Exception as e:
        print(e)


async def load_wallet(user_id):
    """loads wallet by using a keypair"""
    try:
        data = await load_wallet_keys(user_id)
        account = json.loads(data[0])
        account['secret_key'] = account['secret_key'].encode("latin-1")
        return account

    except Exception as e:
        print(e)
        return None


async def fund_account(user_id, amount):
    """SOL test faucet"""
    try:
        amount = int(1000000000 * amount)
        account = await load_wallet(user_id)
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


async def get_balance(user_id):
    """load balance from blockchain"""
    try:
        account = await load_wallet(user_id)
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


async def send_sol(user_id, amount, receiver):
    """sends funds to someone"""
    try:
        account = await load_wallet(user_id)
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
