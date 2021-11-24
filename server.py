import socket
import mysql.connector
from setup import *

db = mysql.connector.connect(user=USER, password=PWD,
                              host='127.0.0.1',
                              port=DB_PORT,
                              database=DB_NAME)

cursor = db.cursor()

host = HOST
port = 8085
isAuthorized = bytearray([0])
isUserInDB = bytearray([0])
authorizedUser = ""

def receiveReq():
    res = conn.recv(1024)
    res = res.decode()
    return res
    
def queryDB(cursor, query):
    userReq = receiveReq()
    query = query %userReq
    cursor.execute(query)
    dbRes = cursor.fetchall()
    return dbRes

def login():
    query = 'SELECT * FROM `users` WHERE username = "%s"'
    dbResponse = queryDB(cursor, query)
    if len(dbResponse) > 0:
        isUserInDB = bytearray([1])
        conn.sendall(isUserInDB)
        if isUserInDB == b'\x01':
            query = 'SELECT * FROM `users` WHERE password = "%s"'
            dbResponse = queryDB(cursor, query)
            if len(dbResponse) > 0:
                isAuthorized = bytearray([1])
                authorizedUser = dbResponse[0][0]
                conn.sendall(isAuthorized)
                return authorizedUser
                

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((host, port))
    sock.listen(1)
    conn, addr = sock.accept()
    with conn:
        print('connected by: ', addr)
        while isUserInDB == b'\x00':
            authorizedUser = login()
            isAuthorized = b'\x01' if authorizedUser > 0 else b'\x00'
            isUserInDB = isAuthorized if isAuthorized == b'\x01' else b'\x00'
        while isAuthorized == b'\x01':
            message = receiveReq()
            query = f'INSERT INTO messages (id_user, message, ip) VALUES({authorizedUser}, "{message}", "{addr[0]}")'
            cursor.execute(query)
            response = cursor.fetchall()
            db.commit()
            conn.sendall(b'Message was sent to the Data Base')
            if not message:
                sock.close()
                break
