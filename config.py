from papirus import Papirus

## set API URL e.g. https://btcpay.yourdomain.com/lnd-rest/btc/v1
APIURL = 'https://btcpay.21isenough.me/lnd-rest/btc/v1'

## Papirus Setup
WHITE = 1
BLACK = 0
PAPIRUSROT = 0
PAPIRUS = Papirus(rotation = PAPIRUSROT)

## set currency value
CURRENCY = 'EUR'

## Check EPD_SIZE is defined
EPD_SIZE=0.0
if os.path.exists('/etc/default/epd-fuse'):
    exec(open('/etc/default/epd-fuse').read())
if EPD_SIZE == 0.0:
    print("Please select your screen size by running 'papirus-config'.")
    sys.exit()
