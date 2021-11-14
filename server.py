import socket
import mysql.connector
from setup import *

db = mysql.connector.connect(user=USER, password=PWD,
                              host='127.0.0.1',
                              port=DB_PORT,
                              database=DB_NAME)

cursor = db.cursor()

host = HOST
port = 8002
isAuthorized = bytearray([0])
isUserInDB = bytearray([0])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((host, port))
    sock.listen(1)
    conn, addr = sock.accept()
    with conn:
        print('connected by: ', addr)
        while isUserInDB == b'\x00':
            username = conn.recv(1024)
            username = username.decode()
            query = f'SELECT * FROM `users` WHERE username = "{username}"'
            cursor.execute(query)
            dbResponse = cursor.fetchall()
            if len(dbResponse) > 0:
                isUserInDB = bytearray([1])
                conn.sendall(isUserInDB)
                if isUserInDB == b'\x01':
                    password = conn.recv(1024)
                    password = password.decode()
                    query = f'SELECT * FROM `users` WHERE password = "{password}"'
                    cursor.execute(query)
                    dbRes = cursor.fetchall()
                    if len(dbRes) > 0:
                        isAuthorized = bytearray([1])
                        conn.sendall(isAuthorized)
            conn.sendall(isUserInDB)
        #db.commit()
        while True and isAuthorized == b'\x01':
            message = conn.recv(1024)
            message = message.decode()
            query = "INSERT INTO messages (message) VALUES(%s)"
            cursor.execute(query, (message))
            db.commit()
            conn.sendall(b'Message was sent to the Data Base')
            if not message:
                sock.close()
                break
