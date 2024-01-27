import requests
import json
from concurrent.futures import ThreadPoolExecutor

API_URLS = {
    "https://discord.com/api/v9/outbound-promotions/1187085447709610098/claim": "1month.txt",
    "https://discord.com/api/v9/outbound-promotions/1168622933334294528/claim": "3month.txt"
}

TOKENS_FILE = "tokens.txt"
PROXY_URL = "http://proxy.surdm.com:8000"

def read_access_tokens():
    try:
        with open(TOKENS_FILE, "r") as file:
            return [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"{TOKENS_FILE} not found. Please create the file and add your access tokens.")
        exit()


def claim_and_save(access_token, api_url, save_file):
    headers = {
        "Authorization": f"{access_token}",
        "Content-Type": "application/json",
    }
    proxies = {"http": PROXY_URL, "https": PROXY_URL}

    try:
        response = requests.post(api_url, headers=headers, proxies=proxies)

        if response.status_code == 200:
            print(f"Claim for {api_url} successful. Response:")
            response_json = response.json()
            print(json.dumps(response_json, indent=4))

            code = response_json.get("code")
            if code:
                with open(save_file, "a") as file:
                    file.write(code + "\n")
                    print(f"Code appended to {save_file}")
            else:
                print("Code not found in the response.")

        else:
            print(f"Claim for {api_url} failed with status code: {response.status_code}")
            print("Response text:")
            print(response.text)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")

def main():
    access_tokens = read_access_tokens()

    try:
        num_threads = int(input("Enter the number of threads: "))
    except ValueError:
        print("Invalid input for number of threads. Using default value of 1.")
        num_threads = 1

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        for access_token in access_tokens:
            for api_url, save_file in API_URLS.items():
                executor.submit(claim_and_save, access_token, api_url, save_file)

if __name__ == "__main__":
    main()
