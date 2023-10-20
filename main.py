import pygame
pygame.init()
from time import time
from random import randint
from random import choice
FPS = 60
window = pygame.display.set_mode((700, 400))
win_width = 700
win_height = 400
clock = pygame.time.Clock()
background = pygame.image.load('background.png')
background = pygame.transform.scale(background, (1400, 400))
score = 0
level_width = 1400
class Camera:
    def __init__(self, x, y, w, h, speed):
        self.rect = pygame.Rect(x, y, w, h)
        self.speed = speed
    def move(self, player):
        if self.rect.right < level_width:
            if player.rect.x > self.rect.x + int(0.7*self.rect.w):
                self.rect.x += self.speed

camera = Camera(0 ,0, win_width, win_height, 5)

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, image):
        super().__init__()
        self.rect = pygame.Rect(x, y, w, h)
        image = pygame.transform.scale(image, (w, h))
        self.image = pygame.transform.scale(image, (w, h))
    def draw(self):
        window.blit(self.image, (self.rect.x - camera.rect.x, self.rect.y))
class Player(GameSprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__(x, y, w, h, image)
        self.speed = speed
    def move(self):
        k = pygame.key.get_pressed()
        if k[pygame.K_d]:
            if self.rect.x <= level_width - self.rect.width:
                self.rect.x += self.speed
        if k[pygame.K_a]:
            if self.rect.x >= 0:
                self.rect.x -= self.speed
#        if k[pygame.K_d]:
#            if self.rect.right <= 700:
#                self.rect.x += self.speed
#        if k[pygame.K_a]:
#            if self.rect.x >= 0:
#                self.rect.x -= self.speed

    def collide(self, item):
        if self.rect.colliderect(item.rect):
            return True
        else:
            return False
    def chop(self, item):
        
        #k = pygame.key.get_pressed()
        #if k[pygame.K_SPACE]:
        if self.collide(item): #and not item.is_choped
            item.is_choped = True
            #fire_sound.play()
            item.hp -= 1
            print(item.hp)
            if item.hp <= 0:
                trees.remove(item)
trees = []   
class Tree(GameSprite):
    def __init__(self, x, y, w, h, image, hpmax, timemax):
        super().__init__(x, y, w, h, image)
        self.hpmax = hpmax
        self.hp = hpmax
        self.timemax = timemax
        self.time = timemax
        self.is_choped = False
        trees.append(self)
    def restore(self):
        if self.is_choped:
            self.time -= 1
            print(self.time)
            if self.time == 0:
                self.is_choped = False
                self.hp = self.hpmax
                self.time = self.timemax
#class enemy(GameSprite):
player_img = pygame.image.load('player.png')
player = Player(100, 260, 45, 45, player_img, 2)
tree_img = pygame.image.load('tree.png')
for i in range(3):
    tree = Tree(randint(100, 500), 190, 120, 120, tree_img, 5, 300)
game = True
finish = False
while game:
    if not finish:
        window.blit(background, (0, 0))
        player.draw()
        player.move()
        camera.move(player)
        camera.move(background)
        for tree in trees:
            tree.draw()
            tree.restore()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e and not finish:
            for tree in trees:
                player.chop(tree)
                
    clock.tick(FPS)
    pygame.display.update()