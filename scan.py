import sys
import requests
import random
import string
import time
import re
from multiprocessing.dummy import Pool
from colorama import Fore, Style, init
from requests.packages.urllib3.exceptions import InsecureRequestWarning

init(autoreset=True)

fr = Fore.RED
fy = Fore.YELLOW
fg = Fore.GREEN
sb = Style.BRIGHT


def urlfix(url):
    if url[:7] != 'http://' and url[:8] != 'https://':
        url = 'http://' + url
    return url


def exploit(url):
    try:
        se = requests.session()
        agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        response = se.get(url, headers=agent, verify=False, timeout=30)
        
        patterns = {
            "TWILIO|twilio|AC[a-z0-9]{32}": "twilio.txt",
            "email-smtp": "randoman.txt",
            "AKIA[A-Z0-9]{16}": "aws.txt",

            
        }
        
        for pattern, filename in patterns.items():
            if re.search(pattern, response.content.decode()):
                print(fy + sb + f"[GOT KEYWORD] ---->  [SCANNING] : {url}")
                open(filename, 'a').write(url + '\n')
                break
        else:
            print(fr + sb + "[KEYWORD NOT FOUND] [0] -------> " + url)
    except Exception as e:
        print(fr + sb + "[ERROR] -------> " + url + " : " + str(e))


def check(url):
    try:
        url = urlfix(url)
        agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        response = requests.get(url, headers=agent, verify=False, timeout=30)
        if response.status_code == 200:
            print(fy + sb + "[SITE IS WORKING LOOKING FOR VULN] ---->  [SCANNING] :" + url)
            exploit(url)
        else:
            print(fr + sb + "SITE IS DOWN... -------> " + url)
    except requests.exceptions.Timeout:
        print(fr + sb + "[ERROR] -------> " + url + " : Read timed out.")
    except Exception as e:
        print(fr + sb + "[ERROR] -------> " + url + " : " + str(e))


def logo():
    clear = '\x1b[0m'
    colors = [36, 32, 34, 35, 31, 37]
    x = """
                                   .__                
  ______ ____ _____    ____   ____ |__| ____    ____  
 /  ___// ___\\__  \  /    \ /    \|  |/    \  / ___\ 
 \___ \\  \___ / __ \|   |  \   |  \  |   |  \/ /_/  >
/____  >\___  >____  /___|  /___|  /__|___|  /\___  / 
     \/     \/     \/     \/     \/        \//_____/
made by twelve1337                                
"""

    for N, line in enumerate(x.split('\n')):
        sys.stdout.write('\x1b[1;%dm%s%s\n' % (random.choice(colors), line, clear))
        time.sleep(0.05)


def main():
    try:
        logo()
        url_list = input(fr + sb + "\n\t[SCANNING] INPUT UR FILE HERE: ")
        urls = open(url_list, 'r').read().splitlines()

        thread_pool = Pool(40)
        thread_pool.map(check, urls)
        thread_pool.close()
        thread_pool.join()
    except FileNotFoundError:
        print(fr + sb + "[ERROR] FUCK YOU FILE NOT FOUND")
    except Exception as e:
        print(fr + sb + "[ERROR] An error occurred: " + str(e))


if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    main()
