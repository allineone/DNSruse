import argparse
from misc import *
from server import DNSServer
from conf import *



parser = argparse.ArgumentParser()
parser.add_argument("--nameserver", type=str, help="IP address of upstream nameserver.", default="1.1.1.1")
parser.add_argument("--redirect_ip", type=str, help="Domain to redirect blacklisted domains to.", default="")
parser.add_argument("--cache_size", type=str, help="Size of cache in bytes.", default="2048")
FLAGS = parser.parse_args()

blacklist = open_file(blacklist_path)

dnsServer = DNSServer(blacklist=blacklist, redirect_ip=FLAGS.redirect_ip, addr=FLAGS.nameserver, max_cache_size=FLAGS.cache_size)
dnsServer.start()
