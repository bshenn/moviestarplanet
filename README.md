# moviestarplanet
 A comprehensive asynchronous library designed for seamless interaction with both MovieStarPlanet 1 and 2 APIs

```python
from moviestarplanet import MSPAsyncClient
from moviestarplanet.entities import *
from typing import List
import asyncio

async def main():
    msp = MSPAsyncClient(None, 10)

    login = await msp.login_async("VanjaBunny7", "lol999", "fr")

   
    msp2_ = msp.MSP2AsyncClient(accessToken=login.AccessToken, profileId=login.ProfileId)

    ##  search for profiles

    list_profiles: List[SearchProfileResult] = await msp2_.get_profile_search_async(server="fr", username="poupinie")
    first_profile_found: str = list_profiles[0].id

    profile_basic_info: List[GetProfilesResult] = await msp2_.get_profiles_async([first_profile_found])

    print(profile_basic_info[0].avatar.full)
    print(profile_basic_info[0].culture)


asyncio.run(
    main=main()
)
```
