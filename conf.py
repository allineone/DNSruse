
# hosting IP address of the dns server (for external usage avoid 127.0.0.1, use ip of interface)
HOST_IP="127.0.0.1"

# port of dns server (default 53)
PORT=53

# upstream nameserver to handle dns queries
primary_nameserver="1.1.1.1"

# max size of dns cache, in bytes
max_cache_size=4096

# location of blacklist file (entries separated by \n)
blacklist_path="blacklist.txt"

# IP to redirect blacklisted IPs to
redirect_ip="0.0.0.0"
