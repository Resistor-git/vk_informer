# vk_informer
Informs about new events in VK groups of Saint-Petersburg libraries

## work in progress...

## Usage
Create `.env in the` root and fill it with values. As an example use `.env.example`:

* `ACCESS_TOKEN` - token of your VK app.
* `NUMBER_OF_POSTS_TO_PARSE` - amount of posts to search in, starting from the last published.
* `VK_API_VER` - version of VK api, better keep the same as in `.env.example`.
* `GROUPS` - name of the group in the url, for example: https://vk.com/british_book_centre, "british_book_centre" is the group name.
* `KEYWORDS` - words or phrases to search for, divided by commas. If you need to search for a phrase with spaces, then quotation marks are obligatory.

Launch `main.py`. For Windows it would be `py main.py` in terminal/cmd.

## Author
Resistor, https://github.com/Resistor-git/