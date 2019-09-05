import PIL, os
from PIL import ImageDraw
from PIL import ImageFont

from papirus import Papirus

BLACK = 0
WHITE = 1

font1 = ImageFont.truetype(os.path.expanduser('~/LightningATM/resources/FreeMono.ttf'), 18)
font = ImageFont.truetype(os.path.expanduser('~/LightningATM/resources/Sawasdee-Bold.ttf'), 30)
font2 = ImageFont.truetype(os.path.expanduser('~/LightningATM/resources/FreeMono.ttf'), 14)

def startupdisplay():
    papirus = Papirus(rotation = int(argv[0]) if len(sys.argv) > 1 else 0)

    image = PIL.Image.new('1', papirus.size, WHITE)

    draw = ImageDraw.Draw(image)

    draw.text((20, 10), 'Welcome to the', fill=BLACK, font=font1)
    draw.text((10, 20), 'LightningATM', fill=BLACK, font=font)
    draw.text((7, 75), '- please insert coins -', fill=BLACK, font=font2)

    papirus.display(image)
    papirus.update()
