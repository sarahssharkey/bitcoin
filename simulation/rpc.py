from __future__ import print_function
from bitcoinrpc.authproxy import AuthServiceProxy


def create_rpc_connection(rpc_user, rpc_password):
    rpc_port = 18443

    return AuthServiceProxy("http://{}:{}@127.0.0.1:{}".format(rpc_user, rpc_password, rpc_port))
