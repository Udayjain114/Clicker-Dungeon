import pygame
import math
import json
import os
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
# Dictionary To hold colours for future use
Colours = {
    "White": (255, 255, 255),
    "Black": (0, 0, 0),
    "Red": (255, 0, 0),
    "Blue": (0, 0, 255),
    "Green": (0, 255, 0)
}
# Dictionary that holds all of my data, this is used so that later i can use
# Json to load and save said data to allow for save states
data = {
    'Original_HP_Amount': 10,
    'gold_dropped': 10,
    'Whetstone_Level': 0,
    'Mercernary_Level': 0,
    'Assassin_Level': 0,
    'Sniper_Level': 0,
    'current_monster': 0,
    'Mercernary_CPS': 0,
    'Assassin_CPS': 0,
    'Sniper_CPS': 0,
    'level': 1,
    'Gold_Amount': 0,
    'Click_Damage': 1,
    'Whetstone_Cost': 1,
    'Mercernary_Cost': 50,
    'Assassin_Cost': 150,
    'Sniper_Cost': 500,
    'second': 0,
    'counter': 30000,
    'Stage': 1
}
Check_File = os.path.isfile("Save_Data.txt")
if not Check_File:
    with open("Save_Data.txt", "x") as score_file:
        json.dump(data, score_file)
        data["Stage"] == 1
# This class allows me to create multiple screens that I can easily switch
# Between


class Screen:
    def __init__(self, title, x, y, Colour):
        self.title = title
        self.width = x
        self.height = y
        self.fill = Colour
        self.current = False
# Makes screen current when definition is called

    def Make_Current(self):
        pygame.display.set_caption(self.title)
        self.current = True
        self.screen = pygame.display.set_mode((self.width, self.height))
# Makes screen no longer current when called

    def End_Current(self):
        self.current = False
# Checks if screen is current

    def Check_Update(self):
        return self.current
# If screen is current then will update the screen and fill colour

    def Screen_Update(self):
        if(self.current):
            self.screen.fill(self.fill)

    def Return_Title(self):
        return self.screen

# Class that allows me to make buttons that can be clicked and can show pop up
# text easily


class Button():
        def __init__(self, x, y, sx, sy, B_Colour, Fb_Colour, font, Font_Size,
                     F_Colour, text, Tip_Text):
            self.rect = pygame.Rect(x, y, sx, sy)
            self.x = x
            self.y = y
            self.sx = sx
            self.sy = sy
            self.B_Colour = B_Colour
            self.Fb_Colour = Fb_Colour
            self.F_Colour = F_Colour
            self.Font_Size = Font_Size
            self.text = text
            self.current = False
            self.Button_F = pygame.font.SysFont(font, Font_Size)
            self.Text_Surface = self.Button_F.render(text,
                                                     False, self.F_Colour)
            self.tipText_Surface = self.Button_F.render(Tip_Text,
                                                        False,
                                                        (0, 0, 0),
                                                        (255, 255, 0))
# Definiton Shows Buttons

        def Show_Button(self, display):
            Colour = self.Fb_Colour if self.current else self.B_Colour
            pygame.draw.rect(display, Colour, self.rect)
            display.blit(self.Text_Surface,
                         self.Text_Surface.get_rect(center=self.rect.center))
# Definition shows the button tips

        def Show_Tip(self, display):
            if self.current:
                mouse_pos = pygame.mouse.get_pos()
                display.blit(self.tipText_Surface, (mouse_pos[0] + 16,
                                                    mouse_pos[1]))
# Checks if my mouse is hovering over and if i've clicked the button

        def Focus_Check(self, mousepos, mouseclick):
            if(mousepos[0] >= self.x and mousepos[0] <= self.x + self.sx and
               mousepos[1] >= self.y and mousepos[1] <= self.y + self.sy):
                self.current = True
                return mouseclick
            else:
                self.current = False
                return False


# Class that lets me call different sprites called it enemys but can really be
# used for any sprite
class Enemy(pygame.sprite.Sprite):

    def __init__(self, dx, dy, file_name):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(file_name).convert()

        self.rect = self.image.get_rect()
        self.rect.x = dx
        self.rect.y = dy

    def draw(self, screen):
        screen.blit(self.image, self.rect)


# This is just all of my screens that i will be switching between
Information_Screen = Screen("Information", 400, 350, Colours["White"])
Opening_Screen = Screen("Menu", 400, 350, Colours["White"])
Dungeon_Screen = Screen("Dungeon", 400, 700, Colours["White"])
Shop_Screen = Screen("Shop ", 400, 700, Colours["White"])
Game_Over_Screen = Screen("Game Over", 400, 700, Colours["White"])
win = Opening_Screen.Make_Current()


