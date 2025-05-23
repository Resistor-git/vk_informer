# vk_informer
Informs about new events in VK groups of Saint-Petersburg libraries.

## work in progress...


## Usage
Create `.env in the` root and fill it with values. As an example use `.env.example`:

* `VK_ACCESS_TOKEN` - token of your VK app, aka "Сервисный ключ доступа".
* `NUMBER_OF_POSTS_TO_PARSE` - amount of posts to search in, starting from the last published.
* `VK_API_VER` - version of VK api, better keep the same as in `.env.example`.
* `GROUPS` - name of the group in the url, for example: https://vk.com/british_book_centre, "british_book_centre" is the group name.
* `KEYWORDS` - words or phrases to search for, divided by commas.
* `TELEGRAM_BOT` - 'True' to send messages via the telegram bot, otherwise 'False'.
* `TELEGRAM_BOT_TOKEN` - token of your telegram bot.
* `TELEGRAM_CHAT_ID` - id of the telegram chat to send messages to.
* `TELEGRAM_ADMIN_CHAT_ID` - id of the telegram chat for maintenance messages.
* `RESTART_INTERVAL` - time in seconds between program calls.

_Note: If you are planning to use Docker, do not use quotation marks in .env._\
_Remember: in order to get messages from any telegram bot you should first send `/start` to it._

Launch `main.py`. For Windows it would be `py main.py` in terminal/cmd.

## Telegram messages
If you want to get messages in telegram:
* Set `TELEGRAM_BOT` in .env to `True`
* Add `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` and `RESTART_INTERVAL` to .env

## Known bugs
* Empty value for `GROUPS` in .env is not handled properly by check_tokens(). Probable fix: get rid of .env and use configparser.
* KeyError exception for situations with wrong response is not logged.

## Author
Resistor, https://github.com/Resistor-git/