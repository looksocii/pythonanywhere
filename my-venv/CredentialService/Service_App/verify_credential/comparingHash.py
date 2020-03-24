from Service_App.verify_credential.merkletools import MerkleTools
import os

class TargetHash():
    def __init__(self):
        self.targetHash = None

    def getTargetHash(self, nodeName, manifestData):
        name = manifestData['name']
        value = manifestData['value']
        lnode = manifestData['left']
        rnode = manifestData['right']
        if name == nodeName:
            self.targetHash = value
            return self.targetHash
        if lnode is not None and rnode is not None:
            self.getTargetHash(nodeName, lnode)
            self.getTargetHash(nodeName, rnode)
        return self.targetHash

def getCredential(credential_name, credential_path):
    with open('Service_App/verify_credential/data/issuer.json', 'rb') as file_obj:
        issuer = file_obj.read()

    credential_list = os.listdir(credential_path)
    for credential in credential_list:
        if credential == credential_name:
            #get credential
            with open(credential_path + '/' + credential, 'rb') as file_obj:
                data = file_obj.read()
            credential_data = str(issuer) + str(data)

    return credential_data

def comparingHash(name, verifyList, credential_path, manifestData):
    mt = MerkleTools()
    result = False
    targetHash = TargetHash().getTargetHash(name, manifestData)

    if name in verifyList:
        credential = getCredential(name, credential_path)
        credentialHash = '0x00' + mt.getHash_hex(credential.encode('utf-8'))
        if credentialHash == targetHash:
            result = True
    return result




