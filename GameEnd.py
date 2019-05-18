import pygame
import copy
import math
from pygame.locals import *
import random
from GameObject import GameObject
from pygamegame import PygameGame

    
class Bkground(GameObject):
    def init():
        Bkground.bkgroundImage = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/bk2.png').convert_alpha(),
            (800, 600)), 0)
    
    def __init__(self, x, y):
        super(Bkground, self).__init__(x, y, Bkground.bkgroundImage, 30)
        
    def update(self, screenWidth, screenHeight):
        super(Bkground, self).update(screenWidth, screenHeight)
        
        
class Start(GameObject):
    def init(strdata):
        Start.startImage = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/nop.png').convert_alpha(),
            (100, 100)), 0)
        # pygame.draw.circle(Start.startImage, (255, 255, 255), (10, 10), 10)
        w, h = Start.startImage.get_size()
        displayText = pygame.font.SysFont("comicsansms", 26)# set font
        textSurface = displayText.render(strdata, True, (255, 255, 255))# surface for 
        textRect = textSurface.get_rect()# rect for
        textRect.center = (w//2, h//2)
        Start.startImage.blit(textSurface,textRect)  
    
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
class Homepg(GameObject):
    def init():
        Homepg.startImage = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/key5.png').convert_alpha(),
            (120, 50)), 0)    
    def __init__(self, x, y):
        super(Homepg, self).__init__(x, y, Homepg.startImage, 30)
        
    def update(self, screenWidth, screenHeight):
        super(Homepg, self).update(screenWidth, screenHeight)
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


                    
class GameEnd(PygameGame):
    def init(self):
        self.GameStart = False
        self.quitFlg = False
        
        self.bgColor = (0,69,102)
        # quit
        Quit.init()
        quit = Quit(710, 50)
        self.quitGroup = pygame.sprite.GroupSingle(quit)
        # help
        Homepg.init()
        homepg = Homepg(90, 50)
        self.homepgGroup = pygame.sprite.GroupSingle(homepg)
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
        #data
        self.data = [0, 79, 96, 100, 24554, 3] 
 

    def keyPressed(self, code, mod):
        if code == pygame.K_s:
            self.GameStart = True
        if code == pygame.K_q:
            self.quitFlg = True
        
    def mousePressed(self, x, y):        
        self.probeGroup.sprite.x = x
        self.probeGroup.sprite.y = y
        self.GameHelp = False
        
    def timerFired(self, dt, screen, data):
        self.data = copy.deepcopy(data)
        self.data[1] = int(self.data[1]/240*100)
        self.data[1] = -self.data[1]+150
        if self.data[1]<0: self.data[1]=0
        if self.data[1]>100: self.data[1]=100
        self.data[2] = int(self.data[2]/110*100)
        if self.data[2]<0: self.data[2]=0
        if self.data[2]>100: self.data[2]=100
        self.data[3] = int(self.data[3])
        if self.data[3]<0: self.data[3]=0
        if self.data[3]>100: self.data[3]=100          
        # start
        Start.init(str(self.data[1]))
        start = Start(self.width / 2 + 65, self.height / 2 +50)
        self.startGroup1 = pygame.sprite.GroupSingle(start) 
        # start
        Start.init(str(self.data[2]))
        start = Start(self.width / 2 + 65, self.height / 2 +98)
        self.startGroup2 = pygame.sprite.GroupSingle(start) 
        # start
        Start.init(str(self.data[3]))
        start = Start(self.width / 2 + 65, self.height / 2 +146)
        self.startGroup3 = pygame.sprite.GroupSingle(start) 
        # start
        Start.init(str(self.data[-1]))
        start = Start(self.width / 2 + 65, self.height / 2 +200)
        self.startGroup4 = pygame.sprite.GroupSingle(start) 
        print(self.data)
        
        # colors
        textColor = (255,255,255)
        bankColor = (153,102,51)
        buttonColor = (254,200,0)
        clickedButtonColor = (235,225,255)
        buttonText = (255,255,255)
        # display
        self.bkgroundGroup.update(self.width, self.height)
        self.probeGroup.update(self.width, self.height)
        self.startGroup1.update(self.width, self.height)
        self.startGroup2.update(self.width, self.height)
        self.startGroup3.update(self.width, self.height)
        self.startGroup4.update(self.width, self.height)
        self.quitGroup.update(self.width, self.height)
        self.homepgGroup.update(self.width, self.height)
        
        #detect if collide happend between probe and button
        for grapple in pygame.sprite.groupcollide(
            self.quitGroup, self.probeGroup, False, False,
            pygame.sprite.collide_circle):
            self.Gameover = True
        #detect if collide happend between probe and button
        for grapple in pygame.sprite.groupcollide(
            self.homepgGroup, self.probeGroup, False, False,
            pygame.sprite.collide_circle):
            self.GameHome = True
        

        
    def redrawAll(self, screen):
        self.bkgroundGroup.draw(screen)
        self.probeGroup.draw(screen)
        self.startGroup1.draw(screen)
        self.startGroup2.draw(screen)
        self.startGroup3.draw(screen)
        self.startGroup4.draw(screen)
        self.quitGroup.draw(screen)
        self.homepgGroup.draw(screen)
        
        
            