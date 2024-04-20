import pygame, time, math
pygame.init()

class PlaceMine:
    def __init__(self, Self):
        self.Self = Self
        self.name = "Mine"
        self.usages = Usage(1)
        self.icon = "textures/mine.png"
        self.texture = pygame.image.load("textures/mine.png").convert_alpha()

    def init(self):
        self.loading = False

    def show(self, position, angle, direction):
        self.position = position
        self.direction = direction
        self.Self.show(pygame.transform.rotate(pygame.transform.flip(self.scaledTexture, direction, 0), angle - (1 - direction) * 270 - direction * 90), position)

    def active(self):
        self.loading = True

    def release(self):
        if self.loading == True:
            self.position[0] += 11 + self.direction * -22

            self.Self.mines.append(Mine(self.Self, self.position))

            if self.usages.use() == False:
                self.Self.actualSoldier.active = False
            self.init()

    def scaleTexture(self):
        self.scaledTexture = self.Self.scaleTexture(self.texture)

class Mine:
    def __init__(self, Self, position = []):
        self.Self = Self
        if len(position) != 2:
            self.position =  self.Self.defineMapPosition()
        else:
            self.position = position
        self.texture = pygame.image.load("textures/mine.png").convert_alpha()
        self.timer = 0
        self.radius = 15
        self.detectionRadius = 10
        self.damages = 30
        self.scaleTexture()

    def show(self):
        self.Self.show(self.scaledTexture, self.position)

        self.position = self.Self.gravity(self.position, [3, 3, 3, 0])

        if self.position[1] > len(self.Self.map.array[0]) / 2 + 20:
            self.timer = time.time()

        if self.timer != 0:
            text = self.Self.font.render(str(int(self.timer - time.time())), True, (255, 255, 255))
            self.Self.show(text, [self.position[0], self.position[1] - 13])

            if time.time() > self.timer - 0.2:
                self.Self.explode(self.position, self.radius, self.damages, self.timer)

                if time.time() > self.timer:
                    for i in range(len(self.Self.mines)):
                        if self.Self.mines[i].position == self.position:
                            self.Self.mines.pop(i)
                            break

        else:
            for i in range(len(self.Self.soldiers)):
                for soldier in self.Self.soldiers[i]:
                    if (abs(self.position[0] - soldier.position[0]) ** 2 + abs(self.position[1] - soldier.position[1]) ** 2) ** 0.5 < 10:
                        self.timer = time.time() + 0.5

    def scaleTexture(self):
        self.scaledTexture = self.Self.scaleTexture(self.texture)

class Dynamite:
    def __init__(self, Self):
        self.Self = Self
        self.name = "Dynamite"
        self.damages = 30
        self.radius = 30
        self.usages = Usage(1)
        self.icon = "textures/dynamite.png"
        self.texture = pygame.image.load("textures/dynamite.png").convert_alpha()
        self.animatedTexture = pygame.image.load("textures/dynamiteAnimation.png").convert_alpha()

    def init(self):
        self.launched = False
        self.loading = False

    def show(self, position, angle, direction):
        if self.launched == False:
            self.position = position
            self.direction = direction
            self.Self.show(pygame.transform.flip(self.scaledTexture, direction, 0), position)
        else:
            self.Self.showAnimated(self.scaledAnimatedTexture, self.position)

            text = self.Self.font.render(str(int(self.timer - time.time())), True, (255, 255, 255))
            self.Self.show(text, [self.position[0], self.position[1] - 13])

            self.position = self.Self.gravity(self.position, [3, 3, 6, 6])

            if time.time() > self.timer - 0.2:
                self.Self.explode(self.position, self.radius, self.damages, self.timer)
                if time.time() > self.timer:
                    if self.usages.use() == False:
                        self.Self.actualSoldier.active = False
                    self.init()

    def active(self):
        if self.launched == False:
            self.loading = True

    def release(self):
        if self.loading == True:
            self.loading = False
            self.launched = True
            self.position[0] += 5 + self.direction * -10
            self.timer = time.time() + 4

    def scaleTexture(self):
        self.scaledTexture = self.Self.scaleTexture(self.texture)
        self.scaledAnimatedTexture = self.Self.scaleTexture(self.animatedTexture)

