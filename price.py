import requests
import json
import sys


def main(argv):

    print(argv)

    currency = argv[0] if len(sys.argv) > 1 else 'EUR'

    price = requests.get('https://apiv2.bitcoinaverage.com/indices/global/ticker/BTC' + currency)
    json_data = json.loads(price.text)

    print(json_data['last'])

if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        sys.exit('interrupted')
