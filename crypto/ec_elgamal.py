from itertools import islice
from math import log
from random import randrange
from core.elliptic_curve_operations import add, multiply
from core.int_operations import to_base
from core.point import Point

BASE = 65536
WHITESPACE = ord(' ')
SEPARATOR = 'g'


def cipher_to_point(ciphertext):
    x_string, y_string = ciphertext.split(SEPARATOR)
    x, y = int(x_string, 16), int(y_string, 16)
    return Point(x, y)


def generate_keys(curve_type, p, a, b, g):
    priv_key_b = randrange(1, p)
    pub_key_b = multiply(a, b, p, priv_key_b, g)
    with open(f'priv_key_{curve_type}', 'w') as priv_file, open(f'pub_key_{curve_type}', 'w') as pub_file:
        priv_file.write(f'{priv_key_b:x}')
        pub_file.write(
            f'{pub_key_b.get_x():x}{SEPARATOR}{pub_key_b.get_y():x}')


def get_keys(curve_type):
    with open(f'priv_key_{curve_type}', 'r') as priv_file, open(f'pub_key_{curve_type}', 'r') as pub_file:
        priv_key_b = int(priv_file.readline(), 16)
        pub_key_b = cipher_to_point(pub_file.readline())
        return priv_key_b, pub_key_b


def encrypt(p, a, b, g, src, dest, pub_key_b):
    def read_in_chunks(file_object, chunk_size=512):
        while True:
            data = file_object.read(chunk_size)
            if not data:
                break
            yield data
    
    GROUP_SIZE = int(log(p, BASE))

    with open(src, 'r', encoding='utf-8') as plain_file, open(dest, 'w' ,encoding='utf-8') as cipher_file:
        priv_key_a = randrange(1, p)
        cipher_1 = multiply(a, b, p, priv_key_a, g)
        shared_key = multiply(a, b, p, priv_key_a, pub_key_b)
        cipher_file.write(
            f'{cipher_1.get_x():x}{SEPARATOR}{cipher_1.get_y():x}\n')

        for text in read_in_chunks(plain_file):
            ascii_values = list(map(ord, list(text)))
            ascii_value_group_sums = []

            for i in range(0, len(ascii_values), GROUP_SIZE):
                group = ascii_values[i:i + GROUP_SIZE][::-1]
                coordinate = sum(
                    [e * BASE ** j for j, e in enumerate(group)])
                ascii_value_group_sums.append(coordinate)

            if (len(ascii_value_group_sums) % 2 == 1):
                ascii_value_group_sums.append(WHITESPACE)

            for i in range(0, len(ascii_value_group_sums), 2):
                point = ascii_value_group_sums[i:i + 2]
                cipher_point = add(a, b, p, Point(
                    point[0], point[1]), shared_key)
                cipher_file.write(
                    f'{cipher_point.get_x():x}{SEPARATOR}{cipher_point.get_y():x}\n')


def decrypt(p, a, b, src, dest, priv_key_b):
    def read_in_chunks(file_object, chunk_size=512):
        while True:
            data = list(islice(file_object, chunk_size))
            if not data:
                break
            yield data

    with open(src, 'r', encoding='utf-8') as cipher_file, open(dest, 'w', encoding='utf-8') as plain_file:
        cipher_1 = cipher_to_point(cipher_file.readline())
        neg_shared_key = multiply(a, b, p, -priv_key_b, cipher_1)
        for lines in read_in_chunks(cipher_file):
            cipher_2 = list(map(cipher_to_point, lines))
            ascii_values = []
            for cipher in cipher_2:
                message_point = add(a, b, p, cipher, neg_shared_key)
                x, y = message_point.get_x(), message_point.get_y()
                ascii_values.extend(to_base(x, BASE) + to_base(y, BASE))
            plaintext = ''.join(list(map(chr, ascii_values)))
            plain_file.write(plaintext)
