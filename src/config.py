from typing import cast
from os import getenv


BOT_TOKEN = cast(str, getenv('BOT_TOKEN'))
DB_USER = cast(str, getenv('DB_USER'))
DB_PASSWORD = cast(str, getenv('DB_PASSWORD'))
DB_HOST = cast(str, getenv('DB_HOST'))
DB_NAME = cast(str, getenv('DB_NAME'))

assert BOT_TOKEN is not None
assert DB_USER is not None
assert DB_PASSWORD is not None
assert DB_HOST is not None
assert DB_NAME is not None
