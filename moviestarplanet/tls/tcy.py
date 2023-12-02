from pyamf import remoting

def t(dt):
    try:
        return remoting.decode(dt)["/1"].body['Code']
    except:
        return -1