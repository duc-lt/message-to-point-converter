from time import time
from core.elliptic_curve_operations import add, multiply
from core.point import Point
from random import randrange
import base64
from datetime import timedelta
from math import log
from itertools import islice
import os

BASE = 65536
WHITESPACE = ord(' ')
SEPARATOR = 'g'
PRIV_KEY_PATH = 'D:\message-to-point-converter\priv_key'
PUB_KEY_PATH = 'D:\message-to-point-converter\pub_key'

# NIST P-192
# p = 0xfffffffffffffffffffffffffffffffeffffffffffffffff
# a = 0xfffffffffffffffffffffffffffffffefffffffffffffffc
# b = 0x64210519e59c80e70fa7e9ab72243049feb8deecc146b9b1
# g = Point(0x188da80eb03090f67cbf20eb43a18800f4ff0afd82ff1012,
#           0x07192b95ffc8da78631011ed6b24cdd573f977a11e794811)

# NIST P-256
p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
a = 0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc
b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
g = Point(0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296,
          0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5)

# brainpoolP192t1
# p = 0xc302f41d932a36cda7a3463093d18db78fce476de1a86297
# a = 0xc302f41d932a36cda7a3463093d18db78fce476de1a86294
# b = 0x13d56ffaec78681e68f9deb43b35bec2fb68542e27897b79
# g = Point(0x3ae9e58c82f63c30282e1fe7bbf43fa72c446af6f4618129,
#           0x97e2c5667c2223a902ab5ca449d0084b7e5b3de7ccc01c9)

# ANSI prime192v3
# p = 0xfffffffffffffffffffffffffffffffeffffffffffffffff
# a = 0xfffffffffffffffffffffffffffffffefffffffffffffffc
# b = 0x22123dc2395a05caa7423daeccc94760a7d462256bd56916
# g = Point(0x7d29778100c65a1da1783716588dce2b8b4aee8e228f1896,
#           0x38a90f22637337334b49dcb66a6dc8f9978aca7648a943b0)

# ANSI prime256v1
# p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
# a = 0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc
# b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
# g = Point(0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296,
#           0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5)

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
    def read_in_chunks(file_object, chunk_size=1024):
        while True:
            data = file_object.read(chunk_size)
            if not data:
                break
            yield data
    real_name = os.path.split(filename)[1]
    with open(filename, 'rb') as plain_file, open(f'{real_name}.enc', 'wb') as cipher_file:
        priv_key_a = randrange(1, p)
        cipher_1 = multiply(a, b, p, priv_key_a, g)
        shared_key = multiply(a, b, p, priv_key_a, pub_key_b)
        cipher_file.write(
            b'%x%b%x\n' % (cipher_1.get_x(),
                           SEPARATOR.encode(),
                           cipher_1.get_y()))

        for text in read_in_chunks(plain_file):
            b64text = base64.b64encode(text).decode()
            ascii_values = list(map(ord, b64text))
            ascii_value_group_sums = []

            for i in range(0, len(ascii_values), GROUP_SIZE):
                group = ascii_values[i:i + GROUP_SIZE][::-1]
                coordinate = sum(
                    [e * BASE ** j for j, e in enumerate(group)])
                ascii_value_group_sums.append(coordinate)

            if len(ascii_value_group_sums) % 2 == 1:
                ascii_value_group_sums.append(WHITESPACE)

            for i in range(0, len(ascii_value_group_sums), 2):
                point = ascii_value_group_sums[i:i + 2]
                cipher_point = add(a, b, p, Point(
                    point[0], point[1]), shared_key)
                cipher_file.write(
                    b'%x%b%x\n' % (cipher_point.get_x(),
                                   SEPARATOR.encode(),
                                   cipher_point.get_y()))


def decrypt(filename, priv_key_b):
    def read_in_lines(file_object, lines_count=128):
        while True:
            data = list(islice(file_object, lines_count))
            if not data:
                break
            yield data

    with open(filename, 'rb') as cipher_file, open(filename.replace('.enc', ''), 'wb') as plain_file:
        cipher_1 = cipher_to_point(cipher_file.readline().decode())
        neg_shared_key = multiply(a, b, p, -priv_key_b, cipher_1)
        plaintext = ''
        for lines in read_in_lines(cipher_file):
            cipher_2 = list(map(cipher_to_point, [line.decode() for line in lines]))
            for cipher in cipher_2:
                message_point = add(a, b, p, cipher, neg_shared_key)
                x, y = message_point.get_x(), message_point.get_y()
                plaintext += ''.join(list(map(chr, to_base(x, BASE) + to_base(y, BASE))))
        b64lines = plaintext.split(' ')
        lines = list(map(base64.b64decode, b64lines))
        for line in lines:
            plain_file.write(line)


def main():
    plain = """National Institute of Technology, Manipur, 795001 (English)

राष्ट्रीय प्रौद्योगिकी संस्थान, मणिपुर, ७९५००१ (Hindi)

প্রযু্তি ন্যাশনাল ইনস্টিটিউট, মণিপুর, ৭৯৫০০১ (Bengali)

தேசிய தொழில்நுட்பக்‌ கழகம்‌, மணிப்பூர்‌, ௭௯௫௦௦௧ (Tamil)

技術総合研究所，マニプール, 七九五零零一 (Japanese)

技術研究院，曼尼普爾邦, 柒玖伍零零壹  (Chinese)
"""

    # if not (os.path.exists(PRIV_KEY_PATH) and os.path.exists(PUB_KEY_PATH)):
    #     generate_keys()
    # generate_keys()

    # khi nào cần decrypt thì comment dòng 140 -> 143, tắt comment dòng 144
    # encrypt thì làm ngược lại
    start_time = time()
    # text_file_to_encrypt = "test.txt"
    text_file_to_encrypt = "D:\Downloads\Danh-gia_Mau_Bao-cao-tieu-luan-cuoi-ky.pdf"
    # directory_to_encrypt = os.path.join(os.getcwd(), 'nested')
    # for root, _, files in os.walk(directory_to_encrypt):
    #     if len(files) == 0:
    #         continue
    #     text_files = [os.path.join(root, text_file) for text_file in files]
    # with Pool(2) as pool:
    #     pool.starmap_async(encrypt, [(text_file, pub_key_b)
    #                  for text_file in text_files])
    #     pool.starmap_async(decrypt, [(text_file, priv_key_b)
    #                  for text_file in text_files])
    # for text_file_to_encrypt in text_files:
    #     encrypt(text_file_to_encrypt, pub_key_b)
    # encrypt(text_file_to_encrypt, pub_key_b)
    # decrypt('test.txt.enc', priv_key_b)
    decrypt("D:\message-to-point-converter\week_8\Danh-gia_Mau_Bao-cao-tieu-luan-cuoi-ky.pdf.enc", priv_key_b)
    print(f'time: {str(timedelta(seconds=time() - start_time))}')


if __name__ == '__main__':
    main()
