from argparse import ArgumentParser

import json
import os
import subprocess
import sys

parser = ArgumentParser()
parser.add_argument('action', help='action')
parser.add_argument('--subchain_index', type=int, default=-1, help='subchain index')
parser.add_argument('--block_hash', default=None, help='block hash')
parser.add_argument('--verbosity', type=int, default=1, help='0 is hex data, 1 is json')
parser.add_argument('--nblocks', type=int, default=0, help='number of blocks to generate')
args = parser.parse_args()
action = args.action
subchain_index = args.subchain_index
home_dir = os.environ['HOME']

process = subprocess.Popen(
        [
            './src/bitcoin-cli',
            '-regtest',
            '-rpcport=3776',
            '-datadir={home}/.bitcoin/0'.format(home=home_dir),
            '-conf={home}/.bitcoin/0/bitcoin.conf'.format(home=home_dir),
            'getblockchaininfo',
        ], stdout=subprocess.PIPE)
info, err = process.communicate()
if err:
    sys.exit('could not get number of sub chains: {}'.format(str(err)))
blockchain_info = json.loads(info.decode('utf8'))
num_chains = int(blockchain_info['numsubchains'])

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

elif action == 'getblockheader':
    if subchain_index == -1:
        sys.exit('must specify a subchain index with getblockheader')
    block_hash = args.block_hash
    if not block_hash:
        sys.exit('must specify a block hash with getblockheader')
    os.system('./src/bitcoin-cli -regtest -rpcport={} -datadir={} -conf={} getblockheader {}'.format(
        chains[subchain_index]['rpc_port'],
        chains[subchain_index]['data_dir'],
        chains[subchain_index]['conf'],
        block_hash,
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
