import json
from Service_App.issue_credential.merkletools import MerkleTools
import os, shutil
from collections import OrderedDict

mTools = MerkleTools()

def create_credential():

    with open('Service_App/issue_credential/issuer.json', 'rb') as file_obj:
        issuer = file_obj.read()

    credential_dir = 'Service_App/issue_credential/credential'
    student_list = os.listdir(credential_dir)

    #remove folder in 'data' if exist
    shutil.rmtree('Service_App/issue_credential/data')
    #remove folder in 'tree' if exist
    shutil.rmtree('Service_App/issue_credential/tree')

    #create credential
    data_path = 'Service_App/issue_credential/data'

    for student in student_list:
        assocList = list()
        credential_list = os.listdir(credential_dir + '/' + student)
        for credential in credential_list:
            #copy credential
            old_path = credential_dir + '/' + student + '/' + credential
            new_path = data_path + '/' + student + '/credential'
            if os.path.isdir(new_path):
                pass
            else:
                os.makedirs(new_path)

            shutil.copyfile(old_path , new_path + '/' + credential)

            #get credential
            with open(old_path, 'rb') as file_obj:
                data = file_obj.read()

            #create credential tree
            assocDic = OrderedDict()
            assocDic['name'] = credential
            dataStr = str(issuer) + str(data)
            assocDic['targetHash'] = '0x00' + mTools.getHash_hex(dataStr.encode('utf-8'))
            assocDic['child'] = list()
            assocList.append(assocDic)

        #copy issuer file
        shutil.copyfile('Service_App/issue_credential/issuer.json', data_path + '/' + student + '/issuer.json')

        #create_tree (association)
        tree = OrderedDict()
        tree['credentialTree'] = assocList
        tree_path = 'Service_App/issue_credential/tree'
        if os.path.isdir(tree_path):
            pass
        else:
            os.makedirs(tree_path)

        filename = tree_path + '/' + student + '.json'

        with open(filename, 'w') as file_obj:
            json.dump(tree, file_obj, indent=2)


if __name__ == '__main__':
    create_credential()





