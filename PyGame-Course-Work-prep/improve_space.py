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

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodgy Star Game by ZOIR")

BORDER = pygame.Rect(WIDTH//2 -5, 0, 10, HEIGHT)

HEALTH_FONT = pygame.font.SysFont('Aharoni', 40)
WINNER_FONT = pygame.font.SysFont('Biome', 80)

BULLET_HSOUND = pygame.mixer.Sound(os.path.join('resourcesExtra', 'Grenade+1.mp3'))
BULLET_FSOUND = pygame.mixer.Sound(os.path.join('resourcesExtra', 'Gun+Silencer.mp3'))

FPS = 60
VEL = 5

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 50, 50

SPACE_BG = pygame.transform.scale(pygame.image.load(os.path.join('resourcesExtra','space.png')),(WIDTH, HEIGHT))

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('resourcesExtra', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('resourcesExtra', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), -90)

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT  = pygame.USEREVENT + 2

BULL_VEL = 7
MAX_BULL = 3

def main():
    red = pygame.Rect(700,300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100,300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    Rbullets = []
    Ybullets = []

    yellow_health = 10
    red_health = 10

    clock = pygame.time.Clock()
    run = True

    while run :
        clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LCTRL and len(Ybullets) < MAX_BULL:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10,5)
                    Ybullets.append(bullet)
                    BULLET_FSOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HSOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1 
                BULLET_HSOUND.play()

        winner_text = ""
        if red_health <= 0:
            red_health = 0
            winner_text = "Yellow Wins"
        if yellow_health <= 0:
            yellow_health = 0
            winner_text = "Red Wins"
        if winner_text != "":
            draw_winner(winner_text)
            break
        #red_handle_movement(red, Ybullets)

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        #red_handle_movement(red, Ybullets)
        
        handle_bullets(Ybullets, Rbullets, red, yellow) 
        red_handle_movement(red,Ybullets)
        draw_window(red, yellow, Rbullets, Ybullets, red_health, yellow_health)
    main()

def draw_window(red, yellow, Rbullets, Ybullets, red_health, yellow_health):
    WIN.blit(SPACE_BG,(0,0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Health :" + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health :" + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text,(WIDTH - red_health_text.get_width() - 15, 15 ))
    WIN.blit(yellow_health_text,(10,10))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x,yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x,red.y))

    for bullet in Rbullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in Ybullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL>0: #LEFT
        yellow.x -= VEL
    elif keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width <BORDER.x: #RIGHT
        yellow.x += VEL
    elif keys_pressed[pygame.K_w] and yellow.y - VEL>0: #UP
        yellow.y -= VEL
    elif keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height<HEIGHT: #DOWN
        yellow.y += VEL

def red_handle_movement(red, Ybullets):
    for bullet in Ybullets:
        if (red.x - bullet.x) <= 40 and ((red.y - bullet.y) <= 40 or (bullet.y - red.y) <= 40):
            print('condition passed')

            if bullet.y < red.y and red.y + red.height < HEIGHT and red.y - bullet.y <= 40:
                red.y += 15
                print("situation 1")
            elif bullet.y+ 5 > red.y and red.y - red.height > 0 and bullet.y - red.y <= 40:
                red.y -= 15
                print("situation 2")
            elif bullet.y == red.y:
                    if bullet.y > HEIGHT/2 :
                        print("situation 3")
                        red.y -= 15
                    elif bullet.y < HEIGHT/2:
                        print("situation 4")
                        red.y +=15
            
def handle_bullets(Ybullets, Rbullets, red, yellow):
    for bullet in Ybullets:
        bullet.x += BULL_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            Ybullets.remove(bullet)
        elif bullet.x > WIDTH:
            Ybullets.remove(bullet)

    for bullet in Rbullets:
        bullet.x -= BULL_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            Rbullets.remove(bullet)
        elif bullet.x < 0:
            Rbullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text,1,WHITE)
    WIN.blit(draw_text ,(WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)
    
if __name__ == "__main__":
    main()