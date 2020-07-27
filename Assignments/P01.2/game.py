import pygame
pygame.init()
WIDTH = 500
HEIGHT = 500
img_path = ("baseball_48x48.png")
img_backgroud_path = ("backgroud_1000x1000.png")
class Player:
    def __init__(self):
        self.image = pygame.image.load(img_path)
        self.rect = self.image.get_rect()
        self.rect = pygame.Rect((WIDTH/2 - 48, HEIGHT/2 - 48),(48,48)) #set the player at the center
    def move(self,camera_pos):
        pos_x,pos_y = camera_pos

        key = pygame.key.get_pressed() # Get Keyboard Input
        if key[pygame.K_UP]: 
            self.rect.y -= 10 
            pos_y += 10 # keep the player at the center
        if key[pygame.K_LEFT]:
            self.rect.x -= 10
            pos_x += 10
        if key[pygame.K_DOWN]:
            self.rect.y += 10
            pos_y -= 10
        if key[pygame.K_RIGHT]:
            self.rect.x += 10
            pos_x -= 10

        if self.rect.x < 0: 
            self.rect.x = 0 
            pos_x = camera_pos[0] 
        if self.rect.x > 952:
            self.rect.x = 952
            pos_x = camera_pos[0]
        if self.rect.y < 0:
            self.rect.y = 0
            pos_y = camera_pos[1]
        if self.rect.y > 952:
            self.rect.y = 952
            pos_y = camera_pos[1]

        return (pos_x,pos_y) 

    def is_collided(self): # check if the player hit the edge
        if (self.rect.x == 0 and self.rect.y == 0): #upper left
            return 1
        if (self.rect.x == 952 and self.rect.y == 0): #upper left
            return 2
        if (self.rect.x == 0 and self.rect.y == 952): #lower right
            return 3
        if (self.rect.x == 952 and self.rect.y == 952): #lower right
            return 4
        if (self.rect.x == 0): #left
            return 5
        if  (self.rect.x == 952): #right
            return 6
        if (self.rect.y == 0): #upper
            return 7
        if (self.rect.y == 952): #lower
            return 8
        
    def render(self,display):
        display.blit(self.image,(self.rect.x,self.rect.y))

def Main(display,clock):

    world = pygame.image.load(img_backgroud_path)
    player = Player()
    camera_pos = (26,26) # Create Camara Starting Position

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        display.fill(WHITE) 
        camera_pos = player.move(camera_pos) 
        
        if(player.is_collided() == 1): #upper left
            pygame.draw.line(display, RED, (WIDTH/2-24-2, 0), (WIDTH/2-24-2, HEIGHT), 4)
            pygame.draw.line(display, RED, (0, HEIGHT/2-24-2), (WIDTH, HEIGHT/2-24-2), 4)
        if(player.is_collided() == 2): #upper right
            pygame.draw.line(display, RED, (WIDTH/2+24+2, 0), (WIDTH/2+24+2, HEIGHT), 4)
            pygame.draw.line(display, RED, (0, HEIGHT/2-24-2), (WIDTH, HEIGHT/2-24-2), 4)
        if(player.is_collided() == 3): #lower left
            pygame.draw.line(display, RED, (WIDTH/2-24-2, 0), (WIDTH/2-24-2, HEIGHT), 4)
            pygame.draw.line(display, RED, (0, HEIGHT/2+24+2), (WIDTH, HEIGHT/2+24+2), 4)
        if(player.is_collided() == 4): #lower right
            pygame.draw.line(display, RED, (WIDTH/2+24+2, 0), (WIDTH/2+24+2, HEIGHT), 4)
            pygame.draw.line(display, RED, (0, HEIGHT/2+24+2), (WIDTH, HEIGHT/2+24+2), 4)
        if(player.is_collided() == 5): #left
            pygame.draw.line(display, RED, (WIDTH/2-24-2, 0), (WIDTH/2-24-2, HEIGHT), 4)
        if(player.is_collided() == 6): #right
            pygame.draw.line(display, RED, (WIDTH/2+24+2, 0), (WIDTH/2+24+2, HEIGHT), 4)
        if(player.is_collided() == 7): #upper
            pygame.draw.line(display, RED, (0, HEIGHT/2-24-2), (WIDTH, HEIGHT/2-24-2), 4)
        if(player.is_collided() == 8): #lower
            pygame.draw.line(display, RED, (0, HEIGHT/2+24+2), (WIDTH, HEIGHT/2+24+2), 4)
        world = pygame.image.load(img_backgroud_path)
        
        player.render(world)
        display.blit(world,camera_pos) 
        pygame.display.flip()

if __name__ in "__main__":
    display = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("MY GAME")
    clock = pygame.time.Clock()

    WHITE = (255,255,255),
    RED  =(255,0,0),
    BLACK=(0,0,0)
    Main(display,clock)
