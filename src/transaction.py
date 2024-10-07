"tb1qk2uvd444ha39jyey9jmehlya3dpc2vykjd5meg"

from pybtc import *

a1 = Address("cVKyUF5j3Lx43Kh3AEwfMBrj9cDLcrjWy5yf8Za3gfbVE1XSYP26")
a2 = Address("cW4KX5N8fUCmAcdn9dSCLgnEYSpmCSnpTBPVyEudHsjZtADkzK5u")
a3 = Address("cNiKhw2fAmUMTneBTRQQNnfa2x36Zs8v1UGiGfc2dTx3Bqvn1uKY")


script_1 = b"".join([OP_1,
                   op_push_data("03807d4cb06ef628e2a790b03cc84bc28777df3cae559492cc950e70b77116698b"),
                   op_push_data("022d99046c64354bc867d21cf90a224b89dc79e17bc40782bb1a3564ccea3c885c"),
                   op_push_data("02d86b51a7a42e31fb6feea675b2c41d8b3eae6c9ddb5880fc2635051190e109f8"),
                   OP_3, OP_CHECKMULTISIG])

script_2 = b"".join([OP_1,
                   op_push_data("024548c428862b741a4fe93cd185bf930b41fcae0642ec0bec65019c8806f24c50"),
                   op_push_data("03843247193be8dd3bca9ca997dd5ad544f404833ca043659704cfb78ac8e10f8d"),
                   op_push_data("02d86b51a7a42e31fb6feea675b2c41d8b3eae6c9ddb5880fc2635051190e109f8"),
                   OP_3, OP_CHECKMULTISIG])


tx = Transaction(testnet=True)
tx.add_input("42ce0d6e2abb3d0014bdc320a6ab053c3e69de43c9a22f16c896be1a4058d329", 0)
tx.add_output(800, script_pub_key=script_1)
tx.add_output(800, script_pub_key=script_2)
tx.serialize()
tx.sign_input(0, private_key="cSM3kuwfLikfxyGDwz3qnq7JxkrPVa7dWqjU83YFXeG4ZbuQ1H2d", address="tb1q4kf79ynx9nzxtjy0lj7gak060lam3u8puua2kw")

