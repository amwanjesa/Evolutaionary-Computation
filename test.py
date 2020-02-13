import random


def generate_population(length, size):
    def get_binary_string(length):
        return ''.join((random.choice('01') for i in range(length)))

    return [get_binary_string(length) for i in range(size)]

print(generate_population(10, 5))