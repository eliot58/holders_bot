from pydantic import BaseModel


class WalletSchema(BaseModel):
    initData: str
    wallet: dict