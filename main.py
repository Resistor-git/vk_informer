import os
import requests
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN: str = os.getenv('ACCESS_TOKEN')
VK_API_VER: str = os.getenv('VK_API_VER')
NUMBER_OF_POSTS_TO_PARSE: int = int(os.getenv('NUMBER_OF_POSTS_TO_PARSE'))

# group = 'stremyannaya'
# domain = f'https://api.vk.com/method/wall.get?domain={group}&count=1&filter=owner&&access_token={ACCESS_TOKEN}&v=5.131'

# req = requests.get(domain)
# print(req.json())


def get_posts(group: str) -> list:
    url = f'https://api.vk.com/method/wall.get?domain={group}&count={NUMBER_OF_POSTS_TO_PARSE}&filter=owner' \
          f'&&access_token={ACCESS_TOKEN}&v={VK_API_VER}'
    request = requests.get(url)
    # print(request.json()['response']['items'])
    for item in request.json()['response']['items']:
        if 'ComeToSpeak' in item['text']:
            post_url = f'https://vk.com/wall{item["owner_id"]}_{item["id"]}'
            print(f'нашлось в посте по ссылке {post_url}')
    # print(f'В последних {NUMBER_OF_POSTS_TO_PARSE} объявлениях об английском клубе не нашлось.')


def main():
    group = 'stremyannaya'
    get_posts(group)


if __name__ == '__main__':
    main()