class Grenade:
    def __init__(self, Self):
        self.Self = Self
        self.name = "Grenade"
        self.damages = 40
        self.radius = 20
        self.usages = Usage(1)
        self.icon = "textures/grenade.png"
        self.texture = pygame.image.load("textures/grenade.png").convert_alpha()
        self.loadingTexture = pygame.image.load("textures/loading.png").convert_alpha()

    def init(self):
        self.loading = False
        self.launched = False
        self.loadingPower = 0

    def show(self, position, angle, direction):
        if self.launched == False:
            self.position = position
            self.angle = angle
            self.Self.show(pygame.transform.rotate(pygame.transform.flip(self.scaledTexture, direction, 0), angle - (1 - direction) * 270 - direction * 90), position)
        else:
            ancientPosition = self.position.copy()
            self.position, self.loadingPower, self.angle = self.Self.curveMoving(self.position, self.loadingPower, self.angle, [3, 3, 3, 3])
            if int(ancientPosition[0]) != int(self.position[0]) or int(ancientPosition[1]) != int(self.position[1]):
                rotation = (self.timer - time.time()) * 360
            else:
                rotation = 0

            self.Self.show(pygame.transform.rotate(self.scaledTexture, rotation), self.position)

            text = self.Self.font.render(str(int(self.timer - time.time())), True, (255, 255, 255))
            self.Self.show(text, [self.position[0], self.position[1] - 13])

            if time.time() > self.timer - 0.2:
                self.Self.explode(self.position, self.radius, self.damages, self.timer)
                if time.time() > self.timer:
                    if self.usages.use() == False:
                        self.Self.actualSoldier.active = False
                    self.init()

        if self.loading == True:
            self.Self.show(pygame.transform.rotate(self.scaledLoadingTexture.subsurface((0, int((32 - self.loadingPower) * self.Self.scale), int(16 * self.Self.scale), int(self.loadingPower * self.Self.scale))), angle), [position[0] + math.cos(math.radians(angle + 90)) * self.loadingPower / 2, position[1] - math.sin(math.radians(angle + 90)) * self.loadingPower / 2])

    def scaleTexture(self):
        self.scaledTexture = self.Self.scaleTexture(self.texture)
        self.scaledLoadingTexture = self.Self.scaleTexture(self.loadingTexture)

    def active(self):
        if self.launched == False:
            self.loading = True
            if self.loadingPower < 32:
                self.loadingPower += 0.5
            else:
                self.release()

    def release(self):
        if self.loading == True:
            self.loading = False
            self.launched = True
            self.timer = time.time() + 4

class AirBomb:
    def __init__(self, Self, position, angle):
        self.Self = Self
        self.position = position
        self.angle = angle
        self.damages = 10
        self.radius = 20
        self.timer = 0
        self.texture = pygame.image.load("textures/shell.png")
        self.scaleTexture()

    def scaleTexture(self):
        self.scaledTexture = self.Self.scaleTexture(self.texture)

    def show(self):
        if self.timer == 0:
            self.position[0] += math.cos(math.radians(self.angle + 90)) * 4
            self.position[1] -= math.sin(math.radians(self.angle + 90)) * 4

            self.Self.show(pygame.transform.rotate(self.scaledTexture, self.angle), self.position)

            if - len(self.Self.map.array) / 2 + 3 < self.position[0] < len(self.Self.map.array) / 2 - 3 and - len(self.Self.map.array[0]) / 2 + 3 < self.position[1] < len(self.Self.map.array[0]) / 2 - 3:
                position = [int(self.position[0] + len(self.Self.map.array) / 2), int(self.position[1] + len(self.Self.map.array[0]) / 2)]
                if self.Self.map.array[position[0] - 3, position[1] - 3] != 0 or self.Self.map.array[position[0] + 3, position[1] - 3] != 0 or self.Self.map.array[position[0] - 3, position[1] + 3] != 0 or self.Self.map.array[position[0] + 3, position[1] + 3] != 0:
                    self.timer = time.time() + 0.2

            if self.position[1] > len(self.Self.map.array[0]) / 2 + 20:
                    self.timer = time.time()

        else:
            self.Self.explode(self.position, self.radius, self.damages, self.timer)

            if time.time() > self.timer:
                return True
        return False

class AirAttack:
    def __init__(self, Self):
        self.Self = Self
        self.name = "Air Attack"
        self.usages = Usage(1)
        self.airBombs = []
        self.direction = -1
        self.icon = "textures/teleporter.png"
        self.texture = pygame.image.load("textures/teleporter.png")

    def left(self):
        self.angle = 210
        self.Self.mouse.setTexture(pygame.image.load("textures/airAttackMouse.png").convert_alpha().subsurface((0, 0, 16, 16)), (-16, -16))

    def right(self):
        self.angle = 150
        self.Self.mouse.setTexture(pygame.image.load("textures/airAttackMouse.png").convert_alpha().subsurface((0, 16, 16, 16)), (0, -16))

    def scaleTexture(self):
        self.scaledTexture = self.Self.scaleTexture(self.texture)
        for airBomb in self.airBombs:
            airBomb.scaleTexture()

    def init(self):
        self.loading = False
        self.launched = False
        self.left()

    def show(self, position, angle, direction):
        self.Self.show(pygame.transform.flip(self.scaledTexture, direction, 0), position)

        if self.launched == True:
            if len(self.airBombs) == 0:
                self.init()
                if self.usages.use() == False:
                    self.Self.actualSoldier.active = False
                    self.Self.mouse.init()

            for airBomb in self.airBombs: 
                if airBomb.show() == True:
                    self.airBombs.pop(self.airBombs.index(airBomb))

    def move(self, keysPressed):
        if keysPressed[pygame.K_a]:
            self.left()

        if keysPressed[pygame.K_e]:
            self.right()

    def active(self):
        self.loading = True

    def release(self):
        if self.loading == True:
            if self.launched == False:
                self.airBombs = [AirBomb(self.Self, [self.Self.mousePos[0] + math.cos(math.radians(self.angle + 90)) * ((self.Self.mousePos[1] + len(self.Self.map.array[0]) / 2) / math.sin(math.radians(self.angle + 90))) + i * 10 - 20, - len(self.Self.map.array[0]) / 2], self.angle) for i in range(5)]
                self.launched = True

