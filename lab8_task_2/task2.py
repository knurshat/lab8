import pygame
import sys
import random
import time, os

# Цвета
blue = (50, 153, 213)
red = (255, 0, 0)
black = (0, 0, 0)
green = (50,213,153)
purple = (0,200, 100)

# Размеры окна
WIDTH = 600
HEIGHT = 400
snake_block = 10
LEVEL = 5

pygame.init()
pygame.mixer.init()

# Шрифты
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)

game_over_text = font.render("Game Over", True, black)
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

script_dir = os.path.dirname(__file__)

class Point(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        lemon1 = os.path.join(script_dir, "lemon.png")
        image = pygame.image.load(lemon1)
        self.image = pygame.transform.scale(image, (snake_block, snake_block))  # уравниваем размер монеты с размером змеи
        self.rect = self.image.get_rect()
        self.respawn()

    def respawn(self):
        grid_x = random.randint(0, (WIDTH // snake_block) - 1) * snake_block
        grid_y = random.randint(0, (HEIGHT // snake_block) - 1) * snake_block
        self.rect.topleft = (grid_x, grid_y)

def main():
    global LEVEL  # Используем глобальную переменную уровня

    game_over = False
    x1 = WIDTH // 2
    y1 = HEIGHT // 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    snake_length = 1  # Начинаем с 1 блока
    score = 0
    level = 0
    # Флаги для увеличения уровня
    level_up = {3: False, 10: False, 20: False, 35: False}

    # Создаём монету и группу спрайтов
    lemon = Point()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(lemon)
    sound1 = os.path.join(script_dir, "Sound_07127.mp3")
    pygame.mixer.Sound(sound1).play()
    while not game_over:
        DISPLAYSURF.fill(blue)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                
                #Кнопки    
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0

        # Двигаем змейку
        x1 += x1_change
        y1 += y1_change

        # Проверка столкновения с границами
        if x1 < 0 or x1 >= WIDTH or y1 < 0 or y1 >= HEIGHT:
            game_over = True

        # Проверка столкновения головы с телом змеи
        for segment in snake_list[:-1]:
            if segment == [x1, y1]:
                game_over = True

        # Обновляем змейку
        snake_head = [x1, y1]
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        # Проверка столкновения головы змеи с монетой
        if lemon.rect.collidepoint(x1, y1):
            coin_sound = os.path.join(script_dir, "coin-257878.mp3")
            pygame.mixer.Sound(coin_sound).play()
            snake_length += 1 
            score += 1
            lemon.respawn() 

        for segment in snake_list:
            pygame.draw.rect(DISPLAYSURF, black, [segment[0], segment[1], snake_block, snake_block])

        all_sprites.draw(DISPLAYSURF)

        # Отображение счёта
        score_text = font_small.render(f"Score: {score}", True, black)
        level_text = font_small.render(f"Level: {level}", True, black)
        DISPLAYSURF.blit(score_text, (10, 10))
        DISPLAYSURF.blit(level_text, (10, 30))

        # Увеличение уровня
        if score in level_up and not level_up[score]:
            if score == 3:
                pygame.mixer.stop()
                LEVEL += 3
                level += 1
                DISPLAYSURF.fill((204,204,0))
                sound1 = os.path.join(script_dir, "Sound_07128.mp3")
                pygame.mixer.Sound(sound1).play()
            elif score == 10:
                LEVEL += 4
                level += 1
                pygame.mixer.stop()
                DISPLAYSURF.fill(green)
                sound1 = os.path.join(script_dir, "Sound_07129.mp3")
                pygame.mixer.Sound(sound1).play()
            elif score == 20:
                LEVEL += 5
                level += 1
                pygame.mixer.stop()
                DISPLAYSURF.fill(purple)
                sound1 = os.path.join(script_dir, "Sound_07130.mp3")
                pygame.mixer.Sound(sound1).play()
            elif score == 35:
                LEVEL += 6
                level += 1
                pygame.mixer.stop()
                DISPLAYSURF.fill((100,100,100))
                sound1 = os.path.join(script_dir, "Sound_07131.mp3")
                pygame.mixer.Sound(sound1).play()
            level_up[score] = True  

        pygame.display.update()
        clock.tick(LEVEL)

    # "Game Over"
    pygame.mixer.stop()
    pygame.mixer.Sound("tyajelyiy-tupoy-udar.mp3").play()
    DISPLAYSURF.fill(red)
    # Сначало показываем очки
    DISPLAYSURF.blit(font.render(f"Your Score: {score}", True, black), (WIDTH // 4 - 50, HEIGHT // 3))
    pygame.display.update()
    time.sleep(2) 
    # Убираем очки наславанием текста
    DISPLAYSURF.blit(font.render(f"Your Score: {score}", True, red), (WIDTH // 4 - 50, HEIGHT // 3))
    # Отображаем "Game Over"
    DISPLAYSURF.blit(game_over_text, (WIDTH // 4, HEIGHT // 3))
    pygame.display.update()
    time.sleep(3) 
    pygame.quit()
    sys.exit()

main()
