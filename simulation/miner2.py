from __future__ import print_function
import binascii
from bitcoinrpc.authproxy import AuthServiceProxy
import json
import hashlib
import struct


def dblsha(data):
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()


def varint_encode(n):
    if n < 0xfd:
        return struct.pack('<B', n)
    return b'\xfd' + struct.pack('<H', n)


def merkle_root(txns):
    merklehashes = [dblsha(t) for t in txns]
    while len(merklehashes) > 1:
        if len(merklehashes) % 2:
            merklehashes.append(merklehashes[-1])
            merklehashes = [dblsha(merklehashes[i] + merklehashes[i + 1]) for i in range(0, len(merklehashes), 2)]
    return merklehashes[0]


rpc_port = 18443
rpc_user = 'bitcoinrpc'
rpc_password = 'sharkpass'
rpc_connection = AuthServiceProxy("http://{}:{}@127.0.0.1:{}".format(rpc_user, rpc_password, rpc_port))

template = json.loads(str(rpc_connection.getblocktemplate()))
coinbase = binascii.a2b_hex(template['coinbasetxn']['data'])
extradata = b'my block'

origLen = ord(coinbase[41:42])
newLen = origLen + len(extradata)
coinbase = coinbase[0:41] + chr(newLen).encode('ascii') + coinbase[42:42 + origLen] + extradata + coinbase[
                                                                                                  42 + origLen:]

txnlist = [coinbase] + [binascii.a2b_hex(a['data']) for a in template['transactions']]
merkleroot = merkle_root(txnlist)
print(struct.pack('<I', template['version']))
'''
blkheader = struct.pack('<I', template['version']) + \
            binascii.a2b_hex(template['previousblockhash']) + \
            merkleroot + \
            struct.pack('<I', template['curtime']) + \
            binascii.a2b_hex(template['bits']) + \
            b'NONC'
blkdata = blkheader + varint_encode(len(txnlist)) + coinbase
if 'submit/coinbase' not in template.get('mutable', ()):
    for txn in txnlist[1:]:
        blkdata += txn
'''
