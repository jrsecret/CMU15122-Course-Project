############
#indicator part#
############


import pygame
import math
from GameObject import GameObject
import random

                
class Indicator1(GameObject):
    @staticmethod
    def init(select):
        (scale0, scale1) = (70, 70)
        if select == "speed":
            Indicator1.image = pygame.transform.rotate(pygame.transform.scale(
                pygame.image.load('images/speed2.png').convert_alpha(),
                (scale0, scale1)), 0)
        elif select == "distance":
            Indicator1.image = pygame.transform.rotate(pygame.transform.scale(
                pygame.image.load('images/ruler2.png').convert_alpha(),
                (scale0, scale1)), 0)
        elif select == "energy":
            Indicator1.image = pygame.transform.rotate(pygame.transform.scale(
                pygame.image.load('images/heart2.png').convert_alpha(),
                (scale0, scale1)), 0)    

    def __init__(self, x, y):
        super(Indicator1, self).__init__(x, y, Indicator1.image, 30)
        
    def update(self, screenWidth, screenHeight):
        super(Indicator1, self).update(screenWidth, screenHeight)
        
class Indicator2(GameObject):
    @staticmethod
    def init():
        (scale0, scale1) = (180, 70)
        Indicator2.image = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/bar.png').convert_alpha(),
            (scale0, scale1)), 0) 

    def __init__(self, x, y):
        super(Indicator2, self).__init__(x, y, Indicator2.image, 30)
        
    def update(self, screenWidth, screenHeight):
        super(Indicator2, self).update(screenWidth, screenHeight)
        