from PIL import Image, ImageFont, ImageDraw
from papirus import Papirus

import socket
import subprocess

# Get FreeMono Font
font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 15)

WHITE = 1
BLACK = 0
PAPIRUSROT = 0
PAPIRUS = Papirus(rotation=PAPIRUSROT)

def init_screen(color):
    """Prepare the screen for drawing and return the draw variables
    """
    image = Image.new("1", PAPIRUS.size, color)
    # Set width and height of screen
    width, height = image.size
    # prepare for drawing
    draw = ImageDraw.Draw(image)
    return image, width, height, draw

# Get SSID of connected network
ssidoutput = subprocess.check_output(['sudo', 'iwgetid'])

# Get local IP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print(s.getsockname()[0])


image, width, height, draw = init_screen(color=WHITE)
draw.text(
    (10, 10),
    "Connected Wifi SSID: ",
    fill=BLACK,
    font=font,
)
draw.text(
    (35, 30),
    '• "' + ssidoutput.decode().split('"')[1] + '"',
    fill=BLACK,
    font=font,
)
draw.text(
    (10, 50),
    "Local IP of RPi Zero: ",
    fill=BLACK,
    font=font,
)
draw.text(
    (35, 70),
    '• ' + s.getsockname()[0],
    fill=BLACK,
    font=font,
)


PAPIRUS.display(image)
PAPIRUS.update()

s.close()
