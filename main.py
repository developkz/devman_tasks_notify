import os
from pprint import pprint

import requests
from dotenv import load_dotenv
from pathlib import Path


def fetch_dvmn_long_polling():
    headers = {
        'Authorization': f'Token {dvmn_auth_token}'
    }
    timestamp_to_request = []
    dvmn_answer = []

    while True:
        dvmn_answer = requests.get(f'https://dvmn.org/api/long_polling/', params=timestamp_to_request, headers=headers)
        dvmn_answer.raise_for_status()
        if dvmn_answer.ok:
            timestamp_to_request = {'timestamp': str(dvmn_answer.json()['last_attempt_timestamp'])}
        else:
            timestamp_to_request = {'timestamp': str(dvmn_answer.json()['timestamp_to_request'])}


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
