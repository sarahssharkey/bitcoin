from argparse import ArgumentParser
import json
import os
import sys
import subprocess
import time


def main():
    parser = ArgumentParser()
    parser.add_argument('num_chains', type=int, help='number of subchains')
    args = parser.parse_args()
    num_chains = args.num_chains

    if num_chains > 20:
        sys.exit("too many chains, max 20")

    if num_chains < 1:
        sys.exit("num_chains must be greater than 0")

    home_dir = os.environ['HOME']
    chains = [
        {
            'conf': '{home}/.bitcoin/{index}/bitcoin.conf'.format(home=home_dir, index=i),
            'data_dir': '{home}/.bitcoin/{index}'.format(home=home_dir, index=i),
            'rpc_port': 3776 + i * 2,
        } for i in range(0, num_chains)
    ]
'''
    for index, chain in enumerate(chains):
        data_dir = chain['data_dir']
        rpc_port = chain['rpc_port']
        port = rpc_port + 1
        if not os.path.isdir(data_dir):
            os.system('mkdir {}'.format(data_dir))
            if not os.path.isdir('{}/regtest'.format(data_dir)):
                os.system('mkdir {}/regtest'.format(data_dir))
        conf_info = 'rpcuser=sarah\nrpcpassword=password\nrpcport={rpcport}\nport={port}'.format(rpcport=rpc_port,
                                                                                                 port=port)
        f = open('{}/bitcoin.conf'.format(data_dir), 'w+')
        f.write(conf_info)
        f.close()
        continue
        os.system('./src/bitcoind -daemon -regtest -rpcport={} -port={} -datadir={} -conf={}/bitcoin.conf -numChains={} -chainIndex={}'.format(rpc_port, port, data_dir, data_dir, num_chains, index))
'''
    #time.sleep(4)
    setup_genesis_and_first_blocks(chains)


def setup_genesis_and_first_blocks(chains):
    process = subprocess.Popen(
        [
            './src/bitcoin-cli',
            '-regtest',
            '-rpcport={}'.format(chains[0]['rpc_port']),
            '-datadir={}'.format(chains[0]['data_dir']),
            '-conf={}'.format(chains[0]['conf']),
            'generate',
            '1',
        ], stdout=subprocess.PIPE)
    blocks, err = process.communicate()
    if err:
        sys.exit('could not create genesis: {}'.format(str(err)))
    block_hash = json.loads(blocks.decode('utf8'))[0]
    process = subprocess.Popen(
        [
            './src/bitcoin-cli',
            '-regtest',
            '-rpcport={}'.format(chains[0]['rpc_port']),
            '-datadir={}'.format(chains[0]['data_dir']),
            '-conf={}'.format(chains[0]['conf']),
            'getblock',
            block_hash,
            '0',
        ], stdout=subprocess.PIPE)
    hex_data, err = process.communicate()
    if err:
        sys.exit('could not get genesis hex data: {}'.format(str(err)))
    hex_data = hex_data.decode('utf8')
    for chain in chains[1:]:
        os.system('./src/bitcoin-cli -regtest -rpcport={} -datadir={} -conf={} submitblock {}'.format(
            chain['rpc_port'],
            chain['data_dir'],
            chain['conf'],
            hex_data
        ))
    for chain in chains:
        os.system('./src/bitcoin-cli -regtest -rpcport={} -datadir={} -conf={} generate 1'.format(
            chain['rpc_port'],
            chain['data_dir'],
            chain['conf'],
        ))
        

main()
