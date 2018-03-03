from argparse import ArgumentParser

import os, sys

parser = ArgumentParser()
parser.add_argument('action', help='action')
parser.add_argument('num_chains', type=int, help='number of subchains')
args = parser.parse_args()
action = args.action
num_chains = args.num_chains
home_dir = os.environ['HOME']

if action == 'stop':
    chains = [
        {
            'conf': '{home}/.bitcoin/{index}/bitcoin.conf'.format(home=home_dir, index=i),
            'data_dir': '{home}/.bitcoin/{index}'.format(home=home_dir, index=i),
            'rpc_port': 3776 + i * 2,
        } for i in range(0, num_chains)
    ]

    for chain in chains:
        os.system('./src/bitcoin-cli -regtest -rpcport={} -datadir={} -conf={} stop'.format(
            chain['rpc_port'],
            chain['data_dir'],
            chain['conf'],
        ))

else:
    sys.exit('unknown action: {}'.format(action))
