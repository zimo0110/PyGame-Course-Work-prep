import pygame
import os
import random

pygame.mixer.init()
pygame.font.init()
pygame.init()

BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (50,50,255)
YELLOW = (255,255,0)
RED = (255,0,0)

WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodgy Star Game by ZOIR")

HEALTH_FONT = pygame.font.SysFont('Aharoni', 40)
WINNER_FONT = pygame.font.SysFont('Biome', 80)

BULLET_HSOUND = pygame.mixer.Sound(os.path.join('resourcesExtra', 'Grenade+1.mp3'))
BULLET_FSOUND = pygame.mixer.Sound(os.path.join('resourcesExtra', 'Gun+Silencer.mp3'))

FPS = 60
VEL = 5

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 40, 40

SPACE_BG = pygame.transform.scale(pygame.image.load(os.path.join('resourcesExtra','space.png')),(WIDTH, HEIGHT))

invader_SPACESHIP_IMAGE = pygame.image.load(os.path.join('resourcesExtra', 'spaceship_yellow.png'))
invader_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(invader_SPACESHIP_IMAGE, (5, 5)), 90)

player_SPACESHIP_IMAGE = pygame.image.load(os.path.join('resourcesExtra', 'spaceship_red.png'))
player_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(player_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 180)

INVADER_PLAYER = pygame.USEREVENT + 1
BULLET_INVADER  = pygame.USEREVENT + 2

BULL_VEL = 3
MAX_BULL = 3

HEALTH_FONT = pygame.font.SysFont('Aharoni', 40)

class invaders(pygame.sprite.Sprite):

    def __init__(self,color, width, height):
        super().__init__()
        self.image = pygame.Surface([width,height])
        self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,600)
        self.rect.y = random.randrange(0,400)
        self.width = width
        self.height = height
        self.speed = 5
        self.color = color

    def movement(self, my_inv):
        for my_inv in self:

            if my_inv.rect.y + 5 <= HEIGHT:
                my_inv.rect.y += 3
            else:
                my_inv.rect.y = -1

class player(pygame.sprite.Sprite):

    def __init__(self, width,height,x,y):
        super().__init__()
        self.image = player_SPACESHIP
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.height = height
        self.width = width
        self.speed = 5
        self.lives  = 3
    
    def movement(self, keys_pressed):
        if keys_pressed[pygame.K_a] and self.rect.x > 0:
            self.rect.x -= VEL
        if keys_pressed[pygame.K_d] and self.rect.x + self.width < WIDTH:
            self.rect.x += VEL
    
    def get_x(self):
        return self.rect.x
    def get_y(self):
        return self.rect.y
    def collision(self, inv_group, my_inv, lives):
        for my_inv in inv_group:
            col2 = pygame.sprite.collide_rect(self,my_inv)
            if col2 == True:
                inv_group.remove(my_inv)
                self.lives -= 1      
    def scoreP(self):
        draw_text = HEALTH_FONT.render("Health :" + str(self.lives), 1, WHITE)
        winner_text = HEALTH_FONT.render("YOU LOST", 1, WHITE)
        WIN.blit(draw_text ,(draw_text.get_width()//2 - 20, 0 + draw_text.get_height()//2))
        if self.lives == 0:
            WIN.blit(winner_text ,(winner_text.get_width()//2 - 20, 30 + winner_text.get_height()//2))
            pygame.display.update()
        else:
            pygame.display.update()
            pygame.time.delay(5000)
            

class Bullets(pygame.sprite.Sprite):

    def __init__(self, width, height,x ,y):
        super().__init__()
        self.image = pygame.Surface([5,5])
        self.image.fill(RED)

        #self.bullet = bullet
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.height = 5
        self.width = 5
        self.speed = 5
    
    def movement(self, playerW, inv_group, my_inv, bullets):

        for self in bullets:
            self.rect.y -= BULL_VEL

            if self.rect.y <= 0:
                bullets.remove(self)
            for my_inv in inv_group:
                col = pygame.sprite.collide_rect(self, my_inv)
                if col == True:
                    bullets.remove(self)
                    inv_group.remove(my_inv)

#main loop
def main():
    clock = pygame.time.Clock()
    run = True
    FPS = 60

    inv_group = pygame.sprite.Group() 
    sprites_group = pygame.sprite.Group() 

    number_of_flakes = 30 
    invH = 8
    invW = 8
    
    bullets = []
    lives = 3

    playerW = player(SPACESHIP_WIDTH, SPACESHIP_HEIGHT,WIDTH//2,HEIGHT -SPACESHIP_HEIGHT)
    for n in range(0, number_of_flakes):
        my_inv = invaders(WHITE, invW,  invH)
        #my_inv = invaders(pygame.Rect(WIDTH//2,HEIGHT, invW, invH))
        inv_group.add(my_inv)
        sprites_group.add(my_inv)

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
         
                if event.key == pygame.K_LCTRL and len(bullets) < MAX_BULL:
                    bullet = Bullets(5,5,player.get_x(playerW)+ SPACESHIP_WIDTH/2, player.get_y(playerW))
                    bullets.append(bullet)
                    BULLET_FSOUND.play()

        keys_pressed = pygame.key.get_pressed()
        bullet = Bullets(5,5,player.get_x(playerW)+ SPACESHIP_WIDTH/2, player.get_y(playerW))
        invaders.movement(inv_group, my_inv)
        player.movement(playerW,keys_pressed)
        Bullets.movement(bullet,playerW, inv_group, my_inv, bullets)
        player.collision(playerW, inv_group, my_inv, lives)
        #player.scoreP(playerW, lives)
        draw(inv_group, playerW, bullets,lives)

def draw(inv_group, playerW, bullets,lives):
    WIN.blit(SPACE_BG, (0,0))
    #player.scoreP(playerW)
    inv_group.draw(WIN)
    WIN.blit(player_SPACESHIP, (player.get_x(playerW), player.get_y(playerW)))

    for bullet in bullets:
        pygame.draw.rect(WIN, WHITE, bullet)

    pygame.display.update()

if __name__ == "__main__":
    main()