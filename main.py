import socket
import re
import sys
import gc

def get_url(request):
    return request.split()[1]

tmp = []

def change_memory(value):
    tmp = range(value * 1024 * 1024)
    gc.collect()

def scale(port):
    if port == 8000:
        return 0.5
    if port == 8001:
        return 2.0

def send(ip, port, value):
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        send_socket.connect((ip, port))
        send_socket.sendall('comm /mem_use=' + str(value) + '!')
    except socket.error:
        pass
    send_socket.close()

def check(ip, port):
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    flag = True
    try:
        send_socket.connect((ip, port))
        send_socket.sendall('test hello')
    except socket.error:
        flag = False
    send_socket.close()
    return flag

port = int(sys.argv[1])
mem = 0
ip = 'localhost'
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind(('', port))
listen_socket.listen(1)
while True:
    client_connection, client_address = listen_socket.accept()
    request = client_connection.recv(1024)
    url = get_url(request)
    http_response = None
    if url.startswith('/set_ip'):
        ip = re.match('/set_ip=(.*)', url).group(1)
        if check(ip, port ^ 1):
            http_response = 'set ip to %s' % ip
        else:
            http_response = 'ip error'
    elif url == '/mem_info':
        http_response = 'memory used %d' % mem
    elif url.startswith('/mem_use'):
        mem = int(re.match('/mem_use=([0-9]*)', url).group(1))
        change_memory(mem)
        if url[-1] != '!':
            send(ip, port ^ 1, int(mem * scale(port)))
        http_response = 'change memory used to %d' % mem
    else:
        http_response = 'Hello, world!'
    client_connection.sendall(http_response)
    client_connection.close()
