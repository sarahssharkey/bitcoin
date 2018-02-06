from __future__ import print_function
import requests, json, argparse

parser = argparse.ArgumentParser()
parser.add_argument('--instance_num', help='Instance number')
instance_num = parser.parse_args().instance_num

rpcPort = 18444
rpcUser = 'bitcoinrpc'

rpcPassword = 'sharkpass' + instance_num
serverURL = 'http://' + rpcUser + ':' + rpcPassword + '@localhost:' + str(rpcPort)

headers = {'content-type': 'application/json'}
payload = json.dumps({"method": 'getpeerinfo', "jsonrpc": "2.0"})
response = requests.get(serverURL, headers=headers, data=payload)
print(response.json()['result'])