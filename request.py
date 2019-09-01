import os, codecs, requests, json

with open(os.path.expanduser('~/admin.macaroon'), 'rb') as f:
    macaroon_bytes = f.read()
    macaroon = codecs.encode(macaroon_bytes, 'hex')

payment_request = 'lnbc1pwkcxh5pp58e40fc0gqcfw4aa9v4cmcv5ecdtafl9mu22a9rphw6pgk5el9jrqdqu2askcmr9wssx7e3q2dshgmmndp5scqzpgxqrrssy5npx2rg52mjwlejttyvy7m4dhjj3kzv74rdwn28w57ur6awq23xc4lzp2gvdlxntwlztgph25lgqgyhpt6lghnjshpmq65rvqfzl5gqshu4yx'
amt = 7

data = {
        'payment_request': payment_request,
        'amt': amt,
}

response =  requests.post(
    'https://btcpay.21isenough.me/lnd-rest/btc/v1/channels/transactions',
    headers = {'Grpc-Metadata-macaroon': macaroon},
    data=json.dumps(data),
)
