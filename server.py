# This is the script for the server side of the file transfer program
# Author: Juan Andrés Méndez, Jesus David Barrios, Sergio Esteban Peñuela

import socket
import sys
import logging
import time
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

# The batch size is 64 KB
BATCHE_SIZE = 1024 * 36


# Create a UDP sockets
server = None
try:
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error as e:
    print('Error creating socket: ' + str(e))
    sys.exit()
 
# Bind the socket to the PORT
try:
    server.bind(ADDR)
    print('Server started')
except socket.error as e:
    print('Bind failed. Error Code : ' + str(e))
    print('Bind failed')
    sys.exit()

print('SERVER STARTED AT PORT: ', PORT)

def main():
    logging.basicConfig(filename=f'{time.strftime("%Y%m%d-%H%M%S")}'+'-log.txt', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')
    # Ask the user to select the file to send
    print('Select the file to send')
    print('1. 100MB.bin')
    print('2. 250MB.bin')
    option = input('Select an option: ')
    while True:

        data , addr = server.recvfrom(BATCHE_SIZE)
        if option == '1' and data.decode(FORMAT) == 'Ready':
            # Send the file
            print ('Sending file 100MB.bin to ', addr)
            send_file(FILE_100MB, FILESIZE_100MB, addr)
            break
        elif option == '2' and data.decode(FORMAT) == 'Ready':
            # Send the file
            print ('Sending file 250MB.bin to ', addr)
            send_file(FILE_250MB, FILESIZE_250MB, addr)
            break
        else:
            print('Invalid option')
            option = input('Select an option: ')

def send_file(file, size, addr):
    # Send the file size
    server.sendto(str(size).encode(FORMAT), addr)
    # Send the file hash
    with open(file, 'rb') as f:
        data = f.read(BATCHE_SIZE)
        server.sendto(data, addr)
        logging.info(f'Sent {BATCHE_SIZE} bytes')
        while data:
            data = f.read(BATCHE_SIZE)
            server.sendto(data, addr)
            logging.info(f'Sent {BATCHE_SIZE} bytes')

    print('File sent')

    


if __name__ == '__main__':
    main()


