import qrcode
import qrcode.image.svg
import cv2
from qreader import QReader
import tkinter as tk
from tkinter import ttk
import os


def get_link(path):
    reader = QReader()

    image = cv2.imread(path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    decoded = reader.detect_and_decode(image=image)
    print(decoded)

    return decoded


def create_qr_svg(url: str, output_path: str, box_size: int = 500, border: int = 4):
    factory = qrcode.image.svg.SvgPathImage

    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_M,  # H=30%, Q=25%, M=15%, L=7%
        box_size=box_size,
        border=border,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(image_factory=factory)
    img.save(output_path)
    print(f"Saved: {output_path}")


class App:
    svg_path_entry = None
    qr_path_entry = None
    generate_btn = None
    err_label = None

    check_box = None
    check_box_val = None

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("400x400")
        self.root.title("QR -> SVG")
        self.root.resizable(width=False, height=False)

        style = ttk.Style()
        style.theme_use('clam')


        self.build_app()
        self.root.mainloop()


    def build_app(self):
        welcome_label = tk.Label(self.root, text="Welcome to arzs QR to SVG converter", font=('Arial', 16))
        welcome_label.pack()

        self.make_room()
        self.make_room()

        qr_path_label = tk.Label(self.root, text="Photo name: ", font=('Arial', 12))
        qr_path_label.pack()

        self.qr_path_entry = tk.Entry(self.root)
        self.qr_path_entry.pack()

        self.make_room()

        svg_path_label = tk.Label(self.root, text="SVG name: ", font=('Arial', 12))
        svg_path_label.pack()

        self.svg_path_entry = tk.Entry(self.root)
        self.svg_path_entry.pack()

        self.make_room()

        self.generate_btn = tk.Button(self.root, text="Generate", command=lambda :self.generate(), font=('Arial', 12))
        self.generate_btn.pack()

        self.check_box_val = tk.IntVar()
        self.check_box = tk.Checkbutton(self.root, text="Open destination folder", variable=self.check_box_val, font=('Arial', 12))
        self.check_box.pack()

        self.err_label = tk.Label(self.root, text="", font=('Arial', 16))
        self.err_label.pack()


    def generate(self):
        self.err_label.config(text="")
        output_path = self.svg_path_entry.get()
        input_path = self.qr_path_entry.get()

        if not input_path or not output_path:
            self.err_label.config(text="Please enter values")
            return

        output_path = f'qr_as_svg/{output_path}.svg'
        input_path = f'qr_folder/{input_path}.jpeg'

        if not os.path.exists(input_path):
            self.err_label.config(text="Photo does not exist")
            return

        link = get_link(input_path)
        create_qr_svg(link, output_path, border=4)
        self.err_label.config(text="SVG generated!")

        if self.check_box_val.get():
            os.startfile('qr_as_svg')


    def make_room(self):
        tk.Label(self.root, text="").pack()


app = App()

"""
name = 'fadi_halabi'

output_path = f'qr_as_svg/{name}2.svg'
input_path = f'qr_folder/{name}.jpeg'

link = get_link(input_path)
create_qr_svg(link, output_path, border=4)
"""