import requests

URL = "https://api.digitalocean.com/v2/domains/parmserv.com/records"
API_Key = ""

headers = {"Content-Type":"application/json", "Authorization":"Bearer " + API_Key}

res = requests.get(URL, headers=headers).json()
for obj in res['domain_records']:
    if obj['name'] == 'home':
        print(obj['name'])