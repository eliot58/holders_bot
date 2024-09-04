import base64
import hashlib
import time
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from tonsdk.boc import Cell



def signature_verify(pubkey: bytes, message: bytes, signature: bytes) -> bool:
    try:
        verify_key = VerifyKey(pubkey)
        verify_key.verify(message, signature)
        return True
    except BadSignatureError:
        return False

def convert_ton_proof_message(tp):
    try:
        sig = base64.b64decode(tp["connectItems"]["tonProof"]["proof"]["signature"])

        parsed_message = {
            'address': tp['account']['address'],
            'domain': tp["connectItems"]["tonProof"]["proof"]["domain"],
            'timestamp': tp["connectItems"]["tonProof"]["proof"]["timestamp"],
            'payload': tp["connectItems"]["tonProof"]["proof"]["payload"],
            'signature': sig,
            'state_init': tp['account']['walletStateInit']
        }

        return parsed_message
    except Exception as e:
        return None
    
def create_message(message, payload):
    try:
        wc = int(message['address'].split(":")[0]).to_bytes(4, byteorder='big', signed=True)

        ts = message['timestamp'].to_bytes(8, byteorder='little', signed=True)

        dl = message['domain']['lengthBytes'].to_bytes(4, byteorder='little', signed=True)
        

        m = bytearray("ton-proof-item-v2/".encode())
        m.extend(wc)
        m.extend(bytes.fromhex(message['address'].split(":")[1]))
        m.extend(dl)
        m.extend(message['domain']['value'].encode())
        m.extend(ts)
        m.extend(payload.encode())

        message_hash = hashlib.sha256(m).digest()

        full_mes = bytearray(b'\xff\xff')
        full_mes.extend("ton-connect".encode())
        full_mes.extend(message_hash)

        res = hashlib.sha256(full_mes).digest()

        return res
    except Exception as e:
        return None

def check_proof(address, ton_proof_req, payload):
    try:
        state_init = Cell.one_from_boc(base64.b64decode(ton_proof_req['state_init']))
        address_hash_part = base64.b16encode(state_init.bytes_hash()).decode('ascii').lower()
        
        if address.endswith(address_hash_part):
            pub_key = state_init.refs[1].bits.array[8:][:32]

        if time.time() > ton_proof_req['timestamp'] + 300000:
            return False

        if ton_proof_req['domain']['value'] != "holder.notwise.co":
            return False
        
        mes = create_message(ton_proof_req, payload)
        if not mes:
            return False
        
        
        return signature_verify(bytes(pub_key), mes, ton_proof_req["signature"])
    except Exception as e:
        return False

