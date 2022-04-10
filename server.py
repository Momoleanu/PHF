import socket
from _thread import *
import pickle
from game import Game

server = "Intre ghilimele inserati adresa IPv4"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Asteptare conexiune. Serverul a fost deschis")

connected = set()
games = {}
idCount = 0


def thClient(connection, player, gameId):
    global idCount
    connection.send(str.encode(str(player)))

    reply = ""
    while True:
        try:
            data = connection.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetMoved()
                    elif data != "get":
                        game.play(player, data)

                    connection.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Conexiune pierduta")
    try:
        del games[gameId]
        print("Inchidere joc", gameId)
    except:
        pass
    idCount -= 1
    connection.close()


while True:
    conn, addr = s.accept()
    print("Conectat la: ", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1) // 2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creare joc nou...")
    else:
        games[gameId].ready = True
        p = 1

    start_new_thread(thClient, (conn, p, gameId))
