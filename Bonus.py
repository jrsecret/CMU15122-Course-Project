############
#bonus part#
############


import pygame
import math
from GameObject import GameObject
import random

class Bonus1(GameObject):
    @staticmethod
    def init():
        image = pygame.image.load('images/bonus1.png').convert_alpha()
        width, height = image.get_size()
        Bonus1.images = []
        num = 10
        #read grapples one by one
        for i in range(num):
                subImage = image.subsurface((0, 0, width, height))
                Bonus1.images.append(subImage)

    def __init__(self, x, y, level=None):
        factor = 1
        image = random.choice(Bonus1.images)
        w, h = image.get_size()
        #set size of grapple
        image = pygame.transform.scale(image, (int(w*factor), int(h*factor)))
        super(Bonus1, self).__init__(x, y, image, w / 2 * factor)
        
    def update(self, screenWidth, screenHeight):
        super(Bonus1, self).update(screenWidth*4, screenHeight)
class Bonus2(GameObject):
    @staticmethod
    def init():
        image = pygame.image.load('images/bonus2.png').convert_alpha()
        width, height = image.get_size()
        Bonus2.images = []
        num = 10
        #read grapples one by one
        for i in range(num):
                subImage = image.subsurface((0, 0, width, height))
                Bonus2.images.append(subImage)

    def __init__(self, x, y, level=None):
        factor = 1
        image = random.choice(Bonus2.images)
        w, h = image.get_size()
        #set size of grapple
        image = pygame.transform.scale(image, (int(w*factor), int(h*factor)))
        super(Bonus2, self).__init__(x, y, image, w / 2 * factor)
        
    def update(self, screenWidth, screenHeight):
        super(Bonus2, self).update(screenWidth*4, screenHeight)
        
class Bonus3(GameObject):
    @staticmethod
    def init():
        image = pygame.image.load('images/bonus3.png').convert_alpha()
        width, height = image.get_size()
        Bonus3.images = []
        num = 10
        #read grapples one by one
        for i in range(num):
                subImage = image.subsurface((0, 0, width, height))
                Bonus3.images.append(subImage)

    def __init__(self, x, y, level=None):
        factor = 1
        image = random.choice(Bonus3.images)
        w, h = image.get_size()
        #set size of grapple
        image = pygame.transform.scale(image, (int(w*factor), int(h*factor)))
        super(Bonus3, self).__init__(x, y, image, w / 2 * factor)
        
    def update(self, screenWidth, screenHeight):
        super(Bonus3, self).update(screenWidth*4, screenHeight)