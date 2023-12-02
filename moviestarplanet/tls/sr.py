import aiohttp
from moviestarplanet.entities import AMFResult
from pyamf import remoting
from moviestarplanet.tls.tcy import t

async def sd(s: aiohttp.ClientSession, server: str, method: str, data: bytes, headers, proxy: str = None, custom_timeout: int = 10):
    async with s.post(f'https://ws-{server}.mspapis.com/Gateway.aspx?method={method}', data=data, headers=headers, proxy=proxy, timeout=aiohttp.ClientTimeout(total=custom_timeout)) as resp:
      
        rawbnytes = await resp.read()
    
        if resp.status == 200:
            try:
                return AMFResult(remoting.decode(rawbnytes)["/1"].body, resp.status, t(rawbnytes))
            except:
                return AMFResult(rawbnytes, resp.status, t(rawbnytes))
        
        else:
            return AMFResult(rawbnytes, resp.status, t(rawbnytes))
