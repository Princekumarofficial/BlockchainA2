# Bitcoin Scripting Assignment Report

This repository contains the code and documentation for the Bitcoin Scripting Assignment, completed as part of CS 216: Introduction to Blockchain. The report demonstrates our implementation and analysis of Bitcoin transactions using both Legacy (P2PKH) and SegWit (P2SH-P2WPKH) address formats.

## Team Information

**Team Name:** symmetrical octo sniffle  
**Team Members:**  
- Yash Vijay Kumbhkarn (230001083)  
- Vikrant (230001082)  
- Prince Kumar (230051013)

## Overview

The assignment involved interacting with the Bitcoin Core daemon in regtest mode to create and analyze transactions. We focused on understanding Bitcoin's scripting mechanisms for transaction validation and comparing the two transaction formats in terms of size and efficiency.

## Environment Setup

- **Bitcoin Core Version:** v25.0 (regtest mode)
- **Programming Language:** Python 3.9
- **Library:** bitcoinrpc (for interacting with the Bitcoin daemon)
- **Configuration Parameters:**
- **Credentials are in config.txt file**

## Transaction Flows and Analysis

### Part 1: Legacy P2PKH Transactions

#### Workflow

1. **Address Generation:**  
   - Three legacy addresses were created: Address A, Address B, and Address C.

2. **Mining:**  
   - Mined 105 blocks to ensure coins became spendable (coins from the first 100 blocks matured).

3. **Funding:**  
   - Funded Address A with 10 BTC.

4. **Transactions:**  
   - **Transaction A → B:** Sent 1.0 BTC from Address A to Address B.
   - **Transaction B → C:** Used the UTXO from the A→B transaction to send 0.5 BTC from Address B to Address C.

#### Script Execution Flow

- **Input Script (ScriptSig):** Contains the signature and public key.
- **Output Script (ScriptPubKey):** Consists of operations: `OP_DUP`, `OP_HASH160`, `OP_EQUALVERIFY`, and `OP_CHECKSIG`.
- **Validation Process:**  
  The scripts are concatenated and executed step-by-step: pushing data to the stack, duplicating the public key, hashing, verifying the public key hash, and finally checking the signature.

### Part 2: P2SH-SegWit Address Transactions

#### Workflow

1. **Address Generation:**  
   - Three P2SH-SegWit addresses were created: Address A', Address B', and Address C'.

2. **Funding:**  
   - Funded Address A' with 10 BTC.

3. **Transactions:**  
   - **Transaction A' → B':** Sent 1.0 BTC from Address A' to Address B'.
   - **Transaction B' → C':** Utilized the UTXO from the A'→B' transaction to send 0.5 BTC from Address B' to Address C'.

#### Script Execution Flow

- **Input Script (ScriptSig):** Contains only the redeem script.
- **Witness Data:** Holds the signature and public key, moved outside the main transaction data.
- **Output Script (ScriptPubKey):** Uses `OP_HASH160` and `OP_EQUAL`.
- **Validation Process:**  
  First, the redeem script is verified through P2SH validation. Then, the witness data (signature and public key) is used to validate the transaction, ensuring that the transaction ID is protected from malleability.

### Comparison and Key Benefits

- **Transaction Size:**  
  - **Legacy P2PKH:** Approximately 225 bytes (or vbytes).  
  - **P2SH-P2WPKH:** Physical size is around 247 bytes but with a reduced virtual size of 166 vbytes due to the segregation of witness data.
  
- **Advantages of SegWit Transactions:**  
  - **Reduced Transaction Fees:** Lower virtual sizes lead to lower fees.
  - **Transaction Malleability Fix:** The transaction ID is immune to signature manipulations since the witness data is excluded from the transaction hash.
  - **Increased Block Capacity:** The witness discount allows more transactions to be included in a block.
  - **Future-proofing:** Introduces script versioning, paving the way for protocol upgrades.
  - **Efficient Signature Operation Counting:** Ensures linear scaling and mitigates potential DoS attacks.

## Conclusion

This assignment provided hands-on experience with Bitcoin's transaction mechanisms. By comparing Legacy and SegWit transactions, we highlighted the structural differences, efficiency improvements, and benefits of using SegWit. For detailed analysis, refer to the complete report.

---
**Reference:** Bitcoin Scripting Assignment Report (CS 216: Introduction to Blockchain)
