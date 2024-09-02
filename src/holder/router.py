from fastapi import APIRouter, HTTPException
from src.holder.auth import get_userId
from src.holder.models import Holder
from src.holder.utils import check_nft
from .schemas import WalletSchema
from .proof import convert_ton_proof_message, check_proof

router = APIRouter(
    tags=["holder"]
)

@router.post("/check")
async def check(data: WalletSchema):
    userId = await get_userId(data.initData)

    address = data.wallet['account']['address']

    parsed = convert_ton_proof_message(data.wallet)

    flag = check_proof(address, parsed, userId)
    
    if not flag:
        raise HTTPException(status_code=403, detail="Forbidden")

    holder = await Holder.get_or_none(address=address)
    if not holder:
        if await check_nft(address):
            return await Holder.create(id=userId, address=address)
        else:
            raise HTTPException(status_code=403, detail="You are not the owner of the owls")
    else:
        raise HTTPException(status_code=403, detail="This wallet is already in use")