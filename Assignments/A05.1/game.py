import pygame
import os

WIDTH = 640
HEIGHT = 480
PLAYERWIDTH = 48
PLAYERHEIGHT = 48
FPS = 30

# define colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# it is better to have an extra variable, than an extremely long line.
img_path = ("baseball_48x48.png")

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MY GAME")
clock = pygame.time.Clock()

class Player(object):  # represents the Player, not the game
    def __init__(self):
        """ The constructor of the class """
        self.image = pygame.image.load(img_path)
        # The code that make it as a green rect
        #self.image = pygame.Surface((PLAYERWIDTH, PLAYERHEIGHT))
        #self.image.fill(GREEN)

        # the Player's position
        self.x = 0
        self.y = HEIGHT / 2 - PLAYERHEIGHT / 2

    def handle_keys(self):
        """ Handles Keys """
        key = pygame.key.get_pressed()
        dist = 10 # distance moved in 1 frame, try changing it to 5
        if key[pygame.K_DOWN]: # down key
            self.y += dist # move down
        elif key[pygame.K_UP]: # up key
            self.y -= dist # move up
        if key[pygame.K_RIGHT]: # right key
            self.x += dist # move right
        elif key[pygame.K_LEFT]: # left key
            self.x -= dist # move left

    def draw(self, surface):
        """ Draw on surface """
        # blit yourself at your current position
        if self.x > WIDTH - PLAYERWIDTH:
            self.x = WIDTH - PLAYERWIDTH
        if self.x < 0:
            self.x = 0
        if self.y > HEIGHT - PLAYERHEIGHT:
            self.y = HEIGHT - PLAYERHEIGHT
        if self.y < 0:
            self.y = 0
        surface.blit(self.image, (self.x, self.y))


player = Player() # create an instance

running = True
while running:
    clock.tick(FPS)
    # handle every event since the last frame.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() # quit the screen
            running = False

    player.handle_keys() # handle the keys
    screen.fill(BLACK) # fill the screen with white
    player.draw(screen) # draw the player to the screen
    pygame.display.update() # update the screen

pygame.quit()
