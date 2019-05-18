import pygame
import math
from pygame.locals import *
import random
from GameObject import GameObject
from pygamegame import PygameGame

    
class Bkground(GameObject):
    def init():
        Bkground.bkgroundImage = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/bk1.png').convert_alpha(),
            (800, 600)), 0)
    
    def __init__(self, x, y):
        super(Bkground, self).__init__(x, y, Bkground.bkgroundImage, 30)
        
    def update(self, screenWidth, screenHeight):
        super(Bkground, self).update(screenWidth, screenHeight)
        
        
class Start(GameObject):
    def init():
        Start.startImage = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/key1.png').convert_alpha(),
            (120, 50)), 0)    
    def __init__(self, x, y):
        super(Start, self).__init__(x, y, Start.startImage, 30)
        
    def update(self, screenWidth, screenHeight):
        super(Start, self).update(screenWidth, screenHeight)
class Quit(GameObject):
    def init():
        Quit.startImage = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/key2.png').convert_alpha(),
            (120, 50)), 0)    
    def __init__(self, x, y):
        super(Quit, self).__init__(x, y, Quit.startImage, 30)
        
    def update(self, screenWidth, screenHeight):
        super(Quit, self).update(screenWidth, screenHeight)
class Help(GameObject):
    def init():
        Help.startImage = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/key3.png').convert_alpha(),
            (120, 50)), 0)    
    def __init__(self, x, y):
        super(Help, self).__init__(x, y, Help.startImage, 30)
        
    def update(self, screenWidth, screenHeight):
        super(Help, self).update(screenWidth, screenHeight)
class Helper(GameObject):
    def init():
        Helper.startImage = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/bk0.png').convert_alpha(),
            (300, 300)), 0)    
    def __init__(self, x, y):
        super(Helper, self).__init__(x, y, Helper.startImage, 30)
        
    def update(self, screenWidth, screenHeight):
        super(Helper, self).update(screenWidth, screenHeight)
