import pygame

def draw_circle(screen, start, end, color):
    """Функция для рисования круга"""
    radius = int(((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2) ** 0.5)  # Вычисляем радиус
    pygame.draw.circle(screen, color, start, radius)  # Рисуем круг

def draw_rectangle(screen, start, end, color):
    """Функция для рисования прямоугольника"""
    rect = pygame.Rect(start, (end[0] - start[0], end[1] - start[1]))  # Создаем прямоугольник
    pygame.draw.rect(screen, color, rect)  # Рисуем прямоугольник

def get_color(color):
    """Функция выбора цвета"""
    colors = {
        'blue': (0, 0, 255),
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'black': (0, 0, 0)
    }
    return colors.get(color, (255, 255, 255))

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Paint Brush")
    clock = pygame.time.Clock()

    radius = 10  # Размер кисти
    mode = 'brush'  # Режим по умолчанию
    drawing = False  # Флаг рисования
    last_pos = None  # Последняя позиция мыши
    color = 'red'
    start_pos = None  # Начальная позиция для фигур

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                """Кнопки"""
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    """Кнопки для выбора фигур"""
                elif event.key == pygame.K_q:
                    mode = 'brush'
                elif event.key == pygame.K_w:
                    mode = 'rectangle'
                elif event.key == pygame.K_e:
                    mode = 'circle'
                    """"Кнопки выбора цвета"""
                elif event.key == pygame.K_1:
                    color = 'red'
                elif event.key == pygame.K_2:
                    color = 'green'
                elif event.key == pygame.K_3:
                    color = 'blue'
                elif event.key == pygame.K_0:
                    color = 'black'
                elif event.key == pygame.K_MINUS:
                    radius = max(1, radius - 2)
                elif event.key == pygame.K_EQUALS:
                    radius = min(50, radius + 2)

            # Начало рисования
            if event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
                start_pos = event.pos  # Запоминаем начальную позицию
                last_pos = event.pos  

            # Окончание рисования
            if event.type == pygame.MOUSEBUTTONUP:
                drawing = False
                end_pos = event.pos  # Запоминаем конечную позицию

                if mode == 'circle':
                    draw_circle(screen, start_pos, end_pos, get_color(color))
                elif mode == 'rectangle':
                    draw_rectangle(screen, start_pos, end_pos, get_color(color))

        # Проверка нажатия мыши (для кисти)
        if drawing and mode == 'brush':
            mouse_pos = pygame.mouse.get_pos()
            if last_pos:
                pygame.draw.line(screen, get_color(color), last_pos, mouse_pos, radius * 2)
            pygame.draw.circle(screen, get_color(color), mouse_pos, radius)
            last_pos = mouse_pos

        pygame.display.flip()
        clock.tick(120)

    pygame.quit()

main()
