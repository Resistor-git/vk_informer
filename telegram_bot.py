# TODO:
#  обновиться на последнюю версию python-telegram-bot (будут баги)
#  не отправлять повторные сообщения
#  отправлять несколько результатов одним сообщением
#  отправлять сообщения об ошибках

import os
from datetime import datetime

from dotenv import load_dotenv
from telegram import Bot

load_dotenv()

TELEGRAM_BOT_TOKEN: str = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID: str = os.getenv('TELEGRAM_CHAT_ID')

bot: Bot = Bot(token=TELEGRAM_BOT_TOKEN)


def send_message(posts: list) -> None:
    if len(posts) > 0:
        for post in posts:
            post_url: str = f'https://vk.com/wall{post["owner_id"]}_{post["id"]}'
            post_date: datetime = datetime.fromtimestamp(post['date'])
            text: str = f'Информация о клубе нашлась в посте от {post_date} по ссылке {post_url}'
            bot.send_message(TELEGRAM_CHAT_ID, text)
            print('Отправлено сообщение в телеграм')
    else:
        print('Информации об английских клубах не нашлось.')
