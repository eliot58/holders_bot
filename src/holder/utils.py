import aiohttp
from src.config.settings import TONAPI, COLLECTION

async def check_nft(account_id):
    url = f'https://tonapi.io/v2/accounts/{account_id}/nfts'
    data = {
        'collection': COLLECTION,
        'limit': 1000,
        'offset': 0,
        'indirect_ownership': True
    }
    headers = {
        "Authorization": f"Bearer {TONAPI}"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, data=data, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return bool(data["nft_items"])
            