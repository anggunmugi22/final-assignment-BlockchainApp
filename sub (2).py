from web3 import Web3
import json
import paho.mqtt.client as mqtt
import time
from web3.middleware import geth_poa_middleware
import sys


url = "HTTP://192.168.12.5:8545"
web3 = Web3(Web3.HTTPProvider(url))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)
web3.eth.defaultAccount = web3.eth.accounts[0]

abi = json.loads('[{"constant": true,"inputs": [],"name": "getDaya","outputs": [{"internalType": "string","name": "","type": "string"}],"payable": false,"stateMutability": "view","type": "function"},{"constant": false,"inputs": [{"internalType": "string","name": "_daya","type": "string"}],"name": "setData","outputs": [],"payable": false,"stateMutability": "nonpayable","type": "function"}]')
bytecode = '608060405234801561001057600080fd5b5061030f806100206000396000f3fe608060405234801561001057600080fd5b50600436106100365760003560e01c8063105061fb1461003b57806347064d6a146100be575b600080fd5b610043610179565b6040518080602001828103825283818151815260200191508051906020019080838360005b83811015610083578082015181840152602081019050610068565b50505050905090810190601f1680156100b05780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b610177600480360360208110156100d457600080fd5b81019080803590602001906401000000008111156100f157600080fd5b82018360208201111561010357600080fd5b8035906020019184600183028401116401000000008311171561012557600080fd5b91908080601f016020809104026020016040519081016040528093929190818152602001838380828437600081840152601f19601f82011690508083019250505050505050919291929050505061021b565b005b606060008054600181600116156101000203166002900480601f0160208091040260200160405190810160405280929190818152602001828054600181600116156101000203166002900480156102115780601f106101e657610100808354040283529160200191610211565b820191906000526020600020905b8154815290600101906020018083116101f457829003601f168201915b5050505050905090565b8060009080519060200190610231929190610235565b5050565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f1061027657805160ff19168380011785556102a4565b828001600101855582156102a4579182015b828111156102a3578251825591602001919060010190610288565b5b5090506102b191906102b5565b5090565b6102d791905b808211156102d35760008160009055506001016102bb565b5090565b9056fea265627a7a72315820655ea62a25f14526f3a0e85f12b47a98d385408f852d31c434f90b7bb8adab2e64736f6c634300050b0032'
constructor = web3.eth.contract(abi=abi, bytecode=bytecode)

tx_hash = constructor.constructor().transact()

tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
contract = web3.eth.contract(
    address=tx_receipt.contractAddress,
    abi=abi
)
daya = 0.0
blockhash = ""

def on_connect(client, userdata, flags, rc):
    print("Broker Connected!!!")
    client.subscribe("Data")

def on_message(client, userdata, message):
    t = (message.payload)
    print(t)
    size = sys.getsizeof(t)
    print(size)
    start_time3 = time.time() #delay konsensus
    tx_hash = contract.functions.setData(t).transact()
    print(tx_hash)
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    print('tx_receipt = ', tx_receipt)
    end_time3 = time.time() #delay konsensus
    print("delay3: ", end_time3 - start_time3)
    global daya
    daya = contract.functions.getDaya().call()
    print("dayasub = ", daya)
    global blockhash
    block = web3.eth.getBlock('latest') 
    print(block)
    blockhash = block['hash'].hex()
    print(blockhash)

def getdaya():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("192.168.1.14", 1883, 60)
    client.loop_forever()
    return daya, blockhash
