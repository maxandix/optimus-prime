import os
import requests
from requests.exceptions import ReadTimeout, ConnectionError
import telegram
import time

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
DVMN_TOKEN = os.getenv('DVMN_TOKEN')
AUTHORIZATION_HEADER = {'Authorization': f'Token {DVMN_TOKEN}'}


def main():
    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
    timestamp = None
    params = {}
    while True:
        print('new iteration')
        try:
            if timestamp:
                params = {'timestamp': timestamp}
            response = requests.get('https://dvmn.org/api/long_polling/', headers=AUTHORIZATION_HEADER, params=params)
            response.raise_for_status()
            body = response.json()
            if body['status'] == 'timeout':
                timestamp = body['timestamp_to_request']
            elif body['status'] == 'found':
                timestamp = body['last_attempt_timestamp']
                for attempt in body['new_attempts']:
                    text = f'У вас проверили работу "{attempt["lesson_title"]}". Ссылка на урок: https://dvmn.org{attempt["lesson_url"]}'
                    if attempt['is_negative']:
                        text += '\n\nК сожалению в работе нашлись ошибки.'
                    else:
                        text += '\n\nПреподавателю всё понравилось, можно приступать к следующему уроку!'
                    bot.send_message(chat_id=CHAT_ID, text=text)

        except ReadTimeout:
            print('ReadTimeout exception')
            time.sleep(60)
        except ConnectionError:
            print('ConnectionError exception')
            time.sleep(60)


if __name__ == '__main__':
    main()
