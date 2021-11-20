import socket
from setup import HOST

host = HOST
port = 8085

amIauthorized = bytearray([0])
option = 3

def menuChoice():
    option = input('Menu: \n 0  -- Create account \n 1  -- Login \n 2  --  Quit \n ~ ')
    return option

def request(msg):
    req = input(f'{msg}')
    req = str.encode(req)
    sock.sendall(req)
    res = sock.recv(1024)
    return res
    
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host, port))
    while option != "2":
        option = menuChoice()
        if option == "1":
            while amIauthorized == b'\x00':
                response = request("Please, insert your username: ~ ")
                if response == b'\x01':
                    res = request("Please, insert your password: ~ ")
                    if res == b'\x01':
                        amIauthorized = res
                        print('You are logged in')
                        option = "2"
                else:
                    print("User not found")
        elif option == "0":
            print("Create account")
    while amIauthorized == b'\x01':
        message = input("Type your message: ~ ")
        message = str.encode(message)
        sock.sendall(message)
        response = sock.recv(1024)
        print(response)

    

        