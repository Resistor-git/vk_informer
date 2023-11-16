# TODO:
#  обновиться на последнюю версию python-telegram-bot (будут баги)
#  не отправлять повторные сообщения
#  отправлять сообщения об ошибках

import os
from datetime import datetime

from dotenv import load_dotenv
from telegram import Bot

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

bot = Bot(token=TELEGRAM_BOT_TOKEN)


def send_message(posts):
    if len(posts) > 0:
        for post in posts:
            post_url: str = f'https://vk.com/wall{post["owner_id"]}_{post["id"]}'
            post_date: datetime = datetime.fromtimestamp(post['date'])
            text = f'Информация о клубе нашлась в посте от {post_date} по ссылке {post_url}'
            bot.send_message(TELEGRAM_CHAT_ID, text)
