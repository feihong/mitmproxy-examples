import socket
import subprocess

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('10.255.255.255', 1))
ip = s.getsockname()[0]
print(f'Starting the proxy at {ip}:8080\n')
s.close()

subprocess.call(['mitmdump', '-w', 'dumpfile'])
