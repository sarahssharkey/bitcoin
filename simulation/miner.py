from __future__ import print_function
from simulation.rpc import create_rpc_connection
from threading import Thread, Timer, Event
from random import randrange


class Miner(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.rpc_conn = create_rpc_connection()
        self.stop_mining = Event()

    def run(self):
        while not self.stop_mining.is_set():
            (start, end) = get_block_interval_range()
            t = Timer(randrange(start, end), self.create_block)
            t.start()

    def create_block(self):
        self.rpc_conn.generate(1)


def get_block_interval_range():
    target_time = float(2*60)
    return int(target_time - 0.1*target_time), int(target_time + 0.1*target_time)
