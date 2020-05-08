from PIL import Image
import io
import numpy as np

if __name__ == "__main__":
    arr = io.BytesIO()
    with Image.open("img.jpg") as im:
        # im.save(arr, format='JPEG')
        # arr = arr.getvalue()
        # hex_arr = arr.hex()
        # im2 = Image.open(io.BytesIO(arr))
        # im2.show()
        im2 = im.resize((256, 256))
        im2.save('img_resized.jpg', format='JPEG')
