import pygame

class Balloon():
    def __init__(self, x, y, w, h, image):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, win):
        win.blit(self.image, (self.x,self.y))
    
    def moveIncrement(self, x, y):
        self.x += x
        self.y += y