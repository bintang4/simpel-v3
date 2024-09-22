import requests
import re
import sys
import multiprocessing as mp
import os
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

# Disable SSL warnings
requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning
)

# Define a list of patterns to exclude
EXCLUDE_PATTERNS = [
    r"cloudflare",
    r"bootstrap",
    r"jquery",
    r"cdn",
    r"font-awesome",
    r"cdnjs",
    r"static",
    r"assets",
    r"jquery\.min\.js",
    r"jquery\.js",
    r"bootstrap\.min\.js",
    r"bootstrap\.js",
    r"cloudflare\.js",
    r"react\.js",
    r"vue\.js",
    r"angular\.js",
    r"lodash\.js",
    r"moment\.js",
    r"underscore\.js",
    r"axios\.js",
    r"knockout\.js",
    r"backbone\.js",
    r"chart\.js",
    r"leaflet\.js",
    r"datatables\.js",
    r"select2\.js",
    r"dropzone\.js",
    r"tinyMCE\.js",
    r"ckeditor\.js",
    r"webfont\.js",
    r"popper\.js",
    r"materialize\.js",
    r"bulma\.js",
    r"semantic\.js",
    r"foundation\.js",
    r"sockjs\.js",
    r"stomp\.js",
    r"firebase\.js",
    r"pusher\.js",
    r"socket\.io\.js",
    r"swfobject\.js",
    r"/static/js/main\.js"
]

EXCLUDE_REGEX = re.compile('|'.join(EXCLUDE_PATTERNS), re.I)

def save(url: str, file_path: str):
    if EXCLUDE_REGEX.search(url):
        return
    print(Fore.GREEN + f"Extracted: {url}")
    with open(file_path, 'a') as file:
        file.write(url + '\n')

def extract_js_from_body(body: str, protocol: str, domain: str, credentials_file_path: str):
    scripts = re.findall(
        pattern=r"<script[^>]+src=['\"]([^'\"]*?\.js)['\"]",
        string=body,
        flags=re.IGNORECASE,
    )
    for script in scripts:
        script = script.lower() 
        if script.startswith("http"):
            if domain not in script:
                continue
            save(script, credentials_file_path)
        else:
            if not script.startswith("/"):
                script = "/" + script
            save(f"{protocol}://{domain}{script}", credentials_file_path)

def request_and_extract(domain: str, credentials_file_path: str):
    protocol = "http"
    if "://" in domain:
        protocol, domain = domain.split("://")
    if domain.endswith('/'):
        domain = domain[:-1]
    
    # Using session for better performance
    with requests.Session() as session:
        try:
            with open(os.devnull, 'w') as devnull:
                old_stderr = sys.stderr
                sys.stderr = devnull
                response = session.get(
                    f"{protocol}://{domain}",
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
                    },
                    timeout=3,
                    allow_redirects=True,
                    verify=False
                )
                response.raise_for_status()
                extract_js_from_body(response.text, protocol, domain, credentials_file_path)
        except requests.Timeout:
            print(Fore.YELLOW + f"Timeout : {domain}")
        except requests.RequestException:
            print(Fore.RED + f"Not Vuln : {domain}")
        finally:
            sys.stderr = old_stderr

# Main function
def main() -> None:
    if len(sys.argv) < 2:
        print(Fore.RED + "Usage: python script.py <file_with_urls>")
        sys.exit(1)
    
    try:
        with open(sys.argv[1], mode='r') as file:
            urls = file.read().splitlines()
    except FileNotFoundError:
        print(Fore.RED + "File not found.")
        sys.exit(1)
    
    credentials_file_path = 'extracted.txt'
    
    with mp.Pool(mp.cpu_count()) as pool:
        pool.starmap(
            request_and_extract,
            [(url, credentials_file_path) for url in urls]
        )

if __name__ == "__main__":
    main()
