from argparse import ArgumentParser

import os, sys

parser = ArgumentParser()
parser.add_argument('num_chains', type=int, help='number of subchains')
parser.add_argument('action', help='action')
parser.add_argument('--subchain_index', type=int, default=-1, help='subchain index')
parser.add_argument('--block_hash', deafult=None, help='block hash')
parser.add_argument('--verbosity', type=int, default=1, help='0 is hex data, 1 is json')
parser.add_argument('--nblocks', type=int, default=0, help='number of blocks to generate')
args = parser.parse_args()
action = args.action
subchain_index = args.subchain_index
num_chains = args.num_chains
home_dir = os.environ['HOME']

chains = [
    {
        'conf': '{home}/.bitcoin/{index}/bitcoin.conf'.format(home=home_dir, index=i),
        'data_dir': '{home}/.bitcoin/{index}'.format(home=home_dir, index=i),
        'rpc_port': 3776 + i * 2,
    } for i in range(0, num_chains)
]

if action == 'stop':
    for chain in chains:
        os.system('./src/bitcoin-cli -regtest -rpcport={} -datadir={} -conf={} stop'.format(
            chain['rpc_port'],
            chain['data_dir'],
            chain['conf'],
        ))
        os.system('rm -rf {}'.format(chain['data_dir']))

elif action == 'getblock':
    if subchain_index == -1:
        sys.exit('must specify a subchain index with getblock')
    block_hash = args.block_hash
    if not block_hash:
        sys.exit('must specify a block hash with getblock')
    os.system('./src/bitcoin-cli -regtest -rpcport={} -datadir={} -conf={} getblock {} {}'.format(
        chains[subchain_index]['rpc_port'],
        chains[subchain_index]['data_dir'],
        chains[subchain_index]['conf'],
        block_hash,
        args.verbosity
    ))

elif action == 'generate':
    nblocks = args.nblocks
    if not nblocks:
        sys.exit('must specify nblocks with getblock')
    if subchain_index == -1:
        for index, chain in enumerate(chains):
            print('--- Subchain {} ---'.format(index))
            os.system('./src/bitcoin-cli -regtest -rpcport={} -datadir={} -conf={} generate {}'.format(
                chain['rpc_port'],
                chain['data_dir'],
                chain['conf'],
                nblocks
            ))
            print('\n')
    else:
        os.system('./src/bitcoin-cli -regtest -rpcport={} -datadir={} -conf={} generate {}'.format(
            chains[subchain_index]['rpc_port'],
            chains[subchain_index]['data_dir'],
            chains[subchain_index]['conf'],
            nblocks
        ))

elif action == 'getblockchaininfo':
    if subchain_index == -1:
        for index, chain in enumerate(chains):
            print('--- Subchain {} ---'.format(index))
            os.system('./src/bitcoin-cli -regtest -rpcport={} -datadir={} -conf={} getblockchaininfo'.format(
                chain['rpc_port'],
                chain['data_dir'],
                chain['conf'],
            ))
    else:
        os.system('./src/bitcoin-cli -regtest -rpcport={} -datadir={} -conf={} getblockchaininfo'.format(
            chains[subchain_index]['rpc_port'],
            chains[subchain_index]['data_dir'],
            chains[subchain_index]['conf'],
        ))
else:
    sys.exit('unknown action: {}'.format(action))
