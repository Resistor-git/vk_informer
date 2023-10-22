# TODO:
#  создать список групп и искать в них
#  прикрутить бота для тг
#  задеплоить

import os
from datetime import datetime
from typing import List, Dict

import requests

from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN: str = os.getenv('ACCESS_TOKEN')
VK_API_VER: str = os.getenv('VK_API_VER')
NUMBER_OF_POSTS_TO_PARSE: int = int(os.getenv('NUMBER_OF_POSTS_TO_PARSE'))


def get_posts(group: str) -> List[Dict]:
    posts_with_keyword = []
    url = f'https://api.vk.com/method/wall.get?domain={group}&count={NUMBER_OF_POSTS_TO_PARSE}&filter=owner' \
          f'&&access_token={ACCESS_TOKEN}&v={VK_API_VER}'
    request = requests.get(url)
    for item in request.json()['response']['items']:
        if 'ComeToSpeak' in item['text']:
            posts_with_keyword.append(item)
    return posts_with_keyword


def print_results(posts: List) -> None:
    found = False
    for post in posts:
        if 'ComeToSpeak' in post['text']:
            post_url: str = f'https://vk.com/wall{post["owner_id"]}_{post["id"]}'
            post_date: datetime = datetime.fromtimestamp(post['date'])
            print(f'Информация о клубе нашлась в посте от {post_date} по ссылке {post_url}')
            found = True
    if not found:
        print(f'В последних {NUMBER_OF_POSTS_TO_PARSE} постах информации об английском клубе не нашлось.')


def main() -> None:
    group: str = 'stremyannaya'
    print_results(get_posts(group))
    print('Парсер закончил свою работу.')


if __name__ == '__main__':
    main()
