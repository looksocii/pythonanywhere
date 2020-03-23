from Service_App.verify_credential.merkletools import MerkleTools

mt = MerkleTools()

def h2b(data):
    if data:
        return bytearray.fromhex(data)

class checkingMerkleProof():
    def __init__(self, item):
        self.item = item
        self.hash = None
        self.verifyList = list()

    def getRoot(self, data, nodeName):
        if data['name'] == nodeName:
            self.hash = data['value']
            return self.hash

        lnode = data['left']
        rnode = data['right']
        if lnode != None and rnode != None:
            if lnode['name'] == nodeName or rnode['name'] == nodeName:
                left = lnode['value']
                right = rnode['value']
                self.hash = '0x01' + mt.getHash_hex(left.encode('utf-8') + right.encode('utf-8'))
                self.hash = self.getProofHash(self.item, self.hash)
                return self.hash

            self.getRoot(lnode, nodeName)
            self.getRoot(rnode, nodeName)
        return self.hash

    def getProofHash(self, data, hash):
        lnode = data['left']
        rnode = data['right']

        if lnode != None and rnode != None:
            left = lnode['value']
            right = rnode['value']
            if left == hash or right == hash:
                self.hash = '0x01' + mt.getHash_hex(left.encode('utf-8') + right.encode('utf-8'))
                if data['name'] == "Root":
                    return self.hash
                self.getProofHash(self.item, self.hash)

            self.getProofHash(lnode, hash)
            self.getProofHash(rnode, hash)
        return self.hash

    def getVerifyList(self, data):
        name = data['name']
        if name is not None:
            if name != "Root":
                self.verifyList.append(name)
        lnode = data['left']
        rnode = data['right']
        if lnode is not None and rnode is not None:
            if lnode['name'] is not None:
                self.verifyList.append(lnode['name'])
            if rnode['name'] is not None:
                self.verifyList.append(rnode['name'])

            if lnode['left'] is not None and lnode['right'] is not None:
                self.getVerifyList(lnode)
            if rnode['left'] is not None and rnode['right'] is not None:
                self.getVerifyList(rnode)
        return self.verifyList