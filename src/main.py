import random
import pygame
import os
from Balloon import Balloon
from Bubbles import Bubbles
from Spikes import SpikeArray

# Initialize pygame
pygame.init()

# Globals
SCREEN_WIDTH, SCREEN_HEIGHT = 480, 640
BUBBLE_WIDTH, BUBBLE_HEIGHT = 15, 15
BALLOON_WIDTH, BALLOON_HEIGHT = 60, 60
SPIKE_WIDTH, SPIKE_HEIGHT = 15, 30
RISING_SPEED = 1
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

# Main loop
def main():
    EXIT = False
    CLOCK = pygame.time.Clock()
    balloon_moving = False

    bubbles_visible = 20
    bubbles = []

    spike_arrays = 2
    spike_heights = [i for i in range(-SCREEN_HEIGHT, 0, 2*BALLOON_HEIGHT)]
    max_spikes = SCREEN_WIDTH//SPIKE_WIDTH
    spikes = []

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
        if len(spikes) < spike_arrays:
            spike_height = random.choice(spike_heights)
            gap_index = random.randint(0,max_spikes-((2*BALLOON_WIDTH)//SPIKE_WIDTH))
            gap_length = random.randint(8, max_spikes-gap_index)
            spikes.append(SpikeArray(spike_height, SPIKE_WIDTH, SPIKE_HEIGHT, SPIKE_IMAGE, max_spikes, spike_height, gap_index, gap_length))
            for i in spike_heights:
                if i >= spike_height:
                    spike_heights.remove(i)

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

        for spike_array in spikes[:]:
            spike_array.moveWithVelocity(0,RISING_SPEED)
            print(spike_array.y > SCREEN_HEIGHT-100)
            if spike_array.y > SCREEN_HEIGHT-100:
                spike_heights.append(spike_array.getInitHeight())
                spikes.remove(spike_array)
        
        for bubble in bubbles[:]:
            bubble.moveWithVelocity(0,RISING_SPEED)
            if bubble.y > SCREEN_HEIGHT:
                bubbles.remove(bubble)

        # Redraw window
        redrawWindow()

    pygame.quit()

if __name__ == "__main__":
    main()
