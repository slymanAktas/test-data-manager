from random import randint


def generate_random_number(length):
    range_start = 10 ** (length - 1)
    range_end = (10 ** length) - 1
    random_number = randint(range_start, range_end)

    return random_number

