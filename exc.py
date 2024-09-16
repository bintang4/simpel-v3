import requests
import re
import sys
import multiprocessing as mp
import ctypes

# Disable SSL warnings
requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning)

# Function to save URLs to a file


def save(url: str):
    if re.search(r"cloudflare|bootstrap|jquery", url, re.I):
        return
    print(f"Extracted: {url}")
    with open('extracted.txt', 'a') as file:
        file.write(url + '\n')

# Function to extract JavaScript URLs from HTML body


def extract_js_from_body(body: str, protocol: str, domain: str):
    scripts = re.findall(
        pattern=r"\<script.*?src=[\"|\']([^\"\']*?\.js)[\"|\'].*?>.*?<\/script>",
        string=body,
    )
    for script in scripts:
        if script.startswith("http"):
            if domain not in script:
                continue
            save(script)
        else:
            if not script.startswith("/"):
                script = "/" + script
            save(f"{protocol}://{domain}{script}")

# Function to make HTTP request and extract JavaScript URLs


def request(domain: str):
    protocol = "http"
    if "://" in domain:
        protocol, domain = domain.split("://")
    if domain.endswith('/'):
        domain = domain[:-1]
    try:
        response = requests.get(
            f"{protocol}://{domain}",
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"},
            timeout=7,
            allow_redirects=True,
            verify=False
        )
        response.raise_for_status()
        extract_js_from_body(response.text, protocol, domain)
    except Exception as e:
        print(f"Error: {e}")
        # Log the error to a file

# Main function


def main():
    # Check if the command-line argument is provided
    if len(sys.argv) < 2:
        print("Usage: python script.py <file_with_urls>")
        sys.exit(1)
    try:
        urls = open(sys.argv[1], mode='r').read().splitlines()
    except FileNotFoundError:
        print("File not found.")
        sys.exit(1)
    # Use multiprocessing to make requests concurrently
    pool = mp.Pool(mp.cpu_count())
    pool.map(request, urls)
    pool.close()
    pool.join()


if __name__ == "__main__":
    main()