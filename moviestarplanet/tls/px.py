def set(proxy: str):
    
    if proxy == None:
        return None
    
    if proxy.lower().startswith('http'):
        return proxy

    return f'http://{proxy}'