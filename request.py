import os, codecs, requests, json, base64

with open(os.path.expanduser('~/admin.macaroon'), 'rb') as f:
    macaroon_bytes = f.read()
    macaroon = codecs.encode(macaroon_bytes, 'hex')

url = 'https://btcpay.21isenough.me/lnd-rest/btc/v1/payments'

data = {
        'include_incomplete': True,
}

r = requests.get(url, headers = {'Grpc-Metadata-macaroon': macaroon}, data=json.dumps(data))
json_data = json.loads(r.text)
payment_data = json_data['payments']
last_payment = payment_data[-1]

print(last_payment['value'])
