import os
from os.path import dirname, join
import argparse
from urllib.parse import urlparse
from dotenv import load_dotenv
import requests


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
ACCESS_TOKEN = 'Bearer {}'.format(os.getenv('ACCESS_TOKEN'))


def create_parser():
    parser = argparse.ArgumentParser(
        description="You can enter a 'short' or regular link")
    parser.add_argument("user_link", nargs="?", help="'Short' or regular link")

    return parser


def print_user_info():
    url = 'https://api-ssl.bitly.com/v4/user'
    headers = {
        'Authorization': ACCESS_TOKEN,
    }

    response = requests.get(url, headers=headers)
    if response.ok:
        print(response.text)
    else:
        print('Status code: {}. Something is wrong!'.format(response.status_code))


def get_bitlink(regular_link, token=ACCESS_TOKEN):
    url = 'https://api-ssl.bitly.com/v4/bitlinks'
    headers = {
        'Authorization': token,
    }

    request_data = {
        'long_url': regular_link,
    }

    response = requests.post(
        url=url,
        json=request_data,
        headers=headers,
    )

    if not response.ok:
        return None

    return response.json()['link']


def get_bitlink_id(bitlink):
    bitlink_parse_result = urlparse(bitlink)
    return '{}{}'.format(
        bitlink_parse_result.netloc,
        bitlink_parse_result.path
    )


def is_bitlink_exists(bitlink, token=ACCESS_TOKEN):
    bitlink_id = get_bitlink_id(bitlink)

    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink_id}'
    headers = {
        'Authorization': token,
    }

    response = requests.get(
        url = url,
        headers=headers
    )
    return response.ok


def get_clicks_count(bitlink, token=ACCESS_TOKEN):
    bitlink_id = get_bitlink_id(bitlink)

    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink_id}/clicks/summary'
    headers = {
        'Authorization': token,
    }
    params = {
        'unit': 'day',
        'units': -1,
    }

    response = requests.get(
        url=url,
        params=params,
        headers=headers
    )
    if not response.ok:
        return None
    try:
        return response.json()['total_clicks']
    except KeyError:
        return None


def main():
    parser = create_parser()
    args = parser.parse_args()

    user_link = args.user_link if args.user_link else input('Введите ссылку: ')

    if is_bitlink_exists(user_link):
        print('Количество переходов по ссылке битли:', get_clicks_count(user_link))
        return

    bitlink = get_bitlink(user_link)
    print('Ошибка! Неправильная "короткая" ссылка.') if bitlink is None \
        else print(bitlink)
    return


if __name__ == '__main__':
    main()
