# blockchain-sniffer

This project is based on https://github.com/sebicas/bitcoin-sniffer by @sebicas
and also pynode on https://github.com/jgarzik/pynode by @jgarzik

This sniffer realizes a X number of connections (set maxConnections variable) to different blockchain nodes and listen to 
every transaction or new block. Also storing transactions on postgresql with asyncore and a not completed feature to 
parse transactions scriptPubKey into respectives opcodes.

TODO: migrate to python3
