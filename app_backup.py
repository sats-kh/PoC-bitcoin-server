from flask import Flask, request, render_template
from src.decoder import decode_multisig
import os
from src.poc import PoC
from utils.helper import allowed_file
from werkzeug.utils import secure_filename
from utils.ipfs_api import upload_to_ipfs
from src.bitcoin_rpc import bitcoin_rpc
from src.bitcoin_function import create_raw_transaction, sign_raw_transaction_with_privkey, send_rawtransaction

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 512 * 512

# Define a simple HTML template for displaying transaction data
INDEX_TEMPLATE = 'index.html'
CREATE_TRANSACTION_TEMPLATE = 'createtransaction.html'

# Sample TxID
# 9348f529d870dbd47c750db3cc00da0bc4825796b093afbd9ab892e9b798673b
# 0598bda798c7d11e52bf597f725a13346708a4618138f67e6c6aad0d33bf72c2

@app.route('/createtransaction', methods=['GET', 'POST'])
def createtransaction():
    error = None
    txid = None
    phrase = None
    cid = None

    if request.method == 'POST':
        if 'file' not in request.files:
            error = "No file part"
        else:
            file = request.files['file']

            if file.filename == '':
                error = "No selected file"
            elif file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                # User input messages
                phrase = request.form.get('phrase')
                print(f"Uploaded file: {filename}")
                print(f"Phrase: {phrase}")
                try:
                    cid = upload_to_ipfs("./" + file_path)
                    serialized_tx, inTxid = create_raw_transaction(cid, phrase)
                    sig = sign_raw_transaction_with_privkey(serialized_tx, inTxid)
                    txid = send_rawtransaction(sig)
                    print(txid)

                except Exception as e:
                    error = f"Error occurred at adding (file to ipfs daemon): {str(e)}"
            else:
                error = "Invalid file format. Only PNG, JPG, JPEG, GIF are allowed."

    return render_template('createtransaction.html', error=error, txid=txid, cid=cid, phrase=phrase)

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
            blockheight = None
            time = transaction['time']
            try :
                blockheight = transaction['blockheight']
            except:
                blockheight = "Waiting for it to appear in the mempool..."

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
    return render_template(INDEX_TEMPLATE, txid=txid, poc=poc if poc else None, error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
