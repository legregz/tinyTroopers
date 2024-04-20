import random, json, pygame, math, time
from weapons import *

pygame.init()
screen = pygame.display.set_mode(flags = pygame.FULLSCREEN)
pygame.key.set_repeat(1000, 100)

screenWidth, screenHeight = screen.get_width(), screen.get_height()
screenHalfWidth, screenHalfHeight = screenWidth / 2, screenHeight / 2
font = pygame.font.Font("fonts/PixelBold.otf", int(screenWidth / 200) * 5)

file = open("teams.json")
teams = eval(file.read())
file.close()

colorDict = {
    "Cyan": (0, 255, 255),
    "darkCyan": (0, 230, 230),
    "Violet": (255, 0, 255),
    "darkViolet": (230, 0, 230),
    "Yellow": (255, 255, 0),
    "darkYellow": (230, 230, 0),
    "Green": (0, 255, 0),
    "darkGreen": (0, 230, 0),
    "Red": (255, 0, 0),
    "darkRed": (230, 0, 0),
    "Blue": (0, 0, 255),
    "darkBlue": (0, 0, 230),
    "Black" : (0, 0, 0),
    "lightBlue": (0, 177, 255),
    "Grey": (200, 200, 200),
    "White": (255, 255, 255)
}

teamsColorList = ["Green", "Red", "Blue", "Violet", "Yellow", "Cyan"]
deathMessagesList = [" leave us", " is dead", " was great"]
eliminationMessagesList = [" is eliminated"]

def nosign(number):
    if number < 0:
        return 0
    else:
        return number

def randomDeathMessage(name):
    return name + random.choice(deathMessagesList)

def randomEliminationMessage(name):
    return name + random.choice(eliminationMessagesList)

def color(color):
    return colorDict[color]

def draw(image, xy, centered = (True, True)):
	pos = image.get_rect()
	pos.center = xy
	x, y = xy
	if centered[0] == True:
		x = pos[0]
	if centered[1] == True:
		y = pos[1]
	screen.blit(image, (x, y))

def center(rect, xCentered = True, yCentered = True):
    if xCentered == True:
        rect[0] -= rect[2] / 2
    if yCentered == True:
        rect[1] -= rect[3] / 2
    return rect

def createRect(rect):
    if len(rect) == 4:
        return [rect[0] / 100 * screenWidth, rect[1] / 100 * screenHeight, rect[2] / 100 * screenWidth, rect[3] / 100 * screenHeight]
    else:
        return [rect[0] / 100 * screenWidth, rect[1] / 100 * screenHeight]
    
def play(teams):
    if len(teams) > 1:
        Game(teams, "map3")

