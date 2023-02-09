import random
import string
from datetime import datetime
import time

def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def unix_to_normalize(unix):
    return datetime.utcfromtimestamp(unix).strftime('%d.%m %H:%M')

def normalize_to_unix(value):
    try:
        value += f" {datetime.now().year}/00"
        obj = datetime.strptime(value, "%d.%m %H:%M %Y/%S")
        return int(time.mktime(obj.timetuple()))
    except ValueError as e:
        print(f'Вызвана ошибка {e}')