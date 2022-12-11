import base64
from random import randrange
from time import time
import tkinter
from tkinter import *
from tkinter import messagebox
import os
from tkinter import filedialog
import openpyxl

from core.elliptic_curve_operations import add, multiply
from core.point import Point
from random import randrange
from os import path

BASE = 65536
whitespace = ord(' ')
separator = 'UwU'

def encript_file():
    try:
        start_time = time()
        a = int(a_entry.get())
        b = int(b_entry.get())
        p = int(p_entry.get())
        g = Point(int(x_entry.get()), int(y_entry.get()))

        file = open(import_file_entry.get(), 'r', encoding='utf-8')
        plaintext = file.read()

        keys_file = 'keys.txt'
        if not path.exists(keys_file):
            generate_keys(a, b, p, keys_file, g)
        priv_key_b, pub_key_b = get_keys(keys_file)

        text_file_to_encrypt = browse_folder_entry.get() + '/test.txt'
        with open(text_file_to_encrypt, 'w', encoding='utf-8') as text:
            text.write(plaintext)
        text.close()
        encrypt(a, b, p, text_file_to_encrypt, pub_key_b, g)
        encript_time = time() - start_time
        messagebox.showinfo("Message", f"Convert file successfully!!! \nConvert time: {encript_time}")
    except Exception as e:
        messagebox.showinfo("Error", e)

def upload_file():
    file_location = filedialog.askopenfilename()
    import_file_location.set(file_location)

def browse_folder():
    global folder_path
    foldername = filedialog.askdirectory()
    browse_folder_path.set(foldername)


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


def generate_keys(a, b, p, keys_file, g):
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


def encrypt(a, b, p, filename, pub_key_b, g):
    with open(filename, 'r+', encoding='utf-8') as file:
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


# def decrypt(filename, priv_key_b):
#     with open(filename, 'r+') as file:
#         first_line, *rest = file.readlines()
#         cipher_1 = cipher_to_point(first_line)
#         cipher_2 = list(map(cipher_to_point, rest))
#         message_points = [add(a, b, p, cipher, multiply(
#             a, b, p, -priv_key_b, cipher_1)) for cipher in cipher_2]

#         ascii_value_group_sums = []
#         for point in message_points:
#             ascii_value_group_sums.extend((point.get_x(), point.get_y()))

#         ascii_value_groups = []
#         for n in ascii_value_group_sums:
#             if n == 32:
#                 continue
#             ascii_value_groups.append(to_base(n))

#         ascii_values = []
#         for group in ascii_value_groups:
#             ascii_values.extend(group)

#         plaintext = ''.join([chr(ascii_value) for ascii_value in ascii_values])
#         file.seek(0)
#         file.write(plaintext)
#         file.truncate()
#     file.close()

window = tkinter.Tk()
window.title("Data Entry Form")

frame = tkinter.Frame(window)
frame.pack()

# Elliptic Info
elliptic_info_frame = tkinter.LabelFrame(frame, text="Elliptic curve Information")
elliptic_info_frame.grid(row= 0, column=0, padx=20, pady=10)

a_label = tkinter.Label(elliptic_info_frame, text="a value:")
a_label.grid(row=0, column=0)
a_entry = tkinter.Entry(elliptic_info_frame)
a_entry.grid(row=0, column=1)

b_label = tkinter.Label(elliptic_info_frame, text="b value:")
b_label.grid(row=1, column=0)
b_entry = tkinter.Entry(elliptic_info_frame)
b_entry.grid(row=1, column=1)

p_label = tkinter.Label(elliptic_info_frame, text="p value:")
p_label.grid(row=2, column=0)
p_entry = tkinter.Entry(elliptic_info_frame)
p_entry.grid(row=2, column=1)

gene_point_label = tkinter.Label(elliptic_info_frame, text="Generate point:")
gene_point_label.grid(row=3, column=0)

x_entry = tkinter.Entry(elliptic_info_frame)
# x_entry.insert(END, 'x')
x_entry.grid(row=3, column=1)

y_entry = tkinter.Entry(elliptic_info_frame)
# y_entry.insert(END, 'y')
y_entry.grid(row=3, column=2)

a_entry.insert(END, '6277101735386680763835789423207666416083908700390324961276')
b_entry.insert(END, '2455155546008943817740293915197451784769108058161191238065')
p_entry.insert(END, '6277101735386680763835789423207666416083908700390324961279')
x_entry.insert(END, '602046282375688656758213480587526111916698976636884684818')
y_entry.insert(END, '174050332293622031404857552280219410364023488927386650641')

for widget in elliptic_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Accept terms
import_file_frame = tkinter.LabelFrame(frame, text="Convert infomation")
import_file_frame.grid(row=1, column=0, sticky="news", padx=20, pady=10)

import_file_label = tkinter.Label(import_file_frame,text='File location:')  
import_file_label.grid(row=1, column=0)
import_file_location = tkinter.StringVar()
import_file_entry = tkinter.Entry(import_file_frame, textvariable=import_file_location, state=DISABLED,  width=50)
import_file_entry.grid(row=1, column=1)

import_file_button = tkinter.Button(import_file_frame, text='Import File', command = lambda:upload_file())
import_file_button.grid(row=1, column=2)

browse_folder_label = tkinter.Label(import_file_frame,text='Save location:')  
browse_folder_label.grid(row=2, column=0)
browse_folder_path = tkinter.StringVar()
browse_folder_path.set('D:\Documents\DuAnTotNghiep\Elliptic\elliptic-curve-python\message_to_point\Saves')
browse_folder_entry = tkinter.Entry(import_file_frame, textvariable=browse_folder_path, state=DISABLED,  width=50)
browse_folder_entry.grid(row=2, column=1)

browse_folder_button = tkinter.Button(import_file_frame, text='Browse', command = lambda:browse_folder())
browse_folder_button.grid(row=2, column=2)

for widget in import_file_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Button
button = tkinter.Button(frame, text="CONVERT", command = encript_file)
button.grid(row=2, column=0, sticky="news", padx=20, pady=10)
 
window.mainloop()