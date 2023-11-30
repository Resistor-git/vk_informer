# TODO:
#  докер некорректно читает кавычки - переехать на configparser
#  отдельные результаты для каждого keyword, чтобы фильтровать по ним; через словарь {keyword: results}?
#  проверять наличие необходимых ключей и прочее
#  обрабатывать исключения
#  прикрутить workflow (как минимум с проверкой синтаксиса, лучше с тестами)
#  создать конфиг для логгера
#  создать volume и писать логи туда

import os
import sys
import time
import logging
from datetime import datetime

import requests
from dotenv import load_dotenv
from telegram_bot import send_tg_message, check_posts_sent, send_error_message

load_dotenv()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s -- %(name)s -- %(message)s')

file_handler = logging.FileHandler('logs/vk_informer.log')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

VK_ACCESS_TOKEN: str = os.getenv('VK_ACCESS_TOKEN')
VK_API_VER: str = os.getenv('VK_API_VER')
NUMBER_OF_POSTS_TO_PARSE: str = os.getenv('NUMBER_OF_POSTS_TO_PARSE')
GROUPS: list[str, ...] = os.getenv('GROUPS').split(',')
KEYWORDS: list[str, ...] = os.getenv('KEYWORDS').split(',')
TELEGRAM_BOT: bool = eval(os.getenv('TELEGRAM_BOT'))
if TELEGRAM_BOT:
    try:
        TELEGRAM_BOT_TOKEN: str = os.getenv('TELEGRAM_BOT_TOKEN')
        TELEGRAM_CHAT_ID: int = int(os.getenv('TELEGRAM_CHAT_ID'))
        TELEGRAM_ADMIN_CHAT_ID: int = int(os.getenv('TELEGRAM_ADMIN_CHAT_ID'))
        RESTART_INTERVAL: int = int(os.getenv('RESTART_INTERVAL'))
    except ValueError:
        logger.critical('Unexpected data in .env')
        sys.exit()


def check_tokens():
    """Check that necessary tokens are provided.
    """
    if TELEGRAM_BOT:
        expected_variables: dict = {
            'VK_ACCESS_TOKEN': VK_ACCESS_TOKEN,
            'VK_API_VER': VK_API_VER,
            'GROUPS': GROUPS,
            'KEYWORDS': KEYWORDS,
            'NUMBER_OF_POSTS_TO_PARSE': NUMBER_OF_POSTS_TO_PARSE,
            'TELEGRAM_BOT': TELEGRAM_BOT,
            'TELEGRAM_BOT_TOKEN': TELEGRAM_BOT_TOKEN,
            'TELEGRAM_CHAT_ID': TELEGRAM_CHAT_ID,
            'TELEGRAM_ADMIN_CHAT_ID': TELEGRAM_ADMIN_CHAT_ID,
            'RESTART_INTERVAL': RESTART_INTERVAL
        }
    else:
        expected_variables: dict = {
            'VK_ACCESS_TOKEN': VK_ACCESS_TOKEN,
            'VK_API_VER': VK_API_VER,
            'NUMBER_OF_POSTS_TO_PARSE': NUMBER_OF_POSTS_TO_PARSE,
            'GROUPS': GROUPS,
            'KEYWORDS': KEYWORDS,
        }
    for variable in expected_variables:
        if not expected_variables[variable]:
            logger.critical(f'{variable} not found. Program stopped')
            sys.exit()


def get_posts(groups: list[str, ...]) -> list[dict]:
    """
    Gets posts from the vk groups. Filters them by keywords.
    """
    posts_with_keyword: list = []
    for group in groups:
        url = f'https://api.vk.com/method/wall.get?domain={group}&count={NUMBER_OF_POSTS_TO_PARSE}&filter=owner' \
              f'&&access_token={VK_ACCESS_TOKEN}&v={VK_API_VER}'
        request = requests.get(url)
        try:
            for post in request.json()['response']['items']:
                for keyword in KEYWORDS:
                    if keyword in post['text']:
                        posts_with_keyword.append(post)
        except KeyError:
            logger.exception(f'Something wrong with request: {request.json()}')            
    return posts_with_keyword


def print_results(posts: list) -> None:
    """
    Prints the formatted results of search in terminal.
    """
    if len(posts) < 1:
        print(f'В последних {NUMBER_OF_POSTS_TO_PARSE} постах информации об английских клубах не нашлось.')
        return
    for post in posts:
        post_url: str = f'https://vk.com/wall{post["owner_id"]}_{post["id"]}'
        post_date: datetime = datetime.fromtimestamp(post['date'])
        print(f'Информация о клубе нашлась в посте от {post_date} по ссылке {post_url}')


def main() -> None:
    try:
        check_tokens()
        if TELEGRAM_BOT:
            while True:
                send_tg_message(posts=get_posts(GROUPS))
                check_posts_sent()
                logger.info(
                    f'{datetime.now().strftime("%Y.%m.%d %H:%M",)}'
                    f' Парсер отработал цикл.'
                )
                time.sleep(RESTART_INTERVAL)
        else:
            print_results(get_posts(GROUPS))
            logger.info(
                f'{datetime.now().strftime("%Y.%m.%d %H:%M",)}'
                f' Парсер закончил свою работу.'
            )
    except Exception:
        logger.exception('Unexpected Exception')
        if TELEGRAM_BOT:
            send_error_message('Unexpected Exception')


if __name__ == '__main__':
    main()