class Bazooka:
    def __init__(self, Self):
        self.Self = Self
        self.name = "Bazooka"
        self.damages = 40
        self.radius = 25
        self.usages = Usage(1)
        self.icon = "textures/bazooka.png"
        self.iconTexture = pygame.image.load("textures/bazooka.png").convert_alpha()
        self.texture = pygame.image.load("textures/shell.png").convert_alpha()
        self.loadingTexture = pygame.image.load("textures/loading.png").convert_alpha()
        self.position =  [0, 0]

    def scaleTexture(self):
        self.scaledTexture = self.Self.scaleTexture(self.texture)
        self.scaledIconTexture = self.Self.scaleTexture(self.iconTexture)
        self.scaledLoadingTexture = self.Self.scaleTexture(self.loadingTexture)
        
    def init(self):
        self.loading = False
        self.launched = False
        self.loadingPower = 0
        self.timer = 0

    def show(self, position, angle, direction):
        if self.launched == False:
            self.position[0] = position[0] + math.cos(math.radians(angle + 90)) * 9
            self.position[1] = position[1] - math.sin(math.radians(angle + 90)) * 9
            self.angle = angle
            self.Self.show(pygame.transform.rotate(pygame.transform.flip(self.scaledIconTexture, direction, 0), angle - (1 - direction) * 270 - direction * 90), position)
        else:
            if self.timer == 0:
                self.position, self.loadingPower, self.angle = self.Self.curveMoving(self.position, self.loadingPower, self.angle, [0, 0, 0, 0], bounce = False)

                self.Self.show(pygame.transform.rotate(self.scaledTexture, self.angle), self.position)

                if - len(self.Self.map.array) / 2 + 3 < self.position[0] < len(self.Self.map.array) / 2 - 3 and - len(self.Self.map.array[0]) / 2 + 3 < self.position[1] < len(self.Self.map.array[0]) / 2 - 3:
                    position = [int(self.position[0] + len(self.Self.map.array) / 2), int(self.position[1] + len(self.Self.map.array[0]) / 2)]
                    if self.Self.map.array[position[0] - 3, position[1] - 3] != 0 or self.Self.map.array[position[0] + 3, position[1] - 3] != 0 or self.Self.map.array[position[0] - 3, position[1] + 3] != 0 or self.Self.map.array[position[0] + 3, position[1] + 3] != 0:
                        self.timer = time.time() + 0.2

                if self.position[1] > len(self.Self.map.array[0]) / 2 + 20:
                    self.timer = time.time()
            else:
                self.Self.explode(self.position, self.radius, self.damages, self.timer)
                if time.time() > self.timer:
                    if self.usages.use() == False:
                        self.Self.actualSoldier.active = False
                    self.init()

        if self.loading == True:
            self.Self.show(pygame.transform.rotate(self.scaledLoadingTexture.subsurface((0, int((32 - self.loadingPower) * self.Self.scale), int(16 * self.Self.scale), int(self.loadingPower * self.Self.scale))), angle), [position[0] + math.cos(math.radians(angle + 90)) * self.loadingPower / 2, position[1] - math.sin(math.radians(angle + 90)) * self.loadingPower / 2])

    def active(self):
        if self.launched == False:
            self.loading = True
            if self.loadingPower < 32:
                self.loadingPower += 0.5
            else:
                self.release()

    def release(self):
        if self.loading == True:
            self.loading = False
            self.launched = True

