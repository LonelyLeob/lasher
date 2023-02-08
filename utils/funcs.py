import random
import string
from datetime import datetime

def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def unix_to_normalize(date):
    return datetime.utcfromtimestamp(date).strftime('%m.%d %H:%M')