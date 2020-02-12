import os
import requests
from requests.exceptions import ReadTimeout, ConnectionError
import telegram
import time
import logging

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
DVMN_TOKEN = os.getenv('DVMN_TOKEN')
AUTHORIZATION_HEADER = {'Authorization': f'Token {DVMN_TOKEN}'}


class TelegramLogsHandler(logging.Handler):
    def __init__(self, token, chat_id):
        super().__init__()
        self.bot = telegram.Bot(token=token)
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


def main():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(TELEGRAM_BOT_TOKEN, CHAT_ID))

    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
    logger.warning("I've woken up!")
    timestamp = None
    params = {}
    while True:
        try:
            logger.debug('new iteration')
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
            logger.exception('Произошёл ReadTimeout', exc_info=False)
            time.sleep(60)
        except ConnectionError:
            logger.exception('Произошёл ConnectionError', exc_info=False)
            time.sleep(60)
        except Exception:
            logger.exception('Шеф, усё пропало!', exc_info=True)
            time.sleep(60)


if __name__ == '__main__':
    main()
