# moviestarplanet
 A comprehensive asynchronous library designed for seamless interaction with both MovieStarPlanet 1 and 2 APIs

MovieStarPlanet2 Profile Gathering
```python
list_profiles: List[SearchProfileResult] = await msp2_.get_profile_search_async(server="fr", username="poupinie")
first_profile_found: str = list_profiles[0].id

profile_basic_info: List[GetProfilesResult] = await msp2_.get_profiles_async([first_profile_found])

print(profile_basic_info[0].avatar.full)
print(profile_basic_info[0].culture)


asyncio.run(
    main=main()
)
```
