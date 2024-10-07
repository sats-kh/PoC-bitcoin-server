import json, requests

# Bitcoin RPC credentials
RPC_USER = 'kh'
RPC_PASSWORD = '123'
RPC_PORT = 18332  # Testnet port
RPC_HOST = '10.0.0.176'  # Assuming local bitcoin-cli json-rpc server

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
        print(f"BITCOIN RPC ERROR: {response.status_code}")
        return None
