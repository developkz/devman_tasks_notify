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

    while True:
        dvmn_answer = requests.get(f'https://dvmn.org/api/long_polling/', params=timestamp_to_request, headers=headers)
        dvmn_answer.raise_for_status()
        answer = dvmn_answer.json()
        if 'last_attempt_timestamp' in answer:
            timestamp_to_request = {'timestamp': str(answer['last_attempt_timestamp'])}
        elif 'timestamp_to_request' in dvmn_answer.json():
            timestamp_to_request = {'timestamp': str(answer['timestamp_to_request'])}



'''
Good Answer:

{'last_attempt_timestamp': 1652811311.116004,
 'new_attempts': [{'is_negative': True,
                   'lesson_title': 'Отправляем уведомления о проверке работ',
                   'lesson_url': 'https://dvmn.org/modules/chat-bots/lesson/devman-bot/',
                   'submitted_at': '2022-05-17T21:15:11.116004+03:00',
                   'timestamp': 1652811311.116004}],
 'request_query': [],
 'status': 'found'}
 
 
 Timeout Answer:
 {'request_query': [],
 'status': 'timeout',
 'timestamp_to_request': 1652811930.771743}
 

'''





if __name__ == '__main__':
    env_path = Path('.') / '.env'
    load_dotenv(env_path)
    dvmn_auth_token = os.getenv('DVMN_TOKEN')

    while True:
        try:
            print(fetch_dvmn_long_polling())
        except requests.exceptions.ReadTimeout:
            print('ReadTimeout')
        except requests.exceptions.ConnectionError:
            print('No Internet connection. Awaiting for internet connection...')
