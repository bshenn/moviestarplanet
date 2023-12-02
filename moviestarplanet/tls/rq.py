from pyamf import remoting

def bhtq(method: str, params: dict):
    return remoting.Request(target=method, body=params)