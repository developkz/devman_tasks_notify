# Статус проверки домашнего задания Devman

Бот подключается к [API Девмана](https://dvmn.org/api/docs/) и с помощью механизма long_polling
ждет ответ от сервера в бесконечном цикле. Когда скрипт получает ответ от сервера Девмана, ответ форматируется 
и отправляется в телеграм бота. 