from flask import Flask, request, jsonify, render_template, redirect, url_for, make_response
import sub
from web3 import Web3
import json
import paho.mqtt.client as mqtt
from time import time
from web3.middleware import geth_poa_middleware

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def main():
    return render_template('index3.html')


@app.route('/data', methods=["POST", "GET"])
def data():
    x, y = sub.getdaya()

    data = [time() * 1000, x, y]

    response = make_response(json.dumps(data))

    response.content_type = 'application/json'

    return response
    

if __name__=="__main__":
    app.run(debug=True)
