from papirus import Papirus

## set API URL e.g. https://btcpay.yourdomain.com/lnd-rest/btc/v1
APIURL = 'https://btcpay.21isenough.me/lnd-rest/btc/v1'
## Add variable to set certificate check to true or false ##

## Papirus Setup
WHITE = 1
BLACK = 0
PAPIRUSROT = 0
PAPIRUS = Papirus(rotation = PAPIRUSROT)

## set currency value
CURRENCY = 'EUR'
## Add var for fee in % ##

## set user and password for lntxbot
USER = 'XXXXXX'
PASS = 'XXXXXX'
