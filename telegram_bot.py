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

MAX_LEN = 1_000
posts_sent: set[int, ...] = set()
bot: Bot = Bot(token=TELEGRAM_BOT_TOKEN)


def send_message(posts: list[dict, ...]) -> None:
    """
    Sends a message for each post with a keyword.
    """
    if len(posts) > 0:
        for post in posts:
            post_url: str = f'https://vk.com/wall{post["owner_id"]}_{post["id"]}'
            post_date: datetime = datetime.fromtimestamp(post['date'])
            text: str = f'Информация о клубе нашлась в посте от {post_date} по ссылке {post_url}'
            if post['id'] not in posts_sent:
                posts_sent.add(post['id'])
                bot.send_message(TELEGRAM_CHAT_ID, text)
                print('Отправлено сообщение в телеграм')
    else:
        print('Информации об английских клубах не нашлось.')


def clear_posts_sent() -> None:
    """
    Clears the list of posts which have been sent by send_message()
    if it achieved max length.
    Should save some memory.
    """
    if len(posts_sent) > MAX_LEN:
        posts_sent.clear()
        print(f'Список отправленных постов достиг максимальной длины {MAX_LEN} '
              f'и был очищен')