class Button:
    def __init__(self, text, rect, color, borderColor, active = True, function = "0", image = ""):
        self.active = active
        self.text = text
        self.updateState()
        self.mainRect = Rect(rect, color, False)
        self.borderRect = Rect(rect, borderColor)
        self.rect = createRect(rect)
        self.function = function
        if image != "":
            self.image = pygame.image.load(image)
            self.image = pygame.transform.scale(self.image, (self.image.get_width() * self.rect[3] // self.image.get_height(), self.image.get_height() * self.rect[3] // self.image.get_height()))
        else:
            self.image = ""

    def updateState(self):
        if self.active == True:
            self.text = font.render(self.text, True, color("White"))
        else:
            self.text = font.render(self.text, True, color("Grey"))

    def show(self):
        if self.rect[0] - self.rect[2] / 2 < pygame.mouse.get_pos()[0] < self.rect[0] + self.rect[2] / 2 and self.rect[1] - self.rect[3] / 2 < pygame.mouse.get_pos()[1] < self.rect[1] + self.rect[3] / 2:
            hover = True
            upsize = 1
        else:
            upsize = 0
            hover = False

        self.mainRect.show(upsize)
        self.borderRect.show(upsize)

        if self.image != "":
            draw(self.image, (self.rect[0], self.rect[1]))
        draw(self.text, (self.rect[0], self.rect[1]))

        return hover

    def click(self):
        if self.active == True:
            if self.rect[0] - self.rect[2] / 2 < pygame.mouse.get_pos()[0] < self.rect[0] + self.rect[2] / 2 and self.rect[1] - self.rect[3] / 2 < pygame.mouse.get_pos()[1] < self.rect[1] + self.rect[3] / 2:
                return True

class Rect:
    def __init__(self, rect, color, empty = True):
        self.rect = createRect(rect)
        self.color = color
        self.empty = empty

    def show(self, upsize = 0):
        if self.empty == True:
            pygame.draw.rect(screen, color(self.color), center(self.upSize(self.rect.copy(), upsize)), 5)
        else:
            pygame.draw.rect(screen, color(self.color), center(self.upSize(self.rect.copy(), upsize)))

    def upSize(self, rect, upsize):
        return [rect[0], rect[1], rect[2] + upsize / 100 * screenWidth, rect[3] + upsize / 100 * screenHeight]

class Text:
    def __init__(self, text, textColor, position, centered = (True, True)):
        self.textColor = textColor
        self.setText(text)
        self.position = createRect(position)
        self.centered = centered

    def setText(self, text):
        self.text = font.render(text, True, color(self.textColor))

    def show(self):
        draw(self.text, self.position, centered = self.centered)

class Entry:
    def __init__(self, rect, defaultText, text = ""):
        self.rect = createRect(rect)
        self.defaultText = font.render(defaultText, True, color("Grey"))
        self.text = text
        self.active = False
        self.repeatTime = 0
        self.upsize = 0
        self.border = Rect(rect, "Grey")

    def click(self):
        mousePosition = pygame.mouse.get_pos()
        if self.rect[0] - self.rect[2] // 2 < mousePosition[0] < self.rect[0] + self.rect[2] // 2 and self.rect[1] - self.rect[3] // 2 < mousePosition[1] < self.rect[1] + self.rect[3] // 2:
            self.active = True
        else:
            self.active = False
			
    def show(self, char):
        self.border.show(self.upsize)
		
        mousePosition = pygame.mouse.get_pos()

        if self.active == False:
            if self.rect[0] - self.rect[2] // 2 < mousePosition[0] < self.rect[0] + self.rect[2] // 2 and self.rect[1] - self.rect[3] // 2 < mousePosition[1] < self.rect[1] + self.rect[3] // 2:
                self.border.color = "White"
                self.upsize = 1
            else:
                self.border.color = "Grey"
                self.upsize = 0

            if len(self.text) == 0:
                draw(self.defaultText, (self.rect[0], self.rect[1]))
            else:
                draw(font.render(self.text, True, color("White")), (self.rect[0], self.rect[1]))
        else:
            if char == "\b":
                self.text = self.text[:-1]
            else:
                self.text += char

            if self.rect[0] - self.rect[2] // 2 < mousePosition[0] < self.rect[0] + self.rect[2] // 2 and self.rect[1] - self.rect[3] // 2 < mousePosition[1] < self.rect[1] + self.rect[3] // 2:
                self.border.color = "Green"
                self.upsize = 1
            else:
                self.border.color = "darkGreen"
                self.upsize = 0

            draw(font.render(self.text + "|", True, color("White")), (self.rect[0], self.rect[1]))

class Team:
    def __init__(self, index, name = "", level = 0, team = [f"Player {i}" for i in range(8)], color = "Blue"):
        rect = [80, 10 * index + 10, 37.5, 9]
        self.rect = createRect(rect)
        self.name = name
        self.index = index
        self.level = level
        self.color = color
        self.eliminated = False
        self.numberOfSoldiers = 4
        text = font.render(str(level), True, (0, 0, 0))
        self.textsList = [
            Text(name, "White", [rect[0] - rect[2] / 2, rect[1]], centered = (False, True)),
            Text(str(level), "Yellow", [rect[0] + rect[2] / 2 - text.get_width() / screenWidth * 100, rect[1]], centered = (False, True)),
            Text(str(self.numberOfSoldiers), "Yellow", [30, 83], centered = (True, True))
        ]
        self.rectsList = [
            Rect(rect, "Grey"),
            Rect([30, 50, 59.5, 99], "White")
        ]
        self.entryList = [
            Entry([10, 11 * i + 17, 18, 9], "Player " + str(i), team[i]) for i in range(len(team))
        ]
        self.entryList.insert(0, Entry([10, 6, 18, 9], "Team name", name))
        self.buttonsList = [
            Button("Save", [50, 94, 18, 9], "Green", "darkGreen", True, "self.modify('save')"),
            Button("Delete Team", [30, 94, 18, 9], "Red", "darkRed", True, "self.modify('delete')"),
            Button("Color choice", [50, 83, 18, 9], self.color, "dark" + self.color, True, "self.modify('color')"),
            Button("+", [35.5, 83, 7, 9], "Green", "darkGreen", True, "self.changeNumberOfSoldiers('+')"),
            Button("-", [24.5, 83, 7, 9], "Red", "darkRed", True, "self.changeNumberOfSoldiers('-')")
        ]
        self.team = team
        self.selected = False
        self.showed = False

    def changeNumberOfSoldiers(self, action):
        if action == "+":
            if self.numberOfSoldiers < 8:
                self.numberOfSoldiers += 1
        else:
            if self.numberOfSoldiers > 1:
                self.numberOfSoldiers -= 1

        self.textsList[2].setText(str(self.numberOfSoldiers))

        return ""

    def modify(self, action = ""):
        try:
            file = open("teams.json")
            teams = eval(file.read())
            file.close()
            del teams[self.name]
        except:
            pass

        if action == "color":
            index = teamsColorList.index(self.buttonsList[2].color) + 1
            if index == len(teamsColorList):
                index = 0
            self.buttonsList[2].color = teamsColorList[index]
            self.buttonsList[2].borderColor = "dark" + teamsColorList[index]
            self.color = self.buttonsList[2].color

        if action == "save":
            self.name = self.entryList[0].text
            self.team = [self.entryList[i].text for i in range(1, len(self.entryList))]
            self.textsList[0].setText(self.name)

            teams[self.name] = {"level": self.level, "team": self.team, "color": self.color}

            file = open("teams.json", "w")
            file.write(json.dumps(teams))
            file.close()

        if action == "delete":
            return ["delete", self.index]
        else:
            return ""

    def show(self, char):
        if self.selected == True:
            if self.rect[0] - self.rect[2] / 2 < pygame.mouse.get_pos()[0] < self.rect[0] + self.rect[2] / 2 and self.rect[1] - self.rect[3] / 2 < pygame.mouse.get_pos()[1] < self.rect[1] + self.rect[3] / 2:
                self.rectsList[0].color = self.color
                upsize = 1
            else:
                self.rectsList[0].color = "dark" + self.color
                upsize = 0
        else:
            if self.rect[0] - self.rect[2] / 2 < pygame.mouse.get_pos()[0] < self.rect[0] + self.rect[2] / 2 and self.rect[1] - self.rect[3] / 2 < pygame.mouse.get_pos()[1] < self.rect[1] + self.rect[3] / 2:
                self.rectsList[0].color = "White"
                upsize = 1
            else:
                self.rectsList[0].color = "Grey"
                upsize = 0

        self.rectsList[0].show(upsize)
        
        self.textsList[0].show()
        self.textsList[1].show()
            
        if self.showed == True:
            self.rectsList[1].show()
            for elt in self.entryList:
                elt.show(char)

            for elt in self.buttonsList:
                elt.show()

            self.textsList[2].show()

    def setRect(self, rect):
        self.rect = createRect(rect)

    def click(self, side):
        result = ""
        if self.rect[0] - self.rect[2] / 2 < pygame.mouse.get_pos()[0] < self.rect[0] + self.rect[2] / 2 and self.rect[1] - self.rect[3] / 2 < pygame.mouse.get_pos()[1] < self.rect[1] + self.rect[3] / 2:
            if side == "left":
                if self.selected == False:
                    self.selected = True
                else:
                    self.selected = False
            if side == "right":
                if self.showed == False:
                    self.showed = True
                else:
                    self.showed = False
        if side == "left":
            if self.showed == True:
                for elt in self.entryList:
                    elt.click()

                for elt in self.buttonsList:
                    if elt.click() == True:
                        result = eval(elt.function)
                        if len(result) > 0:
                            return result
        return ""
        
class Menu:
    def __init__(self):
        self.teams = teams
        self.buttonsList = [
            Button("Play", (90, 95, 19, 9), "Green", "darkGreen", function = "play(self.selectedTeams())"),
            Button("Create Team", (70, 95, 19, 9), "Green", "darkGreen", function = "self.createTeam()"),
        ]

        self.teamsList = [
            Team(i, list(teams.keys())[i], teams[list(teams.keys())[i]]["level"], teams[list(teams.keys())[i]]["team"], teams[list(teams.keys())[i]]["color"]) for i in range(len(teams.keys()))
        ]

        self.rectsList = [
            Rect((80, 42, 39, 75), "White")
        ]

        self.textsList = [
            Text("Teams available", "Green", (80, 2))
        ]

        self.mouse = Mouse()

        pygame.mouse.set_visible(False)

        self.loop()

    def selectedTeams(self):
        selectedTeamList = []
        for elt in self.teamsList:
            if elt.selected == True:
                selectedTeamList.append(elt)
        return selectedTeamList
    
    def createTeam(self):
        self.teamsList.append(Team(len(self.teamsList)))

    def loop(self):
        self.run = True
        mouseButtonsState = []

        while self.run == True:
            char = ""
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    if mouseButtonsState[0] == 1:
                        for elt in self.buttonsList:
                            if elt.click() == True:
                                eval(elt.function)

                    mouseButtonsState = []

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseButtonsState = pygame.mouse.get_pressed()
                    if pygame.mouse.get_pressed()[2] == 1:
                        for elt in self.teamsList:
                            elt.showed = False
                            elt.click("right")
                    
                    if pygame.mouse.get_pressed()[0] == 1:
                        for elt in self.teamsList:
                            result = elt.click("left")
                            if len(result) > 0:
                                if result[0] == "delete":
                                    self.teamsList.pop(result[1])

                if event.type == pygame.KEYDOWN:
                    if pygame.key.get_pressed()[pygame.K_BACKSPACE] == 1:
                        char = "\b"
                    else:
                        char = event.unicode

            screen.fill((0, 0, 60))

            for elt in self.buttonsList:
                elt.show()

            for elt in self.teamsList:
                elt.show(char)

            for elt in self.rectsList:
                elt.show()

            for elt in self.textsList:
                elt.show()

            self.mouse.show()
            
            pygame.display.flip()

class Mouse:
    def __init__(self):
        self.init()

    def show(self):
        if pygame.mouse.get_pressed()[0] == 1:
            screen.blit(self.clickTexture, (pygame.mouse.get_pos()))
        else:
            screen.blit(self.texture, (pygame.mouse.get_pos()[0] + self.position[0] * 2, pygame.mouse.get_pos()[1] + self.position[1] * 2))

    def setTexture(self, texture, position):
        self.position = position
        self.texture = pygame.transform.scale(texture, (32, 32))

    def setClickTexture(self, texture):
        self.clickTexture = pygame.transform.scale(texture, (32, 32))

    def init(self):
        self.setTexture(pygame.image.load("textures/cursor.png").convert_alpha().subsurface((0, 0, 16, 16)), (0, 0))
        self.setClickTexture(pygame.image.load("textures/cursor.png").convert_alpha().subsurface((0, 16, 16, 16)))

class Game:
    def __init__(self, teams, mapName):
        self.time = time.time()
        self.mouse = Mouse()
        self.animationStep = 0
        self.animationDelayTime = self.time
        self.scale = 1
        self.scaleFont()
        self.fps = 60
        self.camera = Camera()
        self.map = Map(self, (0, 0), mapName)
        self.teams = [elt for elt in teams]
        importWeapons(self)
        self.teamsInventories = [Inventory(self) for elt in teams]
        self.soldiers = []
        self.mines = [Mine(self) for i in range(8)]
        for team in teams:
            self.soldiers.append([])
        for i in range(len(teams)):
            for soldier in range(teams[i].numberOfSoldiers):
                self.soldiers[i].append(Soldier(self, teams[i].team[soldier], teams[i]))

        self.soldiers[0][0].active = True
        self.turns = [0 for i in range(len(self.soldiers))]
        self.actualTeam = 0
        self.actualSoldier = self.soldiers[self.actualTeam][self.turns[self.actualTeam]]
        self.teamTurnTime = self.time
        self.showText = ShowText()
        self.showText.append(f"{self.actualSoldier.team.name}, it's your turn!", "White", 5)

        self.barrels = [Barrel(self) for i in range(8)]
        self.lootBoxs = []
        self.particles = []
        self.mousePosition = [0, 0]
        self.pings = [PingArrow(self)]
        self.explosionImage = pygame.image.load("textures/explosion.png").convert_alpha()

        self.loop()

    def collision(self, position, radius):
        for elt in self.barrels:
            if elt.explode(position, radius) == True:
                return True

        for i in range(len(self.soldiers)):
            for soldier in self.soldiers[i]:
                distance = ((soldier.position[0] - position[0])**2 + (soldier.position[1] + 4 - position[1])**2)**0.5
                if distance <= soldier.radius:
                    return True

        if self.map.array[int(position[0] + len(self.map.array) / 2)][int(position[1] + len(self.map.array[0]) / 2)] != 0:
            return True
        else:
            return False

    def scaleFont(self):
        self.font = pygame.font.Font("fonts/PixelBold.otf", int(10 * self.scale))

    def safe(self, position):
        safe = True
        for elt in self.mines:
            distance = ((elt.position[0] - position[0])**2 + (elt.position[1] - position[1])**2)**0.5
            if distance < elt.detectionRadius:
                safe = False
                break

        return safe

    def defineMapPosition(self, soldier = False):
        def loop():
            color = 0
            y = len(self.map.array[0]) - 1
            while color == 0:
                x = random.randint(0, len(self.map.array) - 1)
                color = self.map.array[x, y]

            while color != 0:
                color = self.map.array[x, y]
                y -= 1

            return x, y

        if soldier == True:
            x, y = loop()
            while self.safe([x - len(self.map.array) / 2, y - 2 - len(self.map.array[0]) / 2]) == False:
                x, y = loop()
        else:
            x, y = loop()

        return [x - len(self.map.array) / 2, y - 2 - len(self.map.array[0]) / 2]

    def explode(self, position, radius, damages, timer = 0, smoke = True):
        if time.time() > timer:
            for team in range(len(self.soldiers)):
                for soldier in self.soldiers[team]:
                    soldier.explode(position, radius, damages)

                for barrel in self.barrels:
                    barrel.explode(position, radius)

            self.map.explode(position, radius)
        else:
            try:
                self.show(pygame.transform.scale(self.explosionImage.subsurface((0, int(4 - (timer - time.time()) * 20) * 16, 16, 16)), (16 * self.scale * int(radius / 8), 16 * self.scale * int(radius / 8))), position)
                if smoke == True:
                    self.particles.append(Smoke(self, [random.randint(int(position[0] - radius), int(position[0] + radius)), random.randint(int(position[1] - radius), int(position[1] + radius))]))
            except:
                pass

    def gravity(self, position, hitbox):
        if - len(self.map.array) / 2 + hitbox[0] < position[0] < len(self.map.array) / 2 - hitbox[1] and - len(self.map.array[0]) / 2 + hitbox[2] < position[1] < len(self.map.array[0]) / 2 - hitbox[3] - 1:
            if self.map.array[int(position[0] + hitbox[1] + len(self.map.array) / 2), int(position[1] + hitbox[3] + len(self.map.array[0]) / 2 + 1)] == 0 and self.map.array[int(position[0] - hitbox[0] + len(self.map.array) / 2), int(position[1] + hitbox[3] + len(self.map.array[0]) / 2 + 1)] == 0:
                position[1] += 1
        else:
            position[1] += 1
        
        return position

    def curveMoving(self, position, power, angle, hitbox, bounce = True):
        inMap = False
        if - len(self.map.array) / 2 + hitbox[1] < position[0] < len(self.map.array) / 2 - hitbox[0] and - len(self.map.array[0]) / 2 + hitbox[3] < position[1] < len(self.map.array[0]) / 2 - hitbox[2]:
            inMap = True
            collisions = [
            self.map.array[int(position[0] + hitbox[1] + len(self.map.array) / 2), int(position[1] + hitbox[3] + len(self.map.array[0]) / 2)],
            self.map.array[int(position[0] - hitbox[0] + len(self.map.array) / 2), int(position[1] + hitbox[3] + len(self.map.array[0]) / 2)],
            self.map.array[int(position[0] + hitbox[1] + len(self.map.array) / 2), int(position[1] - hitbox[2] + len(self.map.array[0]) / 2)],
            self.map.array[int(position[0] - hitbox[0] + len(self.map.array) / 2), int(position[1] - hitbox[2] + len(self.map.array[0]) / 2)]
            ]

            if bounce == True:
                ancientAngle = angle
                if 0 <= angle <= 90:
                    if collisions[3] != 0 and collisions[1] != 0:
                        if collisions[2] == 0:
                            angle = 360 - angle
                        else:
                            angle = angle + 180

                    elif ((collisions[3] != 0 and collisions[2] != 0) or (collisions[3] == 0 and collisions[2] != 0)) and collisions[1] == 0:
                        angle = 180 - angle

                    elif collisions[3] != 0 and collisions[1] == 0 and collisions[2] == 0:
                        angle = angle + 180

                elif 90 < angle <= 180:
                    if collisions[3] != 0 and collisions[1] != 0:
                        if collisions[0] == 0:
                            angle = 360 + angle
                        else:
                            if power > 12:
                                angle = angle + 180 

                    elif ((collisions[0] != 0 and collisions[1] != 0) or (collisions[1] == 0 and collisions[0] != 0)) and collisions[3] == 0:
                        if power > 10:
                            angle = 180 - angle

                    elif collisions[1] != 0 and collisions[0] == 0 and collisions[3] == 0:
                        angle = angle + 180

                elif 180 < angle <= 270:
                    if collisions[0] != 0 and collisions[2] != 0:
                        if collisions[1] == 0:
                            angle = 360 + angle
                        else:
                            if power > 12:
                                angle = angle - 180

                    elif ((collisions[0] != 0 and collisions[1] != 0) or (collisions[0] == 0 and collisions[1] != 0)) and collisions[2] == 0:
                        if power > 10:
                            angle = 540 - angle

                    elif collisions[0] != 0 and collisions[1] == 0 and collisions[2] == 0:
                        angle = angle - 180

                elif 270 < angle <= 360:
                    if collisions[0] != 0 and collisions[2] != 0:
                        if collisions[3] == 0:
                            angle = 360 - angle
                        else:
                            angle = angle - 180

                    elif ((collisions[3] != 0 and collisions[2] != 0) or (collisions[2] == 0 and collisions[3] != 0)) and collisions[0] == 0:
                        angle = 540 - angle

                    elif collisions[2] != 0 and collisions[0] == 0 and collisions[3] == 0:
                        angle = angle - 180

                if ancientAngle != angle:
                    power -= power / 2

        ancientPosition = position.copy()
        if inMap == True:
            if (collisions[3] == 0 and collisions[2] == 0 and (0 < angle < 90 or 270 < angle < 360)) or (collisions[1] == 0 and collisions[0] == 0 and 90 < angle < 270):
                position[1] -= math.sin(math.radians(angle + 90)) * 4
                position[1] += 1 - 1 / 32 * power
        else:
            position[1] -= math.sin(math.radians(angle + 90)) * 4
            position[1] += 1 - 1 / 32 * power

        if inMap == True:
            if (collisions[1] == 0 and collisions[3] == 0 and 0 < angle < 180) or (collisions[0] == 0 and collisions[2] == 0 and 180 < angle < 360):
                position[0] += math.cos(math.radians(angle + 90)) * 4
        else:
            position[0] += math.cos(math.radians(angle + 90)) * 4

        xDifference, yDifference = position[0] - ancientPosition[0], position[1] - ancientPosition[1]
        if xDifference > 0 and yDifference > 0:
            angle = 270 - math.degrees(math.asin(abs(yDifference / (xDifference**2 + yDifference**2)**0.5)))
        elif xDifference > 0 and yDifference < 0:
            angle = 270 + math.degrees(math.asin(abs(yDifference / (xDifference**2 + yDifference**2)**0.5)))
        elif xDifference < 0 and yDifference > 0:
            angle = 90 + math.degrees(math.asin(abs(yDifference / (xDifference**2 + yDifference**2)**0.5)))
        elif xDifference < 0 and yDifference < 0:
            angle = 90 - math.degrees(math.asin(abs(yDifference / (xDifference**2 + yDifference**2)**0.5)))

        if power > 0:
            power -= 0.05

        return position, power, angle

    def animationUpdate(self):
        if time.time() > self.animationDelayTime + 0.125:
            self.animationDelayTime += 0.125
            self.animationStep += 1
            if self.animationStep == 4:
                self.animationStep = 0

    def teamTurnUpdate(self):
        active = False
        try:
            if self.actualSoldier.weapon.launched == True:
                active = True
        except:
            pass

        for elt in self.barrels:
            if elt.timer != 0:
                active = True
                break

        for elt in self.mines:
            if elt.timer != 0:
                active = True
                break

        if len(self.particles) > 0:
            active = True

        if active == False:
            if time.time() > self.teamTurnTime + 65 or self.actualSoldier.active == False:
                self.actualSoldier.active = False

                for team in self.soldiers:
                    for soldier in team:
                        soldier.damagesShowTime = time.time() + 3
                        soldier.life -= soldier.damages

                self.teamTurnTime = time.time()

                def loopContent():
                    self.turns[self.actualTeam] += 1
                    if self.turns[self.actualTeam] >= len(self.soldiers[self.actualTeam]):
                        self.turns[self.actualTeam] = 0

                loopContent()
                while self.actualSoldier.dead == True:
                    loopContent()

                def loopContent():
                    self.actualTeam += 1
                    if self.actualTeam >= len(self.turns):
                        self.actualTeam = 0

                loopContent()
                while self.teams[self.actualTeam].eliminated == True:
                    loopContent()

                self.actualSoldier = self.soldiers[self.actualTeam][self.turns[self.actualTeam]]

                self.actualSoldier.active = True

                self.showText.append(f"{self.actualSoldier.team.name}, it's your turn!", "White", 5)

    def showAnimated(self, texture, position):
        screen.blit(texture.subsurface((0, self.animationStep * 16 * self.scale, 16 * self.scale, 16 * self.scale)), (position[0] * self.scale - 8 * self.scale + (self.camera.x + screenHalfWidth) * self.scale + screenHalfWidth, position[1] * self.scale - 8 * self.scale + (self.camera.y + screenHalfHeight) * self.scale + screenHalfHeight))

    def show(self, texture, position):
        screen.blit(texture, (position[0] * self.scale - texture.get_width() / 2 + (self.camera.x + screenHalfWidth) * self.scale + screenHalfWidth, position[1] * self.scale - texture.get_height() / 2 + (self.camera.y + screenHalfHeight) * self.scale + screenHalfHeight))

    def scaleTexture(self, texture):
        return pygame.transform.scale(texture, (texture.get_width() * self.scale, texture.get_height() * self.scale))

    def loop(self):
        self.run = True

        while self.run == True:
            startTime = time.time()

            end = 0
            for elt in self.teams:
                if elt.eliminated == False:
                    end += 1

            if end < 2:
                self.run == False

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0] == 1:
                        self.mousePosition = pygame.mouse.get_pos()

                    for elt in self.teamsInventories:
                        result = elt.click()
                        if result != None:
                            self.actualSoldier.weapon = result
                            self.actualSoldier.weapon.init()
                            self.actualSoldier.scaleTexture()

                if event.type == pygame.MOUSEWHEEL:
                    if event.y == -1 and self.scale > 1 or event.y == 1 and self.scale < 5:
                        self.scale += event.y * 0.5

                        self.map.scaleTexture()

                        for elt in self.barrels:
                            elt.scaleTexture()

                        for elt in self.mines:
                            elt.scaleTexture()

                        for elt in self.lootBoxs:
                            elt.scaleTexture()

                        for elt in self.particles:
                            elt.scaleTexture()

                        for team in self.soldiers:
                            for elt in team:
                                elt.scaleTexture()

                        for elt in self.pings:
                            elt.scaleTexture()

                        self.scaleFont()

                keysPressed = pygame.key.get_pressed()

            try:
                if sum(keysPressed) > 0:
                    if keysPressed[pygame.K_i]:
                        if self.actualSoldier.weapon == "" or self.actualSoldier.weapon.usages.get() == 0:
                            self.teamsInventories[self.actualTeam].open()
                    else:
                        self.actualSoldier.move(keysPressed)
                        try:
                            self.actualSoldier.weapon.move(keysPressed)
                        except:
                            pass
                else:
                    self.actualSoldier.release()
            except:
                pass

            self.animationUpdate()
            self.teamTurnUpdate()

            screen.fill((0, 0, 60))

            self.map.show()

            for elt in self.barrels:
                elt.show()

            for elt in self.mines:
                elt.show()

            for elt in self.lootBoxs:
                elt.show()

            for elt in self.particles:
                elt.show()

            for team in self.soldiers:
                for elt in team:
                    elt.show()

            for elt in self.pings:
                elt.show()

            self.showText.show()

            self.teamsInventories[self.actualTeam].show()

            turnTime = font.render(str(65 - int(time.time() - self.teamTurnTime)), True, (255, 255, 255))
            screen.blit(turnTime, (screenWidth - screenWidth / 10, screenHeight - screenHeight / 10))
            self.mousePos = [int(- self.camera.x - screenHalfWidth - (screenHalfWidth - pygame.mouse.get_pos()[0]) / self.scale), int(- self.camera.y - screenHalfHeight - (screenHalfHeight - pygame.mouse.get_pos()[1]) / self.scale)]

            self.mouse.show()

            if pygame.mouse.get_pressed()[0] == 1:
                self.camera.updatePosition((self.camera.x - (self.mousePosition[0] - pygame.mouse.get_pos()[0]) / self.scale, self.camera.y - (self.mousePosition[1] - pygame.mouse.get_pos()[1]) / self.scale))
                self.mousePosition = pygame.mouse.get_pos()

            pygame.display.flip()

            if time.time() - startTime < 1 / 60:
                sleepTime = 1 / 60 - (time.time() - startTime)
                if sleepTime > 0:
                    time.sleep(sleepTime)

class PingArrow:
    def __init__(self, Self):
        self.Self = Self
        self.texture = pygame.image.load("textures/ping.png").convert_alpha()
        self.movement = 0
        self.direction = 0.5
        self.changeTime = time.time() + 0.5
        self.scaleTexture()

    def show(self):
        if time.time() - self.Self.teamTurnTime < 5:
            if time.time() > self.changeTime:
                if self.direction > 0:
                    self.direction = -0.5
                else:
                    self.direction = 0.5
                
                self.changeTime = time.time() + 0.5

            self.movement += self.direction

            self.Self.show(self.scaledTexture, [self.Self.actualSoldier.position[0], self.Self.actualSoldier.position[1] - 35 + self.movement])

    def scaleTexture(self):
        self.scaledTexture = self.Self.scaleTexture(self.texture)

class Crossair:
    def __init__(self, Self, angle):
        self.Self = Self
        self.angle = angle
        self.texture = pygame.image.load("textures/crossair.png")

    def show(self, position):
        self.Self.show(self.scaledTexture, [position[0] + math.cos(math.radians(self.angle + 90)) * 20, position[1] - math.sin(math.radians(self.angle + 90)) * 20])

    def scaleTexture(self):
        self.scaledTexture = self.Self.scaleTexture(self.texture)

class Inventory:
    def __init__(self, Self):
        self.Self = Self
        self.opened = False
        self.delay = time.time() + 0.1
        self.rectsList = [
            Rect((80, 50, 39, 99), "Black", False),
            Rect((80, 50, 39, 99), "White")
        ]
        self.buttonsDict = {
            self.Self.weapons[i]: Button("", (65.75 + i % 4 * 9.5, 6 + i // 4 * 9.5, 9, 9), "Black", "Grey", image = self.Self.weapons[i].icon) for i in range(len(self.Self.weapons))
        }

        self.textsList = [
            Text("", "White", [80, 95])
        ]

    def show(self):
        if self.opened == True:
            for elt in self.rectsList:
                elt.show()

            for key in list(self.buttonsDict.keys()):
                if self.buttonsDict[key].show():
                    self.textsList[0].setText(key.name)

            self.textsList[0].show()

    def open(self):
        if time.time() > self.delay:
            self.delay = time.time() + 0.1
            if self.opened == True:
                self.opened = False
            else:
                self.opened = True

    def click(self):
        if self.opened == True:
            for elt in list(self.buttonsDict.keys()):
                if self.buttonsDict[elt].click() == True:
                    self.opened = False
                    return elt

class Camera:
    def __init__(self):
        self.updatePosition([-screenHalfWidth, -screenHalfHeight])

    def updatePosition(self, position):
        self.x = position[0]
        self.y = position[1]

class Soldier:
    def __init__(self, Self, name, team):
        self.Self = Self
        self.dead = False
        self.life = 100
        self.position = self.Self.defineMapPosition(soldier = True)
        self.texture = pygame.image.load("textures/soldier.png").convert_alpha()
        self.name = name
        self.team = team
        self.usages = 0
        self.active = False
        self.moving = False
        self.jumping = False
        self.damagesShowTime = 0
        self.damages = 0
        self.knockbackPower = 0
        self.knockbackDirection = 0
        self.direction = random.randint(0, 1)
        self.falling = False
        self.weapon = ""
        self.crossair = Crossair(Self, self.direction * -180 + 270)
        self.scaleTexture()
        self.radius = 8

    def explode(self, position, radius, damages):
        if self.dead == False:
            distance = ((self.position[0] - position[0])**2 + (self.position[1] + 4 - position[1])**2)**0.5
            if distance <= radius + self.radius:
                self.damages += int(damages / radius * (radius - nosign(distance - self.radius)))

                self.knockbackDirection = math.degrees(abs(self.position[1] + 4 - position[1]) / (distance + 0.1))
                if self.position[0] >= position[0]:
                    if self.position[1] + 4 >= position[1]:
                        self.knockbackDirection = 270 - self.knockbackDirection
                    else:
                        self.knockbackDirection = 270 + self.knockbackDirection
                else:
                    if self.position[1] + 4 >= position[1]:
                        self.knockbackDirection = 90 + self.knockbackDirection
                    else:
                        self.knockbackDirection = 90 - self.knockbackDirection
                self.knockbackPower = 30 / radius * (radius - distance)
                return True
            else:
                return False

    def move(self, keysPressed):
        if self.dead == False:
            if self.knockbackPower == 0 and self.active == True:
                self.moving = False
                if - len(self.Self.map.array) / 2 + 4 < self.position[0] < len(self.Self.map.array) / 2 - 4 and - len(self.Self.map.array[0]) / 2 + 6 < self.position[1] < len(self.Self.map.array[0]) / 2 - 6:
                    if keysPressed[pygame.K_d] and self.falling == False and self.Self.map.array[int(self.position[0] + 4 + len(self.Self.map.array) / 2), int(self.position[1] - 6 + len(self.Self.map.array[0]) / 2)] == 0:
                        self.position[0] += 1
                        if self.direction == 1:
                            self.crossair.angle = 360 - self.crossair.angle
                            self.direction = 0
                        self.moving = True

                    if keysPressed[pygame.K_q] and self.falling == False and self.Self.map.array[int(self.position[0] - 4 + len(self.Self.map.array) / 2), int(self.position[1] - 6 + len(self.Self.map.array[0]) / 2)] == 0:
                        self.position[0] -= 1
                        if self.direction == 0:
                            self.crossair.angle = 360 - self.crossair.angle
                            self.direction = 1
                        self.moving = True

                    if keysPressed[pygame.K_c] and self.falling == False and self.Self.map.array[int(self.position[0] - 4 + len(self.Self.map.array) / 2), int(self.position[1] - 6 + len(self.Self.map.array[0]) / 2)] == 0 and self.Self.map.array[int(self.position[0] + 4 + len(self.Self.map.array) / 2), int(self.position[1] - 6 + len(self.Self.map.array[0]) / 2)] == 0:# and (self.Self.map.array[int(self.position[0] - 4 + len(self.Self.map.array) / 2), int(self.position[1] + 6 + len(self.Self.map.array[0]) / 2)] != 0 or self.Self.map.array[int(self.position[0] + 4 + len(self.Self.map.array) / 2), int(self.position[1] + 6 + len(self.Self.map.array[0]) / 2)] != 0):
                        self.knockbackPower = 10
                        if self.direction == 0:
                            self.knockbackDirection = 350
                        else:
                            self.knockbackDirection = 10

                if keysPressed[pygame.K_z]:
                    if self.direction == 1:
                        if self.crossair.angle > 0:
                            self.crossair.angle -= 2
                    elif self.direction == 0:
                        if self.crossair.angle < 360:
                            self.crossair.angle += 2

                if keysPressed[pygame.K_s]:
                    if self.direction == 1:
                        if self.crossair.angle < 180:
                            self.crossair.angle += 2
                    elif self.direction == 0:
                        if self.crossair.angle > 180:
                            self.crossair.angle -= 2

                if keysPressed[pygame.K_SPACE]:
                    self.weapon.active()

    def release(self):
        self.moving = False
        self.weapon.release()

    def show(self):
        if self.dead == False:
            position = self.position.copy()
            self.position = self.Self.gravity(self.position, [4, 4, 6, 6])
            if self.position != position:
                self.falling = True
            if self.knockbackPower == 0:
                if - len(self.Self.map.array) / 2 + 4 < self.position[0] < len(self.Self.map.array) / 2 - 4 and - len(self.Self.map.array[0]) / 2 + 6 < self.position[1] < len(self.Self.map.array[0]) / 2 - 13:
                    if self.Self.map.array[int(self.position[0] + 4 + len(self.Self.map.array) / 2), int(self.position[1] + 6 + len(self.Self.map.array[0]) / 2 + 1)] != 0 or self.Self.map.array[int(self.position[0] - 4 + len(self.Self.map.array) / 2), int(self.position[1] + 6 + len(self.Self.map.array[0]) / 2 + 1)] != 0:
                        maxOnLeft, maxOnRight, self.falling = 0, 0, False
                        for y in range(1, 7):
                            if self.Self.map.array[int(self.position[0] + 4 + len(self.Self.map.array) / 2), int(self.position[1] + 6 - y + len(self.Self.map.array[0]) / 2)] == 0:
                                maxOnRight = y - 1
                                break

                        for y in range(1, 7):
                            if self.Self.map.array[int(self.position[0] - 4 + len(self.Self.map.array) / 2), int(self.position[1] + 6 - y + len(self.Self.map.array[0]) / 2)] == 0:
                                maxOnLeft = y - 1
                                break

                        if maxOnRight >= maxOnLeft:
                            self.position[1] -= maxOnRight
                        else:
                            self.position[1] -= maxOnLeft
            else:
                self.position, self.knockbackPower, self.knockbackDirection = self.Self.curveMoving(self.position, self.knockbackPower, self.knockbackDirection, [4, 4, 6, 6])
                if self.knockbackPower < 5:
                    self.knockbackPower = 0

            if self.active == True and self.moving == True:
                self.Self.showAnimated(pygame.transform.flip(self.scaledTexture, self.direction, 0), self.position)
            else:
                self.Self.show(pygame.transform.flip(self.scaledTexture.subsurface((0, 0, 16 * self.Self.scale, 16 * self.Self.scale)), self.direction, 0), self.position)

            if self.active == False:
                text = self.Self.font.render(self.name, True, self.team.color)
                self.Self.show(text, [self.position[0], self.position[1] - 13])
                text = self.Self.font.render(str(self.life), True, (255, 255 ,255))
                self.Self.show(text, [self.position[0], self.position[1] - 20])
            else:
                if self.weapon != "":
                    self.weapon.show([self.position[0], self.position[1] + 4], self.crossair.angle, self.direction)
                
                self.crossair.show([self.position[0], self.position[1] + 4])

            if self.damages != 0:
                if time.time() < self.damagesShowTime:
                    text = self.Self.font.render(str(self.damages), True, (200, 0, 0))
                    self.Self.show(text, [self.position[0], self.position[1] - 80 + 20 * (self.damagesShowTime - time.time())])
                elif self.damagesShowTime != 0:
                    self.damages = 0
                    self.damagesShowTime = 0

            if self.position[1] > len(self.Self.map.array[0]) / 2 + 20:
                self.death()

            if self.life <= 0:
                self.death()

        else:
            if self.weapon != "":
                try:
                    if self.weapon.launched == True:
                        self.weapon.show([self.position[0], self.position[1] + 4], self.crossair.angle, self.direction)
                except:
                    pass

    def death(self):
        self.dead = True
        self.Self.showText.append(randomDeathMessage(self.name), "White", 3)
        self.team.eliminated = True
        for elt in self.Self.soldiers[self.Self.actualTeam]:
            if elt.dead == False:
                self.team.eliminated = False

        if self.team.eliminated == True:
            self.Self.showText.append(randomEliminationMessage(self.team.name), "White", 3)

        if self.weapon != "":
            try:
                if self.weapon.launched == False:
                    self.active = False
            except:
                self.active = False
        else:
            self.active = False  

    def scaleTexture(self):
        if self.dead == False:
            self.scaledTexture = self.Self.scaleTexture(self.texture)
            self.crossair.scaleTexture()
            if self.weapon != "":
                self.weapon.scaleTexture()

class Barrel:
    def __init__(self, Self):
        self.Self = Self
        self.position = self.Self.defineMapPosition()
        self.texture = pygame.image.load("textures/barrel.png").convert_alpha()
        self.scaleTexture()
        self.timer = 0
        self.radius = 5

    def show(self):
        self.Self.showAnimated(self.scaledTexture, self.position)

        if self.timer != 0 and time.time() > self.timer - 0.2:
            self.Self.explode(self.position, 15, 30, self.timer)
            if time.time() > self.timer:
                for i in range(len(self.Self.barrels)):
                    if self.Self.barrels[i].position == self.position:
                        self.Self.barrels.pop(i)
                        break

    def scaleTexture(self):
        self.scaledTexture = self.Self.scaleTexture(self.texture)

    def explode(self, position, radius):
        if self.timer == 0:
            distance = ((self.position[0] - position[0])**2 + (self.position[1] - position[1])**2)**0.5
            if distance <= radius + self.radius:
                self.timer = time.time() + 0.2
                for x in range(int(self.position[0]) - 15, int(self.position[0]) + 15, 2):
                    self.Self.particles.append(Napalm(self.Self, [x, self.position[1] + random.randint(-3, 3)]))
                return True
            else:
                return False

class Napalm:
    def __init__(self, Self, position):
        self.Self = Self
        self.position = position
        self.durability = time.time() + 5 + random.randint(-5, 5) / 10
        self.texture = pygame.transform.flip(pygame.image.load("textures/napalm.png").convert_alpha(), random.randint(0, 1), random.randint(0, 1))
        self.scaleTexture()

    def show(self):
        self.Self.showAnimated(self.scaledTexture, self.position)

        if - len(self.Self.map.array) / 2 < self.position[0] < len(self.Self.map.array) / 2 and - len(self.Self.map.array[0]) / 2 < self.position[1] < len(self.Self.map.array[0]) / 2 - 1:
            if self.Self.map.array[int(self.position[0] + len(self.Self.map.array) / 2), int(self.position[1] + 1 + len(self.Self.map.array[0]) / 2)] != 0:
                self.Self.explode(self.position, 2, 2, smoke = False)
            else:
                self.position[1] += 0.1

        if time.time() > self.durability:
            for i in range(len(self.Self.particles)):
                if self.Self.particles[i].position == self.position:
                    self.Self.particles.pop(i)
                    break

        if random.randint(0, 60) == 0:
            self.Self.particles.append(Smoke(self.Self, self.position.copy(), 2))

    def scaleTexture(self):
        self.scaledTexture = self.Self.scaleTexture(self.texture)

class Smoke:
    def __init__(self, Self, position, durability = 3):
        self.Self = Self
        self.position = position
        self.durability = time.time() + durability + random.randint(-5, 5) / 10
        self.texture = pygame.transform.flip(pygame.image.load("textures/smoke.png").convert_alpha(), random.randint(0, 1), random.randint(0, 1))
        self.scaleTexture()

    def show(self):
        self.Self.showAnimated(self.scaledTexture, self.position)

        self.position[1] -= 0.2
        self.position[0] += random.randint(-1, 1) / 5

        if time.time() > self.durability:
            for i in range(len(self.Self.particles)):
                if self.Self.particles[i].position == self.position:
                    self.Self.particles.pop(i)
                    break

    def scaleTexture(self):
        self.scaledTexture = self.Self.scaleTexture(self.texture)

class LootBox:
    def __init__(self, Self, position):
        self.Self = Self
        self.position = position
        self.texture = pygame.image.load("textures/lootBox.png").convert_alpha()
        self.scaleTexture()

    def show(self):
        self.Self.showAnimated(self.scaledTexture, self.position)

    def scaleTexture(self):
        self.scaledTexture = self.Self.scaleTexture(self.texture)

class Map:
    def __init__(self, Self, position, texture):
        self.Self = Self
        self.position = position
        self.texture = pygame.image.load("textures/" + texture + ".png").convert_alpha()
        self.array = pygame.PixelArray(self.texture.copy())
        self.scaleTexture()

    def explode(self, position, radius):
        position = [int(position[0] + len(self.array) / 2), int(position[1] + len(self.array[0]) / 2)]

        for x in range(position[0] - radius, position[0] + radius):
            for y in range(position[1] - radius, position[1] + radius):
                if 0 < x < len(self.array) and 0 < y < len(self.array[0]):
                    if abs(position[0] - x)**2 + abs(position[1] - y)**2 < radius**2:
                        self.array[x][y] = int(hex(pygame.Color(0, 0, 0, 0)), 16)

        self.texture = self.array.make_surface()

        self.scaleTexture()

    def show(self):
        self.Self.show(self.scaledTexture, self.position)

    def scaleTexture(self):
        self.scaledTexture = self.Self.scaleTexture(self.texture)

    def blit(self, texture, position):
        self.texture.blit(texture, position)
        self.scaleTexture()
        array = pygame.PixelArray(texture)
        
        for x in range(position[0], position[0] + texture.get_width()):
            for y in range(position[1], position[1] + texture.get_height()):
                if self.array[x][y] == 0:
                    self.array[x][y] = array[x - position[0]][y - position[1]]

class ShowText:
    def __init__(self):
        self.textList = []

    def append(self, text, color, timer):
        if len(self.textList) == 0:
            self.textList.append([Text(text, color, (50, 5)), time.time() + timer])
        else:
            self.textList.append([Text(text, color, (50, 5)), self.textList[-1][1] + timer])

    def show(self):
        if len(self.textList) > 0:
            if time.time() < self.textList[0][1]:
                self.textList[0][0].show()
            else:
                self.textList.pop(0)

menu = Menu()