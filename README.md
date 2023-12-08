# MovieStarPlanet Python Library
Welcome to the MovieStarPlanet Python Library, a comprehensive asynchronous toolkit designed for seamless interaction with both MovieStarPlanet 1 and 2 APIs. This library empowers developers to effortlessly access and manipulate MovieStarPlanet user profiles, common services, and official cheat functionalities.

# Installation
To use this library, download the source code from the repository. As the library is not available on PyPI, you won't find it on pip.
```bash
git clone https://github.com/bshenn/moviestarplanet.git
cd moviestarplanet
```

# Usage
Initializing the Library for MovieStarPlanet 1
```python
import asyncio
from moviestarplanet import MSPAsyncClient


async def main():
    msp1_client = MSPAsyncClient(proxy='your_proxy', timeout=10)

asyncio.run(main())
```
This code initializes the library for MovieStarPlanet 1, accepting optional arguments like proxy for the default proxy for all requests and timeout for request timeout.

# Logging in to MovieStarPlanet 1
You will need to access first LoginResult dataclass.
```python
from moviestarplanet.entities import *
```
```python
login: LoginResult = await msp.login_async('username', 'password', 'fr')
```
