# blockchain-sniffer

This project is based on https://github.com/sebicas/bitcoin-sniffer by @sebicas
and also pynode on https://github.com/jgarzik/pynode by @jgarzik

This sniffer realizes a X number of connections (set maxConnections variable) to different blockchain nodes and listen to 
every transaction or new block. Also storing transactions on postgresql with psycopg2 and a not completed feature to 
parse transactions scriptPubKey into respectives opcodes.

# Running

Make sure you have python2.7 with pip installed.

Create a database named transactions on postgresql and configure psycopg2

`pip install requests`

`python2.7 main.py`


# TODO 
- migrate to python3
- finishe opcodes parser
- store CtxIn transaction objects
