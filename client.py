import socket
import base64

host = '192.168.56.1'
port = 8080

amIauthorized = bytearray([0])
option = 3

def encryptPwd(pwd):
    pwd = pwd.encode("utf-8")
    encoded = base64.b64encode(pwd)
    return encoded

def menuChoice():
    option = input('Menu: \n 0  -- Create account \n 1  -- Login \n 2  --  Quit \n ~ ')
    return option

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host, port))
    while option != "2":
        option = menuChoice()
        if option == "1":
            while amIauthorized == b'\x00':
                username = input("Please, insert your username: ~ ")
                username = str.encode(username)
                sock.sendall(username)
                response = sock.recv(1024)
                if response == b'\x01':
                    password = input("Please, insert your password: ~ ")
                    password = str.encode(password)
                    sock.sendall(password)
                    resp = sock.recv(1024)
                    if resp == b'\x01':
                        amIauthorized = resp
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
        print(f'{response}')

    

        