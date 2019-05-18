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

class Wheel(GameObject):
    angleSpeed = 0
    # anglePower = random.randint(0, 10)
    anglePower = 0.2
    maxangleSpeed = 5
    def init():
        Wheel.image = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/wheel.png').convert_alpha(),
            (400, 400)), 0)
    
    def __init__(self, x, y):
        super(Wheel, self).__init__(x, y, Wheel.image, 30)
        
    def update(self, screenWidth, screenHeight):
        self.angleSpeed += self.anglePower
        self.angle -= self.angleSpeed
        if self.angleSpeed > self.maxangleSpeed: self.angleSpeed = self.maxangleSpeed
        super(Wheel, self).update(screenWidth, screenHeight)
        
class Silk(GameObject):
    time = 50 * 55
    size = 5
    x0, y0 = 30, 200
    x1, y1 = 30, 0
    def init(screenWidth,screenHeight):
        size = Silk.size
        Silk.silkImage = pygame.Surface((screenWidth, screenHeight), pygame.SRCALPHA)
        pygame.draw.line(Silk.silkImage, (255, 255, 255), (450, 300), (300,300), size)
            
    def __init__(self, x, y):
        super(Silk, self).__init__(x, y, Silk.silkImage, self.size)

    def update(self, screenWidth, screenHeight):
        self.image = pygame.Surface((screenWidth,screenHeight), pygame.SRCALPHA)
        pygame.draw.line(self.image, (255, 255, 255), (self.x0, self.y0), \
                        (self.x1, self.y1), self.size)
        

class Cloud(GameObject):
    @staticmethod
    def init():
        image = pygame.image.load('images/clouds.png').convert_alpha()
        rows, cols = 4, 4
        width, height = image.get_size()
        cellWidth, cellHeight = width / cols, height / rows
        Cloud.images = []
        #read clouds one by one
        for i in range(rows):
            for j in range(cols):
                subImage = image.subsurface(
                    (i * cellWidth, j * cellHeight, cellWidth, cellHeight))
                Cloud.images.append(subImage)

    (minSize, maxSize) = (5, 6)

    def __init__(self, x, y, level=None):
        if level is None:
            level = random.randint(Cloud.minSize, Cloud.maxSize)
        self.level = level
        factor = self.level / Cloud.maxSize
        image = random.choice(Cloud.images)
        w, h = image.get_size()
        #set size of cloud
        image = pygame.transform.scale(image, (int(w*factor), int(h*factor)))
        super(Cloud, self).__init__(x, y, image, w / 2 * factor)
        
    def update(self, screenWidth, screenHeight):
        super(Cloud, self).update(screenWidth*4, screenHeight)
        
            
class Spider(GameObject):
    # we only need to load the image once, not for every spider we make!
    #   granted, there's probably only one spider...
    @staticmethod
    def init(select):
        (scale0, scale1) = (100, 100)
        if select == "orange90":
            Spider.spiderImage = pygame.transform.rotate(pygame.transform.scale(
                pygame.image.load('images/spider.png').convert_alpha(),
                (scale0, scale1)), 90)
        elif select == "orange":
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
        self.wheelAttach = True
        self.attach = False
        self.speed = 0
        self.attchflg = False
        self.vxtmp = 0
        self.vx = 0;
        self.vy = 0
        self.angle1 = 0

    def update(self, keysDown, screenWidth, screenHeight, scrollx, scrolly):
        #control movement by Keyboard
        if keysDown(pygame.K_LEFT):
            self.angle += self.angleSpeed
        if keysDown(pygame.K_RIGHT):
            self.angle -= self.angleSpeed
        #non-uniform motion
        self.accmotion(self.power, scrollx, scrolly)
        #update rect-coordinate
        self.baseImage = Spider.spiderImage.copy() 
        super(Spider, self).update(screenWidth, screenHeight)

    def accmotion(self, power, scrollx, scrolly): #accelerated (non-uniform) motion
        angle = math.radians(self.angle1)
        vx, vy = self.velocity
        if scrollx != 0: vx = scrollx
        if scrolly != 0: vy = scrolly

        if self.wheelAttach:
            vx, vy = 0, 0
            self.x = 150*math.cos(angle) + 300
            self.y = 150*math.sin(angle) + 300
        elif self.attach:
            vx = vx * math.sin(angle) * math.sin(angle) + vy * math.cos(angle) \
                    * math.sin(angle) + power * math.cos(angle) *math.sin(angle)
            vy = vx * math.cos(angle) * math.sin(angle) + vy * math.cos(angle) \
                    * math.cos(angle) + power * math.cos(angle) *math.cos(angle)
        else:
            self.attchflg = False
            vx += power * math.sin(angle)
            vy += power * math.cos(angle)
            if vy > 60: vy = 60
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

