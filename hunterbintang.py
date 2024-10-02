import requests
import json
import time
import os
import base64
from colorama import Fore
from datetime import datetime, timedelta



os.system('clear')

ascii_banner = f"""
  ___ ___               __                _________              __                 
 /   |   \\ __ __  _____/  |_  ___________/   _____/__ __   ____ |  | __ ___________ 
/    ~    \\  |  \\/    \\   __\\/ __ \\_  __ \\_____  \\|  |  \\_/ ___\\|  |/ // __ \\_  __ \\
\\    Y    /  |  /   |  \\  | \\  ___/|  | \\/        \\  |  /\\  \\___|    <\\  ___/|  | \\/
 \\___|_  /|____/|___|  /__|  \\___  >__| /_______  /____/  \\___  >__|_ \\\\___  >__|   
       \\/            \\/          \\/             \\/            \\/     \\/    \\/       

"""

print(ascii_banner)

apikeys = [
    "40073c95b4571b0085d99ad4859ab7d3894fa314960afe172b55ae203cf33382"
]

page_size = 50
page_size2 = 100
today = datetime.now().strftime('%Y-%m-%d')
start_time = (datetime.now() - timedelta(days=350)).strftime('%Y-%m-%d')

def get_api_key():
    api_key = apikeys.pop(0)
    apikeys.append(api_key)
    return api_key

api_key = ''

def get(qenc, t):
    global api_key
    u = "https://api.hunter.how/search?api-key=%s&query=%s&page=%d&page_size=%d&start_time=%s&end_time=%s" % (
        api_key, qenc, t, page_size2, start_time, today
    )

    x = requests.get(u)
    time.sleep(1.5)
    jsons = x.json()
    if jsons['message'] == 'Exceed the daily query usage, try again tomorrow':
        print('API key exceeded limit: ', api_key)
        api_key = get_api_key()
        print('Trying new API key: ', api_key)
        get(qenc, t)
        return
    if jsons['message'] =='success' and jsons['data']:
        for data in jsons['data']['list']:
            if data['domain'] == None or data['domain'] == '':
                continue
            print(data['domain'])
            open("awsarn.txt", "a").write(data['domain']+'\n')
            open("awsarnip.txt", "a").write(
                data['ip']+":"+str(data['port'])+'\n')
    else:
        print(t, jsons['message'])

try:
    # web.body="hahaha" and ip.country=="Indonesia"
    q = input(Fore.GREEN+'[Input Query Search ]> ')
    qenc = base64.urlsafe_b64encode(q.encode("utf-8")).decode('ascii')
    pages = int(input(Fore.GREEN+'[Start Pages ]> ')) 
    all_page = 200
    api_key = get_api_key()
    for t in range(pages, all_page):
        t = t + 1
        print("Page " + str(t)) 
        get(qenc, t)
except Exception as e:
    print(e)
