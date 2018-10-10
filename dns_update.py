import os
import json
import requests

URL = "https://api.digitalocean.com/v2/domains/parmserv.com/records"
API_KEY = os.environ.get("DO_API_KEY")
DOMAIN_RECORD = "ipfire"

HEADERS = {"Content-Type":"application/json", "Authorization":"Bearer " + API_KEY}

def main():
    print(check_ip())
    print(get_home_domain())

def check_ip():
    new_ip = json.loads(requests.get("https://api.ipify.org?format=text").text)
    with open('ip.txt', 'w') as file_name:
        file_name.write(str(new_ip))
    return new_ip

def get_home_domain():
    res = requests.get(URL, headers=HEADERS).json()
    for obj in res['domain_records']:
        if obj['name'] == DOMAIN_RECORD:
            return obj
    return "Not Found"

def update_home_domain(obj, new_ip):
    update_url = URL + "/" + obj["id"]
    requests.put(update_url, data={'data':new_ip})

if __name__ == '__main__':
    main()
