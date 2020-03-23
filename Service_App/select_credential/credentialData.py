import json

def getData(name_list, data): #get name
    name = data['name']
    left = data['left']
    right = data['right']
    if name != 'Root' and name is not None:
        name_list.append(name)

    if left is not None and right is not None:
        getData(name_list, left)
        getData(name_list, right)

    return name_list


def get_credential():
    filename =  'Service_App/select_credential/data/manifest.json'
    with open(filename) as file_obj:
        manifest = json.load(file_obj)

    name_list = list()
    credential_list = list(set(getData(name_list, manifest['manifest'])))
    return credential_list