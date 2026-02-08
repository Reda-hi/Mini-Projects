import socket
import sys
import argparse
from datetime import datetime as dt

# Setup Argument Parser
parser = argparse.ArgumentParser(description="Python Port Scanner")
parser.add_argument("target", help="Target IP address")
parser.add_argument("--start", type=int, default=1, help="Start port (default: 1)")
parser.add_argument("--end", type=int, default=1024, help="End port (default: 1024)")
args = parser.parse_args()


# Defining the target

target = socket.gethostbyname(args.target) # Translating Hostname to IPV4


# Adding a Banner
print("-" * 50)
print(f"Scanning Target {target}")
print("Started At "+ str(dt.now()))
print("-" * 50)

def Show_open_ports(ports):
    print("\n" + "=" * 20)
    print("|    Open Ports    |")
    print("=" * 20)
    if ports:
        for port in ports:
            print(f"| {str(port).center(16)} |")
    else:
        print(f"| {'None found'.center(16)} |")
    print("=" * 20)


# Post scanning part
Working_ports=[]
try:
    for PORT in range(args.start,args.end + 1):
        if (PORT - args.start) % 20 == 0:
            if PORT + 20 > args.end:
                print(f"Scanning ports from {PORT} to {args.end}")
            else:
                print(f"Scanning ports from {PORT} to {PORT + 20}")
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = s.connect_ex((target,PORT)) # Returns error indicator
        if result == 0:
            Working_ports.append(PORT)
        s.close()
    Show_open_ports(Working_ports)


except KeyboardInterrupt:
    if 'PORT' in locals():
        print(f"\nLast scanned port: {PORT}")
    Show_open_ports(Working_ports)
    print("\nExiting program...")
    sys.exit()
except socket.gaierror:
    print("Hostname Could not be resolved")
    sys.exit()
except socket.error:
    print("Couldn't connect to the server")
    sys.exit()