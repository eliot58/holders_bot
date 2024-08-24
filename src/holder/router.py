from fastapi import APIRouter, Depends, HTTPException
from src.holder.auth import get_userId
from src.holder.models import Holder
from src.holder.utils import check_nft

router = APIRouter(
    tags=["holder"]
)

@router.post("/check")
async def check(address: str, userId: int = Depends(get_userId)):
    holder = await Holder.get_or_none(address=address)
    if not holder:
        if await check_nft(address):
            return await Holder.create(id=userId, address=address)
        else:
            raise HTTPException(status_code=403, detail="You are not the owner of the owls")
    else:
        raise HTTPException(status_code=403, detail="This wallet is already in use")