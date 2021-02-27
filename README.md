# blockchain-sniffer

This project is based on https://github.com/sebicas/bitcoin-sniffer by @sebicas
and also pynode pynode on https://github.com/jgarzik/pynode  by @jgarzik

This sniffer realizes a X number connections (set maxConnections variable) to different blockchain nodes and listen to 
every transactions or new blocks. Also storing transactions on postgresql with asyncore and a not completed feature to 
parse transactions scriptPubKey into respectives opcodes.
