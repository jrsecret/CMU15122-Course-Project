'''
Game.py

Actually implements the game
Lukas Peraza, 2015 for 15-112 Pygame Lecture
'''
import pygame
from pygamegame import PygameGame
import random
import math
from GameObject import GameObject
from Bonus import *
from Hazard import *
from Indicator import *

class Silk(GameObject):
    time = 50 * 55
    size = 5
    x0, y0 = 30, 200
    x1, y1 = 30, 0
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
        

class Probe(GameObject):
    speed = 50
    time = 50 * 2 # last 2 seconds
    size = 20

    def __init__(self, x, y, angle):
        size = Probe.size
        image = pygame.Surface((Probe.size, Probe.size), pygame.SRCALPHA)
        pygame.draw.circle(image, (255, 255, 255), (size//2, size//2), size//2)
        super(Probe, self).__init__(x, y, image, size // 2)
        vx = Probe.speed * math.cos(math.radians(angle))
        vy = -Probe.speed * math.sin(math.radians(angle))
        self.velocity = vx, vy
        self.timeOnScreen = 0

    def update(self, screenWidth, screenHeight):
        vx, vy = self.velocity
        self.x += vx
        self.y += vy
        w, h = self.image.get_size()
        #update rect-coordinate
        self.rect = pygame.Rect(self.x - w / 2, self.y - h / 2, w, h)
        #kill probe when out of screen
        if self.rect.left > screenWidth or self.rect.right < 0 or \
            self.rect.top > screenHeight or self.rect.bottom < 0:
            self.kill()
            
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
        self.maxSpeed = 10
        self.attach = False
        self.speed = 0
        self.attchflg = False
        self.vxtmp = 0
        self.vx = 0;
        self.vy = 0
        self.angle1 = 0

    def update(self, keysDown, screenWidth, screenHeight, scrollx):
        #control movement by Keyboard
        if keysDown(pygame.K_LEFT):
            self.angle += self.angleSpeed
        if keysDown(pygame.K_RIGHT):
            self.angle -= self.angleSpeed
        #non-uniform motion
        self.accmotion(self.power, scrollx)
        #update rect-coordinate
        self.baseImage = Spider.spiderImage.copy() 
        super(Spider, self).update(screenWidth, screenHeight)
        

    def accmotion(self, power, scrollx): #accelerated (non-uniform) motion
        angle = math.radians(self.angle1)
        vx, vy = self.velocity
        if scrollx != 0: vx, vy = scrollx, vy

        if self.attach:
            vx = vx * math.sin(angle) * math.sin(angle) + vy * math.cos(angle) \
                    * math.sin(angle) + power * math.cos(angle) *math.sin(angle)
            vy = vx * math.cos(angle) * math.sin(angle) + vy * math.cos(angle) \
                    * math.cos(angle) + power * math.cos(angle) *math.cos(angle)
        else:
            self.attchflg = False
            vx += power * math.sin(angle)
            vy += power * math.cos(angle)
        self.speed = math.sqrt(vx ** 2 + vy ** 2)
        if self.speed > self.maxSpeed:
            factor = self.maxSpeed / self.speed
            vx *= factor
            vy *= factor
        self.vxtmp = vx
        if scrollx == 0: self.velocity = (vx, vy)
        else: self.velocity = (0, vy)
        (self.vx, self.vy) = (vx, vy)


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
        

class Track(GameObject):
    @staticmethod
    def init():
        image = pygame.image.load('images/track.png').convert_alpha()
        width, height = image.get_size()
        Track.images = []
        num = 1
        #read grapples one by one
        for i in range(num):
                subImage = image.subsurface((0, 0, width, height))
                Track.images.append(subImage)

    def __init__(self, x, y, level=None):
        factor = 0.5
        image = random.choice(Track.images)
        w, h = image.get_size()
        #set size of grapple
        image = pygame.transform.scale(image, (int(w*factor), int(h*factor)))
        super(Track, self).__init__(x, y, image, w / 2 * factor)
        
    def update(self, screenWidth, screenHeight):
        super(Track, self).update(screenWidth*4, screenHeight)    
  
class River(GameObject):
    @staticmethod
    def init():
        (scale0, scale1) = (9000, 500)
        River.riverImage = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/longriver.png').convert_alpha(),
            (scale0, scale1)), 0)

    def __init__(self, x, y):
        super(River, self).__init__(x, y, River.riverImage, 30)

    def update(self, screenWidth, screenHeight):
        super(River, self).update(screenWidth*4, screenHeight)

class Home(GameObject):
    @staticmethod
    def init():
        (scale0, scale1) = (200, 200)
        Home.homeImage = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/home.png').convert_alpha(),
            (scale0, scale1)), 0)

    def __init__(self, x, y):
        super(Home, self).__init__(x, y, Home.homeImage, 30)

    def update(self, screenWidth, screenHeight):
        super(Home, self).update(screenWidth*4, screenHeight)

