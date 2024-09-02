import nacl.signing
from tonsdk.boc import Cell

import hashlib
import base64

received_state_init = "te6cckECFgEAAwQAAgE0AgEAUQAAAAApqaMXrSOjAEGjfrapwohCsPqW846ZR6wMU9f8llvhHvNM+2dAART/APSkE/S88sgLAwIBIAkEBPjygwjXGCDTH9Mf0x8C+CO78mTtRNDTH9Mf0//0BNFRQ7ryoVFRuvKiBfkBVBBk+RDyo/gAJKTIyx9SQMsfUjDL/1IQ9ADJ7VT4DwHTByHAAJ9sUZMg10qW0wfUAvsA6DDgIcAB4wAhwALjAAHAA5Ew4w0DpMjLHxLLH8v/CAcGBQAK9ADJ7VQAbIEBCNcY+gDTPzBSJIEBCPRZ8qeCEGRzdHJwdIAYyMsFywJQBc8WUAP6AhPLassfEss/yXP7AABwgQEI1xj6ANM/yFQgR4EBCPRR8qeCEG5vdGVwdIAYyMsFywJQBs8WUAT6AhTLahLLH8s/yXP7AAIAbtIH+gDU1CL5AAXIygcVy//J0Hd0gBjIywXLAiLPFlAF+gIUy2sSzMzJc/sAyEAUgQEI9FHypwICAUgTCgIBIAwLAFm9JCtvaiaECAoGuQ+gIYRw1AgIR6STfSmRDOaQPp/5g3gSgBt4EBSJhxWfMYQCASAODQARuMl+1E0NcLH4AgFYEg8CASAREAAZrx32omhAEGuQ64WPwAAZrc52omhAIGuQ64X/wAA9sp37UTQgQFA1yH0BDACyMoHy//J0AGBAQj0Cm+hMYALm0AHQ0wMhcbCSXwTgItdJwSCSXwTgAtMfIYIQcGx1Z70ighBkc3RyvbCSXwXgA/pAMCD6RAHIygfL/8nQ7UTQgQFA1yH0BDBcgQEI9ApvoTGzkl8H4AXTP8glghBwbHVnupI4MOMNA4IQZHN0crqSXwbjDRUUAIpQBIEBCPRZMO1E0IEBQNcgyAHPFvQAye1UAXKwjiOCEGRzdHKDHrFwgBhQBcsFUAPPFiP6AhPLassfyz/JgED7AJJfA+IAeAH6APQEMPgnbyIwUAqhIb7y4FCCEHBsdWeDHrFwgBhQBMsFJs8WWPoCGfQAy2kXyx9SYMs/IMmAQPsABqk+PMQ="
received_address = "0:9ee12494825a1878d3c6773f4f8c51408e8459d3da53f6d776ff9c152ebe5cd2"

state_init = Cell.one_from_boc(base64.b64decode(received_state_init))

address_hash_part = base64.b16encode(state_init.bytes_hash()).decode('ascii').lower()
if received_address.endswith(address_hash_part):

        public_key = state_init.refs[1].bits.array[8:][:32]

        verify_key = nacl.signing.VerifyKey(bytes(public_key))


        received_timestamp = 1725300610
        signature = "s9cv/exFS6g7aYcFxIxCOOcD+UveNbQOTaD7vxbLb/s2IEl29+71krJQy3h1n7J2D+Kmazh6Vjc9LPbGhXO2Dw=="

        message = (b'ton-proof-item-v2/'
                + 0 .to_bytes(4, 'big') + state_init.bytes_hash()
                + 28 .to_bytes(4, 'little') + b'holder.notwise.co'
                + received_timestamp.to_bytes(8, 'little')
                + b'doc-example-aimesh777')



        signed = b'\xFF\xFF' + b'ton-connect' + hashlib.sha256(message).digest()

        print(hashlib.sha256(signed).digest())

        print(base64.b64decode(signature))

        verify_key.verify(hashlib.sha256(signed).digest(), base64.b64decode(signature))