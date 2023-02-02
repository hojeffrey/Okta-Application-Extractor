import os 
import requests
import json
import re
import time
import yaml

def main():
    #Import variables from YAML File 
    with open("config.yaml", 'r') as config:
    config_info = yaml.load(config)
    api_token = config_info["api_token"]
    list_application_url =  config_info["application_url"]
    folder_name = config_info["folder_name"]

    #Headers for Okta
    okta_headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'SSWS' + api_token
    }
    saml_headers= {
        'Accept': '*/*',
        'Authorization': 'SSWS' + api_token
    }


    # Create directory folder same path it executes on
    try:
        current_path = os.getcwd()
        folder_path = os.path.join(current_path,folder_name)    
        os.makedirs(folder_path)
        print("Directory '%s' created" % folder_name)
    except FileExistsError:
        print("The Directory is already Created")
        pass


    initiate_list_application = requests.get(list_application_url, headers=okta_headers)

    get_pagination_pointer = str(initiate_list_application.headers)

    pointer_regex = re.compile('rel="self", <((?:(?!").)*)>; rel="next"')

    okta_pagination_next_url = pointer_regex.findall(get_pagination_pointer)[0]

    while okta_pagination_next_url:
        get_application_json_result = json.loads(initiate_list_application.text)

        #Make Directory name under application name, save the json and save xml if it contains 
        for index, i in enumerate(get_application_json_result):
            print("COUNTER: " + str((int(index) + 1)))
            application_id = (i['id'])
            status = (i['status'])
            app_name = (i['name'])
            label = (i['label'])
            
            try:
                app_folder_path = (os.path.join(folder_path,label))
                os.makedirs(app_folder_path)
                print("Directory " + app_folder_path + "created")
            except FileExistsError:
                print("The Directory is already Created")
                pass

            with open((os.path.join(app_folder_path, label) + ".json"), 'w') as f:
                json.dump(i, f, indent=4, sort_keys=True)
                print((os.path.join(app_folder_path, label) + ".json") + " file is created")

            try:
                saml_metadata_url = (i['_links']['metadata']['href'])
            get_saml_metadata = requests.get(saml_metadata_url, headers=saml_headers)
            time.sleep(2)
            with open((os.path.join(app_folder_path, label) + ".xml"), 'w') as xml_file:
                xml_file.write(get_saml_metadata.text)
                print((os.path.join(app_folder_path, label) + ".xml") + " file is created")
        except KeyError:
            pass

if __name__ == "__main__":
    main()
