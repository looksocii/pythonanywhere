import json
import os

def get_credentialAssociation(tree_path, association_path):
        student_list = os.listdir(tree_path)  #'Service_App\\issue_credential\\tree'
        association_list = os.listdir(association_path) #'Service_App\\issue_credential\\association'

        #for all students
        if len(association_list) == 1:
            with open(association_path + '/' + association_list[0]) as file_obj:
                dic =  json.load(file_obj) #dic[parentName] = childList


            for file in student_list:
                with open(tree_path + '/' + file) as file_obj:
                    data = json.load(file_obj)
                for value in data['credentialTree']:
                    name = value['name']

                    if name in dic.keys():
                        value['type'] = dic[name]['type']
                        value['child'] = dic[name]['child'] #add name's childList to child
                # write data back to tree
                    filename = tree_path + '/' + file
                    with open(filename, 'w') as file_obj:
                        json.dump(data, file_obj, indent=2)

        #for each student
        else:
            for file in student_list:
                with open(tree_path + '/' + file) as file_obj:
                    data = json.load(file_obj)

                with open(association_path + '/' + file) as file_obj:
                    dic =  json.load(file_obj) #dic[parentName] = childList

                for value in data['credentialTree']:
                    name = value['name']
                    if name in dic.keys():
                        value['type'] = dic[name]['type']
                        value['child'] = dic[name]['child'] #add name's childList to child
                #write data back to tree
                filename = tree_path + '/' + file
                with open(filename, 'w') as file_obj:
                    json.dump(data, file_obj, indent=2)

if __name__ == '__main__':
    get_credentialAssociation('tree', 'association')
    
    
