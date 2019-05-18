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
        pygame.draw.line(Silk.silkImage, (255, 255, 255), (30, screenHeight//3), (30,0), size)
            
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
    def init():
        (scale0, scale1) = (100, 100)
        Spider.shipImage = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/spider.png').convert_alpha(),
            (scale0, scale1)), 0)

    def __init__(self, x, y):
        super(Spider, self).__init__(x, y, Spider.shipImage, 30)
        self.power = 0.5
        self.angleSpeed = 5
        self.angle = 0  # starts pointing straight up
        self.maxSpeed = 10
        self.attach = False
        self.speed = 0
        self.attchflg = False
        self.vxtmp = 0
        self.vytmp = 0
        self.vx = 0;
        self.vy = 0
        self.hit = False

    def update(self, keysDown, screenWidth, screenHeight, scrollx, scrolly):
        #control movement by Keyboard
        if keysDown(pygame.K_LEFT):
            self.angle += self.angleSpeed
        if keysDown(pygame.K_RIGHT):
            self.angle -= self.angleSpeed
        #non-uniform motion
        self.accmotion(self.power, scrollx, scrolly)
        #update rect-coordinate
        super(Spider, self).update(screenWidth, screenHeight)

    def accmotion(self, power, scrollx, scrolly): #accelerated (non-uniform) motion
        angle = math.radians(self.angle)
        vx, vy = self.velocity
        if scrollx != 0: vx = scrollx
        if scrolly != 0: vy = scrolly
        if self.hit: 
            self.hit = False
            if vx >= 0: vx = -10; vy = -10
            else: vx = 10; vy = -10

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
        self.vytmp = vy
        if scrollx == 0 and scrolly == 0: self.velocity = (vx, vy)
        elif scrolly == 0: self.velocity = (0, vy)
        elif scrollx == 0: self.velocity = (vx, 0)
        else: self.velocity = (0, 0)
        (self.vx, self.vy) = (vx, vy)


class Grapple(GameObject):
    @staticmethod
    def init():
        image = pygame.image.load('images/gem.png').convert_alpha()
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

    (minSize, maxSize) = (5, 6)

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

