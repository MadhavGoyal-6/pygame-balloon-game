class Bubbles():
    def __init__(self, x, y, w, h, image):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image = image
    
    def draw(self, win):
        win.blit(self.image, (self.x,self.y))

    def moveWithVelocity(self, x_vel, y_vel):
        self.x += x_vel
        self.y += y_vel