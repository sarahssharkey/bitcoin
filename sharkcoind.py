from argparse import ArgumentParser
import os
import sys

parser = ArgumentParser()
parser.add_argument('num_chains', type=int, help='number of subchains')
args = parser.parse_args()
num_chains = args.num_chains

if num_chains > 20:
    sys.exit("too many chains, max 20")

current_port = 3776
home_dir = os.environ['HOME']
chains = []

for i in range(0, num_chains):
    data_dir = '{home}/.bitcoin/{index}'.format(home=home_dir, index=i)
    rpc_port = current_port
    port = current_port + 1
    chains.append({'rpcport': rpc_port, 'port': port, 'data_dir': data_dir})
    os.system('mkdir {}'.format(data_dir))
    os.system('mkdir {}/regtest'.format(data_dir))
    conf_info = 'rpcuser=sarah\nrpcpassword=password\nrpcport={rpcport}\nport={port}'.format(rpcport=rpc_port,
                                                                                             port=port)
    f = open('{}/regtest/bitcoin.conf'.format(data_dir), 'w+')
    f.write(conf_info)
    f.close()
    os.system('./src/bitcoind -daemon -regtest -rpcport={} -port={} -datadir={} -conf={}/bitcoin.conf'.format(rpc_port, port, data_dir, data_dir))
    current_port += 2

