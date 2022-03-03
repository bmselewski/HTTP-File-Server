#!/usr/bin/env python3

import socket
import sys
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import select
from file_reader import FileReader


class Jewel:

    # Note, this starter example of using the socket is very simple and
    # insufficient for implementing the project. You will have to modify this
    # code.
    def __init__(self, port, file_path, file_reader):
        self.file_path = file_path
        self.file_reader = file_reader

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("0.0.0.0", port))
        print('Listening on port ' + str(port) + '...')
        s.listen(5)
        while True:
            (client, address) = s.accept()
            ready_client = select.select([client,], [], [], 500)
            if ready_client[0] :
                ip_address = address[0]
                port_number = address[1]
                print('[CONN] Connection from '+str(ip_address)+' on port ' + str(port_number))
                while True:
                    data = client.recv(1024).decode()

                    if not data:
                        break

                    headers = data.split('\n')
                    file = headers[0].split()[1]
                    command = headers[0].split()[0]
                    print('[REQU] [' + str(ip_address) + ':' + str(port_number) + '] ' + command + ' request for ' + file_path +file)
                    print('[FULL REQUEST]\n' + data)
                    if file_path == "":
                        file = file[1:]
                    try:
                        response = file_reader.head(file_path + file, "cookies are a lie")
                        display = file_reader.get(file_path + file, "cookies are fake")

                        print('[RESPONSE HEADER]\n' + response)
                        if command == 'GET':
                            client.sendall(response.encode())
                            client.sendall(display)

                        elif command == 'HEAD':
                            client.sendall(response.encode())

                        else:
                            response = 'HTTP/1.1 501: Method Unimplemented\n\n'
                            print('[ERRO] [' + str(ip_address) + ':' + str(port_number) + '] ' + command + ' request returned error 501')
                            client.sendall(response.encode())

                        client.close()
                        break

                    except FileNotFoundError:
                        now = datetime.now()
                        stamp = mktime(now.timetuple())
                        date = format_date_time(stamp)
                        response = 'HTTP/1.1 404 File Not Found\r\nDate: '+date+'\n\nError 404 File Not Found'
                        print('[ERRO] ['+str(ip_address)+':'+str(port_number)+'] '+ command +' request returned error 404')
                        client.sendall(response.encode())
                        client.close()
                        break


if __name__ == "__main__":
    port = int(sys.argv[1])
    file_path = sys.argv[2]

    FR = FileReader()

    J = Jewel(port, file_path, FR)
