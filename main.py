import requests
import os
import pip
import argparse
from dotenv import load_dotenv


def shorten_link(token, long_link, headers, base_url):
    url = f'{base_url}bitlinks'
    payload = {'long_url': long_link}
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    bitlink = response.json()['id']
    return bitlink


def count_clicks(token, bitlink, headers, base_url):
    url = f'{base_url}bitlinks/{bitlink}/clicks/summary'
    payload = {
        'units': '-1',
        'unit': 'day',
    }
    response = requests.get(url, headers=headers, params=payload)
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(link, headers, base_url):
    url = f'{base_url}bitlinks/{link}'
    response = requests.get(url, headers=headers)
    if response.ok:
        return True
    return False


def main():
    token = os.getenv('BITLY_TOKEN')
    base_url = 'https://api-ssl.bitly.com/v4/'
    headers = {'Authorization': f'Bearer {token}'}
    parser = argparse.ArgumentParser(
        description='Программа сокращает длинные ссылки и показывает '
                    'количество переходов по ссылке')
    parser.add_argument('link', help='Введите длинную ссылку'
                                     ' для сокращения или сокращенную для получения статистики')
    args = parser.parse_args()
    bitlink_info = is_bitlink(args.link, headers, base_url)
    if bitlink_info:
        result = f'По вашей ссылке прошли: {count_clicks(token, args.link, headers, base_url)} раз(а)'
    else:
        try:
            result = f'Битлинк: {shorten_link(token, args.link, headers, base_url)}'
        except requests.exceptions.HTTPError:
            result = "Вы ввели неверный адрес"
    print(result)


if __name__ == "__main__":
    load_dotenv()
    main()