class PumpRifle:
    def __init__(self, Self):
        self.sound = pygame.mixer.Sound("sounds/pumpRifle.wav")
        self.Self = Self
        self.name = "Pump Rifle"
        self.damages = 30
        self.radius = 8
        self.position = [0, 0]
        self.usages = Usage(2)
        self.icon = "textures/pumpRifle.png"
        self.texture = pygame.image.load("textures/pumpRifle.png").convert_alpha()

    def scaleTexture(self):
        self.scaledTexture = self.Self.scaleTexture(self.texture)

    def init(self):
        self.loading = False

    def show(self, position, angle, direction):
        if self.loading == False:
            self.position[0] = position[0] + math.cos(math.radians(angle + 90)) * 17
            self.position[1] = position[1] - math.sin(math.radians(angle + 90)) * 17
            self.angle = angle
            self.direction = direction
        self.Self.show(pygame.transform.rotate(pygame.transform.flip(self.scaledTexture, direction, 0), angle - (1 - direction) * 270 - direction * 90), position)

    def active(self):
        if self.loading == False:
            self.loading = True
            self.sound.play()

    def release(self):
        if self.loading == True:
            explode = False
            position = self.position
            while explode == False:
                position[0] += math.cos(math.radians(self.angle + 90))
                position[1] -= math.sin(math.radians(self.angle + 90))
                if -len(self.Self.map.array) / 2 < position[0] < len(self.Self.map.array) / 2 and -len(self.Self.map.array[0]) / 2 < position[1] < len(self.Self.map.array[0]) / 2:
                    if self.Self.collision(position, self.radius) == True:
                        self.Self.explode(position, self.radius, self.damages)
                        explode = True
                else:
                    explode = True

            if self.usages.use() == False:
                self.Self.actualSoldier.active = False
            self.init()

class Teleporter:
    def __init__(self, Self):
        self.Self = Self
        self.name = "Teleporter"
        self.usages = Usage(1)
        self.icon = "textures/teleporter.png"
        self.texture = pygame.image.load("textures/teleporter.png").convert_alpha()

    def init(self):
        self.loading = False

    def scaleTexture(self):
        self.scaledTexture = self.Self.scaleTexture(self.texture)

    def show(self, position, angle, direction):
        self.Self.show(pygame.transform.flip(self.scaledTexture, direction, 0), position)

    def active(self):
        self.loading = True

    def release(self):
        if self.loading == True:
            self.Self.actualSoldier.position = self.Self.mousePos
            if self.usages.use() == False:
                self.Self.actualSoldier.active = False
            self.init()

class Build:
    def __init__(self, Self):
        self.Self = Self
        self.name = "Build"
        self.usages = Usage(3)
        self.reach = 40
        self.angle = 0
        self.loading = False
        self.icon = "textures/build.png"
        self.iconTexture = pygame.image.load("textures/build.png").convert_alpha()

    def init(self):
        self.texture = pygame.image.load("textures/littleBuild.png").convert_alpha()
        self.angle = 0

    def scaleTexture(self):
        self.scaledIconTexture = self.Self.scaleTexture(self.iconTexture)
        self.scaledTexture = self.Self.scaleTexture(self.texture)

    def show(self, position, angle , direction):
        self.Self.show(pygame.transform.flip(self.scaledIconTexture, direction, 0), position)
        self.distance = ((self.Self.actualSoldier.position[0] - self.Self.mousePos[0])**2 + (self.Self.actualSoldier.position[1] - self.Self.mousePos[1])**2)**0.5

        if self.distance < self.reach:
            self.Self.show(pygame.transform.rotate(self.scaledTexture, self.angle), self.Self.mousePos)

    def active(self):
        self.loading = True

    def move(self, keysPressed):
        if keysPressed[pygame.K_a]:
            self.angle -= 3

        elif keysPressed[pygame.K_e]:
            self.angle += 3

        if self.angle // 180 % 2 == 0:
            self.texture = pygame.image.load("textures/littleBuild.png").convert_alpha()
            self.scaleTexture()
        else:
            self.texture = pygame.image.load("textures/bigBuild.png").convert_alpha()
            self.scaleTexture()

    def release(self):
        if self.loading == True:
            self.loading = False
            if self.distance < self.reach:
                rotatedTexture = pygame.transform.rotate(self.texture, self.angle)
                self.Self.map.blit(rotatedTexture, [int(self.Self.mousePos[0] + self.Self.map.texture.get_width() / 2 - rotatedTexture.get_width() / 2), int(self.Self.mousePos[1] + self.Self.map.texture.get_height() / 2 - rotatedTexture.get_height() / 2)])
                if self.usages.use() == False:
                    self.Self.actualSoldier.active = False
                    self.init()

class Usage:
    def __init__(self, maxUsages):
        self.maxUsages = maxUsages
        self.usages = 0

    def use(self):
        self.usages += 1

        if self.usages == self.maxUsages:
            self.usages = 0
            return False
        else:
            return True
        
    def get(self):
        return self.usages
        
def importWeapons(Self):
    Self.weapons = [Grenade(Self), Bazooka(Self), Dynamite(Self), PlaceMine(Self), PumpRifle(Self), Teleporter(Self), Build(Self), AirAttack(Self)]