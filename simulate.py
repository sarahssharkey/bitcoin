from __future__ import print_function
from simulation.miner import Miner
from simulation.transactions import TransactionCreator
from simulation.constants import addresses
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('address', help='address of this machine')
args = parser.parse_args()
address = args.address

transaction_creators = [TransactionCreator(list(addresses).remove(address)) for _ in range(0, 5)]
for transaction_creator in transaction_creators:
    transaction_creator.start()

miners = [Miner() for _ in range(0, 5)]
for miner in miners:
    miner.start()

try:
    while True:
        pass
except KeyboardInterrupt:
    for miner in miners:
        miner.stop_mining.set()
        miner.join()
    for tc in transaction_creators:
        tc.stop_sending.set()
        tc.join()
