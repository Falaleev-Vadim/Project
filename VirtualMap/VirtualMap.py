from vpython import color
import vpython as vp
import math
import time

# Список для хранения данных о выстрелах
shot_data = []

# Функция для расчета полета снаряда
def calculate_trajectory(v0, angle, aerodynamic_coefficient, projectile_mass, projectile_caliber, distance):
    g = 9.80665  # ускорение свободного падения, м/с^2
    p = 101325 # атмосферное давление, Па
    M = 28.98 # молярная масса, г/моль
    R = 8.314 # газовая постоянная, Дж/(моль*K)
    T = 288.15 # температура воздуха, K
    dt = 0.01 # дельта времени
    x = 0 # координата горизонта
    y = 0 # координата вертикали
    t = 0 # время полета снаряда

    # Площадь лобовой стороны снаряда
    S = math.pi * math.pow(projectile_caliber / 1000, 2) / 4

    # Плотность воздуха, кг/м^3
    air_density = (p * M / (R * T)) / 1000

    # полет снаряда с учетом силы аэродинамического сопротивления воздуха
    projectile_flight = aerodynamic_coefficient * S * air_density / (2 * projectile_mass)

    # Перевод угла в радианы
    angle_rad = math.radians(angle)
    
    # Координаты полета
    trajectory = []
    while(True):
        new_v = v0 - dt * (projectile_flight * math.pow(v0, 2) + g * math.sin(angle_rad))
        new_angle = angle_rad - dt * g * math.cos(angle_rad) / v0
        new_x = x + (v0 * math.cos(angle_rad)) * dt
        new_y = y + (v0 * math.sin(angle_rad)) * dt
        t += dt

        if new_y < 0:
            break

        v0 = new_v
        angle_rad = new_angle
        x = new_x
        y = new_y

        trajectory.append((x, y))
    
    return trajectory

# Функция запуска анимации
def launch_shot(v0, angle, aerodynamic_coefficient, projectile_mass, projectile_caliber, distance):
    # Площадка
    range_box = vp.box(pos=vp.vector(distance * 1000, -50, 0), size=vp.vector(5000, 1, 500), color=color.green)
    
    # Начальная позиция снаряда
    shot = vp.sphere(pos=vp.vector(0, 0, 0), radius=5, color=color.blue, make_trail=True, trail_color=color.white)

    # Получаем траекторию полета
    trajectory = calculate_trajectory(v0, angle, aerodynamic_coefficient, projectile_mass, projectile_caliber, distance)
    
    # Таймер
    timer_text = vp.wtext(text="Время: 0 секунд", width=200, height=50)
    
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
        'аэродинамический коэффициент': aerodynamic_coefficient,
        'масса снаряда': projectile_mass,
        'калибр снаряда': projectile_caliber,
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
        print(f"Скорость: {shot['скорость']} м/с")
        print(f"Угол: {shot['угол']}°")
        print(f"Аэродинамический коэффициент: {shot['аэродинамический коэффициент']}") 
        print(f"Масса снаряда: {shot['масса снаряда']} кг")
        print(f"Калибр снаряда: {shot['калибр снаряда']} мм")
        print(f"Расстояние: {shot['расстояние']} км")
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
    aerodynamic_coefficient = float(input("Введите аэродинамический коэффициент лобового сопротивления: "))
    projectile_mass = float(input("Введите массу снаряда (кг): "))
    projectile_caliber = float(input("Введите калибр снаряда (мм): "))
    distance = float(input("Введите расстояние до полигона (км): "))
    
    # Запуск анимации
    launch_shot(v0, angle, aerodynamic_coefficient, projectile_mass, projectile_caliber, distance)
    
    # После завершения запуска, показать историю выстрелов
    show_history()

# Запуск программы
create_gui()