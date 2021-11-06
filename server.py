import socket
import datetime
import mysql.connector

db = mysql.connector.connect(user='root', password='',
                              host='127.0.0.1',
                              database='messages')

cursor = db.cursor()

host = '192.168.56.1'
port = 8080
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
            currentTime = datetime.datetime.now()
            query = "INSERT INTO messages (message, timeOfRecv) VALUES(%s, %s)"
            cursor.execute(query, (message, currentTime))
            db.commit()
            conn.sendall(b'Message was sent to the Data Base')
            if not message:
                sock.close()
                break
