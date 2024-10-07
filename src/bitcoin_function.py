from src.bitcoin_rpc import bitcoin_rpc
from src.fake_pubkey import create_fake_pubkeys
from pybtc import *

def get_listunspent():
    txids = []
    listunspent = bitcoin_rpc("listunspent", [])
    if len(listunspent) != 0:

        # for i in listunspent:
        #     txids.append(i)
        # return txids
        return listunspent[1]
    else:
        print("ERROR: There is no UTXO. Check the wallet!")
        return

# test = get_listunspent()
# print(get_listunspent())

def get_pubKey(address):
    return bitcoin_rpc("getaddressinfo", [address])['pubkey']

# Example of get_pubkey
# print(get_pubKey("tb1ql9uuh0kmpzzzan4vhefrl0d6wyjydmsy98nutk"))

def get_privkey(address):
    return bitcoin_rpc("dumpprivkey", [address])

# Example of get_pubkey
# print(get_privkey(test['address']))

def create_fake_scriptPubKey(pubkey1, pubkey2, pubkey3):
    scriptPubKey = b"".join([
        OP_1,
        op_push_data(pubkey1),
        op_push_data(pubkey2),
        op_push_data(pubkey3),
        OP_3, OP_CHECKMULTISIG
    ])
    return scriptPubKey

# def create_raw_transaction(inTxid, vout, address, amount, ipfs, phrase, testnet=True):
def create_raw_transaction(ipfs, phrase, testnet=True):
    utxo = get_listunspent()
    inTxid = utxo['txid']
    vout = utxo['vout']
    address = utxo['address']
    amount = 10

    tx = Transaction(testnet=testnet)
    tx.add_input(inTxid, vout)
    pubkey = get_pubKey(address)
    # sample
    # scriptPubKey = create_fake_scriptPubKey("024548c428862b741a4fe93cd185bf930b41fcae0642ec0bec65019c8806f24c50", "03843247193be8dd3bca9ca997dd5ad544f404833ca043659704cfb78ac8e10f8d", pubkey)
    fake_pubkeys = create_fake_pubkeys(ipfs, phrase)

    while len(fake_pubkeys) != 0 :
        scriptPubKey = create_fake_scriptPubKey(fake_pubkeys[0],fake_pubkeys[1], pubkey)
        del fake_pubkeys[0]
        del fake_pubkeys[0]
        tx.add_output(amount, script_pub_key=scriptPubKey)
    # tx.sign_input(1, private_key=get_privkey(address), address=address, sighash_type=None,amount=amount)

    return tx.serialize(), address

# Example of create_raw_transaction
# hex, address = create_raw_transaction("QmbWqxBEKC3P8tqsKc98xmWNzrzDtRLMiMPL8wBuTGsMnR", "hello world", "" )
def sign_raw_transaction_with_privkey(serialized_tx, address):
    try:
        signed_hex = bitcoin_rpc("signrawtransactionwithkey", [serialized_tx, [get_privkey(address)]])
        print(signed_hex)
        if signed_hex["complete"] == True:
            return signed_hex["hex"]
    except:
        print("signed_hex was wrong")
    return None

# Example of sign_raw_transaction_with_privkey
# sig = sign_raw_transaction_with_privkey(hex, address)

def send_rawtransaction(signature):
    transactionID = bitcoin_rpc("sendrawtransaction", [signature])
    return transactionID
#
# send_rawtransaction(sig)
#
# "Waiting for it to appear in the mempool..."
