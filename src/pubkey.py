# How to make PubKey using ARC4
from utils.arc4 import init_arc4, arc4_decrypt

# "https://ipfs.io/ipfs/bafybeihkoviema7g3gxyt6la7vd5ho32ictqbilu3wnlo3rs7ewhnp7lly"
data = b"DSL: bafybeigdyrzt5sfp7udm7hu76uh7y26nf3efuylqabf3oclgtqy55fbzdi; CMD: Generates a surreal image of a forest with floating orbs."
print(len(data), "data length must be 32x")

# encryption
cipher = init_arc4("6005ee8cc02e528e20c8e5ff71191723b0260391020862a03587a985f813dabe")
encryptor = cipher.encryptor()
encrypted = encryptor.update(data) + encryptor.finalize()
encrypted_hex = encrypted.hex()
print(encrypted_hex, '\n', len(encrypted_hex))

count = 1
hex_chunks = [encrypted_hex[i:i+64] for i in range(0, len(encrypted_hex), 64)]
fake_pubkeys = []
for chunk in hex_chunks:
    prefix = '02' if int(chunk, 16) % 2 == 0 else '03'
    fake_pubkey = prefix + chunk
    fake_pubkeys.append(fake_pubkey)
print(fake_pubkeys)

# decryption
result = ""
for i in fake_pubkeys:
    result += i[2:]

result = bytes.fromhex(result)
arc4_decrypt(cipher, result)
