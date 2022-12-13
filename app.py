from time import time
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from config import ELLIPTIC_CURVES
import os
import threading

from crypto.ec_elgamal import decrypt, encrypt, generate_keys, get_keys


class CryptApp(ttk.Notebook):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        f1 = tk.Frame(self)
        f2 = tk.Frame(self)
        self.add(f1, text='Encrypt Files')
        self.add(f2, text='Decrypt Files')
        self.grid(row=0, column=0, sticky="nw")

        curve_select_area = tk.LabelFrame(f1, text="Choose curve")
        curve_select_area.grid(row=0, column=0, padx=20,
                               pady=10, sticky='news')
        options = list(ELLIPTIC_CURVES.keys())
        self.selected = tk.StringVar()
        self.selected.set(options[0])
        curve_selector = ttk.OptionMenu(
            curve_select_area, self.selected, options[0], *options, command=lambda _: self.choose_curve_from_selector())
        curve_selector.grid(row=0, column=0, sticky='news', padx=10, pady=5)
        self.choose_curve_from_selector()

        # Encryption tab
        self.import_file_frame = tk.LabelFrame(
            f1, text="Encryption information")
        self.import_file_frame.grid(
            row=1, column=0, sticky="news", padx=20, pady=10)

        import_file_label = tk.Label(
            self.import_file_frame, text='File location:')
        import_file_label.grid(row=1, column=0)
        self.import_file_location = tk.StringVar()
        self.import_file_entry = tk.Entry(
            self.import_file_frame, textvariable=self.import_file_location, state='disabled', width=50)
        self.import_file_entry.grid(row=1, column=1)

        import_file_button = tk.Button(
            self.import_file_frame, text='Browse file...', command=lambda: self.upload_file())
        import_file_button.grid(row=1, column=2)

        browse_folder_label = tk.Label(
            self.import_file_frame, text='Save location:')
        browse_folder_label.grid(row=2, column=0)
        self.browse_folder_path = tk.StringVar()
        self.browse_folder_entry = tk.Entry(
            self.import_file_frame, textvariable=self.browse_folder_path, state='disabled', width=50)
        self.browse_folder_entry.grid(row=2, column=1)

        browse_folder_button = tk.Button(
            self.import_file_frame, text='Browse folder...', command=lambda: self.browse_folder())
        browse_folder_button.grid(row=2, column=2)

        for widget in self.import_file_frame.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        button = tk.Button(f1, text="ENCRYPT",
                           command=self.tk_process_encryption)
        button.grid(row=2, column=0, sticky="news", padx=20, pady=10)

        # Decryption tab
        self.import_file_frame_dec = tk.LabelFrame(
            f2, text="Decryption information")
        self.import_file_frame_dec.grid(
            row=1, column=0, sticky="news", padx=20, pady=10)

        import_file_label_dec = tk.Label(
            self.import_file_frame_dec, text='File location:')
        import_file_label_dec.grid(row=1, column=0)
        self.import_file_location_dec = tk.StringVar()
        self.import_file_entry_dec = tk.Entry(
            self.import_file_frame_dec, textvariable=self.import_file_location_dec, state='disabled', width=50)
        self.import_file_entry_dec.grid(row=1, column=1)

        import_file_button_dec = tk.Button(
            self.import_file_frame_dec, text='Browse file...', command=lambda: self.upload_file_dec())
        import_file_button_dec.grid(row=1, column=2)

        browse_folder_label_dec = tk.Label(
            self.import_file_frame_dec, text='Save location:')
        browse_folder_label_dec.grid(row=2, column=0)
        self.browse_folder_path_dec = tk.StringVar()
        self.browse_folder_entry_dec = tk.Entry(
            self.import_file_frame_dec, textvariable=self.browse_folder_path_dec, state='disabled', width=50)
        self.browse_folder_entry_dec.grid(row=2, column=1)

        browse_folder_button_dec = tk.Button(
            self.import_file_frame_dec, text='Browse folder...', command=lambda: self.browse_folder_dec())
        browse_folder_button_dec.grid(row=2, column=2)

        for widget in self.import_file_frame_dec.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        button_dec = tk.Button(
            f2, text="DECRYPT", command=self.tk_process_decryption)
        button_dec.grid(row=2, column=0, sticky="news", padx=20, pady=10)

    def choose_curve_from_selector(self):
        self.selected_curve_type = self.selected.get()
        selected_curve = ELLIPTIC_CURVES.get(self.selected_curve_type)
        self.p, self.a, self.b, self.g = [selected_curve.get(key)
                                        for key in selected_curve.keys()]

    def encrypt_file(self):
        try:
            progress_window = tk.Toplevel(window)
            progress_window.title('Encrypting...')
            progress_bar = ttk.Progressbar(
                progress_window, orient='horizontal', length=300, mode='indeterminate')
            progress_bar.pack(pady=20)
            progress_bar.start(5)
            filepath = self.import_file_entry.get()
            filename = os.path.split(filepath)[1]
            generate_keys(self.selected_curve_type,
                          self.p, self.a, self.b, self.g)
            encrypted_file_dest = f'{self.browse_folder_entry.get()}/{filename}.enc'
            pub_key_b = get_keys(self.selected_curve_type)[1]

            start_time = time()
            encrypt(self.p, self.a, self.b, self.g,
                    filepath, encrypted_file_dest, pub_key_b)
            encrypt_time = time() - start_time
            progress_window.destroy()
            messagebox.showinfo(
                "Message", "File has been encrypted!\nEncryption time: %.2fs" % round(encrypt_time, 3))
        except Exception as e:
            messagebox.showinfo("Error", e)

    def tk_process_encryption(self):
        threading.Thread(target=self.encrypt_file).start()

    def decrypt_file(self):
        try:
            progress_window = tk.Toplevel(window)
            progress_window.title('Decrypting...')
            progress_bar = ttk.Progressbar(
                progress_window, orient='horizontal', length=300, mode='indeterminate')
            progress_bar.pack(pady=20)
            progress_bar.start(5)
            filepath = self.import_file_entry_dec.get()
            filename = os.path.split(filepath)[1]
            decrypted_file_dest = f'{self.browse_folder_entry_dec.get()}/{filename.replace(".enc", "")}'
            priv_key_b = get_keys(self.selected_curve_type)[0]

            start_time = time()
            decrypt(self.p, self.a, self.b,
                    filepath, decrypted_file_dest, priv_key_b)
            encrypt_time = time() - start_time
            progress_window.destroy()
            messagebox.showinfo(
                "Message", "File has been decrypted!\nDecryption time: %.2fs" % round(encrypt_time, 3))
        except Exception as e:
            messagebox.showinfo("Error", e)
    
    def tk_process_decryption(self):
        threading.Thread(target=self.decrypt_file).start()

    def upload_file(self):
        file_location = filedialog.askopenfilename()
        self.import_file_location.set(file_location)
        basepath = os.path.split(self.import_file_location.get())[0]
        self.browse_folder_path.set(basepath)

    def browse_folder(self):
        foldername = filedialog.askdirectory()
        self.browse_folder_path.set(foldername)

    def upload_file_dec(self):
        file_location = filedialog.askopenfilename()
        self.import_file_location_dec.set(file_location)
        basepath = os.path.split(self.import_file_location_dec.get())[0]
        self.browse_folder_path_dec.set(basepath)

    def browse_folder_dec(self):
        foldername = filedialog.askdirectory()
        self.browse_folder_path_dec.set(foldername)


window = tk.Tk()
window.title('File Encryption Tool')
CryptApp(window).pack()
window.mainloop()
