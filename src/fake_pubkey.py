from utils.arc4 import init_arc4, arc4_decrypt
# import queue

def concatednate_data(ipfs,phrase=None):
    dsl_ipfs = "DSL: " + ipfs + ";"
    cmd_phrase = ""
    if phrase != None:
        cmd_phrase = " CMD: " + phrase +";"

    concatenated_data = dsl_ipfs + cmd_phrase

    if len(concatenated_data) % 64 != 0:
        concatenated_data += "0" * (64 - len(concatenated_data) % 64)
        return bytes(concatenated_data, 'utf-8')
    else:
        return bytes(concatenated_data, 'utf-8')

def encrypt_data (ipfs, phrase):
    cipher = init_arc4("6005ee8cc02e528e20c8e5ff71191723b0260391020862a03587a985f813dabe")
    concatenated_data = concatednate_data(ipfs, phrase)
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(concatenated_data) + encryptor.finalize()
    encrypted_hex = encrypted.hex()
    # print(encrypted_hex, '\n', len(encrypted_hex))
    return encrypted_hex

# Example of create_fake_pubkey
encrypted = encrypt_data("QmbT3wUErXndX2YU8ih8AkJQgazX5gGQvyb8b26caxaW4K", "helloworld")

def create_fake_pubkeys(ipfs, phrase):
    encrypted_hex = encrypt_data(ipfs, phrase)

    hex_chunks = [encrypted_hex[i:i+64] for i in range(0, len(encrypted_hex), 64)]
    # print(hex_chunks)
    # fake_pubkeys = queue.Queue()
    fake_pubkeys = []
    for chunk in hex_chunks:
        prefix = '02' if int(chunk, 16) % 2 == 0 else '03'
        fake_pubkey = prefix + chunk
        # fake_pubkeys.put(fake_pubkey)
        fake_pubkeys.append(fake_pubkey)

    return fake_pubkeys

# Example of create_pubkeys
fake_pubkeys = create_fake_pubkeys("QmbT3wUErXndX2YU8ih8AkJQgazX5gGQvyb8b26caxaW4K", "hello world")

# fake_pubkeys.get()

def decrypt_pubkes(pubkeys):
    raise NotImplemented


