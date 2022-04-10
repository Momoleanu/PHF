import pygame
from network import Network
import sqlite3

con = sqlite3.connect("scores.db")
cur = con.cursor()

# cur.execute('''CREATE TABLE IF NOT EXISTS scores
#                (scorePlayer integer PRIMARY KEY, scoresEnemy integer)''')
#
# cur.execute("INSERT INTO scores VALUES (0,0)")
#

pygame.font.init()

width = 800
height = 800
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")
font2 = pygame.font.Font("freesansbold.ttf", 32)

textXP = 10
textYP = 10
textXE = 570
textYE = 10
score_valueP = 0
score_valueE = 0


def showScoreP(textX, textY, score_valueP):
    score = font2.render("Scorul tau: " + str(score_valueP), True, (255, 255, 255))
    win.blit(score, (textX, textY))


def showScorePE(textX, textY, score_valueE):
    score = font2.render("Scor inamic: " + str(score_valueE), True, (255, 255, 255))
    win.blit(score, (textX, textY))


class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 200
        self.height = 100

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)

        text = font.render(self.text, True, (255, 255, 255))
        window.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                           self.y + round(self.height / 2) - round(text.get_height() / 2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        return self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height


def redrawWindow(win, game, p, score_valueP, score_valueE):
    win.fill((128, 128, 128))

    if not (game.connected()):
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render("Se asteapta jucator ", True, (255, 255, 255), True)
        win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
    else:
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render("Alegerea ta", True, (255, 255, 255))
        win.blit(text, (70, 200))

        text = font.render("Alegerea oponentului", True, (255, 255, 255))
        win.blit(text, (380, 200))

        move1 = game.getPlayerMove(0)
        move2 = game.getPlayerMove(1)
        if game.bothMoved():
            text1 = font.render(move1, True, (0, 0, 0))
            text2 = font.render(move2, True, (0, 0, 0))
        else:
            if game.p1Moved and p == 0:
                text1 = font.render(move1, True, (0, 0, 0))
            elif game.p1Moved:
                text1 = font.render("Decizie selectata", True, (0, 0, 0))
            else:
                text1 = font.render("Decizie", True, (0, 0, 0))

            if game.p2Moved and p == 1:
                text2 = font.render(move2, True, (0, 0, 0))
            elif game.p2Moved:
                text2 = font.render("Decizie selectata", True, (0, 0, 0))
            else:
                text2 = font.render("Decizie", True, (0, 0, 0))

        if p == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))

        for btn in btns:
            btn.draw(win)

        showScoreP(textXP, textYP, score_valueP)
        showScorePE(textXE, textYE, score_valueE)
    pygame.display.update()


btns = [Button("Piatra", 50, 500, (0, 0, 0)), Button("Hartie", 300, 500, (0, 0, 0)),
        Button("Foarfeca", 550, 500, (0, 0, 0))]


def main():
    score_valueP = 0
    score_valueE = 0

    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("Jucator: ", player)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Joc invalid")
            break

        if game.bothMoved():
            redrawWindow(win, game, player, score_valueP, score_valueE)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Joc invalid")
                break

            font = pygame.font.SysFont("comicsans", 60)
            if (game.win() == 1 and player == 1) or (game.win() == 0 and player == 0):
                text = font.render("Ai castigat!", True, (255, 0, 0))
                score_valueP += 1

            elif game.win() == -1:
                text = font.render("Egalitate!", True, (255, 0, 0))
            else:
                text = font.render("Ai pierdut!", True, (255, 0, 0))
                score_valueE += 1

            win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2 - 300))
            pygame.display.update()
            pygame.time.delay(3000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Moved:
                                n.send(btn.text)
                        else:
                            if not game.p2Moved:
                                n.send(btn.text)

        redrawWindow(win, game, player, score_valueP, score_valueE)


def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render("Apasa pentru a incepe jocul! ", False, (255, 255, 255))
        win.blit(text, (150, 350))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()


while True:
    menu_screen()
