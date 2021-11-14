import pygame
import math
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

colours = {"White" : (255, 255, 255), "Black" : (0, 0, 0), "Red" : (255, 0, 0), "Blue" : (0, 0, 255), "Green" : (0, 255, 0)}
orighpamt = 10
gold_dropped = 10
Whetstone_Level = 1
Mercernary_Level = 0
Assassin_Level = 0
Sniper_Level = 0
current_monster = 0
Mercernary_CPS = 0
Assassin_CPS = 0
Sniper_CPS = 0
level = 1
goldamt = 250
clickdamage = 100000000000000000
WhetstoneCost = 1
Mercernary_Cost = 50
Assassin_Cost = 250
Sniper_Cost = 1000
second = 0
counter = 30000

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
        def __init__(self, x, y, sx, sy, bcolour, fbcolour, font, fontsize, fcolour, text, tiptext):
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
            self.tiptextsurface = self.buttonf.render(tiptext, False, (0, 0, 0), (255, 255, 0))
        def showButton(self, display):
            if(self.current):
                pygame.draw.rect(display, self.fbcolour, (self.x, self.y, self.sx, self.sy))
                                
            else:
                pygame.draw.rect(display, self.bcolour, (self.x, self.y, self.sx, self.sy))

            textsurface = self.buttonf.render(self.text, False, self.fcolour)
            display.blit(textsurface, ((self.x + (self.sx/2) - (self.fontsize/2)*(len(self.text)/2) - 5,(self.y + (self.sy/2) -(self.fontsize/2) - 4))))
            #if self.current:
                #mouse_pos = pygame.mouse.get_pos()
                #display.blit(self.tiptextsurface, (mouse_pos[0]+16, mouse_pos[1]))            
        def showTip(self, display):
            if self.current:
                mouse_pos = pygame.mouse.get_pos()
                display.blit(self.tiptextsurface, (mouse_pos[0]+16, mouse_pos[1]))        
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

hitpoints = orighpamt

