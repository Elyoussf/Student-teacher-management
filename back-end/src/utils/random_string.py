

import random 

import string

def generate_random_string(l):
    s = string.ascii_letters + string.digits
    return "".join([random.choice(s) for _ in range(l)])
