# This is the script for the server side of the file transfer program
# Author: Juan Andrés Méndez, Jesus David Barrios, Sergio Esteban Peñuela

import socket
import sys
import logging
import os

'''
The connection will be made via UDP sockets
'''

## IP and port of the server note that the port must support UDP
IP = '192.168.1.100'
PORT = 5000 
ADDR = (IP, PORT)
FORMAT = 'utf-8'

## The files to be sent
FILE_100MB = '100MB.bin'
FILE_250MB = '250MB.bin'
FILESIZE_100MB = os.path.getsize(FILE_100MB)
FILESIZE_250MB = os.path.getsize(FILE_250MB)

# Get file size from console
file_size = int(input("Ingrese el tamaño del archivo (100,250): "))

# Create a UDP sockets
server = None
try:
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print('Failed to create socket')
    sys.exit()
        
# Bind the socket to the PORT
try:
    server.bind(ADDR)
except socket.error:
    print('Bind failed')
    sys.exit()

print('SERVER STARTED AT PORT: ', PORT)


