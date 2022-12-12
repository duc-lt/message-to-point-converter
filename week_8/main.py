from time import time
from core.elliptic_curve_operations import add, is_on_curve, multiply
from core.point import Point
from random import randrange
import os
from datetime import timedelta
from math import log
from multiprocessing import Pool


BASE = 65536
WHITESPACE = ord(' ')
SEPARATOR = 'g'
PRIV_KEY_PATH = 'priv_key'
PUB_KEY_PATH = 'pub_key'

# Đường cong elliptic NIST P-192
p = 0xfffffffffffffffffffffffffffffffeffffffffffffffff
a = 0xfffffffffffffffffffffffffffffffefffffffffffffffc
b = 0x64210519e59c80e70fa7e9ab72243049feb8deecc146b9b1
g = Point(0x188da80eb03090f67cbf20eb43a18800f4ff0afd82ff1012,
          0x07192b95ffc8da78631011ed6b24cdd573f977a11e794811)

# Đường cong tự tạo
# a = 789527267482250023533321246187221928470553233573
# b = 631385804378468242810549727762799065593611977755
# p = 820692272049904754268558404823550666902242581027
# g = Point(567897938643847309026511906264475250815917655751,
#           389820891852823519475027830793533803851547699598)

GROUP_SIZE = int(log(p, BASE)) - 1
KEY_LENGTH = int(log(p, 2))


def to_base(n, base=BASE):
    digits = []
    while n:
        digits.insert(0, n % base)
        n //= base
    return digits


def cipher_to_point(ciphertext):
    x_string, y_string = ciphertext.split(SEPARATOR)
    x, y = int(x_string, 16), int(y_string, 16)
    return Point(x, y)


def generate_keys():
    priv_key_b = randrange(1, p)
    pub_key_b = multiply(a, b, p, priv_key_b, g)
    with open(PRIV_KEY_PATH, 'w') as priv_file, open(PUB_KEY_PATH, 'w') as pub_file:
        priv_file.write(f'{priv_key_b:x}')
        pub_file.write(
            f'{pub_key_b.get_x():x}{SEPARATOR}{pub_key_b.get_y():x}')


def get_keys():
    with open(PRIV_KEY_PATH, 'r') as priv_file, open(PUB_KEY_PATH, 'r') as pub_file:
        priv_key_b = int(priv_file.readline(), 16)
        pub_key_b = cipher_to_point(pub_file.readline())
        return priv_key_b, pub_key_b


def encrypt(filename, pub_key_b):
    def read_in_chunks(file_object, chunk_size=512):
        while True:
            data = file_object.read(chunk_size)
            if not data:
                break
            yield data

    with open(filename, 'r', encoding='utf-8') as plain_file, open(f'{filename}.enc', 'w', encoding='utf-8') as cipher_file:
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


def decrypt(filename, priv_key_b):
    with open(filename, 'r', encoding='utf-8') as cipher_file, open(filename.replace('.enc', '.dec'), 'w', encoding='utf-8') as plain_file:
        cipher_lines = cipher_file.read().splitlines()
        cipher_1, *cipher_2 = list(map(cipher_to_point, cipher_lines))
        neg_shared_key = multiply(a, b, p, -priv_key_b, cipher_1)
        ascii_values = []
        for cipher in cipher_2:
            message_point = add(a, b, p, cipher, neg_shared_key)
            x, y = message_point.get_x(), message_point.get_y()
            ascii_values.extend(to_base(x) + to_base(y))
        plaintext = ''.join(list(map(chr, ascii_values)))
        plain_file.seek(0)
        plain_file.write(plaintext)
        plain_file.truncate()


def main():
    plain = """National Institute of Technology, Manipur, 795001 (English)

राष्ट्रीय प्रौद्योगिकी संस्थान, मणिपुर, ७९५००१ (Hindi)

প্রযু্তি ন্যাশনাল ইনস্টিটিউট, মণিপুর, ৭৯৫০০১ (Bengali)

தேசிய தொழில்நுட்பக்‌ கழகம்‌, மணிப்பூர்‌, ௭௯௫௦௦௧ (Tamil)

技術総合研究所，マニプール, 七九五零零一 (Japanese)

技術研究院，曼尼普爾邦, 柒玖伍零零壹  (Chinese)
"""

    if not (os.path.exists(PRIV_KEY_PATH) and os.path.exists(PUB_KEY_PATH)):
        generate_keys()
    priv_key_b, pub_key_b = get_keys()

    # khi nào cần decrypt thì comment dòng 140 -> 143, tắt comment dòng 144
    # encrypt thì làm ngược lại
    start_time = time()
    directory_to_encrypt = os.path.join(os.getcwd(), 'nested')
    # text_files = []
    for root, _, files in os.walk(directory_to_encrypt):
        if len(files) == 0:
            continue
        text_files = [os.path.join(root, text_file) for text_file in files]
        # with Pool(2) as pool:
        #     pool.starmap_async(encrypt, [(text_file, pub_key_b)
        #                  for text_file in text_files])
        #     pool.starmap_async(decrypt, [(text_file, priv_key_b)
        #                  for text_file in text_files])
        for text_file_to_encrypt in text_files:
            encrypt(text_file_to_encrypt, pub_key_b)
        # decrypt(text_file_to_encrypt + '.enc', priv_key_b)
    # encrypt(text_file_to_encrypt, pub_key_b)
    # decrypt(f'{text_file_to_encrypt}.enc', priv_key_b)
    print(f'time: {str(timedelta(seconds=time() - start_time))}')


if __name__ == '__main__':
    main()
