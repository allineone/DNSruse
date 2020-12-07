# DNSruse
DNS spoofing tool written in python3

# Installation
Supported on debian-based systems. Requires `dnspython` and `argparse`, found in `python3-pip`.

`git clone https://github.com/allineone/DNSruse`

`cd DNSruse`

`sudo python3 setup.py install`

You can remove DNSruse using:

`sudo python3 setup.py uninstall`

# Usage
DNSruse can be ran in terminal:

`sudo dnsruse <args>`

or as a service (args can be passed in `/etc/dnsruse/conf.py`):

`sudo service dnsruse start`

# Blacklisting Domains

You can add domains to blacklist to `/etc/blacklist.txt` or specify your own file with `blacklist_path`. Blacklist files should be formatted as such, separated by one line:

`www.example.com`

`www.example.com`

`www.example.com`

Requests for these blacklisted domains can then be redirected to your own web server using the `redirect_ip` argument. Note servers should run on the same port as the requested server e.g. HTTPS sites should be hosted on 443.

# Arguments

#### HOST
IP of the DNS server can be set with:

`HOST_IP=""`

This should be the external IP address of an interface e.g. `192.168.0.1`


#### PORT
The port of the DNS server can be set with:

`PORT=53`

#### NAMESERVER
The upstream nameserver to send DNS requests can be set with:

`primary_nameserver="1.1.1.1"`

#### CACHE
The max size of the DNS cache, in bytes:

`max_cache_size=4096`

#### BLACKLIST
The location of the blacklisted domain file:

`blacklist_path="blacklist.txt"`

#### REDIRECTION
IP to redirect blacklisted IPs to:

`redirect_ip="0.0.0.0"`
