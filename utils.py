import os
import requests, json
from PIL import ImageFont

def createfont(font, size):
    pathfreemono = os.path.expanduser('~/LightningATM/resources/fonts/FreeMono.ttf')
    pathfreemonobold = os.path.expanduser('~/LightningATM/resources/fonts/FreeMonoBold.ttf')
    pathsawasdee = os.path.expanduser('~/LightningATM/resources/fonts/Sawasdee-Bold.ttf')

    if font == 'freemono':
        return ImageFont.truetype(pathfreemono, size)
    if font == 'freemonobold':
        return ImageFont.truetype(pathfreemonobold, size)
    if font == 'sawasdee':
        return ImageFont.truetype(pathsawasdee, size)
    else:
        print('Font not available')

def getbtcprice(fiatcode):
    request = requests.get('https://apiv2.bitcoinaverage.com/indices/global/ticker/BTC' + fiatcode)
    json_data = json.loads(request.text)
    return json_data['last']

def updateconfig(variable,newvalue):
    linecount = 0

    ## open the config.py file (read-only) and read the lines
    with open('config.py', 'r') as file:
        lines = file.readlines()

    ## find the line that contains the passed variable
    ## and change it to the new value
    for line in lines:
        if variable in line:
            line = variable + ' = \'' + newvalue + '\'\n'
            lines[linecount] = line
        linecount += 1

    ## open the config.py file (with write permissions) and safe the new lines
    with open('config.py', 'w') as file:
        file.writelines(lines)
