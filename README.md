# MovieStarPlanet Python Library
Welcome to the MovieStarPlanet Python Library, a comprehensive asynchronous toolkit designed for seamless interaction with both MovieStarPlanet 1 and 2 APIs. This library empowers developers to effortlessly access and manipulate MovieStarPlanet user profiles, common services, and official cheat functionalities.

# Initialize the class
```python
from moviestarplanet import MSPAsyncClient
msp1_ = MSPAsyncClient(proxy=..., timeout=...)
```

# Login to MSP1
Login to MSP1 and checks if the jsonwebtoken is not null
```python
login = await msp1_.login_async(username, password, server)
if login.AccessToken != None:
    ...
```

# Intialize the MovieStarPlanet2 Class
You need to initialize the MovieStarPlanet2 class with the login JWT and profileId.
```python
msp2_ = msp.MSP2AsyncClient(accessToken=login.AccessToken, profileId=login.ProfileId)
```

# MovieStarPlanet2 Profile Gathering
Easily retrieve MovieStarPlanet2 profiles and basic information with just a few lines of code:
```python
# Search for a profile and gather basic information
list_profiles: List[SearchProfileResult] = await msp2_.get_profile_search_async(server="fr", username="poupinie")
profile_basic_info: List[GetProfilesResult] = await msp2_.get_profiles_async([list_profiles[0].id])
```

# MovieStarPlanet2 Common Services
Access common services for a specific profile, including attributes, autograph sending, experience & more:
```python
# Retrieve profile attributes
attributes: Attributes  = await msp2_.get_attributes_async(list_profiles[0].id)

# Send an autograph
sent: bool = await msp2_.send_autograph_async(list_profiles[0].id)

# Get experience information
exp: Experience2 = await msp2_.get_experience_async(list_profiles[0].id)
```

# MovieStarPlanet2 Official Cheat Services
Take advantage of official cheat functionalities such as setting mood and changing gender effortlessly:
```python
# Set mood to 'bunny_hold'
await msp2_.set_mood_async(mood_asset='bunny_hold')

# Change gender
await msp2_.change_gender_async()
```

 # Messaging System & Examples
 Explore the messaging system with ease, including fetching conversations and participant details:
 ```python
# Get the latest conversations
conversations: List[Conversation] = await msp2_.get_conversations_async(size=10)

# Access participant information from the first conversation
first_participant, second_participant = conversations[0].participants[0], conversations[0].participants[1]
```
