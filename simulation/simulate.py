from __future__ import print_function
# from simulation.miner import Miner
from rpc import create_rpc_connection

# miners = [Miner() for _ in range(0, 5)]
# for miner in miners:
#     miner.start()

rpc_conn = create_rpc_connection()
print(rpc_conn.getpeerinfo())
