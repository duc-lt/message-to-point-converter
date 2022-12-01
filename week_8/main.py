from core.elliptic_curve_operations import add, multiply
from core.point import Point
from random import randrange
from os import path

BASE = 65536
whitespace = ord(' ')
separator = 'UwU'

# Đường cong elliptic NIST P-192
p = 0xfffffffffffffffffffffffffffffffeffffffffffffffff
a = 0xfffffffffffffffffffffffffffffffefffffffffffffffc
b = 0x64210519e59c80e70fa7e9ab72243049feb8deecc146b9b1
g = Point(0x188da80eb03090f67cbf20eb43a18800f4ff0afd82ff1012,
          0x07192b95ffc8da78631011ed6b24cdd573f977a11e794811)


def to_base(n, base=BASE):
    digits = []
    while n:
        digits.insert(0, n % base)
        n //= base
    return digits


def get_group_size(n):
    return len(to_base(n)) - 1


def cipher_to_point(ciphertext):
    x_string, y_string = ciphertext.split(separator)
    x = int(f'0x{x_string}', 16)
    y = int(f'0x{y_string}', 16)
    return Point(x, y)


def generate_keys(keys_file):
    priv_key_b = randrange(1, p)
    pub_key_b = multiply(a, b, p, priv_key_b, g)
    with open(keys_file, 'w') as keys:
        keys.writelines([f'{priv_key_b:x}\n',
                        f'{pub_key_b.get_x():x}{separator}{pub_key_b.get_y():x}\n'])
    keys.close()


def get_keys(keys_file):
    with open(keys_file, 'r') as keys:
        priv_key_b_str, pub_key_b_str = keys.readlines()
        priv_key_b = int(priv_key_b_str, 16)
        pub_key_b = cipher_to_point(pub_key_b_str)
    keys.close()
    return priv_key_b, pub_key_b


def encrypt(filename, pub_key_b):
    with open(filename, 'r+') as file:
        plaintext = file.read()
        ascii_values = list(map(ord, list(plaintext)))
        group_size = get_group_size(p)
        ascii_value_groups = [ascii_values[i:i + group_size]
                              for i in range(0, len(ascii_values), group_size)]

        ascii_value_group_sums = []
        for group in ascii_value_groups:
            sum = 0
            group_len = len(group)
            for i in range(group_len):
                sum += group[group_len - i - 1] * BASE ** i
            ascii_value_group_sums.append(sum)

        if (len(ascii_value_group_sums) % 2 == 1):
            ascii_value_group_sums.append(whitespace)
        message_points = [tuple(ascii_value_group_sums[i:i + 2])
                          for i in range(0, len(ascii_value_group_sums), 2)]

        priv_key_a = randrange(1, p)
        cipher_1 = multiply(a, b, p, priv_key_a, g)
        cipher_2 = [add(a, b, p, Point(point[0], point[1]), multiply(a, b, p, priv_key_a, pub_key_b))
                    for point in message_points]

        file.seek(0)
        file.write(f'{cipher_1.get_x():x}{separator}{cipher_1.get_y():x}\n')
        file.writelines(
            [f'{cipher.get_x():x}{separator}{cipher.get_y():x}\n' for cipher in cipher_2])
        file.truncate()
    file.close()


def decrypt(filename, priv_key_b):
    with open(filename, 'r+') as file:
        first_line, *rest = file.readlines()
        cipher_1 = cipher_to_point(first_line)
        cipher_2 = list(map(cipher_to_point, rest))
        message_points = [add(a, b, p, cipher, multiply(
            a, b, p, -priv_key_b, cipher_1)) for cipher in cipher_2]

        ascii_value_group_sums = []
        for point in message_points:
            ascii_value_group_sums.extend((point.get_x(), point.get_y()))

        ascii_value_groups = []
        for n in ascii_value_group_sums:
            if n == 32:
                continue
            ascii_value_groups.append(to_base(n))

        ascii_values = []
        for group in ascii_value_groups:
            ascii_values.extend(group)

        plaintext = ''.join([chr(ascii_value) for ascii_value in ascii_values])
        file.seek(0)
        file.write(plaintext)
        file.truncate()
    file.close()


def main():
    plain = """National Institute of Technology, Manipur, 795001 (English)

राष्ट्रीय प्रौद्योगिकी संस्थान, मणिपुर, ७९५००१ (Hindi)

প্রযু্তি ন্যাশনাল ইনস্টিটিউট, মণিপুর, ৭৯৫০০১ (Bengali)

தேசிய தொழில்நுட்பக்‌ கழகம்‌, மணிப்பூர்‌, ௭௯௫௦௦௧ (Tamil)

技術総合研究所，マニプール, 七九五零零一 (Japanese)

技術研究院，曼尼普爾邦, 柒玖伍零零壹  (Chinese)
"""

    keys_file = 'keys.txt'
    if not path.exists(keys_file):
        generate_keys(keys_file)
    priv_key_b, pub_key_b = get_keys(keys_file)

    # khi nào cần decrypt thì comment dòng 140 -> 143, tắt comment dòng 144
    # encrypt thì làm ngược lại
    text_file_to_encrypt = 'test.txt'
    with open(text_file_to_encrypt, 'w') as text:
        text.write(plain)
    text.close()
    encrypt(text_file_to_encrypt, pub_key_b)
    # decrypt(text_file_to_encrypt, priv_key_b)


if __name__ == '__main__':
    main()
