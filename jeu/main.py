import sys
import time
import pygame



pygame.init()
screen = pygame.display.set_mode((1200, 1200))

fic = open("level.txt", "r")
lv = 0
level = {}
for line in fic:
    vierge = [["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
              ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
              ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
              ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
              ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
              ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
              ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
              ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
              ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
              ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
              ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
              ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"]
              ]
    tabl = line
    vbn = []
    k = 0
    for i in range(len(tabl)):
        vbn.append(tabl[i])
    for i in range(len(vierge)):
        for j in range(len(vierge[0])):
            vierge[i][j] = vbn[k]
            k += 1
    mape = vierge
    level[lv] = mape
    lv += 1
fic.close()
vierge = [["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
          ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
          ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
          ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
          ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
          ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
          ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
          ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
          ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
          ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
          ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
          ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"]
          ]


class Square:
    def __init__(self, x, y, size, speed_x, speed_y):
        self.x = x
        self.y = y
        self.size = size
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.bounciness = -.5
        self.niveau = 0
        self.changement()

    def changement(self):
        self.collision = []
        if self.niveau in level:
            for i in range(len(level[self.niveau])):
                for j in range(len(level[self.niveau][0])):
                    if level[self.niveau][i][j] == "x":
                        self.collision.append(pygame.Rect(j * 100, i * 100, 100, 100))
                    if level[self.niveau][i][j] == "f":
                        self.fin = pygame.Rect(j * 100, i * 100, 100, 100)
                    if level[self.niveau][i][j] == "0":
                        self.debut = pygame.Rect(j * 100, i * 100, 100, 100)
                        self.speed_x = 0
                        self.speed_y = 0
                        self.x = j * 100 + 25
                        self.y = i * 100 + 25
            return 1
        else:
            return 4

    def update(self):
        verif = 0
        for i in range(len(self.collision)):
            if pygame.Rect(self.x + self.speed_x, self.y, self.size, self.size).colliderect(self.collision[i]):
                self.speed_x *= self.bounciness
            else:
                verif = 1
        if verif == 1:
            self.x += self.speed_x
        verify = 0
        for ly in range(len(self.collision)):
            if pygame.Rect(self.x, self.y + self.speed_y, self.size, self.size).colliderect(self.collision[ly]):
                self.speed_y *= self.bounciness
            else:
                verify = 1
        if verify == 1:
            self.y += self.speed_y

        # simulate gravity
        self.speed_y += 0.1
        if self.speed_x > 0:
            self.speed_x -= 0.1
        if self.speed_x < 0:
            self.speed_x += 0.1
        if 0.1 >= self.speed_x > 0:
            self.speed_x = 0
        # detect bottom screen boundary
        if self.speed_y > 1:
            if self.y + self.size >= screen.get_height():
                self.speed_y *= self.bounciness
                self.y = screen.get_height() - self.size
            if self.y <= 0:
                self.speed_y *= self.bounciness
                self.y = 0
        else:
            if self.y + self.size >= screen.get_height():
                self.speed_y = 0
                self.y = screen.get_height() - self.size
            if self.y <= 0:
                self.speed_y *= self.bounciness
                self.y = 0
        if self.speed_x > 1:
            if self.x + self.size >= screen.get_width():
                self.speed_x *= self.bounciness
                self.x = screen.get_width() - self.size
            if self.x <= 0:
                self.speed_x *= self.bounciness
                self.x = 0
        else:
            if self.x + self.size >= screen.get_width():
                self.speed_x = 0
                self.x = screen.get_width() - self.size
            if self.x <= 0:
                self.speed_x *= self.bounciness
                self.x = 0

    def draw(self):
        for i in range(len(level[self.niveau])):
            for j in range(len(level[self.niveau][0])):
                if level[self.niveau][i][j] == "x":
                    pygame.draw.rect(screen, (102, 103, 102), (j * 100, i * 100, 100, 100))
        pygame.draw.rect(screen, "green", self.fin)
        pygame.draw.rect(screen, "blue", self.debut)

        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.size, self.size))
        if pygame.Rect(self.x + self.speed_x, self.y, self.size, self.size).colliderect(self.fin):
            t = self.finish()
            return t
        else :
            return 1

    def finish(self):

        self.niveau += 1
        t = self.changement()
        return t

