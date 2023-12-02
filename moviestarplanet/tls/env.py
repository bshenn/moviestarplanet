from pyamf import AMF3, remoting

def genv() -> remoting.Envelope:
    return remoting.Envelope(AMF3)