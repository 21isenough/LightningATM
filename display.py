import time

from utils import *
from config import *

from PIL import Image, ImageFont, ImageDraw



def update_startup_screen():

    image = Image.new('1', PAPIRUS.size, WHITE)

    draw = ImageDraw.Draw(image)

    draw.text((20, 10), 'Welcome to the', fill=BLACK, font=createfont('freemono',18))
    draw.text((10, 20), 'LightningATM', fill=BLACK, font=createfont('sawasdee',30))
    draw.text((7, 75), '- please insert coins -', fill=BLACK, font=createfont('freemono',14))

    PAPIRUS.display(image)
    PAPIRUS.update()

def update_qr_request():

    image = Image.new('1', PAPIRUS.size, WHITE)

    draw = ImageDraw.Draw(image)

    draw.text((25, 10), 'Please scan', fill=BLACK, font=createfont('freemono',20))
    draw.text((10, 30), 'your invoice in 5 sec', fill=BLACK, font=createfont('freemono',20))

    PAPIRUS.display(image)
    PAPIRUS.update()

    for i in range(0,5):
        draw.text((80, 50), str(5 - i), fill=BLACK, font=createfont('freemono',50))
        PAPIRUS.display(image)
        PAPIRUS.partial_update()
        draw.rectangle((75, 55 , 115, 95), fill=WHITE, outline=WHITE)
        time.sleep(1)
