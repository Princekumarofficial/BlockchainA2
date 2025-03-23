from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from decimal import Decimal

# RPC Connection setup
RPC_USER = 'bitcoin'
RPC_PASSWORD = 'bitcoin'
RPC_PORT = 18443
WALLET_NAME = 'assignment_wallet_legacy'

rpc_connection = AuthServiceProxy(f'http://{RPC_USER}:{RPC_PASSWORD}@127.0.0.1:{RPC_PORT}')

# Wallet handling
try:
    wallets = rpc_connection.listwallets()
    if WALLET_NAME in wallets:
        rpc_connection.unloadwallet(WALLET_NAME)
    rpc_connection.loadwallet(WALLET_NAME)
except JSONRPCException as e:
    if e.error['code'] == -18:  # Wallet not found
        rpc_connection.createwallet(WALLET_NAME)
    else:
        raise

wallet = AuthServiceProxy(f'http://{RPC_USER}:{RPC_PASSWORD}@127.0.0.1:{RPC_PORT}/wallet/{WALLET_NAME}')

def mine_blocks(n):
    block_hashes = rpc_connection.generatetoaddress(n, wallet.getnewaddress())
    # print(f"Mined {n} blocks: {block_hashes}")

def create_and_send_tx(from_address, to_address, amount):
    print(f"\nCreating transaction from {from_address} to {to_address} for {amount} BTC")
    inputs = wallet.listunspent(1, 9999999, [from_address])
    print(f"Available UTXOs: {inputs}")
    input_amount = sum(Decimal(input['amount']) for input in inputs)
    if input_amount < amount:
        raise ValueError("Insufficient funds")

    change = input_amount - amount - Decimal('0.0001')  # 0.0001 BTC fee
    raw_tx = wallet.createrawtransaction(
        [{"txid": input['txid'], "vout": input['vout']} for input in inputs],
        {to_address: float(amount), from_address: float(change)}
    )
    print(f"Raw transaction created: {raw_tx}")
    signed_tx = wallet.signrawtransactionwithwallet(raw_tx)
    print(f"Signed transaction: {signed_tx}")
    tx_id = wallet.sendrawtransaction(signed_tx['hex'])
    print(f"Transaction broadcasted with txid: {tx_id}")
    return tx_id

def analyze_transaction(tx_id, description):
    decoded = wallet.decoderawtransaction(wallet.getrawtransaction(tx_id))
    print(f"\n=== {description} ===")
    print(f"Transaction ID: {tx_id}")
    print("Input:")
    for vin in decoded['vin']:
        print(f"  TxID: {vin['txid']}")
        print(f"  Vout: {vin['vout']}")
        if 'scriptSig' in vin:
            print("  ScriptSig:")
            print(f"    {vin['scriptSig']['asm']}")
    print("Outputs:")
    for vout in decoded['vout']:
        print(f"  Amount: {vout['value']} BTC")
        print("  ScriptPubKey:")
        print(f"    {vout['scriptPubKey']['asm']}")
    print(f"Transaction size: {decoded['size']} bytes")
    print(f"Transaction vsize: {decoded['vsize']} vbytes")
    return decoded

# LEGACY P2PKH TRANSACTIONS
print("\n=== Legacy P2PKH Transactions ===")
addr_A = wallet.getnewaddress("", "legacy")
addr_B = wallet.getnewaddress("", "legacy")
addr_C = wallet.getnewaddress("", "legacy")
print(f"Address A: {addr_A}\nAddress B: {addr_B}\nAddress C: {addr_C}")

mine_blocks(105)
fund_txid = wallet.sendtoaddress(addr_A, 10)
print(f"\nFunded Address A with txid: {fund_txid}")
mine_blocks(1)

tx_AB = create_and_send_tx(addr_A, addr_B, Decimal('1.0'))
decoded_AB = analyze_transaction(tx_AB, "Transaction A -> B (Legacy P2PKH)")
mine_blocks(1)

tx_BC = create_and_send_tx(addr_B, addr_C, Decimal('0.5'))
decoded_BC = analyze_transaction(tx_BC, "Transaction B -> C (Legacy P2PKH)")
mine_blocks(1)

print("\n=== Transaction Size Summary (Legacy) ===")
print(f"Legacy A->B size: {decoded_AB['size']} bytes, vsize: {decoded_AB['vsize']} vbytes")
print(f"Legacy B->C size: {decoded_BC['size']} bytes, vsize: {decoded_BC['vsize']} vbytes")