import qrcode
import qrcode.image.svg
import cv2
from qreader import QReader



def get_link(path):
    reader = QReader()

    image = cv2.imread(path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    decoded = reader.detect_and_decode(image=image)
    print(decoded)

    return decoded


def create_qr_svg(url: str, output_path: str, box_size: int = 10, border: int = 4):
    factory = qrcode.image.svg.SvgPathImage

    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # H=30%, Q=25%, M=15%, L=7%
        box_size=box_size,
        border=border,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(image_factory=factory)
    img.save(output_path)
    print(f"Saved: {output_path}")


name = 'fadi_halabi'

output_path = f'qr_as_svg/{name}.svg'
input_path = f'qr_folder/{name}.jpeg'

link = get_link(input_path)
create_qr_svg(link, output_path, border=4)