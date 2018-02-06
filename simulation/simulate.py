from __future__ import print_function
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

rpc_port = 18443
rpc_user = 'bitcoinrpc'
rpc_password = 'sharkpass'

rpc_connection = AuthServiceProxy("http://{}:{}@127.0.0.1:{}".format(rpc_user, rpc_password, rpc_port))
best_block_hash = rpc_connection.getbestblockhash()
print(rpc_connection.getblock(best_block_hash))

# batch support : print timestamps of blocks 0 to 99 in 2 RPC round-trips:
commands = [["getblockhash", height] for height in range(100)]
block_hashes = rpc_connection.batch_(commands)
blocks = rpc_connection.batch_([["getblock", h] for h in block_hashes])
block_times = [block["time"] for block in blocks]
print(block_times)
