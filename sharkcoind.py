from argparse import ArgumentParser
import subprocess
import sys

parser = ArgumentParser()
parser.add_argument('num_chains', help='number of subchains')
args = parser.parse_args()
num_chains = parser.num_chains

if num_chains > 20:
    sys.exit("too many chains, max 20")

current_port = 3776

chains = []

for i in range(0, num_chains):
    home_dir = subprocess.check_output('echo $HOME')
    data_dir = '{home}/.bitcoin/regtest/{index}'.format(home=home_dir, index=i)
    rpcport = current_port
    port = current_port + 1
    chains.append({'rpcport': rpcport, 'port': port, 'data_dir': data_dir})
    subprocess.run(['mkdir', data_dir])
    conf_info = 'rpcuser=sarah\nrpcpassword=password\nrpcport={rpcport}\nport={port}'.format(rpcport=rpcport, port=port)
    current_port += 2
    subprocess.run(['echo', conf_info, '>{}/bitcoin.conf'.format(data_dir)])
    subprocess.run(
        ['./src/bitcoind', '-daemon', '-regtest', '-rpcport={}'.format(rpcport), '-data_dir={}'.format(data_dir)])
