from flask import Flask, request, render_template_string
from decoder import decode_multisig
import requests
import json
from poc import PoC
import logging

# Initialize Flask app
app = Flask(__name__)

# Bitcoin RPC credentials
RPC_USER = 'kh'
RPC_PASSWORD = '123'
RPC_PORT = 18332  # Testnet port
RPC_HOST = '10.0.0.176'  # Assuming local bitcoin-cli json-rpc server

# Sample TxID
# 9348f529d870dbd47c750db3cc00da0bc4825796b093afbd9ab892e9b798673b

# Define a simple HTML template for displaying transaction data
HTML_TEMPLATE = HTML_TEMPLATE = ''' 
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bitcoin Transaction Information</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f4f7f8;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            background-color: white;
            width: 90%;
            max-width: 700px;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            word-wrap: break-word; /* Automatically breaks long words */
        }
        h1 {
            color: #333;
            font-size: 24px;
            text-align: center;
            margin-bottom: 20px;
        }
        form {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: 30px;
        }
        form label {
            font-size: 16px;
            margin-right: 10px;
            color: #555;
        }
        form input {
            padding: 8px;
            font-size: 16px;
            width: 70%;
            margin-right: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        form button {
            padding: 8px 16px;
            font-size: 16px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        form button:hover {
            background-color: #0056b3;
        }
        ul {
            list-style: none;
            padding: 0;
        }
        ul li {
            background-color: #f9f9f9;
            margin-bottom: 10px;
            padding: 10px;
            border-radius: 5px;
            font-size: 14px;
            color: #444;
            overflow-wrap: break-word; /* Ensure long lines break */
        }
        ul li strong {
            color: #007bff;
        }
        a {
            color: #007bff;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        .error {
            color: red;
            text-align: center;
        }
        img {
            display: block;
            margin: 20px auto;
            max-width: 100%;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Bitcoin Transaction Details</h1>
        <form action="/" method="POST">
            <label for="txid">Tx ID:</label>
            <input type="text" id="txid" name="txid" required>
            <button type="submit">Go</button>
        </form>
        
        {% if poc %}
        <h2>PoC Decoder</h2>
        <h3>BITCOIN DATA</h3>
        <ul>
            <li><strong>txID:</strong> {{ poc.txid }}</li>
            <li><strong>Address:</strong> {{ poc.address }}</li>
            <li><strong>Timestamp:</strong> {{ poc.timestamp }}</li>
            <li><strong>Block Height:</strong> {{ poc.blockheight }}</li>
            <li><strong>Fee (BTC):</strong> {{ poc.fee_btc }}</li>
            <li><strong>Encoding:</strong> {{ poc.encoding }}</li>
            <li><strong>Raw Hex:</strong> {{ poc.rawhex }}</li>
            <li><strong>Raw UTF:</strong> {{ poc.rawutf }}</li>
            <li><strong>IPFS address:</strong> <a href="{{ poc.ipfs }}" target="_blank">{{ poc.ipfs }}</a></li>
            <li><strong>Mempool Explorer:</strong> <a href="{{ poc.mempool_url }}" target="_blank">{{ poc.mempool_url }}</a></li>
        </ul>
        {% if poc.ipfs %}
            <img src="{{ poc.ipfs }}" alt="IPFS Image">
        {% endif %}
        {% endif %}
        
        {% if error %}
        <p class="error">Error: {{ error }}</p>
        {% endif %}
    </div>
</body>
</html>
'''

# Bitcoin RPC call function
def bitcoin_rpc(method, params=[]):
    url = f"http://{RPC_HOST}:{RPC_PORT}/"
    headers = {'content-type': 'application/json'}
    payload = json.dumps({
        "method": method,
        "params": params,
        "jsonrpc": "1.0",
        "id": "curltest"
    })
    response = requests.post(url, data=payload, headers=headers, auth=(RPC_USER, RPC_PASSWORD))
    if response.status_code == 200:
        return response.json()['result']
    else:
        print(f"Web server error: {response.status_code}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    txid = None
    transaction = None
    poc = None
    error = None

    if request.method == 'POST':
        txid = request.form.get('txid')
        # Get raw transaction information
        try:
            transaction = bitcoin_rpc('gettransaction', [txid])
            if transaction is None:
                error = "Invalid Transaction ID or RPC Error."

            amount = transaction['amount']
            fee = transaction['fee']
            hex = transaction['hex']
            blockheight = transaction['blockheight']
            time = transaction['time']

            # Decode raw transaction for finding decoded PoC data
            decode_raw_transaction = bitcoin_rpc("decoderawtransaction",[hex])
            decoded_data, raw_hex, dtype, address = decode_multisig(decode_raw_transaction)
            poc = PoC(
                txid,
                address,
                time,
                fee*(-1),
                blockheight,
                dtype,
                raw_hex,
                decoded_data)

        except Exception as e:
            error = f"Error occurred at getting (gettransaction): {str(e)}"

    # Render the HTML page
    return render_template_string(HTML_TEMPLATE, txid=txid, poc=poc if poc else None, error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
