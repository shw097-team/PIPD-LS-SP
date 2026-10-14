import sys
def offline(event, args):
    if event in ("socket.connect", "socket.getaddrinfo", "socket.bind"):
        raise RuntimeError("AO_OFFLINE_NETWORK_FORBIDDEN")
sys.addaudithook(offline)
