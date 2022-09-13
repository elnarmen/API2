import requests
import os
import argparse
import re
from dotenv import load_dotenv
from urllib.parse import urlparse


def strip_scheme(url: str):
    return re.sub(r'^https?:\/\/', '', url)


def shorten_link(token, long_link):
    url = 'https://api-ssl.bitly.com/v4/bitlinks'
    payload = {'long_url': long_link}
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    bitlink = response.json()['id']
    return bitlink


def count_clicks(token, bitlink):
    bitlink = strip_scheme(bitlink)
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(token, link):
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{strip_scheme(link)}'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    return response.ok


def main():
    load_dotenv()
    token = os.getenv('BITLY_TOKEN')
    parser = argparse.ArgumentParser(
        description='Программа сокращает длинные ссылки' +
                    ' и показывает количество переходов по ссылке'
    )
    parser.add_argument(
        'link',
        help='Введите длинную ссылку для сокращения ' +
             'или сокращенную для получения статистики'
    )
    args = parser.parse_args()
    if is_bitlink(token, args.link):
        try:
            print(f'По вашей ссылке прошли: {count_clicks(token, args.link)} раз(а)')
        except requests.exceptions.HTTPError:
            print("Ошибка")
    else:
        try:
            print(f'Битлинк: {shorten_link(token, args.link)}')
        except requests.exceptions.HTTPError:
            print("Вы ввели неверный адрес")


if __name__ == "__main__":
    main()
