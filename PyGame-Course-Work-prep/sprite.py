import pygame
import os
import math
import random

pygame.mixer.init()
pygame.font.init()
pygame.init()

BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (50,50,255)
YELLOW = (255,255,0)
RED = (255,0,0)

WIDTH, HEIGHT = 900, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Let It Snow by ZOIR")

class snow(pygame.sprite.Sprite):

    def __init__(self, color, width, height,speed): # __innit__ is a constructor 
        super().__init__()

        self.image = pygame.Surface([width,height])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,600)
        self.rect.y = random.randrange(0,400)
        self.speed = speed

    def update(self):
        if self.rect.x + self.width <WIDTH:
            self.rect.x += self.speed
        else:
            self.rect.x = -1
        
def main():
    clock = pygame.time.Clock()
    run = True

    snow_group = pygame.sprite.Group() 
    all_sprites_group = pygame.sprite.Group() 

    number_of_flakes = 50 
    FPS = 60
    x = 0
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        while x != number_of_flakes:
            my_snow = snow(WHITE, 5, 5, 5) # snowflakes are white with size 5 by 5 px
            snow_group.add (my_snow) # adds the new snowflake to the group of snowflakes
            all_sprites_group.add (my_snow) # adds it to the group of all Sprites
            x += 1

        draw_snow(snow_group)
        snow.update(snow_group)
        
   
def draw_snow(snow_group):
    WIN.fill(BLACK)
    print(len(snow_group))
    snow_group.draw(WIN)
    pygame.display.update()

if __name__ == "__main__":
    main()