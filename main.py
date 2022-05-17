import os
from pprint import pprint

import requests
from dotenv import load_dotenv
from pathlib import Path


def fetch_dvmn_long_polling():
    headers = {
        'Authorization': f'Token {dvmn_auth_token}'
    }
    params = {

    }

    dvmn_answer = requests.get(f'https://dvmn.org/api/long_polling/', headers=headers, timeout=5)
    dvmn_answer.raise_for_status()
    if dvmn_answer.ok:
        time_stamp = dvmn_answer.json()['']
        return time_stamp
    # return dvmn_answer.json()


if __name__ == '__main__':
    env_path = Path('.') / '.env'
    load_dotenv(env_path)
    dvmn_auth_token = os.getenv('DVMN_TOKEN')

    while True:
        try:
            pprint(fetch_dvmn_long_polling())
        except requests.exceptions.ReadTimeout:
            print('ReadTimeout')
        except requests.exceptions.ConnectionError:
            print('No Internet connection. Awaiting for internet connection...')
