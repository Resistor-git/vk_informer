# TODO:
#  убрать куда-то .env ... прописать в .dockerignore?
#  отдельные результаты для каждого keyword, чтобы фильтровать по ним; через словарь {keyword: results}?
#  проверять наличие необходимых ключей и прочее
#  обрабатывать исключения
#  прикрутить workflow (как минимум с проверкой синтаксиса, лучше с тестами)
#  задеплоить (добавить в workflow - CI/CD и всё такое); временно - pythonanywhere
#  прикрутить логгер (см., например homework_bot)
#  аннотация типов

import os
import sys
import time
import logging
from datetime import datetime

import requests
from dotenv import load_dotenv

from telegram_bot import send_message

load_dotenv()
logger = logging.getLogger(__name__)

VK_ACCESS_TOKEN: str = os.getenv('VK_ACCESS_TOKEN')
VK_API_VER: str = os.getenv('VK_API_VER')
NUMBER_OF_POSTS_TO_PARSE: int = int(os.getenv('NUMBER_OF_POSTS_TO_PARSE'))
GROUPS: list[str, ...] = os.getenv('GROUPS').split(',')
KEYWORDS: list[str, ...] = os.getenv('KEYWORDS').split(',')
TELEGRAM_BOT: bool = eval(os.getenv('TELEGRAM_BOT'))
RESTART_INTERVAL: int = int(os.getenv('RESTART_INTERVAL'))


def check_tokens():
    """Check that necessary tokens are provided.
    By default, necessary tokens are:
    VK_ACCESS_TOKEN, VK_API_VER, NUMBER_OF_POSTS_TO_PARSE,
    GROUPS, KEYWORDS, TELEGRAM_BOT, RESTART_INTERVAL
    """
    expected_variables = {
        'VK_ACCESS_TOKEN': VK_ACCESS_TOKEN,
        'VK_API_VER': VK_API_VER,
        'NUMBER_OF_POSTS_TO_PARSE': NUMBER_OF_POSTS_TO_PARSE,
        'GROUPS': GROUPS,
        'KEYWORDS': KEYWORDS,
        'TELEGRAM_BOT': TELEGRAM_BOT,
        'RESTART_INTERVAL': RESTART_INTERVAL  # ломается выше
    }
    for variable in expected_variables:
        if not expected_variables[variable]:
            logger.critical(f'{variable} not found. Program stopped')
            sys.exit()


def get_posts(groups: list[str, ...]) -> list[dict]:
    """
    Gets posts from the vk groups. Filters them by keywords.
    """
    posts_with_keyword = []
    for group in groups:
        url = f'https://api.vk.com/method/wall.get?domain={group}&count={NUMBER_OF_POSTS_TO_PARSE}&filter=owner' \
              f'&&access_token={VK_ACCESS_TOKEN}&v={VK_API_VER}'
        request = requests.get(url)
        for item in request.json()['response']['items']:
            for keyword in KEYWORDS:
                if keyword in item['text']:
                    posts_with_keyword.append(item)
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
    while True:
        if TELEGRAM_BOT:
            send_message(posts=get_posts(GROUPS))
            print('Отправлено сообщение в телеграм.')
        else:
            print_results(get_posts(GROUPS))
            print('Парсер закончил свою работу.')
        time.sleep(RESTART_INTERVAL)


if __name__ == '__main__':
    main()
