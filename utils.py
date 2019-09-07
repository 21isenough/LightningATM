import os
import requests, json
from PIL import ImageFont

def createfont(font, size):
    pathfreemono = os.path.expanduser('~/LightningATM/resources/fonts/FreeMono.ttf')
    pathsawasdee = os.path.expanduser('~/LightningATM/resources/fonts/Sawasdee-Bold.ttf')

    if font == 'freemono':
        return ImageFont.truetype(pathfreemono, size)
    if font == 'sawasdee':
        return ImageFont.truetype(pathsawasdee, size)
    else:
        print('Font not available')

def getbtcprice(fiatcode):
    request = requests.get('https://apiv2.bitcoinaverage.com/indices/global/ticker/BTC' + fiatcode)
    json_data = json.loads(request.text)
    return json_data['last']