done = False
font = pygame.font.Font('freesansbold.ttf', 32)
# All the buttons that i will need for the game are here
HP = data['Original_HP_Amount']
Return_To_Menu_Button = Button(100, 650, 200, 50, Colours["Black"], Colours["Red"],
                      "arial", 18, Colours["White"], "Menu ", "Return to Menu")
Restart_Game = Button(000, 000, 400, 200, Colours["Black"], Colours["Red"],
                      "arial", 30, Colours["White"], "Play Again? ", "")
Game_Information_Part_1 = Button(000, 000, 400, 20, Colours["White"],
                                 Colours["Red"], "arial", 30, Colours["Black"],
                                 "To play the game you have to click ", "")
Game_Information_Part_2 = Button(000, 30, 400, 20, Colours["White"],
                                 Colours["Red"], "arial", 30, Colours["Black"],
                                 " on the monsters to deal damage to ", "")
Game_Information_Part_3 = Button(000, 60, 400, 20, Colours["White"],
                                 Colours["Red"], "arial", 30, Colours["Black"],
                                 "them. Once you bring their HP down", "")
Game_Information_Part_4 = Button(000, 90, 400, 20, Colours["White"],
                                 Colours["Red"], "arial", 30, Colours["Black"],
                                 "to zero they will drop gold. You can ", "")
Game_Information_Part_5 = Button(000, 120, 400, 20, Colours["White"],
                                 Colours["Red"], "arial", 30, Colours["Black"],
                                 "use this gold in the shop to buy ", "")
Game_Information_Part_6 = Button(000, 150, 400, 20, Colours["White"],
                                 Colours["Red"], "arial", 30, Colours["Black"],
                                 "upgrades. These upgrades make", "")
Game_Information_Part_7 = Button(000, 180, 400, 20, Colours["White"],
                                 Colours["Red"], "arial", 30, Colours["Black"],
                                 "either your Click Damage or your", "")
Game_Information_Part_8 = Button(000, 210, 400, 20, Colours["White"],
                                 Colours["Red"], "arial", 30, Colours["Black"],
                                 "Idle Damage stronger.", "")
Return_To_Menu = Button(100, 250, 200, 50, Colours["Black"], Colours["Red"],
                        "arial", 30, Colours["White"],
                        "Menu", "Return To Menu")
Game_Over_Button = Button(100, 500, 200, 50, Colours["Black"], Colours["Red"],
                          "arial", 20, Colours["White"],
                          "Congratulations You Won!", "")
Game_Information_Link = Button(100, 133, 200, 50, Colours["Black"],
                               Colours["Red"], "arial", 20, Colours["White"],
                               "Information", "")
New_Game = Button(100, 000, 200, 50, Colours["Black"], Colours["Red"], "arial",
                  20, Colours["White"], "New Game", "")
Continue_Game = Button(100, 266, 200, 50, Colours["Black"], Colours["Red"],
                       "arial", 20, Colours["White"], "Continue", "")
Level_Info = Button(100, 600, 200, 50, Colours["Black"], Colours["Red"],
                    "arial", 20, Colours["White"],
                    "Level: {0} Stage: {1}".format(data['level'],
                                                   data['Stage']), "")
Assassin_Upgrade = Button(10, 300, 125, 50, Colours["Black"], Colours["Red"],
                          "arial", 15, Colours["White"], "Assassin",
                          "Upgrade the Assassin for added DPS")
Assassin_Damage_Level = Button(135, 300, 125, 50, Colours["Black"],
                               Colours["Red"], "arial", 15, Colours["White"],
                               str(data['Assassin_Level']), "")
Assassin_Damage_Cost = Button(260, 300, 125, 50, Colours["Black"],
                              Colours["Red"], "arial", 15, Colours["White"],
                              str(int(round(data['Assassin_Cost']))), "")
Sniper_Upgrade = Button(10, 400, 125, 50, Colours["Black"], Colours["Red"],
                        "arial", 15, Colours["White"], "Sniper",
                        "Upgrade the Sniper for added DPS")
Sniper_Damage_Level = Button(135, 400, 125, 50, Colours["Black"],
                             Colours["Red"], "arial", 15, Colours["White"],
                             str(data['Sniper_Level']), "")
