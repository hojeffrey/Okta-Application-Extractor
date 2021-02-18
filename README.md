# Introduction

**Okta Application Extractor** is a python script that pulls the okta application JSON and SAML XML file from your okta tenant. It relies on the Okta API to gather the data. The Okta API Key and Tenant URL will be configured in the YAML file. 

Pagination is currently not supported in the script, I will work on it in the future. The current limit of applications that can be pulled is 200. 

## How to Use
1. Please have a working version of python3 installed. 
2. Configure the Yaml 

```
api_token: "Insert API Token"
application_url: "https://YourComapnyURL.okta.com/api/v1/apps?filter=status+eq+%22ACTIVE%22&limit=200"
folder_name: "Provide_Folder_Name"
```
3. Run python script 

## Result

```
.
├── mycompany_applications
    ├── cool HR application
    |   ├── cool HR application.json
    |   ├── cool HR application.xml
    ├── Social Media
    |   ├── Social Media.json
    |   ├── Social Media.xml
    └── Web Application Firewall
        ├── Web Application Firewall.json
        ├── Web Application Firewall.xml
```
