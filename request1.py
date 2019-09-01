import codecs, grpc, os
import rpc_pb2 as ln, rpc_pb2_grpc as lnrpc
macaroon = codecs.encode(open('/home/pi/admin.macaroon', 'rb').read(), 'hex')
os.environ['GRPC_SSL_CIPHER_SUITES'] = 'HIGH+ECDSA'
cert = open('/etc/ssl/certs/ca-certificates.crt', 'rb').read()
ssl_creds = grpc.ssl_channel_credentials(cert)
channel = grpc.secure_channel('btcpay.21isenough.me:443', ssl_creds)
stub = lnrpc.LightningStub(channel)
# Define a generator that returns an Iterable of SendRequest objects.
        # Initialization code here.
while True:
    # Parameters here can be set as arguments to the generator.
    request = ln.SendRequest(
        payment_request='lnbc50n1pwkktx3pp5h8hz57fvjpnf8lfhp7xaxu83dgm95e37v6phwf3k4455wd4xreaqdqu2askcmr9wssx7e3q2dshgmmndp5scqzpgxqrrsskl7yekx4g7xcrk26034lw85mfyuwn9jj9zxuvn6egnacta4pkcrx6wl4n7ehrphdyh4lj3vw899rk283a7m4qtmd9ht05nq6shutdzqpv5cwg3',
    )
