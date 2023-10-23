# TODO:
#  создать список групп и искать в них
#  прикрутить бота для тг
#  задеплоить

import os
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN: str = os.getenv('ACCESS_TOKEN')
VK_API_VER: str = os.getenv('VK_API_VER')
NUMBER_OF_POSTS_TO_PARSE: int = int(os.getenv('NUMBER_OF_POSTS_TO_PARSE'))
GROUPS: list[str, ...] = os.getenv('GROUPS').split(',')
KEYWORDS: list[str, ...] = os.getenv('KEYWORDS').split(',')


def get_posts(groups: list[str, ...]) -> list[dict]:
    """
    Gets posts from the vk groups. Filters them by keywords.
    """
    posts_with_keyword = []
    for group in groups:
        url = f'https://api.vk.com/method/wall.get?domain={group}&count={NUMBER_OF_POSTS_TO_PARSE}&filter=owner' \
              f'&&access_token={ACCESS_TOKEN}&v={VK_API_VER}'
        request = requests.get(url)
        for item in request.json()['response']['items']:
            for keyword in KEYWORDS:
                if keyword in item['text']:
                    posts_with_keyword.append(item)
    return posts_with_keyword


def print_results(posts: list) -> None:
    """
    Prints the formatted results of search
    """
    found = False
    for post in posts:
        post_url: str = f'https://vk.com/wall{post["owner_id"]}_{post["id"]}'
        post_date: datetime = datetime.fromtimestamp(post['date'])
        print(f'Информация о клубе нашлась в посте от {post_date} по ссылке {post_url}')
        found = True
    if not found:
        print(f'В последних {NUMBER_OF_POSTS_TO_PARSE} постах информации об английских клубах не нашлось.')


def main() -> None:
    print_results(get_posts(GROUPS))
    print('Парсер закончил свою работу.')


if __name__ == '__main__':
    main()
