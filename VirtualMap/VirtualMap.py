from vpython import color
import vpython as vp
import math
import time

# Список для хранения данных о выстрелах
shot_data = []

# Функция для расчета полета снаряда
def calculate_trajectory(v0, angle, distance):
    # Константы
    g = 9.81  # ускорение свободного падения, м/с^2
    
    # Перевод угла в радианы
    angle_rad = math.radians(angle)
    
    # Начальные компоненты скорости
    v0x = v0 * math.cos(angle_rad)  # скорость по оси X
    v0y = v0 * math.sin(angle_rad)  # скорость по оси Y
    
    # Время полета до приземления (формула для снаряда)
    t_flight = (2 * v0y) / g
    
    # Максимальное время для анимации (максимальная продолжительность полета)
    max_time = t_flight
    
    # Координаты полета
    trajectory = []
    for t in range(0, int(t_flight * 100), 1):  # шаг 0.01 секунды
        t_sec = t / 100
        x = v0x * t_sec  # координата по оси X
        y = v0y * t_sec - 0.5 * g * t_sec**2  # координата по оси Y
        if y < 0:  # Если снаряд приземлился, остановим расчет
            break
        trajectory.append((x, y))
    
    return trajectory, max_time

# Функция запуска анимации
def launch_shot(v0, angle, distance):
    # Площадка
    range_box = vp.box(pos=vp.vector(distance * 1000, -50, 0), size=vp.vector(5000, 1, 500), color=vp.color.green)
    
    # Мишень (на площадке)
    # target = vp.box(pos=vp.vector(distance * 1000, 0, 0), size=vp.vector(500, 1, 500), color=vp.color.red)
    
    # Начальная позиция снаряда
    shot = vp.sphere(pos=vp.vector(0, 0, 0), radius=5, color=vp.color.blue, make_trail=True, trail_color=vp.color.white)
    
    # Получаем траекторию полета
    trajectory, max_time = calculate_trajectory(v0, angle, distance)
    
    # Таймер
    timer_text = vp.label(pos=vp.vector(0, 100, 0), text="Время: 0.00 с", height=20, color=vp.color.white)
    
    # Начинаем анимацию
    start_time = time.time()
    for t, (x, y) in enumerate(trajectory):
        dt = time.time() - start_time
        shot.pos = vp.vector(x, y, 0)
        timer_text.text = f"Время: {dt:.2f} с"
        vp.rate(60)  # скорость анимации
    
    # Снаряд приземлился, сохраняем результат
    landing_coords = (shot.pos.x, shot.pos.y)
    flight_time = time.time() - start_time
    
    # Сохраняем данные о выстреле
    shot_data.append({
        'скорость': v0,
        'угол': angle,
        'расстояние': distance,
        'координаты приземления': landing_coords,
        'время полета': flight_time
    })
    
    # Возвращаем траекторию в список
    return shot_data

# Функция для вывода истории выстрелов
def show_history():
    if len(shot_data) == 0:
        print("Нет данных о выстрелах.")
        return
    
    print("История выстрелов:")
    for i, shot in enumerate(shot_data, 1):
        print(f"Выстрел {i}:")
        print(f"Скорость: {shot['скорость']} м/с, Угол: {shot['угол']}°, Расстояние: {shot['расстояние']} км")
        print(f"Координаты приземления: {shot['координаты приземления']}")
        print(f"Время полета: {shot['время полета']:.2f} с")
        print("-" * 50)

# Главная функция для создания интерфейса
def create_gui():
    # Создаем окно
    scene = vp.canvas(title="Анимация полета снаряда", width=800, height=600, background = color.gray(0.5))
    
    # Ввод данных
    v0 = float(input("Введите начальную скорость снаряда (м/с): "))
    angle = float(input("Введите угол выстрела (градусы): "))
    distance = float(input("Введите расстояние до полигона (км): "))
    
    # Запуск анимации
    launch_shot(v0, angle, distance)
    
    # После завершения запуска, показать историю выстрелов
    show_history()

# Запуск программы
create_gui()