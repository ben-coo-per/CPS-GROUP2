from escpos.printer import Usb
from PIL import Image

# Define the out_ep as 0x01, which is common, but you may try 0x02 if this fails
p = Usb(0x0416, 0x5011, 0, profile="NT-5890K", out_ep=0x03)
p.text("Hello World\n")

img = Image.open("processing/receipt_generator/output.jpg")


# split up the image into 20px high chunks
chunk_height = 20  # Height of each chunk
for i in range(0, img.height, chunk_height):
    chunk = img.crop((0, i, img.width, min(i + chunk_height, img.height)))
    p.image(chunk)
    p.text("\n")  # Add a newline between chunks if needed

    p._raw(
        b"\x1B\x64\x02"
    )  # Add small delay between chunks to allow the printer to process

p.cut()
