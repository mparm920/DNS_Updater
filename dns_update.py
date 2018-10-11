import os
import requests

URL = "https://api.digitalocean.com/v2/domains/parmserv.com/records"
API_KEY = os.environ.get("DO_API_KEY")
DOMAIN_RECORD = "ipfire"

HEADERS = {"Content-Type":"application/json", "Authorization":"Bearer " + API_KEY}

def main():
    print(check_ip())

def check_ip():
    new_ip = get_new_ip().split('.')
    current_ip = get_current_ip().split('.')
    if new_ip != current_ip:
        save_new_ip(new_ip)
        domain = get_home_domain()
        if domain:
            update_home_domain(domain, new_ip)
        else:
            pass

def get_new_ip():
    return requests.get("https://api.ipify.org?format=text").text

def get_current_ip():
    ip = ""
    with open('ip.txt', 'r') as file_name:
        ip = file_name.readline()
    return ip

def save_new_ip(ip):
    with open('ip.txt', 'w') as file_name:
        file_name.write(ip)

def get_home_domain():
    res = requests.get(URL, headers=HEADERS).json()
    for obj in res['domain_records']:
        if obj['name'] == DOMAIN_RECORD:
            return obj
    return None

def update_home_domain(obj, new_ip):
    update_url = URL + "/" + obj["id"]
    requests.put(update_url, data={'data':new_ip})

if __name__ == '__main__':
    main()
