import pygame
pygame.init()
pygame.font.init()
colours = {"White" : (255, 255, 255), "Black" : (0, 0, 0), "Red" : (255, 0, 0), "Blue" : (0, 0, 255), "Green" : (0, 255, 0)}

#class Item:
    #def __init__(self, rect, text, base_price, base_cps_each):
        #self.rect = rect
        #self.text = text
        #self.count = 0
        #self.base_price = base_price
        #self.cps_each = base_cps_each

    #def draw(self, surface):
        ##draw background
        #pygame.draw.rect(surface, BUTTON_BG_COLOR, self.rect, 0)
        ##draw border
        #pygame.draw.rect(surface, BUTTON_BG_COLOR, self.rect, 2)
        ##draw text
        #text_surface = FONT.render(str(self.count) + "x" + self.text + " $" + str(int(self.price())), False, BLACK)
        #text_rect = text_surface.get_rect()
        #text_rect.topleft = (self.rect.left + 10, self.rect.top + self.rect.height * 0.25)
        #surface.blit(text_surface, text_rect)

    #def total_cps(self):
        #return self.cps_each * self.count

    #def price(self):
        #return self.base_price * 1.15**self.count

    #def click(self):
        #price = self.price()
        #global COOKIES
        #if COOKIES >= price:
            #self.count += 1
            #COOKIES -= price

    #def collidepoint(self, point):
        #return self.rect.collidepoint(point)

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
                return mouseclick[0]
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
def text_objects(text, font):
    textSurface = font.render(text, True, "Black")
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

done = False
font = pygame.font.Font('freesansbold.ttf', 32)
clickdamage = 1
Whetstone_Level = 0
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
    mouse_click = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()
    
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
        if clickdamageupgrade.focusCheck(mouse_pos, mouse_click):
            message_display("Whetstone Level" + str(Whetstone_Level))
        if returnm:
            win = menuScreen.makeCurrent()
            screen2.endCurrent()
    
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            done = True
    
    
    pygame.display.update()
    
pygame.quit()