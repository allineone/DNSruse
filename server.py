import argparse
from socketserver import BaseRequestHandler, ThreadingUDPServer
from handler import Handler
import sys
from conf import *


class DNSServer:
    def __init__(self, blacklist=[], redirect_ip=None, port=PORT, addr="", max_cache_size=2048):
        self.blacklist = blacklist
        self.redirect_ip = redirect_ip
        self.port = port
        self.dns_addr = addr
        self.max_cache_size = int(max_cache_size)
        self.cache = {}
        handler = Handler
        handler.host = self
        self.server = ThreadingUDPServer((HOST_IP, self.port), Handler)
    def start(self):
        print("dnsruse running on {} port {} ...".format(HOST_IP, self.port))
        self.server.serve_forever()
    def log(self, info):
        print(info)
    def add_cache(self, domain, ip):
        if sys.getsizeof(self.cache) < self.max_cache_size:
            self.cache[domain] = ip
            return "cached."
        else:
            return "unable to cache, full"


    
    
