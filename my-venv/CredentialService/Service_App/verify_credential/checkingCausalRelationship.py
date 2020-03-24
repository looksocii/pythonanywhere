import os

class ChildNode():
    def __init__(self, manifestData):
        self.hash = None
        self.root = manifestData['value']
        self.manifest_data = manifestData

    def getRoot(self, name, evidence, manifestData):
        lnode = manifestData['left']
        rnode = manifestData['right']
        if lnode is not None and rnode is not None:
            if lnode['name'] == name or rnode['name'] == name:
                self.hash = manifestData['value']
                if self.hash == evidence:
                    return self.hash
                self.hash = self.getRootbyValue(self.hash, evidence, self.manifest_data)
                return self.hash
            self.getRoot(name, evidence, lnode)
            self.getRoot(name, evidence, rnode)
            return self.hash

    def getRootbyValue(self, value, evidence, manifestData):
        lnode = manifestData['left']
        rnode = manifestData['right']
        if lnode is not None and rnode is not None:
            if lnode['value'] == value or rnode['value'] == value:
                self.hash = manifestData['value']
                if self.hash == evidence:
                    return self.hash
                self.getRootbyValue(self.hash, evidence, self.manifest_data)
            self.getRootbyValue(value, evidence, lnode)
            self.getRootbyValue(value, evidence, rnode)
            return self.hash

class Evidence():
    def __init__(self):
        self.evidence = None

    def getEvidence(self, name, manifestData):
        lnode = manifestData['left']
        rnode = manifestData['right']
        if lnode is not None and rnode is not None:
            if lnode['name'] == name:
                self.evidence = rnode['value']
                if self.evidence[:4] == '0x01' and rnode['left'] is not None and rnode['right'] is not None:
                    return self.evidence
            if rnode['name'] == name:
                self.evidence = lnode['value']
                if self.evidence[:4] == '0x01' and lnode['left'] is not None and lnode['left'] is not None:
                    return self.evidence
            self.getEvidence(name, lnode)
            self.getEvidence(name, rnode)
        return self.evidence
    
def getChildList(parentName, evidenceValue, ChildNode, verifyList, manifestData):
    childList = list()
    for childName in verifyList:
        childRoot = ChildNode.getRoot(childName, evidenceValue, manifestData)
        if childRoot == evidenceValue:
            childList.append(childName)
    return childList

def checking_causal_relationship(verifyList, credential_path, manifestData):
    relationship_list = list()

    credential_list = os.listdir(credential_path)
    for name in verifyList:
        credential_list.append(name)

    credential_set = set(credential_list)
    if len(credential_set) == len(verifyList):
        child = ChildNode(manifestData)
        evidence = Evidence()
        leafNodes = list()

        for parentName in verifyList:
            # get the evidence of the parentNode
            evidenceValue = evidence.getEvidence(parentName, manifestData)
            if evidenceValue is not None:
                childs = getChildList(parentName, evidenceValue, child, verifyList, manifestData)
                if len(childs) > 0:
                    relationship_list.append(str(childs) + ' is part of the \'' + parentName + '\'')
                else:
                    leafNodes.append(parentName)

        if len(leafNodes) > 1:
            relationship_list.append(str(leafNodes) + " are leaf node")
        else:
            relationship_list.append(str(leafNodes) + " is leaf node")
            
    return relationship_list
    
