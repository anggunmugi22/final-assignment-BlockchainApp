geth --networkid 4444 --mine --miner.threads 2 --datadir "." --nodiscover --rpc --rpcport "8545" --rpcaddr "192.168.12.7" --port "30303" --rpccorsdomain "*" --nat extip:192.168.12.7 --netrestrict 192.168.12.0/24 --rpcapi eth,web3,personal,net --unlock 0x4dE7b729F7e95b50eC5a16366135A8f19a3953EB --password ./password.sec --ipcpath "~/.ethereum/geth.ipc" --allow-insecure-unlock --nousb