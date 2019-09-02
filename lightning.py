import os, codecs, requests, json


def payout(amt):

    with open(os.path.expanduser('~/admin.macaroon'), 'rb') as f:
        macaroon_bytes = f.read()
        macaroon = codecs.encode(macaroon_bytes, 'hex')

        payment_request = 'lnbc1pwk6xx0pp5m7f9mnkstxks9gphft6hfx0x9tzpfmlghxc37lyhupkd4cnsn26qdqu2askcmr9wssx7e3q2dshgmmndp5scqzpgxqrrssj2g95uwqxzrpaadyneqr2gmeefg6j4d6htdhxhgm3cz6nvhzuvphukkdzpkv488846xn97tp0av7pz0qkz0ttq7h3wcs29mq6hgp66qpk72vsu'

    data = {
            'payment_request': payment_request,
            'amt': round(amt),
    }

    response =  requests.post(
        'https://btcpay.21isenough.me/lnd-rest/btc/v1/channels/transactions',
        headers = {'Grpc-Metadata-macaroon': macaroon},
        data=json.dumps(data),
    )

def lastpayment(amt):

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

    print(last_payment['value'] + ' ' +last_payment['status'])
