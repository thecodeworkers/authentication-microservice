import random

def generate_salt(lenght=20):
    ALPHABET = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    chars = []

    for index in range(lenght):
        chars.append(random.choice(ALPHABET))

    return "".join(chars)
