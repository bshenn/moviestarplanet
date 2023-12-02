# moviestarplanet
 A comprehensive asynchronous library designed for seamless interaction with both MovieStarPlanet 1 and 2 APIs

```python
from moviestarplanet import MSPAsyncClient
import asyncio

async def main():
    msp = MSPAsyncClient(proxy="your_proxy", timeout=custom_timeout)

    login = await msp.login_async(u, p, s)

    ## MSP2
    msp2_ = msp.MSP2AsyncClient(accessToken=login.AccessToken, profileId=login.ProfileId)

    ##search for profiles
    list_profiles: List[SearchProfileResult] = await msp2.get_profile_search_async(server="server", username="username")
    print(list_profiles[0].id) ## first profile found


asyncio.run(
    main=main()
)
```
