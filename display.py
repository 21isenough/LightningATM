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

    ## initially set all white background
    image = Image.new('1', PAPIRUS.size, WHITE)

    ## Set width and heigt of screen
    width, height = image.size

    ## prepare for drawing
    draw = ImageDraw.Draw(image)

    draw.rectangle((2, 2, width - 2, height - 2), fill=WHITE, outline=BLACK)
    draw.text((25, 10), 'Please scan', fill=BLACK, font=createfont('freemono',20))
    draw.text((10, 30), 'your invoice in', fill=BLACK, font=createfont('freemono',20))

    PAPIRUS.display(image)
    PAPIRUS.update()

    for i in range(0,3):
        draw.text((80, 45), str(3 - i), fill=BLACK, font=createfont('freemono',50))
        PAPIRUS.display(image)
        PAPIRUS.partial_update()
        draw.rectangle((75, 50 , 115, 90), fill=WHITE, outline=WHITE)
        time.sleep(1)

    draw.rectangle((2, 2, width - 2, height - 2), fill=WHITE, outline=BLACK)
    draw.text((25, 10), 'Scanning...', fill=BLACK, font=createfont('freemono',20))
    PAPIRUS.display(image)
    PAPIRUS.partial_update()

def update_qr_failed():

    ## initially set all white background
    image = Image.new('1', PAPIRUS.size, WHITE)

    ## Set width and heigt of screen
    width, height = image.size

    ## prepare for drawing
    draw = ImageDraw.Draw(image)

    draw.rectangle((2, 2, width - 2, height - 2), fill=WHITE, outline=BLACK)
    draw.text((25, 10), 'Scanning...', fill=BLACK, font=createfont('freemono',20))
    draw.text((25, 40), 'Scan failed.', fill=BLACK, font=createfont('freemono',20))
    draw.text((25, 70), 'Try again.', fill=BLACK, font=createfont('freemono',20))
    PAPIRUS.display(image)
    PAPIRUS.partial_update()

def update_thankyou_screen():

    image = Image.new('1', PAPIRUS.size, WHITE)

    draw = ImageDraw.Draw(image)

    draw.text((15, 10), 'Enjoy your new', fill=BLACK, font=createfont('freemono',19))
    draw.text((40, 35), 'satoshis!!', fill=BLACK, font=createfont('freemono',19))
    draw.text((15, 70), '#bitcoin #lightning', fill=BLACK, font=createfont('freemono',14))

    PAPIRUS.display(image)
    PAPIRUS.update()
