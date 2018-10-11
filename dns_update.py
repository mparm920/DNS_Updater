import os
import logging
import requests

URL = "https://api.digitalocean.com/v2/domains/parmserv.com/records"
API_KEY = os.environ.get("DO_API_KEY")
DOMAIN_RECORD = "ipfire"

HEADERS = {"Content-Type":"application/json", "Authorization":"Bearer " + API_KEY}

def main():
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename="dns_update.log", level=logging.INFO)
    check_ip()

def check_ip():
    new_ip = get_new_ip()
    new_ip_list = new_ip.split('.')
    current_ip = get_current_ip()
    current_ip_list = current_ip.split('.')
    if new_ip_list != current_ip_list:
        save_new_ip(new_ip)
        domain = get_home_domain()
        if domain:
            update_home_domain(domain, new_ip)
        else:
            logging.error("get_home_domain came back with a empty object")
    else:
        logging.info("IP's match new: %s, current: %s", new_ip, current_ip) 

def get_new_ip():
    try:
        return requests.get("https://api.ipify.org?format=text").text
    except Exception as e:
        logging.error("get_new_ip.\nException:\n%s", e)

def get_current_ip():
    ip = ""
    with open('ip.txt', 'r') as file_name:
        ip = file_name.readline()
    return ip

def save_new_ip(ip):
    with open('ip.txt', 'w') as file_name:
        file_name.write(ip)
    logging.info("New IP saved: %s", ip)

def get_home_domain():
    try:
        res = requests.get(URL, headers=HEADERS).json()
        for obj in res['domain_records']:
            if obj['name'] == DOMAIN_RECORD:
                return obj
        return None
    except Exception as e:
        logging.error("get_home_domain. DOMAIN_RECORD: %s. \nException:\n%s", DOMAIN_RECORD, e)

def update_home_domain(obj, new_ip):
    try:
        update_url = URL + "/" + obj["id"]
        requests.put(update_url, data={'data':new_ip})
    except Exception as e:
        logging.error("update_home_domain. Object: %s, New IP: %s\nException:\n%s", str(obj), new_ip, e)

if __name__ == '__main__':
    main()
