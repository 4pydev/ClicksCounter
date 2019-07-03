import os
from os.path import dirname, join
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
    print(response.text)


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

    if response.ok:
        return response.json()['link']
    else:
        return None


def get_clicks_count(bitlink, token=access_token):
    bitlink = bitlink.replace('http://', '')

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
    try:
        return response.json()['total_clicks']
    except KeyError:
        return None


def main():
    user_link = input('Enter a link: ')

    if user_link.startswith('http://bit.ly'):
        total_clicks = get_clicks_count(user_link)
        if total_clicks is None:
            print('Error: Invalid link.')
        else:
            print('Total clicks:', total_clicks)
    else:
        bitlink = get_bitlink(user_link)
        if bitlink is None:
            print('Error: Invalid bitlink.')
        else:
            print('Bitlink:', bitlink)


if __name__ == '__main__':
    main()
