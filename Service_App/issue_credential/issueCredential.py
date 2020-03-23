from Service_App.issue_credential.issueCredentialTool import *
import json, os

def issue():
    with open('Service_App/issue_credential/issue_conf.json') as file_obj:
        conf = json.load(file_obj)
    #to_address and from_address are same
    to_address = conf['to_address']
    private_key = conf['private_key']

    rootList = list()
    # get manifest file
    file_dir = 'Service_App/issue_credential/data'
    student_list = os.listdir(file_dir)
    for dirs in student_list:
        with open(file_dir + '/' + dirs + '/manifest.json') as file_obj:
            data = json.load(file_obj)
        root = data['manifest']['value']
        rootList.append(root)

    rootSet = set(rootList)

    if len(rootSet) == 1:
        tx_id = issue_credential(private_key, to_address, list(rootSet)[0])  # list(rootSet)[0] = root

        chain = get_blockchain_network()

        # add txid to manifest.json
        for dirs in student_list:
            # get signature
            with open(file_dir + '/' + dirs + '/manifest.json') as file_obj:
                data = json.load(file_obj)
            data['signature']['txId'] = tx_id
            data['signature']['chain'] = chain

            # write back to manifest.json
            filename = file_dir + '/' + dirs + '/manifest.json'
            with open(filename, 'w') as file_obj:
                json.dump(data, file_obj, indent=2)
    return tx_id, chain