class Probe(GameObject):
    size = 1
    def init(color):
        size = Probe.size
        Probe.probeImage = pygame.Surface((Probe.size, Probe.size), pygame.SRCALPHA)
        pygame.draw.circle(Probe.probeImage, (255,255,255), (size//2, size//2), size//2)
            
    def __init__(self, x, y):
        super(Probe, self).__init__(x, y, Probe.probeImage, Probe.size // 2)

    def update(self, screenWidth, screenHeight):
        super(Probe, self).update(screenWidth, screenHeight)

class Silk(GameObject):
    time = 50 * 55
    size = 5
    x0, y0 = 0, 0
    x1, y1 = 0, 0
    def init(screenWidth,screenHeight):
        size = Silk.size
        Silk.silkImage = pygame.Surface((screenWidth, screenHeight), pygame.SRCALPHA)
        pygame.draw.line(Silk.silkImage, (255, 255, 255), (30, screenHeight//4), (30,0), size)
            
    def __init__(self, x, y):
        super(Silk, self).__init__(x, y, Silk.silkImage, self.size)

    def update(self, screenWidth, screenHeight):
        self.image = pygame.Surface((screenWidth,screenHeight), pygame.SRCALPHA)
        pygame.draw.line(self.image, (255, 255, 255), (self.x0, self.y0), \
                        (self.x1, self.y1), self.size)
class Spider(GameObject):
    # we only need to load the image once, not for every spider we make!
    #   granted, there's probably only one spider...
    @staticmethod
    def init(select):
        (scale0, scale1) = (100, 100)
        if select == "orange":
            Spider.spiderImage = pygame.transform.rotate(pygame.transform.scale(
                pygame.image.load('images/spider.png').convert_alpha(),
                (scale0, scale1)), 0)
        elif select == "red":
            Spider.spiderImage = pygame.transform.rotate(pygame.transform.scale(
                pygame.image.load('images/spiderred.png').convert_alpha(),
                (scale0, scale1)), 0)

    def __init__(self, x, y):
        super(Spider, self).__init__(x, y, Spider.spiderImage, 30)
        self.power = 0.5
        self.angleSpeed = 5
        self.angle = 0  # starts pointing straight up
        self.maxSpeed = 100
        self.attach = False
        self.speed = 0
        self.attchflg = False
        self.vxtmp = 0
        self.vx = 0;
        self.vy = 0
        self.angle1 = 0

    def update(self, screenWidth, screenHeight):
        #non-uniform motion
        self.accmotion(self.power)
        #update rect-coordinate
        self.baseImage = Spider.spiderImage.copy() 
        super(Spider, self).update(screenWidth, screenHeight)
        

    def accmotion(self, power): #accelerated (non-uniform) motion
        angle = math.radians(self.angle1)
        vx, vy = self.velocity

        vx = vx * math.sin(angle) * math.sin(angle) + vy * math.cos(angle) \
                * math.sin(angle) + power * math.cos(angle) *math.sin(angle)
        vy = vx * math.cos(angle) * math.sin(angle) + vy * math.cos(angle) \
                * math.cos(angle) + power * math.cos(angle) *math.cos(angle)

        self.speed = math.sqrt(vx ** 2 + vy ** 2)
        print(vx, vy)
        if self.speed > self.maxSpeed:
            factor = self.maxSpeed / self.speed
            vx *= factor
            vy *= factor
        (self.vx, self.vy) = (vx, vy)
        self.velocity = (vx, vy)
class Grapple(GameObject):
    @staticmethod
    def init():
        image = pygame.image.load('images/grapples.png').convert_alpha()
        rows, cols = 4, 4
        width, height = image.get_size()
        cellWidth, cellHeight = width / cols, height / rows
        Grapple.images = []
        #read grapples one by one
        for i in range(rows):
            for j in range(cols):
                subImage = image.subsurface(
                    (i * cellWidth, j * cellHeight, cellWidth, cellHeight))
                Grapple.images.append(subImage)

    (minSize, maxSize) = (4, 5)

    def __init__(self, x, y, level=None):
        if level is None:
            level = random.randint(Grapple.minSize, Grapple.maxSize)
        self.level = level
        factor = self.level / Grapple.maxSize
        image = random.choice(Grapple.images)
        w, h = image.get_size()
        #set size of grapple
        image = pygame.transform.scale(image, (int(w*factor), int(h*factor)))
        super(Grapple, self).__init__(x, y, image, w / 2 * factor)
        
    def update(self, screenWidth, screenHeight):
        super(Grapple, self).update(screenWidth*4, screenHeight)
                    
class GameBegin(PygameGame):
    def init(self):
        self.GameStart = False
        self.quitFlg = False
        
        self.bgColor = (0,69,102)
        # start
        Start.init()
        start = Start(self.width / 4*3, self.height / 2 +25)
        self.startGroup = pygame.sprite.GroupSingle(start)
        # quit
        Quit.init()
        quit = Quit(self.width / 4*3, self.height / 2 + 100)
        self.quitGroup = pygame.sprite.GroupSingle(quit)
        # help
        Help.init()
        help = Help(self.width / 4*3, self.height / 2 + 175)
        self.helpGroup = pygame.sprite.GroupSingle(help)
        # background
        Bkground.init()
        bkground = Bkground(self.width / 2, self.height //2)
        self.bkgroundGroup = pygame.sprite.GroupSingle(bkground)
        # helper
        Helper.init()
        helper = Helper(self.width / 2, self.height //2)
        self.helperGroup = pygame.sprite.GroupSingle(helper)
        #probe
        Probe.init(self.bgColor)
        probe = Probe(0, 0)
        self.probeGroup = pygame.sprite.GroupSingle(probe)    
        #spiderGroup
        Spider.init("orange")
        (initSpx, initSpy) = (self.width / 2, 200)
        spider = Spider(initSpx, initSpy)
        self.spiderGroup = pygame.sprite.GroupSingle(spider)
        #grapples
        Grapple.init()
        self.grapples = pygame.sprite.Group()
        x = self.width / 3*2
        y = 80
        self.grapples.add(Grapple(x, y))
        #silkGroup
        Silk.init(self.width, self.height)
        silk = Silk(self.width//2, self.height//2)
        self.silkGroup = pygame.sprite.GroupSingle(silk)
    def keyPressed(self, code, mod):
        if code == pygame.K_s:
            self.GameStart = True
        if code == pygame.K_q:
            self.quitFlg = True
        
    def mousePressed(self, x, y):        
        self.probeGroup.sprite.x = x
        self.probeGroup.sprite.y = y
        self.GameHelp = False
        
    def timerFired(self, dt, screen):

        # colors
        textColor = (255,255,255)
        bankColor = (153,102,51)
        buttonColor = (254,200,0)
        clickedButtonColor = (235,225,255)
        buttonText = (255,255,255)
        # display
        self.bkgroundGroup.update(self.width, self.height)
        self.probeGroup.update(self.width, self.height)
        self.startGroup.update(self.width, self.height)
        self.quitGroup.update(self.width, self.height)
        self.helpGroup.update(self.width, self.height)
        self.helperGroup.update(self.width, self.height)
        
        #detect if collide happend between probe and button
        for grapple in pygame.sprite.groupcollide(
            self.startGroup, self.probeGroup, False, False,
            pygame.sprite.collide_circle):
            self.GameStart = True
        #detect if collide happend between probe and button
        for grapple in pygame.sprite.groupcollide(
            self.quitGroup, self.probeGroup, False, False,
            pygame.sprite.collide_circle):
            self.Gameover = True
        #detect if collide happend between probe and button
        for grapple in pygame.sprite.groupcollide(
            self.helpGroup, self.probeGroup, False, False,
            pygame.sprite.collide_circle):
            self.GameHelp = True
        
        #make alias 
        spider = self.spiderGroup.sprite
        silk = self.silkGroup.sprite
        #get x0,y0,x1,y1, and the angle of silk
        self.silkGroup.sprite.x0 = spider.x
        self.silkGroup.sprite.y0 = spider.y
        (x0, y0) = (silk.x0, silk.y0)
        self.silkGroup.sprite.x1 = self.grapples.sprites()[0].x
        self.silkGroup.sprite.y1 = self.grapples.sprites()[0].y
        (x1, y1) = (silk.x1, silk.y1)
        fullAng, halfAng, deltaAng = 180, 90, 90
        angle = (math.atan2((x1-x0),(y1-y0))/math.pi)*fullAng
        spider.angle = angle - 180
        self.spiderGroup.sprite.angle1 = angle-deltaAng
        #boundary
        if spider.y > self.height//2 - 30:
            spider.y = self.height//2 - 30
        
        #update
        self.spiderGroup.update(self.width, self.height)
        self.silkGroup.sprite.x0 = spider.x
        self.silkGroup.sprite.y0 = spider.y
        self.silkGroup.update(self.width, self.height)
        self.grapples.update(self.width, self.height)
        
    def redrawAll(self, screen):
        self.bkgroundGroup.draw(screen)
        self.probeGroup.draw(screen)
        self.startGroup.draw(screen)
        self.quitGroup.draw(screen)
        self.helpGroup.draw(screen)

        self.silkGroup.draw(screen)
        self.grapples.draw(screen)
        self.spiderGroup.draw(screen)
        if self.GameHelp:
            self.helperGroup.draw(screen)