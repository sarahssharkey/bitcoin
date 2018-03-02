from simulation.rpc import create_rpc_connection
from threading import Thread, Event
from random import choice, randint
from time import sleep


class TransactionCreator(Thread):
    def __init__(self, addresses):
        Thread.__init__(self)
        self.rpc_conn = create_rpc_connection()
        self.addresses = addresses
        self.stop_sending = Event()

    def send_dummy_transaction(self):
        peer = choice(self.addresses)
        balance = self.rpc_conn.getbalance()
        if balance < 1:
            return
        self.rpc_conn.sendtoaddress(peer, randint(1, balance))

    def run(self):
        while not self.stop_sending.is_set():
            self.send_dummy_transaction()
            sleep(1)
