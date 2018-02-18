from __future__ import print_function
from bitcoinrpc.authproxy import AuthServiceProxy


def create_rpc_connection():
    rpc_port = 18443
    rpc_user = 'bitcoinrpc'
    rpc_password = 'sharkpass'

    return AuthServiceProxy("http://{}:{}@127.0.0.1:{}".format(rpc_user, rpc_password, rpc_port))
