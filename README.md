# moviestarplanet
 A comprehensive asynchronous library designed for seamless interaction with both MovieStarPlanet 1 and 2 APIs

MovieStarPlanet2 Profile Gathering
```python
list_profiles: List[SearchProfileResult] = await msp2_.get_profile_search_async(server="fr", username="poupinie")
profile_basic_info: List[GetProfilesResult] = await msp2_.get_profiles_async([list_profiles[0].id])

...
```

MovieStarPlanet2 Common Services
```python
attributes: Attributes = await msp2_.get_attributes_async(list_profiles[0].id)
print(attributes.additionalData.WAYD)

## Sends a normal greetings
sent: bool = msp2._send_autograph_async(list_profiles[0].id)
```
