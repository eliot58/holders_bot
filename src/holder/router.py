from fastapi import APIRouter, Depends, HTTPException
from src.holder.auth import get_userId
from src.holder.models import Holder
from src.holder.utils import check_nft
import nacl.signing
from tonsdk.boc import Cell
import hashlib
import base64
from nacl.exceptions import BadSignatureError

router = APIRouter(
    tags=["holder"]
)

@router.post("/check")
async def check(wallet: dict, userId: int = Depends(get_userId)):

    address = wallet["account"]["address"]

    state_init = Cell.one_from_boc(base64.b64decode(wallet["account"]["walletStateInit"]))

    address_hash_part = base64.b16encode(state_init.bytes_hash()).decode('ascii').lower()
    assert address.endswith(address_hash_part)

    public_key = state_init.refs[1].bits.array[8:][:32]

    verify_key = nacl.signing.VerifyKey(bytes(public_key))

    received_timestamp = wallet["connectItems"]["tonProof"]["proof"]["timestamp"]

    signature = wallet["connectItems"]["tonProof"]["proof"]["signature"]

    message = (b'ton-proof-item-v2/'
            + 0 .to_bytes(4, 'big') + state_init.bytes_hash()
            + 28 .to_bytes(4, 'little') + b'holder.notwise.com'
            + received_timestamp.to_bytes(8, 'little')
            + bytes(userId))

    signed = b'\xFF\xFF' + b'ton-connect' + hashlib.sha256(message).digest()
    try:
        verify_key.verify(hashlib.sha256(signed).digest(), base64.b64decode(signature))
    except BadSignatureError:
        raise HTTPException(status_code=403, detail="Forbidden")

    holder = await Holder.get_or_none(address=address)
    if not holder:
        if await check_nft(address):
            return await Holder.create(id=userId, address=address)
        else:
            raise HTTPException(status_code=403, detail="You are not the owner of the owls")
    else:
        raise HTTPException(status_code=403, detail="This wallet is already in use")