class GameState3(PygameGame):
    @staticmethod
    def bonuhazdinit(self):
        #bonuses1
        Bonus1.init()
        self.bonuses1 = pygame.sprite.Group()
        b1num = 10
        for i in range(b1num):
            x = random.randint(i*(self.width*4//b1num),(i+1)*(self.width*4//b1num))
            y = random.randint(self.height//4, self.height)
            self.bonuses1.add(Bonus1(x, y))
        #bonuses2
        Bonus2.init()
        self.bonuses2 = pygame.sprite.Group()
        b2num = 0
        for i in range(b2num):
            x = random.randint(i*(self.width*4//b2num),(i+1)*(self.width*4//b2num))
            y = random.randint(self.height//4, self.height)
            self.bonuses2.add(Bonus2(x, y))
        #bonuses3
        Bonus3.init()
        self.bonuses3 = pygame.sprite.Group()
        b3num = 5
        for i in range(b3num):
            x = random.randint(i*(self.width*4//b3num),(i+1)*(self.width*4//b3num))
            y = random.randint(self.height//4, self.height)
            self.bonuses3.add(Bonus3(x, y))
        #hazardcone
        Hazardcone1.init()
        Hazardcone2.init()
        Hazardcone3.init()
        self.hazardcones = pygame.sprite.Group()
        x = self.width
        y = 800
        self.hazardcones.add(Hazardcone1(x, y))
        x = self.width//2 * 3 + 20
        y = 250      
        self.hazardcones.add(Hazardcone2(x, y))
        x = self.width*2 + 200
        y = 800
        self.hazardcones.add(Hazardcone1(x, y))
        x = self.width
        y = 900
        self.hazardcones.add(Hazardcone3(x, y))
        x = self.width//2 * 3 + 20
        y = 520    
        self.hazardcones.add(Hazardcone3(x, y))
        x = self.width//2 * 3 + 20
        y = 420    
        self.hazardcones.add(Hazardcone3(x, y))
        x = self.width*2 + 200
        y = 900
        self.hazardcones.add(Hazardcone3(x, y))
        #hazardice
        Hazardice.init("fire")
        self.hazardices = pygame.sprite.Group()
        h2num = 10
        for i in range(h2num):
            x = random.randint(i*(self.width*4//h2num),(i+1)*(self.width*4//h2num))
            y = random.randint(self.height//4, self.height)
            self.hazardices.add(Hazardice(x, y))
        #hazardlava
        Hazardlava.init()
        self.hazardlavas = pygame.sprite.Group()
        x = self.width*3//2
        y = 1000
        self.hazardlavas.add(Hazardlava(x, y))
        #hazardrock
        Hazardrock.init()
        self.hazardrocks = pygame.sprite.Group()
        x = self.width-25
        y = 10
        self.hazardrocks.add(Hazardrock(x, y))
        
    def init(self):
        self.bgColor = (238, 154, 73)
        #spiderGroup
        Spider.init()
        (initSpx, initSpy) = (30, 30)
        spider = Spider(initSpx, self.height//3)
        self.spiderGroup = pygame.sprite.GroupSingle(spider)
        #grapples
        Grapple.init()
        self.grapples = pygame.sprite.Group()
        gnum = 16
        xylist1 = [[255, 123], [371, 43], [579, 125], [678, 323], \
                    [809, 137], [972, 102], [1600, 78], \
                    [1870, 291], [1974, 143], [2151, 125], [2277, 321], \
                    [2433, 209], [2607, 124], [2790, 433], [3035, 142], [3062, 268]]
        xylist2 = [[120, 235], [262, 530], [433, 490],\
                    [550, 400], [745, 553], [879, 350], [1026, 533],\
                    [1101, 500], [1100, 226], [1400, 223], [1424, 550], [1575, 420],\
                    [1633, 376], [1729, 168], [2101, 593], \
                    [2243, 652], [2500, 595], [2490, 330], [2630, 383], \
                    [2659, 179], [2838, 333], [2933, 439], [2999, 265], [3134, 530]]
        for i in range(gnum):
            x = xylist1[i][0]
            y = xylist1[i][1]
            self.grapples.add(Grapple(x, y))
        gnum = 24
        for i in range(gnum):
            x = xylist2[i][0]
            y = xylist2[i][1]
            self.grapples.add(Grapple(x, y))
        self.grapples.add(Grapple(30, 0))
        #probes
        self.probes = pygame.sprite.Group()
        self.probes.add(Probe(30, 0, 0))
        #silkGroup
        Silk.init(self.width, self.height)
        silk = Silk(self.width//2, self.height//2)
        self.silkGroup = pygame.sprite.GroupSingle(silk)
        #tracks
        Track.init()
        self.tracks = pygame.sprite.Group()
        #bonus and hazard init
        self.bonuhazdinit(self)
        #home
        Home.init()
        (initHmx, initHmy) = (100, 100)
        home = Home(self.width*3-initHmx, self.height-initHmy)
        self.homeGroup = pygame.sprite.GroupSingle(home)
        #indicator
        Indicator1.init("energy")
        (initIndx, initIndy) = (40, 30)
        indicator1 = Indicator1(initIndx, initIndy)
        self.indicator1Group = pygame.sprite.GroupSingle(indicator1)  
        Indicator2.init()
        (initIndx, initIndy) = (150, 30)
        indicator2 = Indicator2(initIndx, initIndy)
        self.indicator2Group = pygame.sprite.GroupSingle(indicator2)    
        #for silk attach and time-counting
        #self.attach = False #*this canbe move to silk
        self.moveright, self.moveleft = False, False
        self.highest = 0
        self.timeOnScreen = 0 #*this canbe move to silk
        #game state flag
        self.Timecnt = 3
        self.Gamewin = False
        # self.Gamelose = False
        self.hitcnt = 0
        #scroll
        self.scrollflg = False
        self.scrollvx = 0
        self.scrollvy = 0
        #mouse
        self.mPress = False
        #score and time
        self.score = 0
        self.time = 0
        #scroll
        self.scrollx = 0
        self.scrolly = 0

    def keyPressed(self, code, mod):
        if code == pygame.K_SPACE:
            spider = self.spiderGroup.sprites()[0]
            self.probes.add(Probe(spider.x, spider.y, spider.angle))
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
        # print(x,y, angle)
        self.mPress = True
        
    def mouseReleased(self, x, y):
        self.mPress = False
        
        
    def timerFired(self, dt, screen):
        self.timeOnScreen += 1
        if self.timeOnScreen%50 == 0 and self.Timecnt != 0:
            self.Timecnt -= 1
            # print(self.Timecnt)
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
            self.spiderGroup.sprite.angle = 0
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
            self.spiderGroup.sprite.attach = True
            if spider.vx >= 0: self.moveright = True
            if spider.vx <  0: self.moveleft  = True
            self.highest = y0
            # print(y0)
            self.probes.empty()
        
        #when not attached, just falling down
        if not spider.attach:
            self.silkGroup.sprite.x1 = x0
            self.silkGroup.sprite.y1 = y0 
            self.spiderGroup.sprite.angle = 0
        # when silk is attached, change spider move direction
        elif (angle < -halfAng or angle > halfAng):# and y0 >= self.highest:
            if self.moveright:  self.spiderGroup.sprite.angle = angle-deltaAng
            elif self.moveleft: self.spiderGroup.sprite.angle = angle+deltaAng
            else: self.spiderGroup.sprite.angle = 0
        else:
            self.spiderGroup.sprite.angle = 0
            self.spiderGroup.sprite.attach = False     
            self.moveright, self.moveleft = False, False 
            self.timeOnScreen = 0

        # shrink 
        if self.mPress and spider.attach:
            step = 3
            self.spiderGroup.sprite.y -= step   
        elif spider.attach:
            self.spiderGroup.sprite.y += 1   
            
        # scroll y axis    
        if self.spiderGroup.sprite.y >= self.scrolly + self.height//4*3:
            self.scrolly = self.spiderGroup.sprite.y - self.height//4*3
            self.spiderGroup.sprite.y -= self.scrolly
        if self.spiderGroup.sprite.y <= self.scrolly + self.height//3:
            self.scrolly = self.spiderGroup.sprite.y - self.height//3
            self.spiderGroup.sprite.y -= self.scrolly

        #scroll grapples and net
        self.scrolling(self)
        
        #detect bonus
        self.detectbonus(self)
        #detect hazard
        self.detecthazard(self)
        #detect if collide happend between spider and home
        if (pygame.sprite.groupcollide(self.homeGroup, self.spiderGroup, 
            False, False, pygame.sprite.collide_circle)):
            self.Gamewin = True
            self.GameStart = True

        #update all objects     
        self.spiderGroup.update(self.isKeyPressed,self.width,self.height,self.scrollvx, self.scrollvy)
        self.grapples.update(self.width, self.height)
        self.bonuses1.update(self.width, self.height)
        self.bonuses2.update(self.width, self.height)
        self.bonuses3.update(self.width, self.height)
        self.hazardcones.update(self.width, self.height)
        self.hazardices.update(self.width, self.height)
        self.hazardlavas.update(self.width, self.height)
        self.hazardrocks.update(self.width, self.height)
        self.tracks.update(self.width, self.height)
        self.probes.update(self.width, self.height)
        self.silkGroup.update(self.width, self.height)
        self.homeGroup.update(self.width, self.height)
        self.indicator1Group.update(self.width, self.height)
        self.indicator2Group.update(self.width, self.height)
        
        #add track 
        if self.timeOnScreen%5 == 0:
            self.tracks.add(Track(spider.x, spider.y))
            self.time += 1;
            
        #detect boundary
        if spider.y >= self.hazardlavas.sprites()[0].y - 30:
            spider.y = self.hazardlavas.sprites()[0].y - 30
            self.Gamelose = True
        
        if self.hitcnt > 0: self.hitcnt -= 1
    @staticmethod
    def detectbonus(self):
        #detect if collide happend between spider and bonuses1
        for bonus1 in pygame.sprite.groupcollide(
            self.spiderGroup, self.bonuses1, False, True,
            pygame.sprite.collide_circle):
            # print(y0)
            self.energ += 5
        #detect if collide happend between spider and bonuses2
        for bonus2 in pygame.sprite.groupcollide(
            self.spiderGroup, self.bonuses2, False, True,
            pygame.sprite.collide_circle):
            # print(y0)
            self.energ += 10
        #detect if collide happend between spider and bonuses3
        for bonus3 in pygame.sprite.groupcollide(
            self.spiderGroup, self.bonuses3, False, True,
            pygame.sprite.collide_circle):
            # print(y0)
            self.energ += 15
            
    @staticmethod
    def detecthazard(self):
        #detect if collide happend between spider and hazardcones
        for hazardcone in pygame.sprite.groupcollide(
            self.spiderGroup, self.hazardcones, False, False,
            pygame.sprite.collide_circle):
            # print(y0)
            # self.Gamelose = True
            if self.hitcnt <= 0:
                self.energ -= 40
                print("hit", self.energ)
                self.spiderGroup.sprite.hit = True
                self.spiderGroup.sprite.attach = False
                self.hitcnt = 25
        #detect if collide happend between spider and hazardices
        for hazardice in pygame.sprite.groupcollide(
            self.spiderGroup, self.hazardices, False, True,
            pygame.sprite.collide_circle):
            # print(y0)
            self.energ -= 5

    @staticmethod
    def scrolling(self):
        #scroll grapples and net
        if self.spiderGroup.sprite.x >= self.width//2:
            # (self.scrollvx, self.scrollvy) = self.spiderGroup.sprite.velocity
            self.scrollvx = self.spiderGroup.sprite.vxtmp
            self.scrollflg = True
            # self.spiderGroup.sprite.velocity = (0, self.scrollvy)
            self.silkGroup.sprite.x1 -= self.scrollvx
            for grapple in self.grapples.sprites():
                grapple.x -= self.scrollvx
            for bonus1 in self.bonuses1.sprites():
                bonus1.x -= self.scrollvx     
            for bonus2 in self.bonuses2.sprites():
                bonus2.x -= self.scrollvx     
            for bonus3 in self.bonuses3.sprites():
                bonus3.x -= self.scrollvx      
            for hazardcone in self.hazardcones.sprites():
                hazardcone.x -= self.scrollvx    
            for hazardice in self.hazardices.sprites():
                hazardice.x -= self.scrollvx    
            for hazardlava in self.hazardlavas.sprites():
                hazardlava.x -= self.scrollvx
            for hazardrock in self.hazardrocks.sprites():
                hazardrock.x -= self.scrollvx
            for track in self.tracks.sprites():
                track.x -= self.scrollvx  
            self.homeGroup.sprite.x -= self.scrollvx  
        else: self.scrollflg = False


        
        self.silkGroup.sprite.y1 -= self.scrolly
        for grapple in self.grapples.sprites():
            grapple.y -= self.scrolly
        for bonus1 in self.bonuses1.sprites():
            bonus1.y -= self.scrolly
        for bonus2 in self.bonuses2.sprites():
            bonus2.y -= self.scrolly
        for bonus3 in self.bonuses3.sprites():
            bonus3.y -= self.scrolly
        for hazardcone in self.hazardcones.sprites():
            hazardcone.y -= self.scrolly
        for hazardice in self.hazardices.sprites():
            hazardice.y -= self.scrolly
        for hazardlava in self.hazardlavas.sprites():
            hazardlava.y -= self.scrolly
        for hazardrock in self.hazardrocks.sprites():
            hazardrock.y -= self.scrolly
        for track in self.tracks.sprites():
            track.y -= self.scrolly
        self.homeGroup.sprite.y -= self.scrolly
        self.scrolly = 0


    def redrawAll(self, screen):
        self.bonuses1.draw(screen)
        self.bonuses2.draw(screen)
        self.bonuses3.draw(screen)
        self.hazardcones.draw(screen)
        self.hazardices.draw(screen)
        self.hazardlavas.draw(screen)
        self.hazardrocks.draw(screen)
        self.grapples.draw(screen)
        # self.tracks.draw(screen)
        self.probes.draw(screen)
        self.homeGroup.draw(screen)
        self.silkGroup.draw(screen)
        self.spiderGroup.draw(screen)
        self.indicator1Group.draw(screen)
        self.indicator2Group.draw(screen)
        #display score
        # score = (self.score*3 + 20)/50
        # if self.score*3 + 20 <= 0: self.score = -20/3
        if self.energ >=100: self.energ = 100
        if self.energ <=  0: self.energ = 0; self.Gamelose = True
        score = (self.energ)/102
        image = pygame.Surface((300, 70), pygame.SRCALPHA)
        pygame.draw.line(image, (255, 0, 0), (80, 30), (140*score+82, 30), 20)
        screen.blit(image, (0, 0))
        self.indicator1Group.draw(screen)
        self.indicator2Group.draw(screen)
        # print(140*score+82)
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
        if self.Gamelose:
            my_font = pygame.font.SysFont("arial", 56)
            text_surface = my_font.render("Pity! you lose", True, (0,0,0))
            screen.blit(text_surface, (self.width//2, self.height//2))

