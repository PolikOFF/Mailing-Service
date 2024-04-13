import random


def get_new_password():
    symbol_base = "abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    password_base_list = list(symbol_base)
    random_pass = random.sample(password_base_list, 10)
    new_password = ''.join(random_pass)
    return new_password
