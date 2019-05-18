#############
#hazard part#
#############


import pygame
import math
from GameObject import GameObject
import random

class Hazardcone1(GameObject):
    @staticmethod
    def init():
        Hazardcone1.images = []
        image = pygame.image.load('images/hazardvol.png').convert_alpha()
        width, height = image.get_size()
        subImage = image.subsurface((0, 0, width, height))
        Hazardcone1.images.append(subImage)

    def __init__(self, x, y, level=None):
        factor = 0.6
        image = random.choice(Hazardcone1.images)
        w, h = image.get_size()
        #set size of grapple
        image = pygame.transform.scale(image, (int(w*factor), int(h*factor)))
        super(Hazardcone1, self).__init__(x, y, image, w / 4 * factor)
        
    def update(self, screenWidth, screenHeight):
        super(Hazardcone1, self).update(screenWidth*4, screenHeight)
        
class Hazardcone2(GameObject):
    @staticmethod
    def init():
        Hazardcone2.images = []
        image = pygame.image.load('images/hazardrock2_3.png').convert_alpha()
        width, height = image.get_size()
        subImage = image.subsurface((0, 0, width, height))
        Hazardcone2.images.append(subImage)

    def __init__(self, x, y, level=None):
        factor = 1.5
        image = random.choice(Hazardcone2.images)
        w, h = image.get_size()
        #set size of grapple
        image = pygame.transform.scale(image, (int(w*factor), int(h*factor)))
        super(Hazardcone2, self).__init__(x, y, image, w / 4 *factor)
        
    def update(self, screenWidth, screenHeight):
        super(Hazardcone2, self).update(screenWidth*4, screenHeight)

class Hazardcone3(GameObject):
    @staticmethod
    def init():
        Hazardcone3.images = []
        image = pygame.image.load('images/nop.png').convert_alpha()
        width, height = image.get_size()
        subImage = image.subsurface((0, 0, width, height))
        Hazardcone3.images.append(subImage)

    def __init__(self, x, y, level=None):
        factor = 0.8
        image = random.choice(Hazardcone3.images)
        w, h = image.get_size()
        #set size of grapple
        image = pygame.transform.scale(image, (int(w*factor), int(h*factor)))
        super(Hazardcone3, self).__init__(x, y, image, w/3*factor)
        
    def update(self, screenWidth, screenHeight):
        super(Hazardcone3, self).update(screenWidth*4, screenHeight)


class Hazardice(GameObject):
    @staticmethod
    def init(select):
        if select == "ice":
            image = pygame.image.load('images/ice.png').convert_alpha()
            width, height = image.get_size()
            Hazardice.images = []
            num = 10
            #read grapples one by one
            for i in range(num):
                    subImage = image.subsurface((0, 0, width, height))
                    Hazardice.images.append(subImage)
        elif select == "fire":
            image = pygame.image.load('images/fire.png').convert_alpha()
            width, height = image.get_size()
            Hazardice.images = []
            num = 10
            #read grapples one by one
            for i in range(num):
                    subImage = image.subsurface((0, 0, width, height))
                    Hazardice.images.append(subImage)

    def __init__(self, x, y, level=None):
        factor = 0.2
        image = random.choice(Hazardice.images)
        w, h = image.get_size()
        #set size of grapple
        image = pygame.transform.scale(image, (int(w*factor), int(h*factor)))
        super(Hazardice, self).__init__(x, y, image, w / 2 * factor)
        
    def update(self, screenWidth, screenHeight):
        super(Hazardice, self).update(screenWidth*4, screenHeight)
        
class Hazardlava(GameObject):
    @staticmethod
    def init():
        Hazardlava.images = []
        image = pygame.image.load('images/hazardlava.png').convert_alpha()
        width, height = image.get_size()
        subImage = image.subsurface((0, 0, width, height))
        Hazardlava.images.append(subImage)

    def __init__(self, x, y, level=None):
        factor = 1
        image = random.choice(Hazardlava.images)
        w, h = image.get_size()
        #set size of grapple
        image = pygame.transform.scale(image, (int(w*factor), int(h*factor)))
        super(Hazardlava, self).__init__(x, y, image, w / 4 * factor)
        
    def update(self, screenWidth, screenHeight):
        super(Hazardlava, self).update(screenWidth, screenHeight)
        
class Hazardrock(GameObject):
    @staticmethod
    def init():
        Hazardrock.images = []
        image = pygame.image.load('images/hazardrock1_1.png').convert_alpha()
        width, height = image.get_size()
        subImage = image.subsurface((0, 0, width, height))
        Hazardrock.images.append(subImage)

    def __init__(self, x, y, level=None):
        factor = 1
        image = random.choice(Hazardrock.images)
        w, h = image.get_size()
        #set size of grapple
        image = pygame.transform.scale(image, (int(w*factor), int(h*factor)))
        super(Hazardrock, self).__init__(x, y, image, w / 4 * factor)
        
    def update(self, screenWidth, screenHeight):
        super(Hazardrock, self).update(screenWidth, screenHeight)
# class Hazardvol(pygame.sprite.Sprite):
#     @staticmethod
#     def init():
#         (scale0, scale1) = (1000, 500)
#         Hazardvol.hazardvol = pygame.transform.rotate(pygame.transform.scale(
#             pygame.image.load('images/volcano.png').convert_alpha(),
#             (scale0, scale1)), 0)
# 
#     def __init__(self, x, y):    
#         super(Hazardvol, self).__init__()
#         # x, y define the center of the object
#         self.x, self.y, self.image = x, y, Hazardvol.hazardvol
#         self.baseImage = Hazardvol.hazardvol.copy()  # non-rotated version of image
#         w, h = Hazardvol.hazardvol.get_size()
#         self.updateRect()
#         self.velocity = (0, 0)
#         self.angle = 0
# 
#     def update(self, screenWidth, screenHeight):
#         self.image = pygame.transform.rotate(self.baseImage, self.angle)
#         vx, vy = self.velocity
#         self.x += vx
#         self.y += vy
#         self.updateRect()
# 
#     def updateRect(self):
#         # update the object's rect attribute with the new x,y coordinates
#         w, h = self.image.get_size()
#         self.width, self.height = w, h
#         self.rect = pygame.Rect(self.x - w / 2, self.y - h / 2, w, h)

