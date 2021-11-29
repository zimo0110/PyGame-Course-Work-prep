import pygame
import os
import math
import random

BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (50,50,255)
YELLOW = (255,255,0)
GREY = (200,200,200)
RED = (255,0,0)

pygame.init()
WIDTH, HEIGHT = 640, 480
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong')

FPS = 60

BALL_WIDTH, BALL_HEIGHT = 20,20
RACKET_WIDTH, RACKET_HEIGHT = 10, 100

RPOINT = pygame.USEREVENT + 1
LPOINT = pygame.USEREVENT + 2

game_font = pygame.font.SysFont('Biome', 40)
winner_font = pygame.font.SysFont('Biome', 80)

RACKET_BALL = pygame.mixer.Sound(os.path.join('resourcesExtra', 'pingPong.mp3'))
WIN_POINT = pygame.mixer.Sound(os.path.join('resourcesExtra', 'winPong.mp3'))

def main(): 
    global ball_speed_x, ball_speed_y 
    ball_speed_x = 6
    ball_speed_y = 6

    velocityX = 8
    velocityY = 8 

    clock = pygame.time.Clock()
    run = True

    ball = pygame.Rect(150,200,BALL_WIDTH, BALL_HEIGHT)
    playerR = pygame.Rect(WIDTH - 20, HEIGHT/2 - (RACKET_HEIGHT/2),RACKET_WIDTH,RACKET_HEIGHT)
    playerL = pygame.Rect(10, HEIGHT/2 - (RACKET_HEIGHT/2),RACKET_WIDTH,RACKET_HEIGHT)

    left_score = 0
    right_score = 0

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        ball.x += ball_speed_x
        ball.y += ball_speed_y

        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1
        if ball.left <=0 :
            right_score += 1
            ball.center = (WIDTH/2, HEIGHT/2)
            ball_speed_x *= random.choice((1,-1))
            ball_speed_y *= random.choice((1,-1))
        if ball.right >= WIDTH:
            left_score += 1
            ball.center = (WIDTH/2, HEIGHT/2)
            ball_speed_x *= random.choice((1,-1))
            ball_speed_y *= random.choice((1,-1))
        if ball.colliderect(playerL) or ball.colliderect(playerR):
            ball_speed_x *= -1
            RACKET_BALL.play()

        final_winner = ''
        if left_score == 10:
            final_winner = ' Left player'
        if right_score == 10:
            final_winner = ' Right player'
        if final_winner != '':
            WIN_POINT.play()
            draw_winner(final_winner)
            break

        keys_pressed = pygame.key.get_pressed()
        racketMovement(keys_pressed, playerL, playerR, velocityY, velocityX, ball)
        draw_window(ball, playerR, playerL, left_score, right_score, final_winner)

    main()
       
def draw_window(ball, playerR, playerL, left_score, right_score, final_winner):
    WIN.fill(BLACK)
    pygame.draw.aaline(WIN, GREY, (WIDTH/2,0),(WIDTH/2, HEIGHT ))
    pygame.draw.rect(WIN,RED, playerR)
    pygame.draw.rect(WIN,BLUE, playerL)
    pygame.draw.ellipse(WIN,GREY, ball)

    left_text = game_font.render(f"{left_score}", False, BLUE)
    right_text = game_font.render(f"{right_score}", False, RED)
    WIN.blit(left_text, (WIDTH/2 - 30, HEIGHT/2))
    WIN.blit(right_text, (WIDTH/2 + 20, HEIGHT/2))

    pygame.display.update()

def ballMovement(ball, ball_speed_x, ball_speed_y, playerL, playerR):
    
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1
    if ball.left <=0 or ball.right >= WIDTH:
        ball_restart(ball, ball_speed_x, ball_speed_y)
    if ball.colliderect(playerL) or ball.colliderect(playerR):
            ball_speed_x *= -1
            ball_speed_y *= -1

def racketMovement(keys_pressed, playerL, playerR, speedY, speedX, ball):

    if keys_pressed[pygame.K_w] and playerL.top >= 0:
        playerL.y -= speedY
    if keys_pressed[pygame.K_s] and playerL.bottom <= HEIGHT:
        playerL.y += speedY

    if keys_pressed[pygame.K_KP_8] and playerR.top >= 0:
        playerR.y -= speedY
    if keys_pressed[pygame.K_KP_5] and playerR.bottom <= HEIGHT:
        playerR.y += speedY

def ball_restart(ball, ball_speed_x, ball_speed_y):
    ball.center = (WIDTH/2, HEIGHT/2)
    ball_speed_x *= random.choice((1,-1))
    ball_speed_y *= random.choice((1,-1))

def draw_winner(final_winner):
    winner_text = game_font.render(f"{final_winner} is the Winner", False, WHITE)
    WIN.blit(winner_text, (WIDTH/2 - 180, HEIGHT/2 - 150))
    pygame.display.update()
    pygame.time.delay(6000)

if __name__ == "__main__":
    main()