Sniper_Damage_Cost = Button(260, 400, 125, 50, Colours["Black"],
                            Colours["Red"], "arial", 15, Colours["White"],
                            str(int(round(data['Sniper_Cost']))), "")
Mercernary_Upgrade = Button(10, 200, 125, 50, Colours["Black"], Colours["Red"],
                            "arial", 15, Colours["White"],
                            "Mercernary",
                            "Upgrade the Mercerary for added DPS")
Mercernary_Damage_Level = Button(135, 200, 125, 50, Colours["Black"],
                                 Colours["Red"], "arial", 15, Colours["White"],
                                 str(data['Mercernary_Level']), "")
Mercernary_Damage_Cost = Button(260, 200, 125, 50, Colours["Black"],
                                Colours["Red"], "arial", 15, Colours["White"],
                                str(int(round(data['Mercernary_Cost']))), "")
Click_Damage_Level = Button(135, 100, 125, 50,
                            Colours["Black"], Colours["Red"],
                            "arial", 15, Colours["White"],
                            str(data['Whetstone_Level']), "")
Click_Damage_Cost = Button(260, 100, 125, 50, Colours["Black"],
                           Colours["Red"], "arial", 15, Colours["White"],
                           str(int(round(data['Whetstone_Cost']))), "")
Click_Damage_Upgrade = Button(10, 100, 125, 50, Colours["Black"],
                              Colours["Red"], "arial", 15, Colours["White"],
                              "Whetstone",
                              "Sharpen Your Sword for added Click Damage")
Gold = Button(10, 50, 125, 50, Colours["Black"], Colours["Black"], "arial",
              15, Colours["White"],
              "Gold: {fname}".format(fname=str(data['Gold_Amount'])), "")
Gold_Dungeon = Button(10, 550, 400, 50, Colours["White"],
                      Colours["White"], "arial",
                      15, Colours["Black"],
                      "Gold: {fname}".format(fname=str(data['Gold_Amount'])),
                      "")
Total_CPS_Button = Button(300, 0, 100, 50, Colours["White"],
                          Colours["White"], "arial",
                          15, Colours["Black"],
                          str(data["Mercernary_CPS"] +
                          data["Assassin_CPS"] + data["Sniper_CPS"]),
                          "")
Total_Click_Damage_Button = Button(0, 0, 100, 50, Colours["White"],
                                   Colours["White"], "arial",
                                   15, Colours["Black"],
                                   str(data["Click_Damage"]),
                                    "")
Shop_Button = Button(125, 500, 150, 50, Colours["Black"], Colours["Red"],
                     "arial", 20, Colours["White"], "Shop", "Enter The Shop")
Dungeon_Button = Button(125, 500, 150, 50, Colours["Black"],
                        Colours["Blue"], "arial", 20, Colours["White"],
                        "Dungeon", "Enter The Dungeon")
Hitbox_Button = Button(80, 50, 280, 400, Colours["White"],
                       Colours["White"], "arial", 20, Colours["White"], "", "")
HP_Amount = Button(100, 0, 100, 50, Colours["White"], Colours["Black"],
                   "arial", 20, Colours["Black"], str(HP), "")
boss_timer = Button(125, 450, 150, 50, Colours["Black"], Colours["Red"],
                    "arial", 20, Colours["White"], "Boss", "")
cost = Button(260, 50, 125, 50, Colours["Black"],
              Colours["Red"], "arial", 18, Colours["White"],
              "cost", "")
upgrade_level = Button(135, 50, 125, 50,
                       Colours["Black"], Colours["Red"],
                       "arial", 18, Colours["White"],
                       "level", "")
