import json, os
from Service_App.issue_credential.merkletree import MerkleTree
from Service_App.issue_credential.merkletools import MerkleTools, Node
from Service_App.issue_credential.createCredential import create_credential
from collections import OrderedDict
from Service_App.issue_credential.credentialAssociation import get_credentialAssociation

mTools = MerkleTools()
mTree = MerkleTree()

class Manifest():
    def __init__(self): #clr_data = dic (return from get_credential)
        self.dic = OrderedDict()  # { parent:[childs] }
        self.nodes = list()  

    def get_treeRoot(self, data): #data = tree\student_*.json
        child_list = list() #list of the child
        root_list = list()  #list of the root id (parentId)
        for value in data['credentialTree']:
            if len(value['child']) > 0:
                for v in value['child']:
                    child_list.append(v) #add all of the child to child_list

        for value in data['credentialTree']:
            if value['name'] in child_list:
                continue
            else:
                root_list.append(value['name'])
        return root_list

    #add child node (child's full data) to childList not only name
    def get_treeNode(self, data):#data = tree\student_*.json
        treeNodes = list()
        for credential in data['credentialTree']:
            if len(credential['child']) > 0:
                childList = list()  #add child node to childList not only name
                for child in credential['child']:
                    for childData in data['credentialTree']:
                        if child == childData['name']:
                            childList.append(childData)
                credential['child'] = childList
                treeNodes.append(credential)
            else:
                treeNodes.append(credential)
        return treeNodes

    #add child node (Cyclic traversal)
    def get_treeAddChild(self, treeNodes):
        for node in treeNodes:
            childNodes = node['child']
            if len(childNodes) == 0:
                continue
            for childNode in childNodes:
                for treeNode in treeNodes:
                    if childNode['name'] == treeNode['name']:
                        if len(treeNode['child']) == 0:
                            continue
                        childList = list()
                        for child in treeNode['child']:
                            childList.append(child)
                        childNode['child'] = childList
            #Cyclic traversal child node
            self.get_treeAddChild(childNodes)
        return treeNodes

    #get the root node of the tree
    def get_treeRootNodes(self, treeRoot, treeNodes):
        nodes = list()
        treeNodes = self.get_treeAddChild(treeNodes)
        for rootNode in treeRoot:
            for node in treeNodes:
                if rootNode == node['name']:
                    nodes.append(node)
        return nodes

    #self.dic[parentName] = childDic (childName : childValue)
    def get_nodesDic(self, treeRootNodes):
        for node in treeRootNodes:
            childNodes = node['child']
            if len(childNodes) > 0:
                childDic = OrderedDict()
                for child in childNodes:
                    childDic[child['name']] = child['targetHash']
                    self.dic[node['name']] = childDic
                self.get_nodesDic(childNodes)
        return self.dic

    #get evidence node
    def get_nodesEvidence(self, treeRootNodes):
        nodesDic = self.get_nodesDic(treeRootNodes)
        dicKeyList = list()
        nodesList = list()
        for key in nodesDic.keys():
            nodesList.append(key)  # key = name

        nodesList.reverse()

        for node in nodesList:
            childDic = nodesDic[node] #nodesDic[node] = childName : chlidValue
            childList = list()
            evidenceList = list()
            for key in childDic.keys():
                child = childDic[key]
                key_evidence = key + "_evidence"
                for key in self.dic.keys():
                    dicKeyList.append(key)
                if key_evidence in dicKeyList:
                    evidenceList.append(self.dic[key_evidence]) #evidence = leftChild,
                    evidenceList.append(child)#child = rightChild
                else:
                    childList.append(child) #leafNode

            #append childList to evidenceList
            for child in childList:
                evidenceList.append(child)

            if len(evidenceList) > 1:
                root = mTree.getMerkleTreeByHash(evidenceList)
            else:
                root = mTree.getMerkleTreeByHash([evidenceList[0], evidenceList[0]])

            evidence = root[-1].value
            # print("evidence :", evidence)
            self.dic[node + "_evidence"] = evidence
            for node in root:
                self.nodes.append(node)  # to build MerkleTree
        """
        for node in self.nodes:
            print("value :", node.value)
        """
        return self.dic, self.nodes

    #get full nodes
    def get_nodes(self, treeRootNodes):
        self.dic, self.nodes = self.get_nodesEvidence(treeRootNodes)
        dicKeyList = list()
        for key in self.dic.keys():
            dicKeyList.append(key)

        evidenceList = list()
        nodeList = list()
        for node in treeRootNodes:
            node_evidence = node['name'] + "_evidence"
            targetHash = node['targetHash']
            if node_evidence in dicKeyList:
                evidenceList.append(self.dic[node_evidence]) #leftChild
                evidenceList.append(targetHash)#rightChild
            else:
                nodeList.append(targetHash)#leafNode

        # append childList to evidenceList
        for node in nodeList:
            evidenceList.append(node)

        if len(evidenceList) > 1:
            root = mTree.getMerkleTreeByHash(evidenceList)
        else:
            root = mTree.getMerkleTreeByHash([evidenceList[0], evidenceList[0]])

        # evidence = root[-1].value
        for node in root:
            self.nodes.append(node)  # to build MerkleTree

        return self.nodes

    #using full nodes to build the MerkleTree
    def get_MerkleTree(self, treeRootNodes, data):#data = tree\student_*.json
        self.nodes = self.get_nodes(treeRootNodes)
        valueList = list()
        for value in data['credentialTree']:
            valueList.append(value['targetHash'])

        #add 'name' to manifest (merkleProof)
        for node in self.nodes:
            value = node.value
            if value in valueList:                
                for credential in data['credentialTree']:
                    if value == credential['targetHash']:                        
                        node.name = credential['name']
                        node.type = credential['type']

        root = self.nodes[-1]
        merkleTree = root.get_nodes(self.nodes)

        return merkleTree

    #create manifest
    def create(self):
        tree_path = 'Service_App/issue_credential/tree'
        association_path = 'Service_App/issue_credential/association'
        get_credentialAssociation(tree_path, association_path)

        student_list = os.listdir(tree_path)
        for file in student_list:
            with open(tree_path + '/' + file) as file_obj:
                data = json.load(file_obj)
            treeRoot = self.get_treeRoot(data)
            treeNodes = self.get_treeNode(data)
            treeRootNodes = self.get_treeRootNodes(treeRoot, treeNodes)
            merkleTree = self.get_MerkleTree(treeRootNodes, data)

            # write an individual credential and manifest to 'data' dir
            file_path = 'Service_App/issue_credential/data/' + str(file).split(".json")[0]
            filename = file_path + '/' + 'manifest.json'
            dic = OrderedDict()
            dic['manifest'] = merkleTree
            dic['signature'] = OrderedDict()
            dic['signature']['txId'] = ""
            dic['signature']['type'] = "BTCOpReturn"
            dic['signature']['chain'] = ""
            with open(filename, 'w') as file_obj:
                json.dump(dic, file_obj, indent=2)

            #reset self.dic and self.nodes
            self.dic = OrderedDict()
            self.nodes = list()


