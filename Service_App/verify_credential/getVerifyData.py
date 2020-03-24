import json, subprocess, sys
import blockcypher

API_TOKEN = '288de80ef3eb4341be46da7ad3ea30a7'
COIN_SYMBOL = 'btc-testnet'

def get_issuerAddress(txid):
    tx = blockcypher.get_transaction_details(txid, coin_symbol=COIN_SYMBOL, limit=None, tx_input_offset=None, tx_output_offset=None,
        include_hex=False, show_confidence=False, confidence_only=False, api_key=API_TOKEN)

    address = tx['addresses'][0]
    return address

def get_merkleRoot(txid):
    tx = blockcypher.get_transaction_details(txid, coin_symbol=COIN_SYMBOL, limit=None, tx_input_offset=None, tx_output_offset=None,
        include_hex=False, show_confidence=False, confidence_only=False, api_key=API_TOKEN)

    for output in tx['outputs']:
        if output['script_type'] == 'null-data':
            merkleRoot = output['data_hex']

    return merkleRoot