def menu():
    font = pygame.font.Font(None, 56)
    play_button = pygame.Rect(450, 550, 300, 50)
    new = pygame.Rect(450, 750, 300, 50)
    selectio = pygame.Rect(450, 350, 300, 50)
    pygame.draw.rect(screen, "green", new)
    pygame.draw.rect(screen, "black", new, 3)
    text = font.render("New",True,(255,255,255))
    screen.blit(text,(560,755))
    pygame.draw.rect(screen, "green", play_button)
    pygame.draw.rect(screen, "black", play_button, 3)
    pygame.draw.rect(screen, "green", selectio)
    pygame.draw.rect(screen, "black", selectio, 3)
    text = font.render("Level", True, (255, 255, 255))
    screen.blit(text, (560,355))
    pygame.draw.polygon(screen, "blue", ((620, 575), (580, 595), (580, 555)))
    pygame.draw.polygon(screen, "blue", ((620, 575), (580, 595), (580, 555)), 3)

    if play_button.collidepoint(pygame.mouse.get_pos()):
        if pygame.mouse.get_pressed(3)[0]:
            return 1
        else:
            return 0
    elif selectio.collidepoint(pygame.mouse.get_pos()):
        if pygame.mouse.get_pressed(3)[0]:
            return 3
        else:
            return 0
    elif new.collidepoint(pygame.mouse.get_pos()):
        if pygame.mouse.get_pressed(3)[0]:
            return 5
        else:
            return 0
    else:
        return 0


casse = 0


def nouveau():
    for i in range(len(vierge)):
        for j in range(len(vierge[0])):
            pygame.draw.rect(screen, "black", pygame.Rect(j * 100, i * 100, 100, 100), 1)

    for i in range(len(vierge)):
        for j in range(len(vierge[0])):
            if vierge[i][j] == "x":
                pygame.draw.rect(screen, (102, 103, 102), (j * 100, i * 100, 100, 100))
            if vierge[i][j] == "f":
                pygame.draw.rect(screen, "green", (j * 100, i * 100, 100, 100))
            if vierge[i][j] == "0":
                pygame.draw.rect(screen, "blue", (j * 100, i * 100, 100, 100))

    if 1175 <= pygame.mouse.get_pos()[0] <= 1175 + 25 and 1175 <= pygame.mouse.get_pos()[1] <= 1175 + 25:
        if pygame.mouse.get_pressed(3)[0]:
            fic = open("level.txt", "a")
            texte = "\n"
            for i in range(len(vierge)):
                for j in range(len(vierge[0])):
                    texte += vierge[i][j]
            fic.write(texte)
            fic.close()
            time.sleep(0.2)
            return 0
    elif 1175 <= pygame.mouse.get_pos()[0] <= 1175 + 25 and 0 <= pygame.mouse.get_pos()[1] <= 25:
        if pygame.mouse.get_pressed(3)[0]:
            return 0
    else:
        for i in range(len(vierge)):
            for j in range(len(vierge[0])):

                if j * 100 <= pygame.mouse.get_pos()[0] <= j * 100 + 100 and i * 100 <= pygame.mouse.get_pos()[
                    1] <= i * 100 + 100:
                    if casse == 0:
                        pygame.draw.rect(screen, (102, 103, 102), pygame.Rect(j * 100, i * 100, 100, 100))
                        if pygame.mouse.get_pressed(3)[0]:
                            vierge[i][j] = "x"
                    if casse == 1:
                        pygame.draw.rect(screen, "green", pygame.Rect(j * 100, i * 100, 100, 100))
                        if pygame.mouse.get_pressed(3)[0]:
                            vierge[i][j] = "f"
                    if casse == 2:
                        pygame.draw.rect(screen, "blue", pygame.Rect(j * 100, i * 100, 100, 100))
                        if pygame.mouse.get_pressed(3)[0]:
                            vierge[i][j] = "0"
                    if casse == 3:
                        pygame.draw.rect(screen, "black", pygame.Rect(j * 100, i * 100, 100, 100), 1)
                        if pygame.mouse.get_pressed(3)[0]:
                            vierge[i][j] = "-"
    pygame.draw.rect(screen, "black", (1175, 1175, 25, 25))
    pygame.draw.rect(screen, "red", (1175, 0, 25, 25))
    font = pygame.font.Font(None, 30)
    text = font.render("x", True, (255, 255, 255))
    screen.blit(text, (1175 + 7, 2))
    text = font.render("s", True, (255, 255, 255))
    screen.blit(text, (1175 + 7, 1175))

    return 2


