import pytesseract
from PIL import Image
import time
from io import BytesIO

def initTable(threshold=140):
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)

    return table


def get_code(buf):
    image = Image.open(BytesIO(buf))
    return pytesseract.image_to_string(image, config='-psm 5')

if __name__ == "__main__":
    print(get_code('test.png'))