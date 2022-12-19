import random
import pygame
import os
from Balloon import Balloon
from Bubbles import Bubbles
from Spikes import Spikes, SpikeArray

# Initialize pygame
pygame.init()
pygame.font.init()

# Globals
SCREEN_WIDTH, SCREEN_HEIGHT = 480, 640
BUBBLE_WIDTH, BUBBLE_HEIGHT = 15, 15
BALLOON_WIDTH, BALLOON_HEIGHT = 60, 60
SPIKE_WIDTH, SPIKE_HEIGHT = 15, 30
RISING_SPEED = 2
FPS = 60

# Make main window
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rising Balloon")

# Import image assets
BALLOON_IMAGE = pygame.image.load(os.path.join("../Images", "Balloon.png"))
BALLOON_IMAGE = pygame.transform.scale(BALLOON_IMAGE, (BALLOON_WIDTH, BALLOON_HEIGHT))
BUBBLE_IMAGE = pygame.image.load(os.path.join("../Images", "Bubble.png"))
BUBBLE_IMAGE = pygame.transform.scale(BUBBLE_IMAGE, (BUBBLE_WIDTH, BUBBLE_HEIGHT))
SPIKE_IMAGE = pygame.image.load(os.path.join("../Images", "Spike.png"))
SPIKE_IMAGE = pygame.transform.scale(SPIKE_IMAGE, (SPIKE_WIDTH, SPIKE_HEIGHT))

# Define Basic Colors
COLOR_WHITE = (255, 255, 255)

# Create initial objects
balloon = Balloon(SCREEN_WIDTH//2-(BALLOON_WIDTH//2) ,SCREEN_HEIGHT-200, BALLOON_WIDTH, BALLOON_HEIGHT, BALLOON_IMAGE)

# Collision function
def collide(object1, object2):
    offset_x = object2.x - object1.x
    offset_y = object2.y - object1.y
    return object1.mask.overlap(object2.mask, (offset_x, offset_y)) != None

def selfCollision(self, object):
    return collide(self, object)

Spikes.collision = selfCollision
Bubbles.collision = selfCollision

# Main loop
def main():
    # Initialize variables
    EXIT = False
    CLOCK = pygame.time.Clock()
    balloon_moving = False
    score = 0

    # Load Cascadia Code font in size 20 pygame
    CascadiaCode = pygame.font.SysFont("Cascadia Code", 30)

    # Set bubble parameters
    bubbles_visible = 20
    bubbles = []

    # Set spike parameters
    max_spike_arrays = 5
    max_spikes = SCREEN_WIDTH//SPIKE_WIDTH
    spikes = []

    # Set timer
    now = pygame.time.get_ticks()

    # Screen refresh function
    def redrawWindow():
        # Clear screen
        win.fill(COLOR_WHITE)

        # Draw bubbles
        for bubble in bubbles:
            bubble.draw(win)
        
        # Draw spikes
        for spike_array in spikes:
            spike_array.draw(win)

        # Write score
        score_text = CascadiaCode.render("Score: " + str(score), True, (0,0,0))
        win.blit(score_text, (10,10))

        # Draw balloon
        balloon.draw(win)

        # Update display
        pygame.display.update()


    while not EXIT:
        CLOCK.tick(FPS)

        # Create bubbles if there are less than bubbles_visible
        while len(bubbles) < bubbles_visible:
            bubbles.append(Bubbles(random.randint(0,SCREEN_WIDTH-BUBBLE_WIDTH),random.randint(-SCREEN_HEIGHT,0),30,30,BUBBLE_IMAGE))

        # Create spikes
        if len(spikes) < max_spike_arrays:
            time_difference = pygame.time.get_ticks() - now
            if time_difference >= random.randint(2400, 4800):
                gap_index = random.randint(0,max_spikes-((2*BALLOON_WIDTH)//SPIKE_WIDTH))
                gap_length = random.randint(8, max_spikes-gap_index)
                spikes.append(SpikeArray(-SPIKE_HEIGHT, SPIKE_WIDTH, SPIKE_HEIGHT, SPIKE_IMAGE, max_spikes, gap_index, gap_length))
                now = pygame.time.get_ticks()

        # Event listener
        for event in pygame.event.get():

        # Exit Condition
            if event.type == pygame.QUIT:
                EXIT = True

        # Balloon movement
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x_init, y_init = pygame.mouse.get_pos()
                    balloon_moving = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    balloon_moving = False
            elif event.type == pygame.MOUSEMOTION:
                if balloon_moving:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    balloon.moveIncrement(mouse_x-x_init,0)
                    x_init, y_init = pygame.mouse.get_pos()

        # Remove bubbles which collide with spikes
        for bubble in bubbles:
            for spike_array in spikes:
                if spike_array.collision(bubble):
                    bubbles.remove(bubble)
                    break
        
        # Increase score on collision between balloon and bubble and remove bubble
        for bubble in bubbles:
            if bubble.collision(balloon):
                score += 1
                bubbles.remove(bubble)

        # Check if balloon collides with spikes
        for spike_array in spikes:
            if spike_array.collision(balloon):
                EXIT = True

        # Remove Spikes if they are off screen
        for spike_array in spikes[:]:
            spike_array.moveWithVelocity(0,RISING_SPEED)
            if spike_array.y > SCREEN_HEIGHT:
                spikes.remove(spike_array)
        
        # Remove Bubbles if they are off screen
        for bubble in bubbles[:]:
            bubble.moveWithVelocity(0,RISING_SPEED)
            if bubble.y > SCREEN_HEIGHT:
                bubbles.remove(bubble)

        # Redraw window
        redrawWindow()

    pygame.quit()

if __name__ == "__main__":
    main()
