import requests
import socket
import re
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, init

ips = []  # global list of IPs

# initialize colorama for terminal color output
init(autoreset=True)

def resolve_domain_to_ip(domain: str) -> str:
    """
    Resolve domain name to an IP address.
    """
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return domain

def fetch_data_from_url(url: str) -> str:
    """
    Fetch data from given URL using HTTP GET request.
    """
    try:
        response = requests.get(url, timeout=70)
        return response
    except Exception as e:
        print(f"{Fore.RED}Error occurred while fetching data: {e}")
        return ''

def fetch_results_from_api_1(ip: str) -> list:
    """
    Fetch domains associated with an IP from the first API.
    """
    url = f'https://api.webscan.cc/?action=query&ip={ip}'
    domains = []
    response = fetch_data_from_url(url)
    if response.text != 'null':
        try:
            json_response = response.json()
            for domain in json_response:
                domains.append(domain['domain'])
        except Exception as e:
            print(f"{Fore.RED}Error occurred while parsing JSON: {e} -> {ip}")
    return domains

def fetch_results_from_api_2(ip: str) -> list:
    """
    Fetch domains associated with an IP from the second API.
    """
    url = f'https://rapiddns.io/sameip/{ip}?full=1&down=1&t=None'
    domains = []
    response = fetch_data_from_url(url)
    if response:
        if "scope=\"row \"" in response.text:
            regex_pattern = r'''</th>\n<td>(.+?)</td>\n<td>'''
            domains = re.findall(regex_pattern, response.text)
    return domains

def execute(domain: str) -> None:
    """
    Main execution function for each domain.
    """
    global ips
    # Normalize the domain input
    if '://' in domain:
        domain = domain.split('://')[1]
    elif domain.endswith('/'):
        domain = domain[:-1]
    
    print(f"{Fore.GREEN}Target: {domain}")
    ip = resolve_domain_to_ip(domain)
    if ip in ips:
        print(f"{Fore.RED}IP already resolved: {ip}")
        return
    ips.append(ip)
    print(f"{Fore.YELLOW}Resolved IP: {ip}")
    
    all_domains = []
    # Fetch results from APIs
    domains_from_api_1 = fetch_results_from_api_1(ip)
    all_domains.extend(domains_from_api_1)
    domains_from_api_2 = fetch_results_from_api_2(ip)
    all_domains.extend(domains_from_api_2)
    
    unique_domains = list(set(all_domains))  # Remove duplicates
    print(f"{Fore.BLUE}Results: {len(unique_domains)}")
    
    # Write unique domains to a file
    with open('revip.txt', 'a') as file:
        for domain in unique_domains:
            file.write(f'{domain}\n')

def main():
    """
    Main function to read URLs from a file and execute concurrently.
    """
    urls = input('Urls ? ')
    opened_urls = open(urls, 'r').read().splitlines()
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(execute, opened_urls)

if __name__ == '__main__':
    main()