Assassin_Upgrade = Button(10, 300, 125, 50, colours["Black"], colours["Red"], "arial", 15, colours["White"], "Assassin", "Upgrade the Assassin for added DPS")
Assassin_Damage_Level = Button(135, 300, 125, 50, colours["Black"], colours["Red"], "arial", 15, colours["White"], str(Assassin_Level), "")
Assassin_Damage_Cost = Button(260, 300, 125, 50, colours["Black"], colours["Red"], "arial", 15, colours["White"], str(int(round(Assassin_Cost))), "")
Sniper_Upgrade = Button(10, 400, 125, 50, colours["Black"], colours["Red"], "arial", 15, colours["White"], "Sniper", "Upgrade the Sniper for added DPS")
Sniper_Damage_Level = Button(135, 400, 125, 50, colours["Black"], colours["Red"], "arial", 15, colours["White"], str(Sniper_Level), "")
Sniper_Damage_Cost = Button(260, 400, 125, 50, colours["Black"], colours["Red"], "arial", 15, colours["White"], str(int(round(Sniper_Cost))), "")
Mercernary_Upgrade = Button(10, 200, 125, 50, colours["Black"], colours["Red"], "arial", 15, colours["White"], "Mercernary", "Upgrade the Mercerary for added DPS")
Mercernary_Damage_Level = Button(135, 200, 125, 50, colours["Black"], colours["Red"], "arial", 15, colours["White"], str(Mercernary_Level), "")
Mercernary_Damage_Cost = Button(260, 200, 125, 50, colours["Black"], colours["Red"], "arial", 15, colours["White"], str(int(round(Mercernary_Cost))), "")
clickdamagelevel = Button(135, 100, 125, 50, colours["Black"], colours["Red"], "arial", 15, colours["White"], str(Whetstone_Level), "")
clickdamagecost = Button(260, 100, 125, 50, colours["Black"], colours["Red"], "arial", 15, colours["White"], str(int(round(WhetstoneCost))), "")
clickdamageupgrade = Button(10, 100, 125, 50, colours["Black"], colours["Red"], "arial", 15, colours["White"], "Whetstone", "Sharpen Your Sword for added Click Damage")
Gold = Button(10, 50, 125, 50, colours["Black"], colours["Black"], "arial", 15, colours["White"], "Gold: {fname}".format(fname = str(goldamt)), "")
shopButton = Button(125, 500, 150, 50, colours["Black"], colours["Red"], "arial", 20, colours["White"], "Shop", "Enter The Shop")
DungeonButton = Button(125, 500, 150, 50, colours["Black"], colours["Blue"], "arial", 20, colours["White"], "Dungeon", "")
hitboxButton = Button(80, 50, 280, 400, colours["White"], colours["White"], "arial", 20, colours["White"], "", "")
hitpointamount = Button(100, 0, 200, 50, colours["White"], colours["Black"], "arial", 20, colours["Black"], str(hitpoints), "")
boss_timer = Button(125, 450, 150, 50, colours["Black"], colours["Red"], "arial", 20, colours["White"], "Boss", "")
goblin = Enemy(0 , 20, "images\goblin-resized.png")
monster2 = Enemy(50 , 100, "images\monster2.png")
monster3 = Enemy(50 , 100, "images\monster3.png")
monster4 = Enemy(50 , 100, "images\monster4.png")
monster5 = Enemy(50 , 100, "images\monster5.png")
monster6 = Enemy(50 , 100, "images\monster6.png")
monster7 = Enemy(50 , 100, "images\monster7.png")
monster8 = Enemy(50 , 100, "images\monster8.png")
monster9 = Enemy(50 , 100, "images\monster9.png")
monster_boss = Enemy(50 , 100, "images\monster_boss.png")
toggle = False
while not done:
    dt = clock.tick()
        
        
    menuScreen.screenUpdate()
    screen2.screenUpdate()
    mouse_pos = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    if current_monster == 10:
        level += 1
        current_monster = 0
        
    if goldamt < 0:
        goldamt == 0    
    if current_monster == 9:
        counter -= dt
        boss_timer = Button(125, 450, 150, 50, colours["Black"], colours["Red"], "arial", 20, colours["White"], str(int(counter/1000)),"")
        boss_timer.showButton(menuScreen.returnTitle())
    if counter == 0:
        current_monster = 0
        hitpoints = round(orighpamt*(int(level-1) + 1.55**(level-1)))
        counter = 30000
        
    total_CPS = Mercernary_CPS + Assassin_CPS + Sniper_CPS       
    orighpamt = 10
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
        if current_monster == 0:
            goblin.draw(menuScreen.screen)
            counter = 30000
        elif current_monster== 1:
            monster2.draw(menuScreen.screen)
        elif current_monster== 2:
            monster3.draw(menuScreen.screen)
        elif current_monster== 3:
            monster4.draw(menuScreen.screen)
        elif current_monster== 4:
            monster5.draw(menuScreen.screen)
        elif current_monster== 5:
            monster6.draw(menuScreen.screen)
        elif current_monster== 6:
            monster7.draw(menuScreen.screen)
        elif current_monster== 7:
            monster8.draw(menuScreen.screen)
        elif current_monster== 8:
            monster9.draw(menuScreen.screen)
        elif current_monster== 9:
            monster_boss.draw(menuScreen.screen)            
        hitpointamount.showButton(menuScreen.returnTitle())
        shopButton.showButton(menuScreen.returnTitle())
        shopButton.showTip(menuScreen.returnTitle())
        second += dt
        if second >= 1000:
            hitpoints -= total_CPS
            second = 0
        if attack:
            hitpoints -= clickdamage
        if hitpoints < 0:
            hitpoints = 0
            print(current_monster)
        hitpointamount = Button(100, 0, 200, 50, colours["White"], colours["Black"], "arial", 20, colours["Black"], str(hitpoints), "")
        hitpointamount.showButton(menuScreen.returnTitle())
        if hitpoints == 0:
            
            goldamt += gold_dropped
            Gold = Button(10, 50, 125, 50, colours["Black"], colours["Black"], "arial", 15, colours["White"], "Gold: {fname}".format(fname = str(goldamt)), "")
            
            orighpamt = round(orighpamt*(int(level-1) + 1.55**(level-1)))
            current_monster += 1
            hitpoints = orighpamt
            if current_monster == 10:
                orighpamt = round(10*(int(level) + 1.55**(level)))
                hitpoints = orighpamt
            if current_monster == 9:
                hitpoints = hitpoints * 10
                
            gold_dropped = math.ceil(hitpoints/15)
            hitpointamount = Button(100, 0, 200, 50, colours["White"], colours["Black"], "arial", 20, colours["Black"], str(hitpoints), "")
            hitpointamount.showButton(menuScreen.returnTitle())                
            pygame.display.update()
        if screen2button:
            win = screen2.makeCurrent()

            menuScreen.endCurrent()

    elif screen2.checkUpdate():
        returnm = DungeonButton.focusCheck(mouse_pos, mouse_click)
        DungeonButton.showButton(screen2.returnTitle())
        clickdamageupgrade.showButton(screen2.returnTitle())
        clickdamagelevel.showButton(screen2.returnTitle())
        Gold.showButton(screen2.returnTitle())
        clickdamagecost.showButton(screen2.returnTitle())
        Mercernary_Upgrade.showButton(screen2.returnTitle())
        Mercernary_Damage_Level.showButton(screen2.returnTitle())
        Mercernary_Damage_Cost.showButton(screen2.returnTitle())
        Assassin_Upgrade.showButton(screen2.returnTitle())
        Assassin_Damage_Level.showButton(screen2.returnTitle())
        Assassin_Damage_Cost.showButton(screen2.returnTitle())
        
        
        Sniper_Upgrade.showButton(screen2.returnTitle())
        Sniper_Damage_Level.showButton(screen2.returnTitle())
        Sniper_Damage_Cost.showButton(screen2.returnTitle())
        clickdamageupgrade.showTip(menuScreen.returnTitle())
        Mercernary_Upgrade.showTip(menuScreen.returnTitle())
        Assassin_Upgrade.showTip(menuScreen.returnTitle())
        Sniper_Upgrade.showTip(menuScreen.returnTitle())
        if goldamt < 0:
            goldamt = 0
        if clickdamageupgrade.focusCheck(mouse_pos, mouse_click):
            if goldamt >= WhetstoneCost:
                #Made mistake here where the cost was increased before it was deducted leading to negative gold
                Whetstone_Level += 1
                clickdamage += 2
                goldamt = goldamt - WhetstoneCost
                WhetstoneCost = math.ceil((5+Whetstone_Level)*1.07**(Whetstone_Level-1))
                
                Gold = Button(10, 50, 125, 50, colours["Black"], colours["Black"], "arial", 15, colours["White"], "Gold: {fname}".format(fname = str(math.ceil(goldamt))), "")
                Gold.showButton(screen2.returnTitle())
                clickdamagelevel = Button(135, 100, 125, 50, colours["Black"], colours["Red"], "arial", 15, colours["White"], str(Whetstone_Level), "")
                clickdamagelevel.showButton(screen2.returnTitle())
                clickdamagecost = Button(260, 100, 125, 50, colours["Black"], colours["Red"], "arial", 15, colours["White"], str(int(math.floor(WhetstoneCost))), "")
                clickdamagecost.showButton(screen2.returnTitle())
        if Mercernary_Upgrade.focusCheck(mouse_pos, mouse_click):
            if goldamt >= Mercernary_Cost:
                #During testing the gold amount was going negative after upgrading Mercerary due to error where i was checking if gold was larger than whetstone cost
                goldamt = goldamt - Mercernary_Cost
                Mercernary_Level += 1
                Mercernary_CPS += 5
                
                Mercernary_Cost = math.ceil((50* Mercernary_Level)*1.07**(Mercernary_Level-1))
                Gold = Button(10, 50, 125, 50, colours["Black"], colours["Black"], "arial", 15, colours["White"], "Gold: {fname}".format(fname = str(math.ceil(goldamt))), "")
                Gold.showButton(screen2.returnTitle())
                Mercernary_Damage_Level = Button(135, 200, 125, 50, colours["Black"], colours["Red"], "arial", 15, colours["White"], str(Mercernary_Level))
                Mercernary_Damage_Level.showButton(screen2.returnTitle())
                Mercernary_Damage_Cost = Button(260, 200, 125, 50, colours["Black"], colours["Red"], "arial", 15, colours["White"], str(int(round(Mercernary_Cost))), "")                
                Mercernary_Damage_Cost.showButton(screen2.returnTitle())
        if Assassin_Upgrade.focusCheck(mouse_pos, mouse_click):
            if goldamt >= Assassin_Cost:
                    
                goldamt = goldamt - Assassin_Cost
                Assassin_Level += 1
                Assassin_CPS += 22
                
                Assassin_Cost = math.ceil((250* Assassin_Level)*1.07**(Assassin_Level-1))
                Gold = Button(10, 50, 125, 50, colours["Black"], colours["Black"], "arial", 15, colours["White"], "Gold: {fname}".format(fname = str(math.ceil(goldamt))), "")
                Gold.showButton(screen2.returnTitle())
                Assassin_Damage_Level = Button(135, 300, 125, 50, colours["Black"], colours["Red"], "arial", 15, colours["White"], str(Assassin_Level), "")
                Assassin_Damage_Level.showButton(screen2.returnTitle())
                Assassin_Damage_Cost = Button(260, 300, 125, 50, colours["Black"], colours["Red"], "arial", 15, colours["White"], str(int(round(Assassin_Cost))), "")                
                Assassin_Damage_Cost.showButton(screen2.returnTitle())
        if Sniper_Upgrade.focusCheck(mouse_pos, mouse_click):
            if goldamt >= Sniper_Cost:
            
                goldamt = goldamt - Sniper_Cost
                Sniper_Level += 1
                Sniper_CPS += 74
    
                Sniper_Cost = math.ceil((1000* Sniper_Level)*1.07**(Sniper_Level-1))
                Gold = Button(10, 50, 125, 50, colours["Black"], colours["Black"], "arial", 15, colours["White"], "Gold: {fname}".format(fname = str(math.ceil(goldamt))), "")
                Gold.showButton(screen2.returnTitle())
                Sniper_Damage_Level = Button(135, 400, 125, 50, colours["Black"], colours["Red"], "arial", 15, colours["White"], str(Sniper_Level), "")
                Sniper_Damage_Level.showButton(screen2.returnTitle())
                Sniper_Damage_Cost = Button(260, 400, 125, 50, colours["Black"], colours["Red"], "arial", 15, colours["White"], str(int(round(Sniper_Cost))), "")                
                Sniper_Damage_Cost.showButton(screen2.returnTitle())     

        if returnm:
            win = menuScreen.makeCurrent()
            screen2.endCurrent()

    pygame.display.update()
pygame.quit()