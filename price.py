import requests, json

def getbtcprice(fiatcode):
    request = requests.get('https://apiv2.bitcoinaverage.com/indices/global/ticker/BTC' + fiatcode)
    json_data = json.loads(request.text)
    return json_data['last']