def selection():
    jo = 0
    real = 0
    for i in range(len(level)):
        pygame.draw.rect(screen, "purple", (real * 50, jo * 50, 50, 50))
        pygame.draw.rect(screen, "black", (real * 50, jo * 50, 50, 50), 3)
        font = pygame.font.Font(None, 30)
        text = font.render(str(i+1), True, (255, 255, 255))
        screen.blit(text, (real*50+15,jo*50+15))
        if i % 24 == 23:
            real -= 24
            jo += 1
        real += 1
    jo = 0
    real = 0
    for i in range(len(level)):

        if real * 50 <= pygame.mouse.get_pos()[0] <= real * 50 + 50 and jo * 50 <= pygame.mouse.get_pos()[
            1] <= jo * 50 + 50:
            if pygame.mouse.get_pressed(3)[0]:
                square.niveau = i
                square.changement()
                return 1
        if i % 24 == 23:
            real -= 24
            jo += 1
        real += 1
    if 1175 <= pygame.mouse.get_pos()[0] <= 1175 + 25 and 0 <= pygame.mouse.get_pos()[1] <= 25:
        if pygame.mouse.get_pressed(3)[0]:
            screen.fill("black")
            return 0
    pygame.draw.rect(screen, "red", (1175, 0, 25, 25))
    font = pygame.font.Font(None, 30)
    text = font.render("x", True, (255, 255, 255))
    screen.blit(text, (1175+7,2))

    return 3


