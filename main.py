import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv

import requests

from telebot import types
from telebot.async_telebot import AsyncTeleBot

env_path = Path('.') / '.env'
load_dotenv(env_path)
bot = AsyncTeleBot(os.getenv('TELEGRAM_TOKEN'))


# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
async def start_message(_message):
    name = _message.from_user.first_name
    hello_message = f'Привет! {name} \n\nЭтот бот отправит уведомление если урок проверит преподаватель dvmn.org.' \
                    f'\n\n Введите команду /commands и нажмите на кнопку "Начать отслеживание изменений"'
    await bot.send_message(_message.chat.id, hello_message)


@bot.message_handler(commands=['commands'])
async def button_message(_message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Начать отслеживание изменений')
    markup.add(item1)
    await bot.send_message(_message.chat.id, 'Выберите действие из меню ниже:', reply_markup=markup)


@bot.message_handler(content_types='text')
async def message_reply(message):
    if message.text == "Начать отслеживание изменений":
        await asyncio.sleep(1)
        await bot.send_message(message.chat.id, 'Отслеживание проверки задания начато!')
        await bot.send_message(message.chat.id, str(await_answer_from_dvmn()))


def fetch_dvmn_long_polling():
    headers = {
        'Authorization': f'Token {dvmn_auth_token}'
    }
    timestamp_to_request = None
    dvmn_answer_top = None
    final_json = None

    while dvmn_answer_top != 'last_attempt_timestamp':
        dvmn_answer = requests.get('https://dvmn.org/api/long_polling/', params=timestamp_to_request, headers=headers)
        dvmn_answer.raise_for_status()
        answer = dvmn_answer.json()
        if 'last_attempt_timestamp' in answer:
            timestamp_to_request = {'timestamp': str(answer['last_attempt_timestamp'])}
            dvmn_answer_top = 'last_attempt_timestamp'
            final_json = dvmn_answer.json()
        elif 'timestamp_to_request' in dvmn_answer.json():
            timestamp_to_request = {'timestamp': str(answer['timestamp_to_request'])}
    lesson_url = final_json['new_attempts'][0]['lesson_url']
    task_name = final_json['new_attempts'][0]['lesson_title']
    if final_json['new_attempts'][0]['is_negative'] is True:
        return f'Проверена работа: "{task_name}"\n\nК сожалению нашлись ошибки!\n\nСсылка на урок: {lesson_url}'
    else:
        return f'Проверена работа: "{task_name}"\n\nПреподавателю все понравилось, можно приступать к следующему ' \
               f'уроку!\n\nСсылка на урок: {lesson_url}'


def await_answer_from_dvmn():
    while True:
        try:
            return fetch_dvmn_long_polling()
        except requests.exceptions.ReadTimeout:
            print('ReadTimeout')
        except requests.exceptions.ConnectionError:
            print('No Internet connection. Awaiting for internet connection...')


if __name__ == '__main__':
    dvmn_auth_token = os.getenv('DVMN_TOKEN')
    print('Бот запущен, перейдите  телеграм и выполните команду "/start"')
    asyncio.run(bot.polling())
