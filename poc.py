from datetime import datetime, timezone, timedelta

def convert_timestamp(time):
    utc_time = datetime.fromtimestamp(time, tz=timezone.utc)
    kst_time = utc_time + timedelta(hours=9)
    formatted_time = kst_time.strftime('%Y-%m-%d %H:%M:%S')

    return formatted_time

def parse_dsl_to_ipfs(raw_utf):
    # Convert the bytes to string and split to get the hash after 'DSL:'
    decoded_str = raw_utf.decode('utf-8')

    if 'DSL:' in decoded_str:
        # Extract the hash part after 'DSL:'
        ipfs_hash = decoded_str.split('DSL:')[1].strip()

        # Create the IPFS link
        ipfs_url = f"https://ipfs.io/ipfs/{ipfs_hash}"
        return ipfs_url
    else:
        return "Invalid DSL format"


def parse_txid_to_mempool(txid):
    mempool_url = f"https://mempool.space/testnet/tx/{txid}"
    return mempool_url


class PoC:
    def __init__(self, txid="", address="", time="", fee="", blockheight="", encoding="", raw_hex="", raw_utf=""):
        self.txid = txid
        self.address = address
        self.timestamp = convert_timestamp(time)
        self.fee_btc = fee
        self.blockheight = blockheight
        self.encoding = encoding
        self.rawhex = raw_hex
        self.rawutf = raw_utf
        self.ipfs = parse_dsl_to_ipfs(raw_utf)
        self.mempool_url = parse_txid_to_mempool(txid)

    def __repr__(self):
        print(self.txid, self.address, self.timestamp, self.fee_btc, self.blockheight, self.encoding, self.rawutf, self.rawutf)

    def get_params(self, txid, address, time, blockheight, fee, encoding, raw_hex, raw_utf):
        return self.__class__(txid, address, time, blockheight, fee, encoding, raw_hex, raw_utf)
