import requests
import time
from colorama import Fore, Style, init


init(autoreset=True)


def print_green(text):
    print(Fore.GREEN + text + Style.RESET_ALL)


def print_red(text):
    print(Fore.RED + text + Style.RESET_ALL)

def print_banner():
    banner = """
.____                  __   ._______  ___________            ___.    
|    |    ____ _____  |  | _|   \   \/  /  _____/___________ \_ |__  
|    |  _/ __ \\\\__  \ |  |/ /   |\     /   \  __\_  __ \__  \ | __ \ 
|    |__\  ___/ / __ \|    <|   |/     \    \_\  \  | \// __ \| \_\ \\
|_______ \___  >____  /__|_ \___/___/\  \______  /__|  (____  /___  /
        \/   \/     \/     \/         \_/      \/           \/    \/ 
TOOLS FOR GRABBING IP AND HOST DOMAIN FROM LEAKIX
made by twelve1337
    """
    print_green(banner)

def search_leakix_api(query, scope):
    api_key = "input ur apikey here"
    headers = {"accept": "application/json", "api-key": api_key}
    
    page = 0
    total_results = 0
    
    while True:
        print(f"Requesting page {page + 1} with scope {scope}...")
        url = f"https://leakix.net/search?scope={scope}&page={page}&q={query}"

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            num_results = len(result)
            total_results += num_results
            print_green(f"Received {num_results} results. Total: {total_results}")
            
            
            save_results_to_files(result)
            
           
            print_results(result)
            
            if not result or num_results < 10: 
                break
            
            page += 1

            time.sleep(2)
        except requests.exceptions.RequestException as err:
            print_red(f"Error during API request: {err}")
            return None

def save_results_to_files(results, ip_filename="result.txt", host_filename="result.txt"):
    with open(ip_filename, "a") as ip_file, open(host_filename, "a") as host_file:
        for result in results:
            ip_file.write(f"{result['ip']}\n")
            host_file.write(f"{result['host']}\n")

def print_results(results):
    print("Result:")
    for i, entry in enumerate(results, start=1):
        print(f"{i}. IP: {entry['ip']}, Host: {entry['host']}")

def main():
    print_banner()
    
    search_query = input("Query? ")
    
    scope_choice = input("Input ur scope (1 for 'leak', 2 for 'service'): ")

    if scope_choice == '1':
        scope = 'leak'
    elif scope_choice == '2':
        scope = 'service'
    else:
        print_red("INVALID SCOPE")
        return

    search_leakix_api(search_query, scope=scope)

if __name__ == "__main__":
    main()
