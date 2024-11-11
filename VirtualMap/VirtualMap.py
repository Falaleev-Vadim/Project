import pygame
import numpy as np
import math
import time

# Инициализация Pygame
pygame.init()

# Параметры окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Симуляция полета снарядов")

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Константы
g = 9.81  # Ускорение свободного падения (м/с²)

# Параметры полигона
polygon_width = 500  # Ширина полигона в метрах
polygon_length = 5000  # Длина полигона в метрах
scale = 0.1  # Масштабирование (10 пикселей = 1 метр)

# Точка старта снаряда
start_x, start_y = -100, 300  # Начальная позиция снаряда за пределами полигона

# Список для записи координат падения снарядов
impact_points = []

# Параметры полета снаряда (изначальные)
v0 = 100  # Начальная скорость (м/с)
angle = 45  # Угол (градусы)

# Функция расчета траектории снаряда
def calculate_trajectory(v0, angle, dt=0.1):
    # Начальные условия
    angle_rad = math.radians(angle)
    vx = v0 * math.cos(angle_rad)
    vy = v0 * math.sin(angle_rad)
    
    # Списки для координат
    x_positions = [start_x]
    y_positions = [start_y]

    # Время полета
    t = 0
    while True:
        # Расчет новых координат
        t += dt
        x = start_x + vx * t
        y = start_y + vy * t - 0.5 * g * t**2
        
        # Добавляем новые координаты
        x_positions.append(x)
        y_positions.append(y)

        # Если снаряд упал на землю (y < 0), выходим из цикла
        if y <= 0:
            break

    return x_positions, y_positions

# Функция для отображения интерфейса
def display_info(v0, angle, impact_point):
    font = pygame.font.Font(None, 36)
    info_text = f"Скорость: {v0} м/с, Угол: {angle}°"
    text = font.render(info_text, True, BLACK)
    screen.blit(text, (10, 10))
    
    # Запись координат падения снаряда
    if impact_point:
        x, y = impact_point
        impact_text = f"Место падения: ({x:.2f}, {y:.2f})"
        impact = font.render(impact_text, True, BLACK)
        screen.blit(impact, (10, 50))

# Функция для рисования кнопки
def draw_button(text, x, y, width, height):
    font = pygame.font.Font(None, 36)
    pygame.draw.rect(screen, BLUE, (x, y, width, height))
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, (x + 10, y + 10))

# Главный цикл программы
running = True
clock = pygame.time.Clock()

# Стартовая траектория (еще не запущен полет)
x_positions, y_positions = [], []

# Местоположение кнопки для старта
button_x, button_y = 600, 50
button_width, button_height = 150, 50
flight_started = False

while running:
    screen.fill(WHITE)

    # Отображение полигона
    pygame.draw.rect(screen, GREEN, (0, HEIGHT-100, polygon_length * scale, 100))  # Поле
    pygame.draw.rect(screen, GREEN, (0, 0, polygon_width * scale, HEIGHT))  # Поле

    # Отображение кнопки "Запустить полет"
    draw_button("Запустить полет", button_x, button_y, button_width, button_height)

    # Отображение информации о снаряде
    display_info(v0, angle, impact_points[-1] if impact_points else None)

    # Проверка нажатия кнопки
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()[0]
    if (button_x <= mouse_x <= button_x + button_width and
        button_y <= mouse_y <= button_y + button_height and
        mouse_click):
        if not flight_started:  # Только если полет не запущен
            flight_started = True
            x_positions, y_positions = calculate_trajectory(v0, angle)  # Пересчитываем траекторию

    # Анимация полета снаряда
    if flight_started:
        for i in range(1, len(x_positions)):
            # Рисуем снаряд по координатам
            pygame.draw.circle(screen, RED, (int(x_positions[i]), HEIGHT - int(y_positions[i])), 5)
            pygame.display.flip()
            time.sleep(0.05)  # Пауза для анимации

        # Записываем место падения
        impact_points.append((x_positions[-1], y_positions[-1]))
        flight_started = False  # Сбрасываем состояние после завершения полета

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)  # 60 FPS

pygame.quit()