goblin = Enemy(30, 80, "images\goblin.png")
monster_2 = Enemy(50, 100, "images\monster2.png")
monster_3 = Enemy(50, 100, "images\monster3.png")
monster_4 = Enemy(50, 100, "images\monster4.png")
monster_5 = Enemy(50, 100, "images\monster5.png")
monster_6 = Enemy(50, 100, "images\monster6.png")
monster_7 = Enemy(50, 100, "images\monster7.png")
monster_8 = Enemy(50, 100, "images\monster8.png")
monster_9 = Enemy(50, 100, "images\monster9.png")
monster_boss = Enemy(50, 100, "images\monster_boss.png")
toggle = False
while not done:
    dt = clock.tick()
    Opening_Screen.Screen_Update()
    Dungeon_Screen.Screen_Update()
    Shop_Screen.Screen_Update()
    Game_Over_Screen.Screen_Update()
    Information_Screen.Screen_Update()
    mouse_pos = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    # This part here is for resetting the current monster number so that
    # i dont get above 10
    if data['current_monster'] == 10:
        data['current_monster'] = 0
    if data['current_monster'] == 9:
        # This is the boss timer that counts down from 30s and will go back
        # to stage one in the level if countdown reaches 0
        data['counter'] -= dt
        boss_timer = Button(125, 450, 150, 50, Colours["Black"],
                            Colours["Red"],
                            "arial", 20, Colours["White"],
                            str(int(data['counter'] / 1000)), "")
        boss_timer.Show_Button(Dungeon_Screen.Return_Title())
    if data['counter'] < 0:
        # used a less than sign here because when I hadn't and had it equal to
        # 0 it would only work the first time around, likely because the time
        # would only equal zero for the first time as the second time its run
        # even a a very small fraction of  a second can make it so it never
        # actually equals zero only some negative number
        data['current_monster'] = 0
        data["Stage"] = 1
        if data['level'] == 1:
            data["level"] = 1
        elif data['level'] > 1:
            data['level'] -= 1
        Level_Info = Button(100, 600, 200, 50, Colours["Black"],
                            Colours["Red"],
                            "arial", 20, Colours["White"],
                            "Level: {0} Stage: {1}".format(data['level'],
                                                           data['Stage']), "")
        Level_Info.Show_Button(Dungeon_Screen.Return_Title())

        HP = round(data['Original_HP_Amount'] *
                   (int(data['level'] - 1) + 1.55**(data['level'] - 1)))
        data['counter'] = 30000

    total_CPS = (data['Mercernary_CPS'] + data['Assassin_CPS'] +
                 data['Sniper_CPS'])
    data['Original_HP_Amount'] = 10
    mouse_click = False
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):

            with open("Save_Data.txt", "w") as score_file:
                json.dump(data, score_file)

            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_click = True
    # This is all the components of the menu screen
    if Opening_Screen.Check_Update():
        New_Game.Show_Button(Opening_Screen.Return_Title())
        Continue_Game.Show_Button(Opening_Screen.Return_Title())
        Game_Information_Link.Show_Button(Opening_Screen.Return_Title())
        Game_Information_Link.Show_Tip(Opening_Screen.Return_Title())
        Start_Game = New_Game.Focus_Check(mouse_pos, mouse_click)
        Resume_Game = Continue_Game.Focus_Check(mouse_pos, mouse_click)
        See_Information = Game_Information_Link.Focus_Check(mouse_pos,
                                                            mouse_click)
# Will start a new game
        if Start_Game:
            win = Dungeon_Screen.Make_Current()
            with open("DO_NOT_EDIT.txt") as original_score_file:
                data = json.load(original_score_file)

            data["level"] == 1
            Opening_Screen.End_Current()
# Will continue the last game with everything they had and extra gold
# depending on DPS and how long they've been away
        if Resume_Game:
            win = Dungeon_Screen.Make_Current()
            Check_File = os.path.isfile("Save_Data.txt")
            if not Check_File:
                with open("DO_NOT_EDIT.txt") as original_score_file:
                    data = json.load(original_score_file)
                    data["level"] == 1

            if Check_File:
                with open("Save_Data.txt") as score_file:
                    data = json.load(score_file)
            Opening_Screen.End_Current()
            data["counter"] == 30000
            data["Stage"] -= 1
            if data["Stage"] <= 0:
                data["Stage"] += 2
            if data['current_monster'] == 9:
                data["level"] -= 1
                data["Stage"] += 10

            Gold_Dungeon = Button(10, 550, 400, 50,
                                  Colours["White"], Colours["White"], "arial",
                                  15, Colours["Black"],
                                  "Gold: {fname}".format(fname=str(
                                      data['Gold_Amount'])), "")
            Gold_Dungeon.Show_Button(Dungeon_Screen.Return_Title())
            Level_Info = Button(100, 600, 200, 50,
                                Colours["Black"], Colours["Red"],
                                "arial", 20, Colours["White"],
                                "Level: {0} Stage: {1}".format(
                                    data['level'], data['Stage']), "")
            Level_Info.Show_Button(Dungeon_Screen.Return_Title())
            HP = round(data['Original_HP_Amount'] *
                       (int(data['level'] - 1) + 1.55 ** (data['level'] - 1)))
            if data["current_monster"] == 9:
                HP = HP * 10
            HP_Amount = Button(100, 0, 200, 50, Colours["White"],
                               Colours["Black"],
                               "arial", 20, Colours["Black"], str(HP), "")
            HP_Amount.Show_Button(Dungeon_Screen.Return_Title())