square = Square(300, 500, 50, 0, 0)
clock = pygame.time.Clock()
running = True
maj = 0
jouer = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and jouer == 1:
                square.speed_y -= 5
            if event.key == pygame.K_DOWN and jouer == 1:
                square.speed_y += 5
            if event.key == pygame.K_RIGHT and jouer == 1:
                square.speed_x += 5
            if event.key == pygame.K_LEFT and jouer == 1:
                square.speed_x -= 5
            if event.key == pygame.K_ESCAPE and jouer == 1:
                jouer = 0
            if event.key == pygame.K_r and jouer == 1:
                square.x = square.debut.x + 25
                square.y = square.debut.y + 25
                square.speed_x = 0
                square.speed_y = 0
            if event.key == pygame.K_ESCAPE and jouer == 0:
                jouer = 1
            if event.key == pygame.K_ESCAPE and jouer == 1:
                jouer = 0
        if event.type == pygame.MOUSEBUTTONDOWN and jouer == 4:
            jouer = 0
            square.niveau =0
            square.changement()
            time.sleep(0.5)
            screen.fill("black")
        if event.type == pygame.KEYDOWN and jouer == 5:
            screen.fill("white")
            jouer = 2

    if jouer == 3:
        screen.fill("black")
        jouer = selection()
    if jouer==4:
        screen.fill("black")
        font = pygame.font.Font(None, 30)
        text = font.render("Thank you very much for playing this little game.", True, (255, 255, 255))
        screen.blit(text, (0, 0))
        text = font.render("this is my first public project", True, (255, 255, 255))
        screen.blit(text, (0, 40))
        text = font.render(" I am a beginner coder, but I have invested all my passion for this field.", True, (255, 255, 255))
        screen.blit(text, (0, 80))
        text = font.render("So I sincerely hope you will have liked it.", True, (255, 255, 255))
        screen.blit(text, (0, 120))
        text = font.render("The code is not very elaborate and clean, but I tried to make sure that there are as few bugs as possible.", True, (255, 255, 255))
        screen.blit(text, (0, 160))
        text = font.render(" (also because I developed it in a few days)", True, (255, 255, 255))
        screen.blit(text, (0, 200))
        text = font.render("there may be future updates, with new game mechanics", True, (255, 255, 255))
        screen.blit(text, (0, 240))
        text = font.render("Thanking you,",True, (255, 255, 255))
        screen.blit(text, (0, 280))
        text = font.render("Kayton",True, (255, 255, 255))
        screen.blit(text, (0, 320))
        text = font.render("(click on any mouse button to return to the menu)", True, (255, 255, 255))
        screen.blit(text, (0, 360))
    if jouer == 5:
        screen.fill("black")
        font = pygame.font.Font(None, 30)
        text = font.render("left click to place the block", True, (255, 255, 255))
        screen.blit(text, (0, 0))
        text = font.render("right click to change block", True, (255, 255, 255))
        screen.blit(text, (0, 40))
        text = font.render("When the click shows nothing it is a white block (to remove what you have already put)", True, (255, 255, 255))
        screen.blit(text, (0, 80))
        text = font.render("the 's' at the bottom right is for save",
                           True, (255, 255, 255))
        screen.blit(text, (0, 120))
        text = font.render("the 'x' in the upper right corner is to exit without saving",
                           True, (255, 255, 255))
        screen.blit(text, (0, 160))
        text = font.render("once saved there is no option to delete the saved level ",
                           True, (255, 255, 255))
        screen.blit(text, (0, 200))
        text = font.render("you will have to go to the 'level.txt' file and delete the level line manually",
                           True, (255, 255, 255))
        screen.blit(text, (0, 240))
        text = font.render("if you don't want to crash the game, you have to put only one blue block and one green block",
                           True, (255, 255, 255))
        screen.blit(text, (0, 280))
        text = font.render("press any key on the keyboard to continue",
                           True, (255, 255, 255))
        screen.blit(text, (0, 320))





    if jouer == 1:
        screen.fill((255, 255, 255))
        square.update()
        jouer = square.draw()
    if jouer == 0:
        jouer = menu()
    if jouer == 2:
        if pygame.mouse.get_pressed(3)[2]:
            if casse == 3:
                casse = 0
            else:
                casse += 1
            time.sleep(0.1)

        screen.fill((255, 255, 255))
        jouer = nouveau()
        maj = 2

    if jouer == 0 and maj == 2:
        fic = open("level.txt", "r")
        lv = 0
        level = {}
        for line in fic:
            vierge = [["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
                      ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
                      ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
                      ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
                      ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
                      ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
                      ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
                      ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
                      ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
                      ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
                      ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
                      ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"]
                      ]
            tabl = line
            vbn = []
            k = 0
            for i in range(len(tabl)):
                vbn.append(tabl[i])
            for i in range(len(vierge)):
                for j in range(len(vierge[0])):
                    vierge[i][j] = vbn[k]
                    k += 1
            mape = vierge
            level[lv] = mape
            lv += 1
        fic.close()
        vierge = [["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
                  ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
                  ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
                  ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
                  ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
                  ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
                  ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
                  ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
                  ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
                  ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
                  ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
                  ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"]
                  ]
        maj = 0

    pygame.display.update()
    clock.tick(91)
pygame.quit()
sys.exit()
