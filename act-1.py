import math
import random
import pygame
screen_width=800
screen_height=500
player_start_x=370
player_start_y=380
enemy_start_y_min=50
enemy_start_y_max=150
enemy_speed_x=4
enemy_speed_y=40
bullet_speed_y=10
collision_distance=27

pygame.init()
screen=pygame.display.set_mode((screen_width,screen_height))
background=pygame.image.load("BACKGROUND.png")
pygame.display.set_caption("Space Game")

playerimg=pygame.image.load("PLAYER.png")
playerX=player_start_x
playerY=player_start_y
playerX_change=0

enemyimg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
n_of_enemy=6

for _i in range(n_of_enemy):
    enemyimg.append(pygame.image.load("ENEMY.png"))
    enemyX.append(random.randint(0,screen_width-64))
    enemyY.append(random.randint(enemy_start_y_min,enemy_start_y_max))
    enemyX_change.append(enemy_speed_x)
    enemyY_change.append(enemy_speed_y)

bulletimg=pygame.image.load("BULLET.png")
bulletX=0
bulletY=player_start_y
bulletX_change=0
bulletY_change=bullet_speed_y
bullet_state="ready"

score_value=0
font=pygame.font.Font("freesansbold.ttf",30)
textX=10
textY=10
over_font=pygame.font.Font("freesansbold.ttf",60)

def show_score(x,y):
    score=font.render("Score:"+str(score_value),True,"white")
    screen.blit(score,(x,y))

def game_over_text():
    over_text=over_font.render("Game Over:",True,"white")
    screen.blit(over_text,(200,250))

def player(x,y):
    screen.blit(playerimg,(x,y))
def enemy(x,y,i):
    screen.blit(enemyimg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletimg,(x+16,y+10))

def iscollision(enemyX,enemyY,bulletX,bulletY):
    dist=math.sqrt(math.pow(enemyX-bulletX,2)+math.pow(enemyY-bulletY,2))
    if dist<27:
        return True
    else:
        return False
    
running=True
while running:
    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.KEYDOWN:
            if event.type==pygame.K_LEFT:
                playerX_change=-5
            if event.type==pygame.K_RIGHT:
                playerX_change=5
            if event.type==pygame.K_SPACE and bullet_state=="ready":
                
                    bulletX=playerX
                    fire_bullet(bulletX,bulletY)
        if event.type==pygame.KEYUP and event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
            playerX_change=0
    
    playerX=playerX+playerX_change
    if playerX<=0:
        playerX=0
    elif playerX>=730:
        playerX=730
    
    for i in range(n_of_enemy):
        if enemyY[i]>340:
            for j in range(n_of_enemy):
                enemyY[j]=2000
            game_over_text()
            break
        enemyX[i]+=enemyX_change[i]
        if enemyX[i]<0 or enemyX[i]>736:
            enemyX_change[i]*=-1
            enemyY[i]+=enemyY_change[i]
    
        collision=iscollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            bulletY=380
            bullet_state="ready"
            score_value+=1
            enemyX[i]=random.randint(0,736)
            enemyY[i]=random.randint(50,150)
    
        enemy(enemyX[i],enemyY[i],i)
    if bulletY<=0:
        bulletY=380
        bullet_state="ready"
    if bullet_state=="fire":
        fire_bullet(bulletX,bulletY)
        bulletY-=bulletY_change
    player(playerX,playerY)   
    show_score(textX,textY)
    pygame.display.update()