import json, shutil, os

class Node():
    def __init__(self, name, credential_type, value, left, right):
        self.type = credential_type
        self.name = name
        self.value = value
        self.left = left
        self.right = right

    def get_nodes(self, nodes):
        d = dict()

        d['name'] = self.name
        d['type'] = self.type
        d['value'] = self.value

        lchild = self.get_lchild(nodes)
        if lchild:
            d['left'] = lchild.get_nodes(nodes)
        else:
            d['left'] = None

        rchild = self.get_rchild(nodes)
        if rchild:
            d['right'] = rchild.get_nodes(nodes)
        else:
            d['right'] = None

        return d

    def get_lchild(self, nodes):
       for n in nodes:
           if n.value == self.left:
               return n

    def get_rchild(self, nodes):
        for n in nodes:
            if n.value == self.right:
                return n

    def __repr__(self):
        return self.name

class getNodes():
    def __init__(self, manifest):
        self.manifest = manifest
        self.nodes = list()

    def get_nodebyName(self, manifest, nodeName, selectList):
        lnode = manifest['left']
        rnode = manifest['right']
        if lnode is not None and rnode is not None:
            if lnode['name'] == nodeName: 
                leftNode = Node(lnode['name'], lnode['type'], lnode['value'], None, None)
                if rnode['name'] in selectList:
                    rightNode = Node(rnode['name'], rnode['type'], rnode['value'], None, None)
                else:
                    if rnode['left'] is not None and rnode['right'] is not None:
                        rightNode = Node(None, None, rnode['value'], rnode['left']['value'], rnode['right']['value'])
                    else:
                        rightNode = Node(None, None, rnode['value'], None, None)
                node = Node(None, None, manifest['value'], lnode['value'], rnode['value'])
                self.nodes.append(leftNode)
                self.nodes.append(rightNode)
                self.nodes.append(node)
                self.nodes = self.get_proofDatas(self.manifest, manifest['value'], selectList)
                return self.nodes

            if rnode['name'] == nodeName:
                rightNode = Node(rnode['name'], rnode['type'], rnode['value'], None, None)
                if lnode['name'] in selectList:
                    leftNode = Node(lnode['name'], lnode['type'], lnode['value'], None, None)
                else:
                    if lnode['left'] is not None and lnode['right'] is not None:
                        leftNode = Node(None, None, lnode['value'], lnode['left']['value'], lnode['right']['value'])
                    else:
                        leftNode = Node(None, None, lnode['value'], None, None)
                node = Node(None, None, manifest['value'], lnode['value'], rnode['value'])
                self.nodes.append(leftNode)
                self.nodes.append(rightNode)
                self.nodes.append(node)
                self.nodes = self.get_proofDatas(self.manifest, manifest['value'], selectList)
                return self.nodes

            self.get_nodebyName(lnode, nodeName, selectList)
            self.get_nodebyName(rnode, nodeName, selectList)
        return self.nodes

    def get_proofDatas(self, manifest, value, selectList):
        lnode = manifest['left']
        rnode = manifest['right']
        if lnode is not None and rnode is not None:
            leftValue = lnode['value']
            rightValue = rnode['value']
            if leftValue == value:
                if rnode['left'] is not None and rnode['right'] is not None:
                    if rnode['name'] in selectList:
                        rightNode = Node(rnode['name'], rnode['type'], rightValue, rnode['left']['value'], rnode['right']['value'])
                    else:
                        rightNode = Node(None, None, rightValue, rnode['left']['value'], rnode['right']['value'])
                else:
                    if rnode['name'] in selectList:
                        rightNode = Node(rnode['name'], rnode['type'], rightValue, None, None)
                    else:
                        rightNode = Node(None, None, rightValue, None, None)
                if manifest['name'] == "Root":
                    node = Node("Root", None, manifest['value'], leftValue, rightValue)
                    self.nodes.append(rightNode)
                    self.nodes.append(node)
                    return self.nodes
                else:
                    node = Node(None, None, manifest['value'], leftValue, rightValue)
                    self.nodes.append(rightNode)
                    self.nodes.append(node)

                self.get_proofDatas(self.manifest, manifest['value'], selectList)

            if rightValue == value:
                if lnode['left'] is not None and lnode['right'] is not None:
                    if lnode['name'] in selectList:
                        leftNode = Node(lnode['name'], lnode['type'], leftValue, lnode['left']['value'], lnode['right']['value'])
                    else:
                        leftNode = Node(None, None, leftValue, lnode['left']['value'], lnode['right']['value'])
                else:
                    if lnode['name'] in selectList:
                        leftNode = Node(lnode['name'], lnode['type'], leftValue, None, None)
                    else:
                        leftNode = Node(None, None, leftValue, None, None)
                if manifest['name'] == "Root":
                    node = Node("Root", None, manifest['value'], leftValue, rightValue)
                    self.nodes.append(leftNode)
                    self.nodes.append(node)
                    return self.nodes
                else:
                    node = Node(None, None, manifest['value'], leftValue, rightValue)
                    self.nodes.append(leftNode)
                    self.nodes.append(node)

                self.get_proofDatas(self.manifest, manifest['value'], selectList)

            self.get_proofDatas(lnode, value, selectList)
            self.get_proofDatas(rnode, value, selectList)
        return self.nodes

def getCredential(credential_path, selectList, selectFile_path):
    new_path = selectFile_path + '/credential'
    if os.path.isdir(new_path):
        pass
    else:
        os.makedirs(new_path)

    credential_list = os.listdir(credential_path)
    if selectList == []:        
        for credential in credential_list:
            shutil.copyfile(credential_path + '/' + credential , new_path + '/' + credential)                
    else:
         for credential in credential_list:
            if credential in selectList:
                shutil.copyfile(credential_path + '/' + credential , new_path + '/' + credential)
                

def getManifest(manifestFile, selectList, selectFile_path):    
    if selectList == []:
        filename = selectFile_path + '/manifest.json'
        with open(filename, 'w') as file_obj:
            json.dump(manifestFile, file_obj, indent=2)
            return

    manifest = manifestFile['manifest']
    signature = manifestFile['signature']

    nodes = getNodes(manifest)
    nodeList = list()
    for name in selectList:
        for n in nodeList:
            if name == n.name:
                continue
        node = nodes.get_nodebyName(manifest, name, selectList)
        for n in node:
            nodeList.append(n)

    dic = dict()
    root = nodeList[-1]
    manifest = root.get_nodes(nodeList)
    dic['manifest'] = manifest
    dic['signature'] = signature

    filename = selectFile_path + '/manifest.json'
    with open(filename, 'w') as file_obj:
        json.dump(dic, file_obj, indent=2)

def selectCredential(selectList):
    data_path = 'Service_App/select_credential/data'
    manifestFile =  data_path + '/manifest.json'
    with open(manifestFile) as file_obj:
        manifest = json.load(file_obj)

    credential_path = data_path + '/credential'

    selectFile_path = 'Service_App/select_credential/select_data'

    if os.path.isdir(selectFile_path):
        #remove folder in 'select_data' if exist
    	shutil.rmtree(selectFile_path)

    getCredential(credential_path, selectList, selectFile_path)
    getManifest(manifest, selectList, selectFile_path)

    shutil.copyfile(data_path + '/issuer.json' , selectFile_path + '/issuer.json')


def main():
    selectList = ['blockcerts.json', 'recipientProfile.json']
    selectCredential(selectList)

if __name__ == '__main__':
    main()

