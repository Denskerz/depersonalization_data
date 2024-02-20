import os
import re
import hashlib
import logging
import time
import sys
from re import Match
from dotenv import load_dotenv
from pathlib import Path


def time_ms():
    return round(time.time() * 1000)


def hashing(line: str, personal_data: str) -> str | None:
    coincidence: Match[str] | None = re.search(personal_data, line)
    if coincidence is not None:
        tmp = hashlib.md5(str(coincidence).encode())
        return tmp.hexdigest()
    return None


file_log = logging.FileHandler('Log.log')
console_out = logging.StreamHandler()
logging.basicConfig(level=logging.DEBUG, handlers=(file_log, console_out),
                    format="[%(asctime)s | %(levelname)s]: %(message)s", datefmt='%m.%d.%Y ~ %H:%M:%S')

ROOT_PATH = Path(__file__).resolve().parents[2]
DOTENV_PATH = os.path.join(ROOT_PATH, ".env")
load_dotenv(dotenv_path=DOTENV_PATH)

pattern_list: list[str] = os.getenv('ATTRIBUTES').split('\n')
REGEXP = os.getenv('REGEXP')

for i in range(len(pattern_list)):
    pattern_list[i] = re.sub(pattern='EXAMPLE', repl=pattern_list[i], string=REGEXP)

source = []
listdir = os.listdir(f'{ROOT_PATH}/input_data')
