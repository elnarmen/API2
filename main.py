import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
BASE_URL = 'https://api-ssl.bitly.com/v4/'
HEADERS = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json'
}


def main():
    def shorten_link(token, long_link):
        url = BASE_URL + 'bitlinks'
        payload = {
            'long_url': long_link
        }
        try:
            response = requests.post(url, headers=HEADERS, json=payload)
            response.raise_for_status()
            link = response.json()['link'].replace('http://', '')\
                .replace('https://', '')
            return link
        except requests.exceptions.HTTPError:
            return ('Неверный адрес')

    def count_clicks(token, bitlink):
        url = BASE_URL + f'/bitlinks/{bitlink}/clicks/summary'
        payload = {
            'units': '-1',
            'unit': 'day',
        }
        response = requests.get(url, headers=HEADERS, params=payload)
        response.raise_for_status()
        return response.json()['total_clicks']

    def is_bitlink(link):
        url = BASE_URL + f'/bitlinks/{link}'

        response = requests.get(url, headers=HEADERS)
        if response.ok:
            return response.json()['link']

    user_input = input()
    result = count_clicks(TOKEN, user_input) if is_bitlink(user_input) \
        else shorten_link(TOKEN, user_input)
    print(result)
if __name__ == "__main__":
    main()
