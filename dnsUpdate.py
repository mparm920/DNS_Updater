import requests
import os
import json

URL = "https://api.digitalocean.com/v2/domains/parmserv.com/records"
API_Key = os.environ.get("DO_API_KEY") 
DOMAIN_RECORD = "ipfire"

headers = {"Content-Type":"application/json", "Authorization":"Bearer " + API_Key}

def main():
    print(check_IP())

def check_IP():
    newIP = json.loads(requests.get("https://api.ipify.org?format=json").text)
    with open('ip.txt', 'w') as f:
        f.write(str(newIP))
    return newIP

def get_Home_Domain():
    res = requests.get(URL, headers=headers).json()
    for obj in res['domain_records']:
        if obj['name'] == DOMAIN_RECORD:
            return obj

def update_Home_Domain(obj, newIP):
    updateURL = URL + "/" + obj["id"] 
    res = requests.put(updateURL, data={'data':newIP})

if __name__ == '__main__':
    main()