class Track(GameObject):
    @staticmethod
    def init():
        image = pygame.image.load('images/track.png').convert_alpha()
        width, height = image.get_size()
        Track.images = []
        num = 1
        #read clouds one by one
        for i in range(num):
                subImage = image.subsurface((0, 0, width, height))
                Track.images.append(subImage)

    def __init__(self, x, y, level=None):
        factor = 0.5
        image = random.choice(Track.images)
        w, h = image.get_size()
        #set size of cloud
        image = pygame.transform.scale(image, (int(w*factor), int(h*factor)))
        super(Track, self).__init__(x, y, image, w / 2 * factor)
        
    def update(self, screenWidth, screenHeight):
        super(Track, self).update(screenWidth*4, screenHeight)    
  
class Grass(GameObject):
    @staticmethod
    def init():
        (scale0, scale1) = (9000, 500)
        Grass.grassImage = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/longgrass.png').convert_alpha(),
            (scale0, scale1)), 0)

    def __init__(self, x, y):
        super(Grass, self).__init__(x, y, Grass.grassImage, 30)

    def update(self, screenWidth, screenHeight):
        super(Grass, self).update(screenWidth*5, screenHeight)

class Umbrella(GameObject):
    @staticmethod
    def init():
        (scale0, scale1) = (70, 70)
        Umbrella.umbrellaImage = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/umbrella.png').convert_alpha(),
            (scale0, scale1)), 0)

    def __init__(self, x, y):
        super(Umbrella, self).__init__(x, y, Umbrella.umbrellaImage, 30)

    def update(self, screenWidth, screenHeight):
        super(Umbrella, self).update(screenWidth*4, screenHeight)
        