# Take the user to a screen with the game information on it
        if See_Information:
            win = Information_Screen.Make_Current()
            Opening_Screen.End_Current()
# This is all the components of the information screen, mainly text and one
# button to go back to the start
    elif Information_Screen.Check_Update():
        Game_Information_Part_1.Show_Button(Information_Screen.Return_Title())
        Game_Information_Part_2.Show_Button(Information_Screen.Return_Title())
        Game_Information_Part_3.Show_Button(Information_Screen.Return_Title())
        Game_Information_Part_4.Show_Button(Information_Screen.Return_Title())
        Game_Information_Part_5.Show_Button(Information_Screen.Return_Title())
        Game_Information_Part_6.Show_Button(Information_Screen.Return_Title())
        Game_Information_Part_7.Show_Button(Information_Screen.Return_Title())
        Game_Information_Part_8.Show_Button(Information_Screen.Return_Title())
        Go_to_menu = Return_To_Menu.Focus_Check(mouse_pos, mouse_click)
        Return_To_Menu.Show_Button(Information_Screen.Return_Title())
        if Go_to_menu:
            win = Opening_Screen.Make_Current()
            Information_Screen.End_Current()
# This is the main game screen
    elif Dungeon_Screen.Check_Update():
        if data['level'] == 16 and data['current_monster'] == 0:

            win = Game_Over_Screen.Make_Current()
            Dungeon_Screen.End_Current()
        Total_CPS_Button = Button(300, 0, 100, 50, Colours["White"],
                                  Colours["White"], "arial",
                                  15, Colours["Black"], "DPS: {DPS}".format
                                  (DPS=str(data["Mercernary_CPS"] +
                                   data["Assassin_CPS"] +
                                   data["Sniper_CPS"])), "")
        Total_Click_Damage_Button = Button(0, 0, 100, 50, Colours["White"],
                                           Colours["White"], "arial",
                                           15, Colours["Black"],
                                           "Click Damage: {CD}".format(
                                               CD=str(data["Click_Damage"])),
                                           "")
        Return_To_Menu_Button.Show_Button(Dungeon_Screen.Return_Title())
        Go_Back = Return_To_Menu_Button.Focus_Check(mouse_pos, mouse_click)
        Return_To_Menu_Button.Show_Tip(Dungeon_Screen.Return_Title())
        Total_CPS_Button.Show_Button(Dungeon_Screen.Return_Title())
        Total_Click_Damage_Button.Show_Button(Dungeon_Screen.Return_Title())
        screen2button = Shop_Button.Focus_Check(mouse_pos, mouse_click)
        Level_Info.Show_Button(Dungeon_Screen.Return_Title())
        attack = Hitbox_Button.Focus_Check(mouse_pos, mouse_click)
        Hitbox_Button.Show_Button(Dungeon_Screen.Return_Title())
        Gold_Dungeon = Button(10, 550, 400, 50, Colours["White"],
                              Colours["White"], "arial",
                              15, Colours["Black"],
                              "Gold: {fname}".format(
                                  fname=str(data['Gold_Amount'])),
                              "")
        Gold_Dungeon.Show_Button(Dungeon_Screen.Return_Title())
