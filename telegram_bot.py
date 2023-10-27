from datetime import datetime

from telegram import Bot

bot = Bot(token='5824479024:AAHklyshnqVN203CjlBv-arQhlko8JQwLs4')
chat_id = 5897335213


# # def send_message(posts):
# #     if len(posts) > 0:
# #         for post in posts:
# #             post_url: str = f'https://vk.com/wall{post["owner_id"]}_{post["id"]}'
# #             post_date: datetime = datetime.fromtimestamp(post['date'])
# #             text = f'Информация о клубе нашлась в посте от {post_date} по ссылке {post_url}'
# #             bot.send_message(chat_id, text)
#
# def send_message():
#     text = f'Информация о клубе нашлась в посте от '
#     bot.send_message(chat_id, text)
#
#
# send_message()


# kittybot/kittybot.py

text = 'Вам телеграмма!'
# Отправка сообщения
await bot.send_message(chat_id, text)
