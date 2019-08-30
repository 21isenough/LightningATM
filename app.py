#! /usr/bin/python

import time

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


from papirus import Papirus

WHITE = 1
BLACK = 0
DATE_FONT_FILE  = '/usr/share/fonts/truetype/freefont/FreeMono.ttf'

papirus = Papirus()

image = Image.new('1', papirus.size, WHITE)
width, height = image.size

date_font_size1 = int((width - 10)/(10*1))     # 10 chars YYYY-MM-DD
date_font_size2 = int((width - 10)/(12*1))     # 10 chars YYYY-MM-DD
date_font1 = ImageFont.truetype(DATE_FONT_FILE, date_font_size1)
date_font2 = ImageFont.truetype(DATE_FONT_FILE, date_font_size2)


draw = ImageDraw.Draw(image)
draw.rectangle((2, 2, width - 2, height - 2), fill=WHITE, outline=BLACK)
draw.text((10, 10), '10\'520 sats', fill=BLACK, font=date_font1)
draw.text((10, 30), '1 cent = 108 sats', fill=BLACK, font=date_font2)

papirus.display(image)
papirus.update()
time.sleep(3)

draw.rectangle((3, 30, 197, 50), fill=WHITE, outline=WHITE)
draw.text((10, 30), '1 cent = 112 sats', fill=BLACK, font=date_font2)

papirus.display(image)
papirus.partial_update()
time.sleep(3)

draw.rectangle((3, 30, 197, 50), fill=WHITE, outline=WHITE)
draw.text((10, 30), '1 cent = 102 sats', fill=BLACK, font=date_font2)

papirus.display(image)
papirus.partial_update()

time.sleep(5)
papirus.clear()
