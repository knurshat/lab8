
import pygame, sys
from pygame.locals import *
import random, time, os

  
pygame.init()
  
FPS = 60
FramePerSec = pygame.time.Clock()
 
#Цвета
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
#Переменные
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COIN_SCORE = 0

# Для отображения текста в будущем
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)
script_dir = os.path.dirname(__file__)
image_path = os.path.join(script_dir,  "street.png")

background = pygame.image.load(image_path)
background = pygame.transform.scale(background, (400, 600))


DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

t1 = os.path.join(script_dir,  "1.mp3")
t2 = os.path.join(script_dir,  "2.mp3")
t3 = os.path.join(script_dir,  "3.mp3")
tracks = [t1, t2, t3]
current_track = 0

pygame.mixer.music.load(tracks[current_track])
pygame.mixer.music.play(-1)
#Класс врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        image_path = os.path.join(script_dir,  "Enemy.png")
        image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(image, (40, 80))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(-600, -100))  
        self.delay = random.randint(30, 90)  # Задержка в кадрах перед началом движения, чтобы машинки не появлялись одновременно

    def move(self):
        global SCORE
        if self.delay > 0:
            self.delay -= 1  # Уменьшаем задержку, пока не дойдет до 0
            return  # Пока задержка > 0, враг не двигается
        
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = random.randint(-600, -100)  # Спавним выше экрана
            self.rect.centerx = random.randint(40, SCREEN_WIDTH - 40)
            self.delay = random.randint(30, 90)
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        image_path = os.path.join(script_dir,  "coin.png")
        image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(image,(30,30))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
    def move(self):
        global COIN_SCORE
        self.rect.move_ip(0,5)
        if (self.rect.top > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        image_path = os.path.join(script_dir, "Player.png")
        image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(image, (30,70))
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        
    def move(self):
        pressed_keys = pygame.key.get_pressed()
         
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)
                   
#Спрайты      
P1 = Player()
E1 = Enemy()
E2 = Enemy()
C1 = Coin()
C2 = Coin()
C3 = Coin()
#Создание скриптовых групп
enemies = pygame.sprite.Group()
enemies.add(E1)
enemies.add(E2)
coins = pygame.sprite.Group()
coins.add(C1)
coins.add(C2)
coins.add(C3)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(E2)
all_sprites.add(C1)
all_sprites.add(C2)
all_sprites.add(C3)
 

INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

while True:

    for event in pygame.event.get():
        if event.type == INC_SPEED:
              SPEED += 0.5     
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                current_track = (current_track + 1) % len(tracks)
                pygame.mixer.music.load(tracks[current_track])
                pygame.mixer.music.play(-1)
    DISPLAYSURF.blit(background, (0,0))
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))
    scores = font_small.render("Score: " + str(SCORE), True, BLACK)
    coin_scores = font_small.render("Coins: " + str(COIN_SCORE), True, BLACK)
    DISPLAYSURF.blit(coin_scores, (SCREEN_WIDTH - coin_scores.get_width() - 10, 10))

    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()
    collected_coin = pygame.sprite.spritecollideany(P1, coins)
    if collected_coin:
        coin_sound = os.path.join(script_dir, 'coin-257878.mp3')
        pygame.mixer.Sound(coin_sound).play()
        COIN_SCORE += 1
        collected_coin.kill() 
        new_coin = Coin()  
        coins.add(new_coin)
        all_sprites.add(new_coin)
        coin_score = font.render(f"Score: {COIN_SCORE}",True, BLACK)
    if pygame.sprite.spritecollideany(P1, enemies):
            pygame.mixer.music.stop()
            soundq = os.path.join(script_dir, 'car-crash-sfx.wav')
            pygame.mixer.Sound(soundq).play()
            time.sleep(0.5)
                    
            DISPLAYSURF.fill(RED)
            DISPLAYSURF.blit(game_over, (30,270))
            DISPLAYSURF.blit(coin_score, (30,320))
            pygame.display.update()
            for entity in all_sprites:
                entity.kill() 
            time.sleep(3)
            pygame.quit()
            sys.exit()        
         
    pygame.display.update()
    FramePerSec.tick(FPS)