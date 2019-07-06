import os
from os.path import dirname, join
from urllib.parse import urlparse
from dotenv import load_dotenv
import requests


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
access_token = 'Bearer {}'.format(os.getenv('ACCESS_TOKEN'))


def print_user_info():
    url = 'https://api-ssl.bitly.com/v4/user'
    headers = {
        'Authorization': access_token,
    }

    response = requests.get(url, headers=headers)
    if response.ok:
        print(response.text)
    else:
        print('Status code: {}. Something is wrong!'.format(response.status_code))


def get_bitlink(regular_link, token=access_token):
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


def is_bitlink_exists(bitlink, token=access_token):
    bitlink_parse_result = urlparse(bitlink)
    bitlink = '{}{}'.format(
        bitlink_parse_result.netloc,
        bitlink_parse_result.path
    )

    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}'
    headers = {
        'Authorization': token,
    }

    response = requests.get(
        url = url,
        headers=headers
    )
    return response.ok


def get_clicks_count(bitlink, token=access_token):
    bitlink_parse_result = urlparse(bitlink)
    bitlink = '{}{}'.format(
        bitlink_parse_result.netloc,
        bitlink_parse_result.path
    )

    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
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
    user_link = input('Enter a link: ')

    if is_bitlink_exists(user_link):
        print('Total clicks:', get_clicks_count(user_link))
        return

    bitlink = get_bitlink(user_link)
    print('Error: Invalid bitlink.') if bitlink is None \
        else print('Bitlink:', bitlink)
    return


if __name__ == '__main__':
    main()
