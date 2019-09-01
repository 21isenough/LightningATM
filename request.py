import codecs, os, requests, json

with open(os.path.expanduser('~/admin.macaroon'), 'rb') as f:
    macaroon_bytes = f.read()
    macaroon = codecs.encode(macaroon_bytes, 'hex')

data = {
        'payment_request': 'lnbc50n1pwkktx3pp5h8hz57fvjpnf8lfhp7xaxu83dgm95e37v6phwf3k4455wd4xreaqdqu2askcmr9wssx7e3q2dshgmmndp5scqzpgxqrrsskl7yekx4g7xcrk26034lw85mfyuwn9jj9zxuvn6egnacta4pkcrx6wl4n7ehrphdyh4lj3vw899rk283a7m4qtmd9ht05nq6shutdzqpv5cwg3',
}

response =  requests.get(
    'https://btcpay.21isenough.me/lnd-rest/btc/v1/transactions',
    headers = {'Grpc-Metadata-macaroon': macaroon},
    data=json.dumps(data),
)
