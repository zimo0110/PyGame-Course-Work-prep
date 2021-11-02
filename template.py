import pygame
import cmath
import os
import math

a = 1
b = 0
c = 300

BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (50,50,255)
YELLOW = (255,255,0)

pygame.init()
WIDTH, HEIGHT = 700, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Window")

FPS = 60

SUN_WIDTH = 120
SUN_HEIGHT = 100

HOUSE_WIDTH = 200
HOUSE_HEIGHT = 250

SUN = pygame.transform.scale(pygame.image.load(os.path.join('PyGame-Course-Work-prep', 'NewSunSun.png')),(SUN_WIDTH,SUN_HEIGHT))
HOUSE = pygame.transform.scale(pygame.image.load(os.path.join('PyGame-Course-Work-prep', 'NewHouse.png')),(HOUSE_WIDTH,HOUSE_HEIGHT))
GROUND = pygame.transform.scale(pygame.image.load(os.path.join('PyGame-Course-Work-prep', 'greenLand.png')), (WIDTH, 500))

CX = WIDTH /2
CY = HEIGHT/2
SUN_VEL = 5

def main():
    greenLand = pygame.Rect(0, 400, WIDTH, HEIGHT )
    house = pygame.Rect(WIDTH/2 - HOUSE_WIDTH/2 ,300, HOUSE_WIDTH,SUN_HEIGHT)
    sun = pygame.Rect(0,219, SUN_WIDTH,SUN_HEIGHT)
    sun_angle = 2 * math.pi * 0.5
    sun_radius = 20

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()
        sun_movement(keys_pressed, sun)
        draw_board(sun, house, greenLand)

    pygame.quit()

def draw_board(sun, house, greenLand):
    WIN.fill(WHITE)
    WIN.blit(GROUND,(0,200))
    WIN.blit(SUN, (sun.x, sun.y))
    WIN.blit(HOUSE, (house.x,house.y))
    pygame.display.update()

def sun_movement(keys_pressed, sun):

    if keys_pressed[pygame.K_d] and sun.x + SUN_WIDTH < WIDTH:

        try:
            sun.x += SUN_VEL
            sun.y = -math.sqrt(400 ** 2 - (sun.x - WIDTH / 2 + 50) ** 2) + HEIGHT / 2 + 128
        except ValueError:
            pass
    
    if keys_pressed[pygame.K_a] and sun.x >= 0:

        try:
            sun.x -= SUN_VEL
            sun.y = -math.sqrt(400 ** 2 - (sun.x - WIDTH / 2 + 50) ** 2) + HEIGHT / 2 + 128
        except ValueError:
            pass
    else:
        #print(sun.x, sun.y)
        pass

    if keys_pressed[pygame.K_d] and sun.x + SUN_WIDTH >= WIDTH :
        #print(sun.x, sun.y)
        sun.x = 0
        sun.y = 219

if __name__ == "__main__":
    main()