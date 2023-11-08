import pygame

import random

import math

pygame.init()

#creating game window
screen=pygame.display.set_mode((800,600))

#Title and icon
title="Pumpkin Shooter"
icon=pygame.image.load('data/alien.png')
pygame.display.set_caption(title)
pygame.display.set_icon(icon)


#background image
BG=pygame.image.load('data/BGI.jpg')

# BGM
pygame.mixer.music.load('data/music(G).wav')
pygame.mixer.music.play(-1)
# music
bullet_music=pygame.mixer.Sound('data/gun_shot.wav')
explosion_music=pygame.mixer.Sound('data/explosion.wav')

game_status='running'

#score
score_font=pygame.font.Font('data/Aldrich-Regular.ttf',32)
score_x=10
score_y=10

#game over display
Game_over_font=pygame.font.Font('data/Aldrich-Regular.ttf',64)
game_over_x=200
game_over_y=210

# Restart
Restart_font=pygame.font.Font('data/Aldrich-Regular.ttf',40)
Restart_x=160
Restart_y=370

def Restart(x,y):
    Restart_image=Restart_font.render('To Restart Press R',True,(0,0,0))
    screen.blit(Restart_image,(x,y))

def game_over(x,y):
    global score
    global game_status
    Game_over_image=Game_over_font.render('GAME OVER',True,(255,255,255))
    pygame.mixer.music.stop()
    game_status='end'
    score=0
    screen.blit(Game_over_image,(x,y))


def show_score(x,y):
    score_image=score_font.render('SCORE : '+str(score),True,(255,255,255))
    screen.blit(score_image,(x,y))


#player image and co-ordinates
player_image = pygame.image.load('data/airplane.png')
player_image=pygame.transform.scale(player_image,(80,80))
player_x = 365
player_y = 500
player_x_change=0

# Enemy 
no_of_enemies=6
enemy_image=[]
enemy_img=[]
enemy_x =[]
enemy_y=[]
enemy_x_change=[]
enemy_y_change=[]


for i in range(no_of_enemies):
    enemy_image.append(pygame.image.load('data/villian.png'))
    enemy_x.append(random.randint(0,730))
    enemy_y.append(random.randint(0,250))
    enemy_img.append(pygame.transform.scale(enemy_image[i],(60,60)))
    enemy_x_change.append(1)
    enemy_y_change.append(40)

#bullet 
bullet_image=pygame.image.load('data/bullet.png')
bullet_image=pygame.transform.scale(bullet_image,(40,40))
bullet_x=0
bullet_y=500
bullet_state='ready'
bullet_y_change=2

# initially score
score=0

def is_collision(x1,x2,y1,y2):
    distance=math.sqrt(math.pow((x2-x1),2)+math.pow((y2-y1),2))
    if distance<50:
        return True
    else:
        return False

def bullet(x,y):
    screen.blit(bullet_image,(x,y))

def enemy(x,y,i):
    screen.blit(enemy_img[i],(x,y))

def player(x,y):
    screen.blit(player_image,(x,y))

################################################################
game_on=True
while game_on:
    # just background and real background image
    screen.fill((45,51,71))
    screen.blit(BG,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:    # when it comes in event.get list it works
            game_on=False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change=-1

            if event.key == pygame.K_RIGHT:
                player_x_change=1

            if event.key == pygame.K_SPACE:
                bullet_state='fire'
                if bullet_y==500:
                    bullet_x=player_x+20
                    bullet_music.play()
                bullet(bullet_x,bullet_y)

            if event.key==pygame.K_r:
                pygame.mixer.music.play(-1)
                player_x = 365
                if game_status=='end':
                    game_status='running'
                    for i in range(no_of_enemies):
                        enemy_x[i]= random.randint(0,730)
                        enemy_y[i]= random.randint(0,200)
                        
                   
                
        if event.type== pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player_x_change=0
                
            if event.key == pygame.K_RIGHT:
                player_x_change=0

    
    # collision
    for i in range(no_of_enemies):
        collision=is_collision(enemy_x[i],bullet_x,enemy_y[i],bullet_y)
        if collision==True:
            bullet_y=player_y
            bullet_state='ready'
            if enemy_y[i]<415:
                score+=1
                explosion_music.play()
            enemy_x[i]= random.randint(0,730)
            enemy_y[i]= random.randint(0,300)

    #score
    show_score(score_x,score_y)

    #player movements

    player_x+=player_x_change
    
    if player_x < 0:
        player_x=0
        
    elif player_x > 730:
        player_x=730
        

    #enemy movements
    for i in range(no_of_enemies):
        # Game over
        if enemy_y[i]>440:
            game_over(game_over_x,game_over_y)
            Restart(Restart_x,Restart_y)
            for j in range(no_of_enemies):
                enemy_y[j]=1200
                
        #********
        enemy_x[i]+=enemy_x_change[i]
        if enemy_x[i] < 0:
            enemy_x_change[i]=0.7
            enemy_y[i]+=enemy_y_change[i]
        elif enemy_x[i]> 730:
            enemy_x_change[i]=-0.7
            enemy_y[i]+=enemy_y_change[i]
    
    # bullet
    if bullet_state == 'fire':
        bullet(bullet_x,bullet_y)
        if bullet_y>10:
            bullet_y-=bullet_y_change
        else:
            bullet_y=500
            bullet_state='ready'
        
    player(player_x,player_y)
    for j in range(no_of_enemies):
        enemy(enemy_x[j],enemy_y[j],j)
    pygame.display.update()
