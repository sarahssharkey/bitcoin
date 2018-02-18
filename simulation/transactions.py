from simulation.rpc import create_rpc_connection
from threading import Thread, Event


class TransactionCreator(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.rpc_conn = create_rpc_connection()
        self.stop_sending = Event()

    def get_peers(self):
        peers = self.rpc_conn.getpeerinfo()