# This part replaces the monster and draws the next one in line
        if data['current_monster'] == 0:
            goblin.draw(Dungeon_Screen.screen)
            data['counter'] = 30000
            data['Stage'] = 2
        elif data['current_monster'] == 1:
            monster_2.draw(Dungeon_Screen.screen)
            data['Stage'] = 3
        elif data['current_monster'] == 2:
            monster_3.draw(Dungeon_Screen.screen)
            data['Stage'] = 4
        elif data['current_monster'] == 3:
            monster_4.draw(Dungeon_Screen.screen)
            data['Stage'] = 5
        elif data['current_monster'] == 4:
            monster_5.draw(Dungeon_Screen.screen)
            data['Stage'] = 6
        elif data['current_monster'] == 5:
            monster_6.draw(Dungeon_Screen.screen)
            data['Stage'] = 7
        elif data['current_monster'] == 6:
            monster_7.draw(Dungeon_Screen.screen)
            data['Stage'] = 8
        elif data['current_monster'] == 7:
            monster_8.draw(Dungeon_Screen.screen)
            data['Stage'] = 9
        elif data['current_monster'] == 8:
            monster_9.draw(Dungeon_Screen.screen)
            data['Stage'] = 10
        elif data['current_monster'] == 9:
            monster_boss.draw(Dungeon_Screen.screen)
            data['Stage'] = 1
        HP_Amount.Show_Button(Dungeon_Screen.Return_Title())
        Shop_Button.Show_Button(Dungeon_Screen.Return_Title())
        Shop_Button.Show_Tip(Dungeon_Screen.Return_Title())
        data['second'] += dt
        # Calculates the damage per second and takes away from HP
        if data['second'] >= 1000:
            HP -= total_CPS
            data['second'] = 0
        if attack:
            HP -= data['Click_Damage']
        if HP < 0:
            HP = 0

        HP_Amount = Button(100, 0, 200, 50, Colours["White"], Colours["Black"],
                           "arial", 20, Colours["Black"], str(HP), "")
        HP_Amount.Show_Button(Dungeon_Screen.Return_Title())
        if HP == 0:
            Level_Info = Button(100, 600, 200, 50, Colours["Black"],
                                Colours["Red"], "arial", 20, Colours["White"],
                                "Level: {0} Stage: {1}".format(data["level"],
                                                               data['Stage']),
                                "")
            Level_Info.Show_Button(Dungeon_Screen.Return_Title())
            data['Gold_Amount'] += data['gold_dropped']
            Gold = Button(10, 50, 125, 50, Colours["Black"],
                          Colours["Black"], "arial", 15, Colours["White"],
                          "Gold: {fname}".format(fname=str(
                                      data['Gold_Amount'])), "")
            Gold_Dungeon = Button(10, 550, 400, 50, Colours["White"],
                                  Colours["White"], "arial",
                                  15, Colours["Black"],
                                  "Gold: {fname}".format(fname=str(
                                      data['Gold_Amount'])), "")
            Gold_Dungeon.Show_Button(Dungeon_Screen.Return_Title())
            data['Original_HP_Amount'] = round(data['Original_HP_Amount'] *
                                               (int(data['level'] - 1) +
                                                1.55**(data['level'] - 1)))
            data['current_monster'] += 1
            HP = data['Original_HP_Amount']

            if data['current_monster'] == 9:
                HP = HP * 10
                data['level'] += 1
            data['gold_dropped'] = math.ceil(HP / 15)
            HP_Amount = Button(100, 0, 200, 50, Colours["White"],
                               Colours["Black"], "arial", 20, Colours["Black"],
                               str(HP), "")
            HP_Amount.Show_Button(Dungeon_Screen.Return_Title())
            pygame.display.update()
        if screen2button:
            win = Shop_Screen.Make_Current()

            Dungeon_Screen.End_Current()
        if Go_Back:
            win = Opening_Screen.Make_Current()
            with open("Save_Data.txt", "w") as score_file:
                json.dump(data, score_file)
            Dungeon_Screen.End_Current()
