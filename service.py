from conf import *
from misc import *
from server import DNSServer
from conf import *


blacklist = open_file(blacklist_path)

dnsServer = DNSServer(blacklist=blacklist, redirect_ip=redirect_ip, addr=primary_nameserver, max_cache_size=max_cache_size)
dnsServer.start()