class GameState2(PygameGame):
        
    def init(self):
        self.bgColor = (200, 200, 200)
        #wheel
        Wheel.init()
        self.wheelGroup = pygame.sprite.GroupSingle(Wheel(300,300))
        #spiderGroup
        Spider.init("orange90")
        (initSpx, initSpy) = (450, 300)
        spider = Spider(initSpx, initSpy)
        self.spiderGroup = pygame.sprite.GroupSingle(spider)
        #clouds
        Cloud.init()
        self.clouds = pygame.sprite.Group()
        gnum = 10
        for i in range(gnum):
            x = random.randint(i*(self.width*10//gnum),(i+1)*(self.width*10//gnum))
            y = random.randint(-self.height*4, -self.height*3)
            self.clouds.add(Cloud(x, y))
        gnum = 20
        for i in range(gnum):
            x = random.randint(i*(self.width*10//gnum),(i+1)*(self.width*10//gnum))
            y = random.randint(-self.height*3, -self.height*2)
            self.clouds.add(Cloud(x, y))
        gnum = 70
        for i in range(gnum):
            x = random.randint(i*(self.width*10//gnum),(i+1)*(self.width*10//gnum))
            y = random.randint(-self.height*2, self.height//4)
            self.clouds.add(Cloud(x, y))
        #silkGroup
        Silk.init(self.width, self.height)
        silk = Silk(self.width//2, self.height//2)
        self.silkGroup = pygame.sprite.GroupSingle(silk)
        #tracks
        Track.init()
        self.tracks = pygame.sprite.Group()
        #grass
        Grass.init()
        grass = Grass(self.width*4, self.height * 0.9)
        self.grassGroup = pygame.sprite.GroupSingle(grass)
        #umbrella
        Umbrella.init()
        (initUmx, initUmy) = (0, 0)
        umbrella = Umbrella(initUmx, initUmy)
        self.umbrellaGroup = pygame.sprite.GroupSingle(umbrella)
        #indicator
        Indicator1.init("distance")
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
        self.Timecnt2= 2
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
        #scroll
        self.scrollx = 0
        self.scrolly = 0
        #umbrella flag
        self.umbrellaFlg = False

            
    def mousePressed(self, x, y):     
        spider = self.spiderGroup.sprites()[0]
        if self.Timecnt <= 0:
            if spider.wheelAttach:
                spider.wheelAttach = False
                angle = math.radians(self.wheelGroup.sprite.angle)
                spider.vx = 10*self.wheelGroup.sprite.angleSpeed* math.sin(angle)
                spider.vy = 10*self.wheelGroup.sprite.angleSpeed* math.cos(angle)
                spider.velocity = (spider.vx, spider.vy)
                print(self.wheelGroup.sprite.angle)
                print(spider.velocity)
                self.silkGroup.empty()
            else: #if abs(x-spider.x)<30 and abs(y-spider.y)<20:
                self.umbrellaFlg = True
        
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
        
        #when not attached, just falling down
        if not spider.attach:
            # self.silkGroup.sprite.x1 = x0
            # self.silkGroup.sprite.y1 = y0 
            self.spiderGroup.sprite.angle1 = 0
            spider.angle = 0
        
        
        # when attach to the wheel
        if spider.wheelAttach:
            spider.angle = self.wheelGroup.sprite.angle
            spider.angle1 = -self.wheelGroup.sprite.angle
            silk.x0, silk.y0 = spider.x, spider.y
            silk.x1, silk.y1 = 300, 300
        else:
            spider.init("orange")
        # when open umbrella
        if self.umbrellaFlg:
            if spider.maxSpeed >= 50:
                spider.maxSpeed -= 5
            elif spider.maxSpeed >= 20:
                spider.maxSpeed -= 2
            elif spider.maxSpeed >= 5:
                spider.maxSpeed -= 1


        # scroll y axis 
        if self.spiderGroup.sprite.y >= self.scrolly + self.height//4*3:
            self.scrolly = self.spiderGroup.sprite.y - self.height//4*3
            self.spiderGroup.sprite.y -= self.scrolly
        if self.spiderGroup.sprite.y <= self.scrolly + self.height//4:
            self.scrolly = self.spiderGroup.sprite.y - self.height//4
            self.spiderGroup.sprite.y -= self.scrolly
        #scroll clouds and net
        self.scrolling(self)
        
        #update all objects     
        self.wheelGroup.update(self.width, self.height)
        self.spiderGroup.update(self.isKeyPressed,self.width,self.height,self.scrollvx, self.scrollvy)
        self.tracks.update(self.width, self.height)
        self.clouds.update(self.width, self.height)
        self.silkGroup.update(self.width, self.height)
        self.grassGroup.update(self.width, self.height)
        #umbrella 
        self.umbrellaGroup.sprite.x = spider.x - 30
        self.umbrellaGroup.sprite.y = spider.y - 20
        if self.umbrellaFlg:
            self.umbrellaGroup.update(self.width, self.height)
        self.indicator1Group.update(self.width, self.height)
        self.indicator2Group.update(self.width, self.height)
        self.indicator3Group.update(self.width, self.height)
        self.indicator4Group.update(self.width, self.height)


        #shrink
        if self.mPress and spider.attach:
            step = 3
            spider.y -= step
        elif spider.attach:
            spider.y += 1
        #add track 
        if self.timeOnScreen%5 == 0:
            self.tracks.add(Track(spider.x, spider.y))
            self.time += 1;
        #detect boundary
        if spider.y <= 60:
            spider.y = 60
        if spider.y >= self.grassGroup.sprite.y - 50 and not self.umbrellaFlg:
            if spider.vy > 50: self.energ -= 50
            elif spider.vy > 40: self.energ -= 40
            elif spider.vy > 30: self.energ -= 30
            elif spider.vy > 20: self.energ -= 20
        if spider.y >= self.grassGroup.sprite.y - 50:
            spider.y = self.grassGroup.sprite.y - 50
            self.umbrellaFlg = True
            self.Timecnt2 += 1
            print(self.Timecnt2)
            if  math.isclose(spider.vx, 0, abs_tol=1e-05) and self.Timecnt2 >= 100:
                self.Gamewin = True
                self.GameStart = True


            
    @staticmethod
    def scrolling(self):
        #scroll clouds and net
        if self.spiderGroup.sprite.x >= self.width//2:
            self.scrollvx = self.spiderGroup.sprite.vxtmp

            # self.spiderGroup.sprite.velocity = (0, self.scrollvy)
            self.wheelGroup.sprite.x -= self.scrollvx
            # self.silkGroup.sprite.x1 -= self.scrollvx   
            for cloud in self.clouds.sprites():
                cloud.x -= self.scrollvx       
            for track in self.tracks.sprites():
                track.x -= self.scrollvx  
            self.grassGroup.sprite.x-= self.scrollvx
        if self.spiderGroup.sprite.x >= 150:    
            for cloud in self.clouds.sprites():
                cloud.y -= self.scrolly
            for track in self.tracks.sprites():
                track.y -= self.scrolly
            self.wheelGroup.sprite.y -= self.scrolly
            self.grassGroup.sprite.y -= self.scrolly
            self.scrolly = 0

    def redrawAll(self, screen):
        self.grassGroup.draw(screen)
        self.wheelGroup.draw(screen)
        self.tracks.draw(screen)
        self.clouds.draw(screen)
        if self.umbrellaFlg:
            self.umbrellaGroup.draw(screen)
        self.silkGroup.draw(screen)
        self.spiderGroup.draw(screen)
        #display energy
        if self.energ >=100: self.energ = 100
        if self.energ <=  0: self.energ = 0; self.Gamelose = True
        score2 = (self.energ)/102
        image2 = pygame.Surface((300, 100), pygame.SRCALPHA)
        pygame.draw.line(image2, (255, 0, 0), (80, 90), (140*score2+82, 90), 20)
        screen.blit(image2, (0, 0))
        #display score
        score = (self.spiderGroup.sprite.x - self.wheelGroup.sprite.x - 150)/8000
        if score <=0: score =0
        image = pygame.Surface((300, 70), pygame.SRCALPHA)
        pygame.draw.line(image, (255, 165, 0), (80, 30), (140*score+82, 30), 20)
        self.score = 140*score
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
            screen.blit(text_surface, (self.width//4*3, self.height//2))
        
        #display gameover
        if self.Gamewin:
            my_font = pygame.font.SysFont("arial", 56)
            text_surface = my_font.render("Cool! you win", True, (0,0,0))
            screen.blit(text_surface, (self.width//2, self.height//2))
        if self.Gamelose:
            my_font = pygame.font.SysFont("arial", 56)
            text_surface = my_font.render("Pity! you lose", True, (0,0,0))
            screen.blit(text_surface, (self.width//2, self.height//2))