class Frozen(GameObject):
    def init():
        Frozen.frozenImage = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/icetransparent.png').convert_alpha(),
            (150, 120)), 0)
    
    def __init__(self, x, y):
        super(Frozen, self).__init__(x, y, Frozen.frozenImage, 30)
        
    def update(self, screenWidth, screenHeight):
        super(Frozen, self).update(screenWidth, screenHeight)
        
class GameState1(PygameGame):
    @staticmethod
    def bonuhazdinit(self):
        #bonuses2
        Bonus2.init()
        self.bonuses2 = pygame.sprite.Group()
        b2num = 5
        for i in range(b2num):
            x = random.randint(i*(self.width*6//b2num),(i+1)*(self.width*6//b2num))
            y = random.randint(self.height//4, self.height//4*3)
            self.bonuses2.add(Bonus2(x, y))
        #hazardice
        Hazardice.init("ice")
        self.hazardices = pygame.sprite.Group()
        h2num = 10
        for i in range(h2num):
            x = random.randint(i*(self.width*8//h2num),(i+1)*(self.width*8//h2num))
            y = random.randint(self.height//4, self.height//4*3)
            self.hazardices.add(Hazardice(x, y))
        
    def init(self):
        self.bgColor = (190, 190, 190)
        #spiderGroup
        Spider.init("orange")
        (initSpx, initSpy) = (30, self.height//4)
        spider = Spider(initSpx, initSpy)
        self.spiderGroup = pygame.sprite.GroupSingle(spider)
        #grapples
        Grapple.init()
        self.grapples = pygame.sprite.Group()
        gnum = 60
        for i in range(gnum):
            x = random.randint(i*(self.width*10//gnum),(i+1)*(self.width*10//gnum))
            y = random.randint(0, self.height//4)
            self.grapples.add(Grapple(x, y))
        #probes
        self.probes = pygame.sprite.Group()
        #silkGroup
        Silk.init(self.width, self.height)
        silk = Silk(self.width//2, self.height//2)
        self.silkGroup = pygame.sprite.GroupSingle(silk)
        #tracks
        Track.init()
        self.tracks = pygame.sprite.Group()
        #bonus and hazard init
        self.bonuhazdinit(self)
        #river
        River.init()
        river = River(self.width*4, self.height * 0.6)
        self.riverGroup = pygame.sprite.GroupSingle(river)
        #home
        Home.init()
        (initHmx, initHmy) = (100, 100)
        home = Home(self.width*8-initHmx, self.height//2-initHmx)
        self.homeGroup = pygame.sprite.GroupSingle(home)
        #Frozen
        Frozen.init()
        frozen = Frozen(-100, -100)
        self.frozenGroup = pygame.sprite.GroupSingle(frozen)
        #indicator
        Indicator1.init("speed")
        (initIndx, initIndy) = (40, 30)
        indicator1 = Indicator1(initIndx, initIndy)
        self.indicator1Group = pygame.sprite.GroupSingle(indicator1)  
        Indicator2.init()
        (initIndx, initIndy) = (150, 30)
        indicator2 = Indicator2(initIndx, initIndy)
        self.indicator2Group = pygame.sprite.GroupSingle(indicator2)      
        #indicator
        Indicator1.init("energy")
        (initIndx, initIndy) = (40, 90)
        indicator3 = Indicator1(initIndx, initIndy)
        self.indicator3Group = pygame.sprite.GroupSingle(indicator3)  
        Indicator2.init()
        (initIndx, initIndy) = (150, 90)
        indicator4 = Indicator2(initIndx, initIndy)
        self.indicator4Group = pygame.sprite.GroupSingle(indicator4)    
        
        #for silk attach and time-counting
        #self.attach = False #*this canbe move to silk
        self.moveright, self.moveleft = False, False
        self.highest = 0
        self.timeOnScreen = 0 #*this canbe move to silk
        #game state flag
        self.Timecnt = 3
        self.Gamewin = False
        # self.Gamelose = False
        #scroll
        self.scrollflg = False
        self.scrollvx = 0
        self.scrollvy = 0
        #mouse
        self.mPress = False
        #score and time
        self.score = 0
        self.time = 0
        self.speedtime = 50
        self.frozetime = 50
        self.speedcnt = self.speedtime
        self.frozecnt = self.frozetime

    def keyPressed(self, code, mod):
        if code == pygame.K_SPACE:
            spider = self.spiderGroup.sprites()[0]
            self.probes.add(Probe(spider.x, spider.y, spider.angle1))
            self.spiderGroup.sprite.attach = False   
            self.moveright, self.moveleft = False, False      
            self.timeOnScreen = 0
            
    def mousePressed(self, x, y):        
        spider = self.spiderGroup.sprites()[0]
        fullAng, halfAng = 180, 90
        angle = (math.atan2((x-spider.x),(y-spider.y))/math.pi)*fullAng-halfAng

        self.probes.add(Probe(spider.x, spider.y, angle))
        self.spiderGroup.sprite.attach = False     
        self.moveright, self.moveleft = False, False 
        self.timeOnScreen = 0
        self.mPress = True
        
    def mouseReleased(self, x, y):
        self.mPress = False
        
        
    def timerFired(self, dt, screen):
        self.timeOnScreen += 1
        if self.timeOnScreen%50 == 0 and self.Timecnt != 0:
            self.Timecnt -= 1
            print(self.Timecnt)
        if self.Timecnt == 0:
            if (not self.Gamewin) and (not self.Gamelose):
                self.playfunc(self, screen)

    @staticmethod
    def playfunc(self, screen):
        #make alias 
        spider = self.spiderGroup.sprite
        silk = self.silkGroup.sprite
        #time count
        if self.timeOnScreen > silk.time:
            self.spiderGroup.sprite.angle1 = 0
            spider.angle = 0
            self.spiderGroup.sprite.attach = False
            self.moveright, self.moveleft = False, False
            self.timeOnScreen = 0
        #get x0,y0,x1,y1, and the angle of silk
        self.silkGroup.sprite.x0 = spider.x
        self.silkGroup.sprite.y0 = spider.y
        (x0, y0) = (silk.x0, silk.y0)
        (x1, y1) = (silk.x1, silk.y1)
        fullAng, halfAng, deltaAng = 180, 90, 90
        angle = (math.atan2((x1-x0),(y1-y0))/math.pi)*fullAng
        
        #detect if collide happend between probe and grapple
        for grapple in pygame.sprite.groupcollide(
            self.grapples, self.probes, False, False,
            pygame.sprite.collide_circle):
            self.silkGroup.sprite.x1 = grapple.x
            self.silkGroup.sprite.y1 = grapple.y
            (x1, y1) = (silk.x1, silk.y1)
            angle = (math.atan2((x1-x0),(y1-y0))/math.pi)*fullAng
            if self.frozecnt == self.frozetime:
                self.spiderGroup.sprite.attach = True
            if spider.vx >= 0: self.moveright = True
            if spider.vx <  0: self.moveleft  = True
            self.highest = y0
            self.probes.empty()
        
        #when not attached, just falling down
        if not spider.attach:
            self.silkGroup.sprite.x1 = x0
            self.silkGroup.sprite.y1 = y0 
            self.spiderGroup.sprite.angle1 = 0
            spider.angle = 0
        # when silk is attached, change spider move direction
        elif (angle < -halfAng or angle > halfAng):# and y0 >= self.highest:
            spider.angle = angle - 180
            if self.moveright:  self.spiderGroup.sprite.angle1 = angle-deltaAng
            elif self.moveleft: self.spiderGroup.sprite.angle1 = angle+deltaAng
            else: self.spiderGroup.sprite.angle1 = 0
        else:
            self.spiderGroup.sprite.angle1 = 0
            spider.angle = 0
            self.spiderGroup.sprite.attach = False     
            self.moveright, self.moveleft = False, False 
            self.timeOnScreen = 0


        #detect bonus
        self.detectbonus(self)
        self.detecthazard(self)
        
        if self.speedcnt == self.speedtime and self.frozecnt == self.frozetime:
            self.frozecnt = self.frozetime
            self.spiderGroup.sprite.power = 0.5
            self.spiderGroup.sprite.maxSpeed = 10
            # in water speed down
            if spider.y > self.height *3/4:
                spider.maxSpeed = 2
        elif self.speedcnt < self.speedtime:
            self.speedcnt += 1
        elif self.frozecnt < self.frozetime:
            self.frozecnt += 1

        
        #detect if collide happend between spider and home
        if (pygame.sprite.groupcollide(self.homeGroup, self.spiderGroup, 
            False, False, pygame.sprite.collide_circle)):
            self.Gamewin = True
            self.GameStart = True

        #scroll grapples and net
        self.scrolling(self)

        if self.frozecnt < self.frozetime:
            self.frozenGroup.add(Frozen(spider.x, spider.y))
        else:
            self.frozenGroup.empty()
            
        #update all objects     
        self.spiderGroup.update(self.isKeyPressed,self.width,self.height,self.scrollvx)
        self.grapples.update(self.width, self.height)
        self.bonuses2.update(self.width, self.height)
        self.hazardices.update(self.width, self.height)
        self.tracks.update(self.width, self.height)
        self.probes.update(self.width, self.height)
        self.silkGroup.update(self.width, self.height)
        self.riverGroup.update(self.width, self.height)
        self.homeGroup.update(self.width, self.height)
        self.frozenGroup.update(self.width, self.height)
        self.indicator1Group.update(self.width, self.height)
        self.indicator2Group.update(self.width, self.height)
        self.indicator3Group.update(self.width, self.height)
        self.indicator4Group.update(self.width, self.height)


        #shrink
        if self.mPress and spider.attach:
            step = 3
            spider.y -= step
            if spider.y > self.height *3/4:
                spider.y += 1.5
        elif spider.attach:
            spider.y += 1
        #add track 
        if self.timeOnScreen%5 == 0:
            self.tracks.add(Track(spider.x, spider.y))
            self.time += 1;
        #detect boundary
        if spider.y <= 30:
            spider.y = 30
        if spider.y >= self.height - 30:
            spider.y = self.height - 30
            
    @staticmethod
    def detectbonus(self):
        #detect if collide happend between spider and bonuses2
        for bonus2 in pygame.sprite.groupcollide(
            self.spiderGroup, self.bonuses2, False, True,
            pygame.sprite.collide_circle):
            self.spiderGroup.sprite.power = 0
            self.spiderGroup.sprite.maxSpeed = 20
            self.spiderGroup.sprite.velocity = (18, -2)
            self.spiderGroup.sprite.attach = False
            self.speedcnt = 0
            
    @staticmethod
    def detecthazard(self):
        #detect if collide happend between spider and hazardices
        for hazardice in pygame.sprite.groupcollide(
            self.spiderGroup, self.hazardices, False, True,
            pygame.sprite.collide_circle):
            if self.speedcnt == self.speedtime:
                self.spiderGroup.sprite.power = 0
                self.spiderGroup.sprite.maxSpeed = 0
                self.spiderGroup.sprite.velocity = (0, 0)
                self.spiderGroup.sprite.attach = False
                self.frozecnt = 0
        #detect if collide happend between spider and river
        if self.spiderGroup.sprite.y > self.height *3/4:
            self.energ -= 0.2    
            self.spiderGroup.sprite.init("red")
        else:
            self.spiderGroup.sprite.init("orange")
            
    @staticmethod
    def scrolling(self):
        #scroll grapples and net
        if self.spiderGroup.sprite.x >= self.width//2:
            if self.spiderGroup.sprite.maxSpeed == 20:
                self.scrollvx = 18
            else:
                self.scrollvx = self.spiderGroup.sprite.vxtmp

            # self.spiderGroup.sprite.velocity = (0, self.scrollvy)
            self.silkGroup.sprite.x1 -= self.scrollvx
            for grapple in self.grapples.sprites():
                grapple.x -= self.scrollvx  
            for bonus2 in self.bonuses2.sprites():
                bonus2.x -= self.scrollvx           
            for hazardice in self.hazardices.sprites():
                hazardice.x -= self.scrollvx            
            for track in self.tracks.sprites():
                track.x -= self.scrollvx  
            self.homeGroup.sprite.x -= self.scrollvx  
            self.riverGroup.sprite.x-= self.scrollvx


    def redrawAll(self, screen):
        
        self.bonuses2.draw(screen)
        self.hazardices.draw(screen)
        self.grapples.draw(screen)
        self.tracks.draw(screen)
        self.probes.draw(screen)
        self.homeGroup.draw(screen)
        self.silkGroup.draw(screen)
        self.spiderGroup.draw(screen)
        self.riverGroup.draw(screen)
        self.frozenGroup.draw(screen)
        
        #display energy
        if self.energ >=100: self.energ = 100
        if self.energ <=  0: self.energ = 0; self.Gamelose = True
        score2 = (self.energ)/102
        image2 = pygame.Surface((300, 100), pygame.SRCALPHA)
        pygame.draw.line(image2, (255, 0, 0), (80, 90), (140*score2+82, 90), 20)
        screen.blit(image2, (0, 0))
        
        #display score
        score = (self.time)/600
        image = pygame.Surface((300, 70), pygame.SRCALPHA)
        pygame.draw.line(image, (255, 165, 0), (80, 30), (140*score+82, 30), 20)
        self.score = self.time
        screen.blit(image, (0, 0))

        self.indicator1Group.draw(screen)
        self.indicator2Group.draw(screen)
        self.indicator3Group.draw(screen)
        self.indicator4Group.draw(screen)
        
        #display Timecnt
        if self.Timecnt != 0:
            my_font = pygame.font.SysFont("comicsansms", 86)
            txt = str(self.Timecnt)
            text_surface = my_font.render(txt, True, (255,0,0))
            screen.blit(text_surface, (self.width//2, self.height//2))
        
        #display gameover
        if self.Gamewin:
            my_font = pygame.font.SysFont("arial", 56)
            text_surface = my_font.render("Cool! you win", True, (0,0,0))
            screen.blit(text_surface, (self.width//2, self.height//2))
        if self.Gamelose or self.Timecnt >= 1200:
            my_font = pygame.font.SysFont("arial", 56)
            text_surface = my_font.render("Pity! you lose", True, (0,0,0))
            screen.blit(text_surface, (self.width//2, self.height//2))

