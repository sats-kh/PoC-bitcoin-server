import decimal
from arc4 import arc4_decrypt, init_arc4

KEY = "6005ee8cc02e528e20c8e5ff71191723b0260391020862a03587a985f813dabe"

def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError

def decode_multisig(txhex):
    try:
        arc4_key = init_arc4(KEY)
        asm_fields = []
        decoded_data = ""
        raw_hex = ""
        dtype = ""
        address = ""
        for utxo in txhex['vout']:
            dtype = utxo['scriptPubKey'].get('type')
            address = utxo['scriptPubKey'].get('addresses')[2]
            if dtype == 'multisig':
                asm_fields.append(utxo['scriptPubKey']['asm'])
                asm_string = utxo['scriptPubKey']['asm']
                hex_strings = asm_string.split()[1:3]
                stripped_hex_strings = [hex_string[2:] for hex_string in hex_strings]
                raw_hex = raw_hex + ''.join(stripped_hex_strings)
        bytestring = bytes.fromhex(raw_hex)
        decoded_data = arc4_decrypt(arc4_key, bytestring)

    except Exception as e:
        error = f'Error occured at decoding multisig): {str(e)}'

    return decoded_data, raw_hex, dtype, address
