from __future__ import print_function
from bitcoinrpc.authproxy import AuthServiceProxy
import json
import re
import hashlib
import binascii


# Swap Endian function
def swap_endian(data):
    return ''.join(reversed(re.findall('..', data)))


# Hash pairs of items recursively until a single value is obtained
def merkle(hash_list):
    if len(hash_list) == 1:
        return hash_list[0]
    new_hash_list = []
    # Process pairs. For odd length, the last is skipped
    for i in range(0, len(hash_list) - 1, 2):
        new_hash_list.append(hash2(hash_list[i], hash_list[i + 1]))
    if len(hash_list) % 2 == 1:  # odd, hash last item twice
        new_hash_list.append(hash2(hash_list[-1], hash_list[-1]))
    return merkle(new_hash_list)


def hash2(a, b):
    # Reverse inputs before and after hashing
    # due to big-endian / little-endian nonsense
    a1 = a.decode('hex')
    a11 = a1[::-1]
    # print a11.encode('hex')
    b1 = b.decode('hex')[::-1]
    # print b1.encode('hex')
    concat = a11 + b1
    # print concat.encode('hex')
    concat2 = hashlib.sha256(concat).digest()
    h = hashlib.sha256(concat2).digest()
    return h[::-1].encode('hex')


def field(data, size):
    bytes = size * 2
    return data.rjust(bytes, '0')


def reverse_bytes(data):
    return swap_endian(data)


def hash256(data):
    binary = data.decode('hex')
    hash1 = hashlib.sha256(hashlib.sha256(binary).digest()).digest()
    return hash1


def mine(header, nonce, target):
    while True:
        attempt = header + reverse_bytes(field(hex(nonce), 4))
        block_hash = reverse_bytes(hash256(attempt))

        if int(block_hash, 16) < int(target, 16):
            print("Block Hash is below the Target! This block has been mined!")
            break
        nonce += 1


# Uncomment the line below to slow down the hashing
# sleep(0.1)

rpc_port = 18443
rpc_user = 'bitcoinrpc'
rpc_password = 'sharkpass'

rpc_connection = AuthServiceProxy("http://{}:{}@127.0.0.1:{}".format(rpc_user, rpc_password, rpc_port))
template = json.loads(str(rpc_connection.getblocktemplate()))
version = swap_endian(hex(int(template['version']))[2:])
previous_block = swap_endian(template['previousblockhash'][1:-1])
transaction_ids = [t['txid'] for t in template['transactions']]
merkle_root = swap_endian(merkle(transaction_ids))
timestamp = swap_endian(hex(int(template['curtime'])))
bits = swap_endian(template['bits'][1:-1])
block_header = version + previous_block + merkle_root + timestamp + bits
target = json.loads(str(rpc_connection.getmininginfo()))['difficulty']
mine(block_header, 0, target)
