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
level_width = 1400
vel = 5


class Camera:
    def __init__(self, x, y, w, h, speed):
        self.rect = pygame.Rect(x, y, w, h)
        self.speed = speed
    def move(self, player):
        if self.rect.right < level_width:
            if player.rect.x > self.rect.x + int(0.97*self.rect.w):
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
        self.isJump = False
        self.jumpCount = 20
        
    def jump(self):
        if self.isJump:
            if self.jumpCount >= -20:
                self.rect.y -= (self.jumpCount * abs(self.jumpCount)) * 0.05
                self.jumpCount -= 1
            else: 
                self.jumpCount = 20
                self.isJump = False
                self.rect.y = 260
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
        global score1
        #k = pygame.key.get_pressed()
        #if k[pygame.K_SPACE]:
        if self.collide(item): #and not item.is_choped
            item.is_choped = True
            #fire_sound.play()
            item.hp -= 1
            #print(item.hp)

            if item.hp <= 0:
                trees.remove(item)
                score1 -= 1
                tree = Tree(randint(10, 690), 180, 130, 130, tree_img, 5, 300)

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
            #print(self.time)
            if self.time == 0:
                self.is_choped = False
                self.hp = self.hpmax
                self.time = self.timemax

bots = []   
class Bot(GameSprite):
    def __init__(self, x, y, w, h, image, speed, x_finish):
        super().__init__(x, y, w, h, image)
        self.speed = speed
        if x > x_finish:
            self.direction = "left"
            self.x_start = x_finish
            self.x_finish = x
        else: 
            self.direction = "right"
            self.x_start = x
            self.x_finish = x_finish
        bots.append(self)
    
    def move(self):
        if self.direction == "left":
            self.rect.x -= self.speed
            if self.rect.x <= self.x_start:
                self.direction = "right"
        elif self.direction == "right":
            self.rect.x += self.speed
            if self.rect.x >= self.x_finish:
                self.direction = "left"
player_img = pygame.image.load('player.png')
player = Player(100, 260, 45, 45, player_img, 2)
tree_img = pygame.image.load('tree.png')
font1 = pygame.font.SysFont('Arial', 32)
score1 = randint(3, 8)
#score2 = randint(1, 8)
#score3 = randint(1, 8)
#try:
#    with open('hit.txt', 'r') as file:
#        score1 = int(file.read())
#except FileNotFoundError:
#    file = open('hit.txt', 'x')
#    file.close()
#except ValueError:
#    pass
bot_img = pygame.image.load("bot.png")
bot = Bot(1000, 280, 30, 25, bot_img, 2, 200)
for i in range(5):
    tree = Tree(randint(10, 1100), 180, 130, 130, tree_img, 5, 300)
game = True
finish = False
while game:
    if not finish:
        score1_lb = font1.render('дерева: ' + str(score1), True, (255, 255, 255))
        #score2_lb = font1.render('сосна: ' + str(score2), True, (255, 255, 255))
        #score3_lb = font1.render('сакура: ' + str(score3), True, (255, 255, 255))
        window.blit(background, (-camera.rect.x, 0))
        window.blit(score1_lb, (0, 0))
        #window.blit(score2_lb, (0, 30))
        #window.blit(score3_lb, (0, 60))
        keys = pygame.key.get_pressed()
        player.draw()
        player.move()
        player.jump()
        for bot in bots:
            bot.draw()
            bot.move()
            if player.collide(bot):
                color = (255, 0, 0)
                game_over = font1.render("Game Over!", True, (20, 20, 20))
                window.fill(color)
                window.blit(game_over, (200, 200))
                finish = True
                
        camera.move(player)

        # This is what will happen if we are jumping
        if score1 == 0:
            color = (0, 255, 0)
            win = font1.render("You Win!", True, (20, 20, 20))
            window.fill(color)
            window.blit(win, (200, 200))
            finish = True
        for tree in trees:
            tree.draw()
            tree.restore()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e and not finish:
            for tree in trees:
                player.chop(tree)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not finish:
                if not player.isJump:
                    player.isJump = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and finish:
            #trees.remove()
            finish = False
    clock.tick(FPS)
    pygame.display.update()