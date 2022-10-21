# This is the script for the client side of the file transfer program
# Author: Juan Andrés Méndez, Jesus David Barrios, Sergio Esteban Peñuela

import socket
import sys
import os

'''
The connection will be made via UDP sockets 
'''

## IP and port of the server note that the port must support UDP
IP = 'localhost'
PORT = 5000
ADDR = (IP, PORT)
FORMAT = 'utf-8'
FILE_100MB = '100MB.bin'
FILE_250MB = '250MB.bin'
FILESIZE_100MB = os.path.getsize(FILE_100MB)
FILESIZE_250MB = os.path.getsize(FILE_250MB)


# Create a UDP socket
client = None
try:
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print('Failed to create socket')
    sys.exit()


