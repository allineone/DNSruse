import os
import sys


uid = os.getuid()
if uid > 0:
    exit("Must be run as root!")






def install():
    print("beginning install process...")
    
    

        
    cwd = os.getcwd()
    if ("dnsruse" in cwd) == False:
        exit("Must be executed in dnsruse/ directory!")
    missing_libs = []
    print("checking dependencies...")
    try:
        import argparse
    except ImportError:
        missing_libs.append("argparse")
    try:
        import dns.resolver
    except ImportError:
        missing_libs.append("dnspython")

    if len(missing_libs) > 0:
        exit("missing dependencies: {}".format(", ".join(missing_libs)))
        
    print("creating directory /etc/dnsruse...")
    os.system("rm -rf /etc/dnsruse")
    os.system("mkdir -p /etc/dnsruse")
    
    
    print("copying files to /etc/dnsruse...")
    os.system("cp -r ./* /etc/dnsruse/")
    
    
    print("creating path file....")
    os.system("touch /usr/sbin/dnsruse")
    
    f = open("/usr/sbin/dnsruse", "w")
    f.write("python3 /etc/dnsruse/main.py $@")
    f.close()
    
    print("setting file permissions...")
    os.system("chmod +x /usr/sbin/dnsruse")
    
    service_data = "[Unit]\nDescription=Test Service\nAfter=network.target\n\n[Service]\nUser=root\nWorkingDirectory=/etc/dnsruse/\nExecStart=python3 /etc/dnsruse/service.py\nRestart=always\n\n[Install]\nWantedBy=multi-user.target"
    print("creating systemd files...")
    os.system("touch /lib/systemd/system/dnsruse.service")
    f = open("/lib/systemd/system/dnsruse.service", "w")
    f.write(service_data)
    f.close()
    print("setting file permissions...")
    os.system("chmod 664 /lib/systemd/system/dnsruse.service")
    print("complete!")
        
        
def uninstall():
    print("beginning install process...")
    os.system("rm -rf /etc/dnsruse")
    os.system("rm -rf /usr/sbin/dnsruse")
    os.system("rm -rf /lib/systemd/system/dnsruse.service")
    
    
if sys.argv[1] == "install":
    install()
elif sys.argv[1] == "uninstall":
    uninstall()
else:
    exit("Specify 'install' or 'uninstall'.")
