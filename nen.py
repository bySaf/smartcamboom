import socket


def bezdarnost(x, y):
    print("etot praekt govno")
    print(x, y)
    HOST = ("", 9090)

    server = socket.socket()
    server.bind(HOST)
    server.listen(1)

    text = str(x) + " " + str(y)

    a = 0
    while (a == 0):
        try:
            conn, addr = server.accept()
            print("Connected to - ", addr)
            res = text.encode()
            conn.send(res)
            conn.close()
            a = 1
        except:
            a = 0


