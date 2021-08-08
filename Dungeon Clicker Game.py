import pygame
pygame.init()
pygame.font.init()
colours = {"White" : (255, 255, 255), "Black" : (0, 0, 0), "Red" : (255, 0, 0), "Blue" : (0, 0, 255), "Green" : (0, 255, 0)}
clickdamage = 1
Whetstone_Level = 0

class Screen():
    def __init__(self, title, width=400, height=600, fill=colours["White"]):
        self.title=title
        self.width=width
        self.height = height
        self.fill = fill
        self.current = False

    def makeCurrent(self):
        pygame.display.set_caption(self.title)
        self.current = True
        self.screen = pygame.display.set_mode((self.width, self.height))

    def endCurrent(self):
        self.current = False

    def checkUpdate(self):
        return self.current
    def screenUpdate(self):
        if(self.current):
            self.screen.fill(self.fill)

    def returnTitle(self):
        return self.screen

class Button():
        def __init__(self, x, y, sx, sy, bcolour, fbcolour, font, fontsize, fcolour, text):
            self.x = x
            self.y = y
            self.sx = sx
            self.sy = sy
            self.bcolour = bcolour
            self.fbcolour = fbcolour
            self.fcolour = fcolour
            self.fontsize = fontsize
            self.text = text
            self.current = False
            self.buttonf = pygame.font.SysFont(font, fontsize)
        def showButton(self, display):
            if(self.current):
                pygame.draw.rect(display, self.fbcolour, (self.x, self.y, self.sx, self.sy))
            else:
                pygame.draw.rect(display, self.bcolour, (self.x, self.y, self.sx, self.sy))

            textsurface = self.buttonf.render(self.text, False, self.fcolour)
            display.blit(textsurface, ((self.x + (self.sx/2) - (self.fontsize/2)*(len(self.text)/2) - 5,(self.y + (self.sy/2) -(self.fontsize/2) - 4))))
        def focusCheck(self, mousepos, mouseclick):
            if(mousepos[0] >= self.x and mousepos[0] <= self.x + self.sx and mousepos[1] >= self.y and mousepos[1] <= self.y + self.sy):
                self.current = True
                return mouseclick
            else:
                self.current = False
                return False
class Enemy(pygame.sprite.Sprite):

    def __init__(self, dx, dy, filename):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(filename).convert()

        self.rect = self.image.get_rect()
        self.rect.x = dx
        self.rect.y = dy



    def draw(self, screen):
        screen.blit(self.image, self.rect)



menuScreen = Screen("Menu Screen")
screen2 = Screen("Screen 2")

win = menuScreen.makeCurrent()


done = False
font = pygame.font.Font('freesansbold.ttf', 32)

clickdamagelevel = Button(160, 10, 150, 50, colours["Black"], colours["Red"], "arial", 15, colours["White"], str(Whetstone_Level))
clickdamageupgrade = Button(10, 10, 150, 50, colours["Black"], colours["Red"], "arial", 15, colours["White"], "Whetstone")
shopButton = Button(125, 500, 150, 50, colours["Black"], colours["Red"], "arial", 20, colours["White"], "Shop")
DungeonButton = Button(125, 500, 150, 50, colours["Black"], colours["Blue"], "arial", 20, colours["White"], "Dungeon")
hitboxButton = Button(80, 50, 280, 400, colours["White"], colours["Red"], "arial", 20, colours["White"], "")
goblin = Enemy(0 , 20, "images\goblin-resized.png")
goblin2 = Enemy(0 , 20, "images\goblin.jpg")
toggle = False
while not done:
    menuScreen.screenUpdate()
    screen2.screenUpdate()
    mouse_pos = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()

    mouse_click = False
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_click = True

    if menuScreen.checkUpdate():
        screen2button = shopButton.focusCheck(mouse_pos, mouse_click)
        attack = hitboxButton.focusCheck(mouse_pos, mouse_click)
        hitboxButton.showButton(menuScreen.returnTitle())
        goblin.draw(menuScreen.screen)
        shopButton.showButton(menuScreen.returnTitle())
        if attack:
            print("hitpoints - click damage")
        if screen2button:
            win = screen2.makeCurrent()

            menuScreen.endCurrent()

    elif screen2.checkUpdate():
        returnm = DungeonButton.focusCheck(mouse_pos, mouse_click)
        DungeonButton.showButton(screen2.returnTitle())
        clickdamageupgrade.showButton(screen2.returnTitle())
        clickdamagelevel.showButton(screen2.returnTitle())
        if clickdamageupgrade.focusCheck(mouse_pos, mouse_click):
            Whetstone_Level += 1
            clickdamagelevel = Button(160, 10, 150, 50, colours["Black"], colours["Red"], "arial", 15, colours["White"], str(Whetstone_Level))
            clickdamagelevel.showButton(screen2.returnTitle())
        if returnm:
            win = menuScreen.makeCurrent()
            screen2.endCurrent()

    pygame.display.update()

pygame.quit()