# This is all of the shop components
    elif Shop_Screen.Check_Update():
        Assassin_Damage_Level = Button(135, 300, 125, 50, Colours["Black"],
                                       Colours["Red"], "arial", 15, Colours["White"],
                                       str(data['Assassin_Level']), "")
        Assassin_Damage_Cost = Button(260, 300, 125, 50, Colours["Black"],
                                      Colours["Red"], "arial", 15, Colours["White"],
                                      str(int(round(data['Assassin_Cost']))), "")
        Sniper_Damage_Level = Button(135, 400, 125, 50, Colours["Black"],
                                     Colours["Red"], "arial", 15, Colours["White"],
                                     str(data['Sniper_Level']), "")
        Sniper_Damage_Cost = Button(260, 400, 125, 50, Colours["Black"],
                                    Colours["Red"], "arial", 15, Colours["White"],
                                    str(int(round(data['Sniper_Cost']))), "")
        Mercernary_Damage_Level = Button(135, 200, 125, 50, Colours["Black"],
                                         Colours["Red"], "arial", 15, Colours["White"],
                                         str(data['Mercernary_Level']), "")
        Mercernary_Damage_Cost = Button(260, 200, 125, 50, Colours["Black"],
                                        Colours["Red"], "arial", 15, Colours["White"],
                                        str(int(round(data['Mercernary_Cost']))), "")
        Click_Damage_Level = Button(135, 100, 125, 50,
                                    Colours["Black"], Colours["Red"],
                                    "arial", 15, Colours["White"],
                                    str(data['Whetstone_Level']), "")
        Click_Damage_Cost = Button(260, 100, 125, 50, Colours["Black"],
                                   Colours["Red"], "arial", 15, Colours["White"],
                                   str(int(round(data['Whetstone_Cost']))), "")
        cost.Show_Button(Shop_Screen.Return_Title())
        upgrade_level.Show_Button(Shop_Screen.Return_Title())
        Return_To_Dungeon = Dungeon_Button.Focus_Check(mouse_pos, mouse_click)
        Dungeon_Button.Show_Button(Shop_Screen.Return_Title())
        Dungeon_Button.Show_Tip(Dungeon_Screen.Return_Title())
        Click_Damage_Upgrade.Show_Button(Shop_Screen.Return_Title())
        Click_Damage_Level.Show_Button(Shop_Screen.Return_Title())
        Gold = Button(10, 50, 125, 50, Colours["Black"],
                      Colours["Black"], "arial", 15, Colours["White"],
                      "Gold: {fname}".format(fname=str(
                          data['Gold_Amount'])), "")
        Gold.Show_Button(Shop_Screen.Return_Title())
        Click_Damage_Cost.Show_Button(Shop_Screen.Return_Title())
        Mercernary_Upgrade.Show_Button(Shop_Screen.Return_Title())
        Mercernary_Damage_Level.Show_Button(Shop_Screen.Return_Title())
        Mercernary_Damage_Cost.Show_Button(Shop_Screen.Return_Title())
        Assassin_Upgrade.Show_Button(Shop_Screen.Return_Title())
        Assassin_Damage_Level.Show_Button(Shop_Screen.Return_Title())
        Assassin_Damage_Cost.Show_Button(Shop_Screen.Return_Title())
        Sniper_Upgrade.Show_Button(Shop_Screen.Return_Title())
        Sniper_Damage_Level.Show_Button(Shop_Screen.Return_Title())
        Sniper_Damage_Cost.Show_Button(Shop_Screen.Return_Title())
        Click_Damage_Upgrade.Show_Tip(Dungeon_Screen.Return_Title())
        Mercernary_Upgrade.Show_Tip(Dungeon_Screen.Return_Title())
        Assassin_Upgrade.Show_Tip(Dungeon_Screen.Return_Title())
        Sniper_Upgrade.Show_Tip(Dungeon_Screen.Return_Title())
        if Click_Damage_Upgrade.Focus_Check(mouse_pos, mouse_click):
            if data['Gold_Amount'] >= data['Whetstone_Cost']:
                # Made mistake here where the cost was increased before
                # it was deducted leading to negative gold because I updated
                # cost of the upgrade before I deducted the price so it
                # deducted more than it was supposed to leading to negatives
                data['Whetstone_Level'] += 1
                data['Click_Damage'] += 2
                data['Gold_Amount'] -= data['Whetstone_Cost']
                data['Whetstone_Cost'] = math.ceil((1 *
                                                     data
                                                     ['Whetstone_Level']) *
                                                    1.07 **
                                                    (data['Whetstone_Level']))

                Gold = Button(10, 50, 125, 50, Colours["Black"],
                              Colours["Black"], "arial", 15, Colours["White"],
                              "Gold: {fname}".format(
                                  fname=str(math.ceil(data['Gold_Amount']))),
                              "")
                Gold.Show_Button(Shop_Screen.Return_Title())
                Click_Damage_Level = Button(135, 100, 125, 50,
                                            Colours["Black"],
                                            Colours["Red"], "arial", 15,
                                            Colours["White"],
                                            str(data['Whetstone_Level']), "")
                Click_Damage_Level.Show_Button(Shop_Screen.Return_Title())
                Click_Damage_Cost = Button(260, 100, 125, 50, Colours["Black"],
                                           Colours["Red"], "arial", 15,
                                           Colours["White"],
                                           str(int(
                                               math.floor(
                                                   data['Whetstone_Cost']))),
                                           "")
                Click_Damage_Cost.Show_Button(Shop_Screen.Return_Title())
        if Mercernary_Upgrade.Focus_Check(mouse_pos, mouse_click):
            if data['Gold_Amount'] >= data['Mercernary_Cost']:
                # During testing the gold amount was going negative after
                # upgrading Mercerary due to error where i was checking if gold
                # was larger than whetstone cost
                data['Gold_Amount'] -= data['Mercernary_Cost']
                data['Mercernary_Level'] += 1
                data['Mercernary_CPS'] += 5

                data['Mercernary_Cost'] = math.ceil((50 *
                                                     data
                                                     ['Mercernary_Level']) *
                                                    1.07 **
                                                    (data['Mercernary_Level']))
                Gold = Button(10, 50, 125, 50, Colours["Black"],
                              Colours["Black"], "arial", 15, Colours["White"],
                              "Gold: {fname}".format(fname=str(
                                  math.ceil(data['Gold_Amount']))),
                              "")
                Gold.Show_Button(Shop_Screen.Return_Title())
                Mercernary_Damage_Level = Button(135, 200, 125, 50,
                                                 Colours["Black"],
                                                 Colours["Red"],
                                                 "arial", 15,
                                                 Colours["White"],
                                                 str(data['Mercernary_Level']),
                                                 "")
                Mercernary_Damage_Level.Show_Button(Shop_Screen.Return_Title())
                Mercernary_Damage_Cost = Button(260, 200, 125, 50,
                                                Colours["Black"],
                                                Colours["Red"],
                                                "arial", 15, Colours["White"],
                                                str(
                                                    int
                                                    (round
                                                     (data
                                                      ['Mercernary_Cost']))),
                                                "")
                Mercernary_Damage_Cost.Show_Button(Shop_Screen.Return_Title())
        if Assassin_Upgrade.Focus_Check(mouse_pos, mouse_click):
            if data['Gold_Amount'] >= data['Assassin_Cost']:

                data['Gold_Amount'] -= data['Assassin_Cost']
                data['Assassin_Level'] += 1
                data['Assassin_CPS'] += 22

                data['Assassin_Cost'] = math.ceil((150 *
                                                   data['Assassin_Level']) *
                                                  1.07 **
                                                  (data['Assassin_Level']))
                Gold = Button(10, 50, 125, 50, Colours["Black"],
                              Colours["Black"], "arial", 15, Colours["White"],
                              "Gold: {fname}".format(fname=str
                                                     (math.ceil
                                                      (data['Gold_Amount']))),
                              "")
                Gold.Show_Button(Shop_Screen.Return_Title())
                Assassin_Damage_Level = Button(135, 300, 125, 50,
                                               Colours["Black"],
                                               Colours["Red"],
                                               "arial", 15, Colours["White"],
                                               str(data['Assassin_Level']), "")
                Assassin_Damage_Level.Show_Button(Shop_Screen.Return_Title())
                Assassin_Damage_Cost = Button(260, 300, 125, 50,
                                              Colours["Black"], Colours["Red"],
                                              "arial", 15, Colours["White"],
                                              str(int(round
                                                      (data
                                                       ['Assassin_Cost']))),
                                              "")
                Assassin_Damage_Cost.Show_Button(Shop_Screen.Return_Title())
        if Sniper_Upgrade.Focus_Check(mouse_pos, mouse_click):
            if data['Gold_Amount'] >= data['Sniper_Cost']:

                data['Gold_Amount'] = data['Gold_Amount'] - data['Sniper_Cost']
                data['Sniper_Level'] += 1
                data['Sniper_CPS'] += 76

                data['Sniper_Cost'] = math.ceil((500 * data['Sniper_Level']) *
                                                1.07 **
                                                (data['Sniper_Level']))
                Gold = Button(10, 50, 125, 50, Colours["Black"],
                              Colours["Black"], "arial", 15, Colours["White"],
                              "Gold: {fname}".format(fname=str
                                                     (math.ceil
                                                      (data['Gold_Amount']))),
                              "")
                Gold.Show_Button(Shop_Screen.Return_Title())
                Sniper_Damage_Level = Button(135, 400, 125, 50,
                                             Colours["Black"], Colours["Red"],
                                             "arial", 15, Colours["White"],
                                             str(data['Sniper_Level']), "")
                Sniper_Damage_Level.Show_Button(Shop_Screen.Return_Title())
                Sniper_Damage_Cost = Button(260, 400, 125, 50,
                                            Colours["Black"],
                                            Colours["Red"], "arial", 15,
                                            Colours["White"],
                                            str(int(
                                                round(data['Sniper_Cost']))),
                                            "")
                Sniper_Damage_Cost.Show_Button(Shop_Screen.Return_Title())

        if Return_To_Dungeon:
            win = Dungeon_Screen.Make_Current()
            Shop_Screen.End_Current()
    elif Game_Over_Screen.Check_Update():
        Game_Over_Button.Show_Button(Game_Over_Screen.Return_Title())
        Restart_Game.Show_Button(Game_Over_Screen.Return_Title())
        Restart = Restart_Game.Focus_Check(mouse_pos, mouse_click)
        if Restart:
            win = Opening_Screen.Make_Current()
            os.remove("Save_Data.txt")
            Game_Over_Screen.End_Current()

    pygame.display.update()
pygame.quit()
