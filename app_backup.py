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

# Define a simple HTML template for displaying transaction data
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Bitcoin Transaction Information</title>
</head>
<body>
    <h1>Bitcoin Transaction Details</h1>
    <form action="/" method="POST">
        <label for="txid">Transaction ID:</label>
        <input type="text" id="txid" name="txid" required>
        <button type="submit">Get Transaction Info</button>
    </form>
    <br>
    {% if transaction %}
    <h2>Transaction Info for {{ txid }}</h2>
    <pre>{{ transaction }}</pre>
    {% else %}
    {% if error %}
    <p style="color:red;">Error: {{ error }}</p>
    {% endif %}
    {% endif %}
    
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
            poc = PoC(txid, address, time, fee, blockheight, dtype, raw_hex, decoded_data)

        except Exception as e:
            error = f"Error occurred at getting (gettransaction): {str(e)}"

    # Render the HTML page
    return render_template_string(HTML_TEMPLATE, txid=txid,transaction=json.dumps(transaction, indent=4) if transaction else None, error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
