import blockcypher
from .constants import COIN_SYMBOL_MAPPINGS

BTC_FEE = 60700  # BTC fee to pay per transaction
API_TOKEN = '288de80ef3eb4341be46da7ad3ea30a7'
COIN_SYMBOL = 'btc-testnet'

#get unspent-output
def select_inputs(address, total_amount):
    unspent_inputs_dic = blockcypher.get_address_details(address, coin_symbol=COIN_SYMBOL, txn_limit=None, api_key=API_TOKEN, before_bh=None, after_bh=None, unspent_only=True, show_confidence=False, confirmations=0, include_script=False)
    unspent_inputs = unspent_inputs_dic['txrefs']

    if not isinstance(unspent_inputs, list):
        return {'error': 'Could not retrieve list of unspent inputs'}

    unspent_inputs.sort(key=lambda unspent_input: unspent_input['value'] * unspent_input['confirmations'],
                        reverse=True)

    input_amount = 0

    for unspent_input in unspent_inputs:
        input_amount += unspent_input['value']
        if input_amount >= total_amount:
            break  # stop when we have enough

    if input_amount < total_amount:
        return {'error': 'Not enough funds are available to cover the amount and fee'}

    # Return the successful result

    return {
        'inputs': unspent_inputs,
        'total': input_amount
    }

#create raw txn
def issue_credential(privkey, from_address, metadata):

    balance = blockcypher.get_confirmed_balance(address=from_address, coin_symbol=COIN_SYMBOL, api_key=API_TOKEN)
    send_amount = balance - BTC_FEE
    print('send_amount: ', send_amount)
    print('balance: ', balance)

    tx_id= blockcypher.issue(from_privkey=privkey, to_address=from_address, to_satoshis=send_amount, metadata=metadata, change_address=None,
        privkey_is_compressed=True, min_confirmations=0, api_key=API_TOKEN, coin_symbol=COIN_SYMBOL)

    return tx_id


def get_blockchain_network():

    return 'Bitcion/' + COIN_SYMBOL_MAPPINGS[COIN_SYMBOL]['blockcypher_network']





