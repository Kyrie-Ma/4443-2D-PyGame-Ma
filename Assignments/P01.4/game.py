import pygame
import random
import math
import json

WIDTH = 1280 
HEIGHT = 720
startx=100 
starty=100 
fps=30 
black = (0,0,0)
num_enemies = 15

def load_json(infile):
    with open(infile,'r') as f:
        data = f.read()
        dictionary_json = json.loads(data)
    return dictionary_json

def straightDistance(x1,y1,x2,y2):
    distance = ((x1-x2)**2 + (y1-y2)**2)**0.5
    return distance

player_animations = load_json('./player/info.json')
robot_animations = load_json('./robot/info.json')
bullet_animations = load_json('./fireball/info.json')
   
class Camera():
    def __init__(self):
        self.camera_offset = (0,0)
    
    def update(self, player_target):
        l, t = player_target.actual_position
        self.camera_offset = (WIDTH/2-l, HEIGHT/2-t)
    
    def apply(self):
        return self.camera_offset

class Background(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./backgroud_1920x1080.jpg" ).convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)

    def update(self, position):
        self.rect.topleft = (position[0], position[1])

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.dead_pictureset = robot_animations["Dead"]
        self.idle_pictureset = robot_animations["Idle"]
        self.idle_imagenum = 1
        self.dead_imagenum = 0
        self.idle_imagelimit = self.idle_pictureset["count"]
        self.dead_imagelimit = self.dead_pictureset["count"]
        self.image = pygame.image.load("./robot/"+self.idle_pictureset["name"]+str(self.idle_imagenum)+".png")
        self.rect = self.image.get_rect()
        self.x = random.randint(0,WIDTH)
        self.y = random.randint(0,HEIGHT)
        self.rect.topleft = self.actual_position = (self.x, self.y)
        self.hit = True

    def update(self, position):
        if self.hit:
            self.idle_imagenum = max(1, (self.idle_imagenum + 1) % self.idle_imagelimit)
            self.image = pygame.image.load("./robot/"+self.idle_pictureset["name"]+str(self.idle_imagenum)+".png")
        elif not self.hit:
            self.dead_imagenum += 1
            if self.dead_imagenum == self.dead_imagelimit:
                self.dead_imagenum = 1
                self.kill()
            else:
                self.image = pygame.image.load("./robot/"+self.dead_pictureset["name"]+str(self.dead_imagenum)+".png")
        self.rect.topleft = (self.actual_position[0]+position[0], self.actual_position[1]+position[1])

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.idle_pictureset = player_animations["Idle"]
        self.dead_pictureset = player_animations["Dead"]
        self.walk_pictureset = player_animations["Walk"]
        self.idle_imagenum = 1
        self.dead_imagenum = 1
        self.walk_imagenum = 1
        self.idle_imagelimit = self.idle_pictureset["count"]
        self.dead_imagelimit = self.dead_pictureset["count"]
        self.walk_imagelimit = self.walk_pictureset["count"]
        self.image = pygame.image.load("./player/Idle (1).png")
        self.rect = self.image.get_rect()
        self.IMAGE_WIDTH = self.rect.right - self.rect.left
        self.IMAGE_HEIGHT = self.rect.bottom - self.rect.top
        self.x = startx
        self.y = starty
        self.rect.topleft = self.actual_position = self.old_loc = (self.x, self.y)
        self.distance = 0
        self.speed = 5
        self.target_location = (0,0)

    def Move(self, mouse_position):
        world_coord_x = mouse_position[0]-WIDTH/2+self.actual_position[0]
        world_coord_y = mouse_position[1]-HEIGHT/2+self.actual_position[1]
        self.target_location = (world_coord_x,world_coord_y)
        self.MoveWithMouse()
        self.actual_position = (self.x, self.y)

    def MoveWithMouse(self):
        self.old_loc = self.actual_position
        x = self.target_location[0]
        y = self.target_location[1]
        dx = x - self.x
        dy = y - self.y
        angle = math.atan2(dy, dx)
        self.distance = straightDistance(self.x, self.y, x, y)
        self.x += int(min(5, self.distance/10) * math.cos(angle))
        self.y += int(min(5, self.distance/10) * math.sin(angle))
    
    def update(self, position):
        if self.distance < 10:
            self.idle_imagenum = max(1, (self.idle_imagenum + 1) % self.idle_imagelimit)
            self.image = pygame.image.load("./player/"+self.idle_pictureset["name"]+str(self.idle_imagenum)+").png")
        elif self.distance >= 10:
            self.walk_imagenum = max(1, (self.walk_imagenum + 1) % self.walk_imagelimit)
            self.image = pygame.image.load("./player/"+self.walk_pictureset["name"]+str(self.walk_imagenum)+").png")
        if self.actual_position[0] <= 0 or self.actual_position[0]+self.IMAGE_WIDTH >= 1920 or self.actual_position[1] <= 0 or self.actual_position[1]+self.IMAGE_HEIGHT >= 1080:
            self.dead_imagenum = max(1, (self.dead_imagenum + 1) % self.dead_imagelimit)
            self.image = pygame.image.load("./player/"+self.dead_pictureset["name"]+str(self.dead_imagenum)+").png")
            self.actual_position = self.old_loc
        self.rect.topleft = (self.actual_position[0]+position[0], self.actual_position[1]+position[1])

class Bullet(pygame.sprite.Sprite):
    def __init__(self,player_pos,mouse_pos):
        pygame.sprite.Sprite.__init__(self)
        self.bullet_pictureset = bullet_animations["Shot"]
        self.bullet_imagenum = 1
        self.bullet_imagelimit = self.bullet_pictureset["count"]
        self.image_unrot = pygame.image.load("./fireball/"+self.bullet_pictureset["name"]+str(self.bullet_imagenum)+".png")
        self.rect = self.image_unrot.get_rect()
        self.angle = self.getBulletDirection(mouse_pos)
        self.image = pygame.transform.rotate(self.image_unrot, (self.angle*57.29578)+180)
        self.x = player_pos[0]
        self.y = player_pos[1]
        self.rect.topleft = self.actual_position = (self.x, self.y)
    
    def getBulletDirection(self, mouse_pos):
        x = mouse_pos[0]
        y = mouse_pos[1]
        dx = x - WIDTH/2
        dy = y - HEIGHT/2
        return math.atan2(dy, dx)
    
    def update(self, position):
        self.bullet_imagenum = max(1, (self.bullet_imagenum + 1) % self.bullet_imagelimit)
        self.image_unrot = pygame.image.load("./fireball/"+self.bullet_pictureset["name"]+str(self.bullet_imagenum)+".png")
        self.image = pygame.transform.rotate(self.image_unrot, (self.angle*-57.29578)+180)
        self.x += int(10 * math.cos(self.angle))
        self.y += int(10 * math.sin(self.angle))
        self.actual_position = (self.x,self.y)
        if self.actual_position[0] <= 0 or self.actual_position[0] >= 1920 or self.actual_position[1] <= 0 or self.actual_position[1] >= 1080:
            self.kill()
        else:
            self.rect.topleft = (self.actual_position[0]+position[0], self.actual_position[1]+position[1])

def main():
    pygame.init()

    fireball_thrown = pygame.mixer.Sound("./sounds/throw.wav")
    fireball_hit = pygame.mixer.Sound("./sounds/hit.wav")
    background_music = pygame.mixer.Sound("./sounds/game_track.ogg")
    fireball_thrown.set_volume(0.6)
    fireball_hit.set_volume(0.6)
    background_music.set_volume(0.2)
    background_music.play(loops=-1)

    p1 = Player()
    bkgr = Background()
    camera = Camera()
    main_sprites = pygame.sprite.Group()
    bullet_sprites = pygame.sprite.Group()
    robot_sprites = pygame.sprite.Group()
    main_sprites.add(bkgr)
    main_sprites.add(p1)

    for x in range(num_enemies):
        robot_sprites.add(Enemy())

    running = True
    while running:
        screen.fill(black)
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                fireball_thrown.play()
                fire_bullet = Bullet(p1.actual_position,mouse_pos)
                bullet_sprites.add(fire_bullet)
        if pygame.mouse.get_focused():
            mouse_pos = pygame.mouse.get_pos()
            p1.Move(mouse_pos)

        camera.update(p1)
        for sprite in main_sprites:
            sprite.update(camera.apply())
        for sprite in bullet_sprites:
            sprite.update(camera.apply())
        for sprite in robot_sprites:
            sprite.update(camera.apply())
        for bullet in bullet_sprites:
            for robot in robot_sprites:
                if bullet.rect.colliderect(robot.rect):
                    fireball_hit.play()
                    bullet.kill()
                    robot.hit = False
                    
        main_sprites.draw(screen)
        bullet_sprites.draw(screen)
        robot_sprites.draw(screen)
        pygame.display.flip()

if __name__=='__main__':
    pygame.display.set_caption("MY GAME")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    main()
