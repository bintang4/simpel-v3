import requests
import json

def send_msg(text):
    print(text)
    exit()

def get(url, headers=None):
    response = requests.get(url, headers=headers)
    return response.text

def main():
    # Cek dan baca apikey dari file
    try:
        with open('apikey.txt', 'r') as file:
            apikey = file.read().strip()
    except FileNotFoundError:
        send_msg("Buat file apikey.txt dulu")

    if not apikey:
        send_msg("Masukin apikey dulu di apikey.txt")

    headers = {
        'accept': 'application/json',
        'api-key': apikey
    }

    while True:
        query = input("Query (Dork) : ")
        no = 0
        i = 0

        while True:
            search_url = f"https://leakix.net/search?scope=leak&page={i}&q={query}"
            search = get(search_url, headers)
            if not search:
                send_msg(f"Done! Max Page {i}")

            if "Invalid API key" in search:
                send_msg("Invalid API key")

            json_data = json.loads(search)
            no += 1

            if not json_data:  # If no more data
                send_msg(f"Done! Max Page {i}")

            for item in json_data:
                event_source = item['event_source']
                ip = item['ip']
                protocol = item['protocol']
                domain = item['host']

                with open("result.txt", "a") as result_file:
                    result_file.write(f"{protocol}://{domain}/\n")

                print(f"[{no}] | [{domain} - {ip}] | [{event_source}] | {protocol} -> SAVED")

            i += 1

if __name__ == "__main__":
    main()