class AggregateCredential():
    def __init__(self):
        self.RootList = list()
        self.file_dir = 'Service_App/issue_credential/data'
        self.student_list = os.listdir(self.file_dir)
        self.manifest = OrderedDict()

    def get_node(self, name, credential_type, value, left, right):
        dic = OrderedDict()
        dic['name'] = name
        dic['type'] = credential_type
        dic['value'] = value
        dic['left'] = left
        dic['right'] = right
        return dic

    # hex to binary
    def h2b(self, data):
        if data:
            return bytearray.fromhex(data)

    def get_individualRoot(self):
        if len(self.student_list) > 1:
            for student in self.student_list:
                with open(self.file_dir + '/' + student + '/manifest.json') as file_obj:
                    data = json.load(file_obj)
                data['manifest']['name'] = None
                value = data['manifest']['value']
                self.RootList.append(value)
        else:
            with open(self.file_dir + '/' + self.student_list[0] + '/manifest.json') as file_obj:
                data = json.load(file_obj)
            data['manifest']['name'] = 'Root'
            data['manifest']['value'] = data['manifest']['value'][4:]            
            #write back to manifest.json with name 'Root'
            filename = self.file_dir + '/' + self.student_list[0] + '/manifest.json'
            with open(filename, 'w') as file_obj:
                json.dump(data, file_obj, indent=2)

    def addProof2manifest(self):
        self.get_individualRoot()
        if len(self.RootList) > 0:
            mTools.add_leaf(self.RootList)
            mTools.make_tree()
            for student in self.student_list:
                self.manifest = OrderedDict()
                with open(self.file_dir + '/' + student + '/manifest.json') as file_obj:
                    data = json.load(file_obj)
                self.manifest = data['manifest']
                signature = data['signature']
                index = self.student_list.index(student)
                proof = mTools.get_proof(index)
                root = mTools.get_merkle_root()
                manifestDic = OrderedDict()
                for p in proof:
                    for key in p.keys():
                        if key == "left":
                            manifestDic['name'] = None
                            manifestDic['type'] = None
                            manifestDic['value'] = mTools.getHash_hex(p[key].encode('utf-8') + self.manifest['value'].encode('utf-8'))
                            manifestDic['left'] = self.get_node(None, None, p[key], None, None)
                            manifestDic['right'] = self.manifest
                            self.manifest = self.get_node(None, None, manifestDic['value'], manifestDic['left'],
                                                     manifestDic['right'])
                            continue
                        if key == "right":
                            manifestDic['name'] = None                            
                            manifestDic['type'] = None
                            manifestDic['value'] = mTools.getHash_hex(self.manifest['value'].encode('utf-8') + p[key].encode('utf-8'))
                            manifestDic['left'] = self.manifest
                            manifestDic['right'] = self.get_node(None, None, p[key], None, None)
                            self.manifest = self.get_node(None, None, manifestDic['value'], manifestDic['left'],
                                                     manifestDic['right'])
                            continue

                manifestDic['name'] = "Root"
                manifestDic['type'] = None
                manifestDic['value'] = root[4:]
                manifestDic['left'] = self.manifest['left']
                manifestDic['right'] = self.manifest['right']

                dic = OrderedDict()
                dic['manifest'] = manifestDic
                dic['signature'] = signature
                #add aggregate proof back to individual manifest.json
                filename = self.file_dir + '/' + student + '/manifest.json'
                with open(filename, 'w') as file_obj:
                    json.dump(dic, file_obj, indent=2)

def main():
    create_credential()

    manifest = Manifest()
    manifest.create()

    aggregateCredential = AggregateCredential()
    aggregateCredential.addProof2manifest()

if __name__ == '__main__':
    main()
