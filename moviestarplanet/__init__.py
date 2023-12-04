import aiohttp as a
from aiohttp import TCPConnector
import hashlib as h
import binascii as b
from pyamf import ASObject as aob
from moviestarplanet.entities import AMFResult as lol
from moviestarplanet.entities import LoginResult as lr
from moviestarplanet.entities import GetProfilesResult, GetProfileSnapshot, SearchProfileResult, Experience2, Attributes, AttributesAdditionalData
from moviestarplanet.tls.h import rt
from moviestarplanet.tls.rq import bhtq
from moviestarplanet.tls.env import genv
from moviestarplanet.tls.construct import rty, get_session_id, calculate_checksum
from moviestarplanet.tls.sr import sd
from moviestarplanet.tls.px import set
from moviestarplanet.tls.tcy import t
from moviestarplanet.exceptions import *
from moviestarplanet.ej import Conversation
from pyamf import remoting, AMF3
import base64 as b2
import json as js
from typing import List
from datetime import datetime

class MSPAsyncClient:
    '''
    A comprehensive asynchronous library designed for seamless interaction with both MovieStarPlanet 1 and 2 APIs.\n
    Example Usage:
    ```python
       >>> msp = MSPAsyncClient(proxy="your_proxy", timeout=custom_timeout)
    ```
    
    Parameters:
    - `proxy` (str): A default HTTP proxy to use for your requests, providing flexibility in handling network configurations.
    - `timeout` (int): A custom timeout setting for requests, allowing you to control the duration before considering a request as unsuccessful.

    This library is specifically crafted for asynchronous operations, ensuring efficient communication with MovieStarPlanet APIs. With the provided proxy and timeout options, users can tailor the client to suit their network requirements and optimize their API interactions.

     Usage Tips:
    - Ensure your proxy is correctly formatted as a string (e.g., "http://your_proxy_address").
    - Adjust the timeout value based on your application's specific needs for responsiveness.

    '''
    def __init__(self, proxy: str = None, timeout: int = 10) -> None:
        self._c: t = a.ClientSession(connector=TCPConnector(
            ssl=False, limit=0, limit_per_host=0
        ))
        self._m, self._p, self._t = 0, proxy, timeout
        self.MSP2AsyncClient.session = self._c
        self._pid: str = None
        self.at: str = None

    class a_t:
        def __init__(self, _m: int = 0) -> None:
            self._i: int = _m
            self.l_b = None
        
        def head(self, ticket: str) -> aob:
            def g_lb(self):
                self._i+=1
                self.l_b = str(self._i).encode('utf-8')
                return self.l_b
            
            def g5(self):
                return h.md5(self.l_b).hexdigest()
             
            def h_x(self):
                return b.hexlify(self.l_b).decode()
            
            g_lb()
            return aob({"Ticket": ticket + g5() + h_x(), "anyAttribute": None})

    class MSP2AsyncClient:
        '''Asynchronous library for the MovieStarPlanet2 API.'''
        
        session: a.ClientSession = None
        def __init__(self, accessToken: str, profileId: str) -> None:
            self._at: str = accessToken
            self._hs = {'Authorization': f'Bearer {self._at}'}
            self.pid = profileId
        
        def get_profile_id_from_access_token(self):
            '''
            This deocde the logged in JWT and return the profileId key.
            Do not use.
            '''
            class JWTError(Exception):
                def __init__(self, message="JWT does not contains profileId key."):
                    self.message = message
                    super().__init__(self.message)
            try:
                d_b = b2.b64decode(self._at.split('.')[1])
                d_s = d_b.decode('utf-8')
                
                return js.loads(d_s)['profileId']
            except:
                return JWTError()
        
        
        async def _set_profile_id(self, profileId: str):
            self.pid = profileId

        async def get_profiles_async(self, profileIds: List[str]) -> List[GetProfilesResult]:
            '''
            Returns:
                List[GetProfilesResult]: List of profile results.

            Example Usage:
            ```python
            profiles: List[GetProfilesResult] = await msp2.get_profiles_async([profile_ids])
            print(profiles[0].culture)  
            ```
            '''
            json_data = {
                'query': 'query GetProfiles($profileIds: [String!]!, $gameId: String!){ profiles(profileIds: $profileIds){ id name culture avatar(preferredGameId: $gameId){ gameId face full } membership {currentTier lastTierExpiry } } }',
                'variables': '{"profileIds":' + js.dumps(profileIds) + ',"gameId":"j68d"}',
            }
            async with self.session.post('https://eu.mspapis.com/edgerelationships/graphql/graphql', json=json_data, headers=self._hs) as response:
                if response.status == 200:

                    parser = js.loads(await response.text())
                    profiles_data = parser.get('data', {}).get('profiles', [])
        
                    if not profiles_data:
                        gg = []
                        gg.append(GetProfilesResult(name=None, id=0, culture=None, avatar=GetProfileSnapshot(None, None)))
                        return gg

                    results = []
                    for profile_data in profiles_data:
                        avatar_data = profile_data.get('avatar', {})
            
                        results.append(GetProfilesResult(
                            name=profile_data.get('name'),
                            id=profile_data.get('id'),
                            culture=profile_data.get('culture'),
                            avatar=GetProfileSnapshot(
                                id=profile_data.get('id'),
                                full=avatar_data.get('full') if avatar_data else None,
                                face=avatar_data.get('face') if avatar_data else None
                            )
                        ))
                    return results
             
            
        async def get_profile_search_async(self, server: str,  username: str) -> List[SearchProfileResult]:
            '''
            Asynchronously retrieves a list of search results for a given username on a specified server.

            Returns:
                List[SearchProfileResult]: A list of search results, each represented by a SearchProfileResult object.

            Example:
            ```python
            list_profiles: List[SearchProfileResult] = await msp2.get_profile_search_async(server="server", username="username")
            
            for profile_result in list_profiles:
                print(profile_result.id)

            # Access the first found profile ID
            first_found: str = list_profiles[0].id
            ```
            '''
            if username == None:
                return [SearchProfileResult(id=None)]
            if self._at == None:
                return MissingJWT()

            json_data = {
                'query': 'query GetProfileSearch($region: String!, $startsWith: String!, $pageSize: Int, $currentPage: Int, $preferredGameId: String!) { findProfiles(region: $region, nameBeginsWith: $startsWith, pageSize: $pageSize, page: $currentPage) { totalCount nodes { id avatar(preferredGameId: $preferredGameId) { gameId face full } } } }',
                'variables': '{"region":"'+server+'","startsWith":"'+username+'","pageSize":50,"currentPage":1,"preferredGameId":"j68d"}',
            }
            async with self.session.post('https://eu.mspapis.com/edgerelationships/graphql/graphql', json=json_data, headers={'Authorization': f'Bearer {self._at}'}) as response:
                if response.status == 200:
                    parser = js.loads(await response.text())
                    
                    if parser['data']['findProfiles']['totalCount'] > 0:
                        return [SearchProfileResult(id=node['id']) for node in parser['data']['findProfiles']['nodes']]
                    
                    return [SearchProfileResult(id=None)]

        async def collect_all_rewards_async(self) -> bool:
            '''
            Claims all your rewards.
            '''
            if self._at == None:
                return MissingJWT()
            
            json_data = {
                'collectTypes': [
                    'daily_gift_collects',
                    'reaction_WAYD',
                    'reaction_ArtBooks',
                    'reaction_MyHome',
                    'reaction_Looks',
                    'MoviesViewed',
                    'reaction_Movies',
                    'WAYD_comment_reward',
                    'daily_gift_collects',
                    'welcome_gift_collects'
                ],
            }
            async with self.session.put(f'https://eu.mspapis.com/profilecollects/v3/profiles/{self.get_profile_id_from_access_token()}/games/j68d/collects/claim', json=json_data, headers={'Authorization': f'Bearer {self._at}'}) as response:
                if response.status == 200:
                    return True
                else:
                    return False

        async def collect_gift_async(self) -> bool:
            '''
            Collect a gift.
            '''
            if self._at == None:
                return MissingJWT()
            
            json_data = {
                'state': 'Claimed',
            }
            async with self.session.put(f'https://eu.mspapis.com/timelimitedrewards/v2/profiles/{self.get_profile_id_from_access_token()}/games/j68d/rewards/daily_pickup', json=json_data, headers={'Authorization': f'Bearer {self._at}'}) as response:
                if response.status == 200:
                    return True
                else:
                    return False
        
        async def get_experience_async(self, profileId: str = None):
            """
            Retrieve the experience information for a given profile ID asynchronously.
            
            Returns:
                Experience2: An object representing the experience information, including XP, level, currentLevelXpMin, and currentLevelXpMax.

            Usage:
            ```python
            experience_info = await msp2.get_experience_async(profileId='example_profile_id')
            ``` 
            """
            
            if profileId == None:
                profileId == self.pid
            
            async with self.session.get(f'https://eu.mspapis.com/experience/v1/profiles/{profileId}/games/j68d/experience', headers={'Authorization': f'Bearer {self._at}'}) as response:
                if response.status == 200:
                    try:
                        parser = js.loads(await response.text())
                        return  Experience2(xp=parser['experience']['xp'], level=parser['experience']['level'], currentLevelXpMin=parser['experience']['currentLevelXpMin'], currentLevelXpMax=parser['experience']['currentLevelXpMax'])
                    except:
                        return Experience2(0, 0, 0, 0)

        async def send_autograph_async(self, profileId) -> bool:
            '''
            Sends a greetings to a specified profileId.
            Returns True/False
            
            Usage:
            ```python
            search: List[SearchProfileResult] = await msp2.get_profile_search_async(server="fr", username="Extrm1st")
            sent: bool = await msp2.send_autograph_async(search[0].id)
            ```
            '''

            json_data = {
                'greetingType': "autograph",
                'receiverProfileId': profileId,
                'compatibilityMode': "Nebula",
                'useAltCost': False
            }
            async with self.session.post(f'https://eu.mspapis.com/profilegreetings/v1/profiles/' + self.pid + '/games/j68d/greetings', json=json_data, headers={'Authorization': f'Bearer {self._at}'}) as response:
                if response.status == 200:
                    if 'Succeeded' in await response.text():
                        return True
                    return False
                return False


        async def set_mood_async(self, mood_asset: str) -> bool:
            '''Changes your actual mood. With this, you can set a rare mood like bunny_hold.'''
            attributes: dict = await self.get_attributes_json_async(profileId=self.pid)
            attributes["additionalData"]["Mood"] = mood_asset
            async with self.session.put(url=f'https://eu.mspapis.com/profileattributes/v1/profiles/{self.pid}/games/j68d/attributes', json=attributes, headers={'Authorization': f'Bearer {self._at}'}) as response:
                if mood_asset in await response.text():
                    return True
            return False
    
        async def change_gender_async(self) -> bool:
            '''Switch from boy to girl, girl to boy.'''
            attributes: dict = await self.get_attributes_json_async(profileId=self.pid)
            gender_to_set = "Boy" if attributes["additionalData"]["Gender"] == "Girl" else "Girl"
            attributes["additionalData"]["Gender"] = gender_to_set

            async with self.session.put(url=f'https://eu.mspapis.com/profileattributes/v1/profiles/{self.pid}/games/j68d/attributes', json=attributes, headers={'Authorization': f'Bearer {self._at}'}) as response:
                if response.status == 200:
                    return True
            return False


        async def get_conversations_async(self, size: int = 50):
            '''Loads all your conversations.\n
            Args:
                size (int, optional): The number of conversations to retrieve per request. Defaults to 50.

            Returns:
                List[Conversation]: A list of Conversation objects representing the participant's conversations.
            
            Example Usage:
            ```python
            conversations: List[Conversation] = await msp2.get_conversations_async(size=10)
            for conv in conversations:
                ## your oode here, see Conversation object.
            
            ## the first (latest i guess) conversation:
            print(conversations.id) ## per example
            ```
            '''
            async with self.session.get(url=f'https://eu.mspapis.com/gamemessaging/v1/participants/{self.pid}/conversations?&page=1&pageSize={str(size)}', headers={'Authorization': f'Bearer {self._at}'}) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if not data:  # Check if the response is an empty list
                        return []

                    return [Conversation(
                conv['conversationId'],
                conv['conversationName'],
                conv['conversationStatus'],
                conv['conversationType'],
                datetime.fromisoformat(conv['created']),
                datetime.fromisoformat(conv['joinDate']),
                datetime.fromisoformat(conv['latestActivity']),
                js.loads(conv['latestMessage']),
                datetime.fromisoformat(conv['leaveDate']),
                conv['muted'],
                conv['numberOfUnreadMessages'],
                conv['participants']
            ) for conv in data]




        async def get_attributes_async(self, profileId: str = None) -> Attributes:
            '''
            Retrieve the attributes informations of a profileId.

            Returns:
                Attributes: An object representing the attributes informations.

            Usage:
            ```python
            attributes_info = await msp2.get_attributes_async(profileId='example_profile_id')
            print(attributes_info.avatarId)
            ```
            '''
            if profileId == None:
                profileId == self.get_profile_id_from_access_token()

            async with self.session.get(f'https://eu.mspapis.com/profileattributes/v1/profiles/{profileId}/games/j68d/attributes', headers={'Authorization': f'Bearer {self._at}'}) as response:
                if response.status == 200:
                    try:
                        parser = js.loads(await response.text())
                        return Attributes(
                            profileId=parser.get('profileId'),
                            gameId=parser.get('gameId'),
                            avatarId=parser.get('avatarId'),
                            additionalData=AttributesAdditionalData(
                                ProfilePopupCustomization=parser['additionalData'].get('ProfilePopupCustomization'),
                                Mood=parser['additionalData'].get('Mood'),
                                WelcomeVersion=parser['additionalData'].get('WelcomeVersion'),
                                ChatRoomPositionData=parser['additionalData'].get('ChatRoomPositionData'),
                                Gender=parser['additionalData'].get('Gender'),
                                DefaultMyHome=parser['additionalData'].get('DefaultMyHome'),
                                WAYD=parser['additionalData'].get('WAYD')
                            )
                        )
                    except:
                        return Attributes(None, None, None, additionalData=AttributesAdditionalData(None, None, None, None,None,None,None))
                    
        async def get_attributes_json_async(self, profileId: str = None) -> Attributes:
            '''
            Retrieve the attributes informations of a profileId.

            Returns:
                dict: the parsed json.

            Usage:
            ```python
            attributes_info = await msp2.get_attributes__json_async(profileId='example_profile_id')
            print(attributes_info['avatarId'])
            ```
            '''
            if profileId == None:
                profileId == self.get_profile_id_from_access_token()

            async with self.session.get(f'https://eu.mspapis.com/profileattributes/v1/profiles/{profileId}/games/j68d/attributes', headers={'Authorization': f'Bearer {self._at}'}) as response:
                if response.status == 200:
                    try:
                        return js.loads(await response.text())
                    except:
                        return None
                    



            





    async def s_c_async(self, server: str, method: str, data: dict, proxy: str = None) -> lol:
        proxy: str = self._p if self._p is not None else proxy

        r = bhtq(method, data)
        e = genv()

        e.headers = rty(
             data
        ) 
        e['/1'] = r
        qe = remoting.encode(e).getvalue()
            
        return await sd(s=self._c, server=server,
            method=method, data=qe, headers=rt(qe),
             proxy=set(proxy), custom_timeout=self._t
         )
       

    async def login_async(self, username: str, password: str, server: str, proxy: str = None) -> lr:
        proxy: str = self._p if self._p is not None else proxy
      
        lgd: dict = [
            username,
            password,
            [],
            None,
            None,
            "MSP1-Standalone:XXXXXX"
        ]

        response = await self.s_c_async(
            server=server, method="MovieStarPlanet.WebService.User.AMFUserServiceWeb.Login", data=lgd, proxy=proxy
        )

        if response.StatusCode == 200:
            try:
                if response.Content['loginStatus']['status'] in {'Success', 'ThirdPartyCreated'}:
                    self._pid = response.Content['loginStatus']['nebulaLoginStatus']['profileId']
                    self.at = response.Content['loginStatus']['nebulaLoginStatus']['accessToken']
                    return lr(response.Content['loginStatus']['actor']['ActorId'], response.Content['loginStatus']['ticket'], response.Content['loginStatus']['nebulaLoginStatus']['profileId'], response.Content['loginStatus']['nebulaLoginStatus']['accessToken'])
                else:
                    return lr(0, None, None, None)
            except:
                return lr(0, None, None, None)






