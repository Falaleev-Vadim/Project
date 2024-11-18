import numpy as np
import plotly.graph_objects as go
import tkinter as tk
from tkinter import messagebox

def calculate_trajectory(v0, angle, phi, g=9.81, time_step=0.01):
    # Перевод углов в радианы
    angle_rad = np.radians(angle)
    phi_rad = np.radians(phi)
    
    # Начальная скорость по осям
    v0x = v0 * np.cos(angle_rad) * np.cos(phi_rad)
    v0y = v0 * np.sin(angle_rad)
    v0z = v0 * np.cos(angle_rad) * np.sin(phi_rad)
    
    # Время полета
    t_max = 2 * v0y / g  # Время до падения на землю
    time_points = np.arange(0, t_max, time_step)
    
    # Координаты в 3D
    x = v0x * time_points
    y = v0y * time_points - 0.5 * g * time_points**2
    z = v0z * time_points - 0.5 * g * time_points**2
    
    return x[y >= 0], y[y >= 0], z[y >= 0], t_max

def start_animation():
    global x, y, z, time_max, saved_coords
    
    try:
        speed = float(speed_entry.get())
        angle = float(angle_entry.get())
        phi = float(phi_entry.get())  # Дополнительный угол для оси Z
        max_x = float(max_x_entry.get())
        max_y = float(max_y_entry.get())
        max_z = float(max_z_entry.get())
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректные значения.")
        return

    # Вычисление траектории
    x, y, z, time_max = calculate_trajectory(speed, angle, phi)

    # Ограничиваем максимальные значения
    x = np.clip(x, 0, max_x)
    y = np.clip(y, 0, max_y)
    z = np.clip(z, 0, max_z)

    # Создаем 3D-график
    fig = go.Figure(
        data=[go.Scatter3d(x=x, y=y, z=z, mode='lines', line=dict(color='blue', width=4))],
        layout=go.Layout(
            title="Траектория полета снаряда",
            scene=dict(
                xaxis_title='X (м)',
                yaxis_title='Y (м)',
                zaxis_title='Z (м)',
                xaxis=dict(range=[0, max_x]),
                yaxis=dict(range=[0, max_y]),
                zaxis=dict(range=[0, max_z]),
            ),
            updatemenus=[dict(
                type='buttons',
                showactive=False,
                buttons=[dict(
                    label='Анимация',
                    method='animate',
                    args=[None, dict(frame=dict(duration=0.1, redraw=True), fromcurrent=True)],
                )],
            )],
        )
    )

    # Анимация
    frames = [go.Frame(
        data=[go.Scatter3d(x=x[:k], y=y[:k], z=z[:k], mode='lines', line=dict(color='blue', width=4))],
        name=f'Frame{k}'
    ) for k in range(1, len(x) + 1)]

    fig.frames = frames

    # Добавляем текст времени
    fig.add_annotation(
        x=0.95, y=0.95,  # Используем только x и y для аннотации
        text=f"Time: 0.00 s",
        showarrow=False,
        font=dict(size=16, color="black"),
        align="center",
        xref="paper", yref="paper"
    )

    # Обновляем время на графике
    def update_time(frame):
        time_str = f"Time: {frame * 0.01:.2f} s"
        fig.layout.annotations[0].update(text=time_str)

    # Анимация обновления времени
    fig.frames = [go.Frame(
        data=[go.Scatter3d(x=x[:k], y=y[:k], z=z[:k], mode='lines', line=dict(color='blue', width=4))],
        name=f'Frame{k}',
        layout=dict(
            annotations=[dict(
                x=0.95, y=0.95,  # Обновляем аннотацию с только x и y
                text=f"Time: {k * 0.01:.2f} s",
                showarrow=False,
                font=dict(size=16, color="black"),
                align="center",
                xref="paper", yref="paper"
            )]
        )
    ) for k in range(1, len(x) + 1)]

    # Отображаем график
    fig.show()

    # Записываем координаты падения
    saved_coords.append((x[-1], y[-1], z[-1]))

def show_coordinates():
    coords_str = "\n".join([f"X: {coord[0]:.2f}, Y: {coord[1]:.2f}, Z: {coord[2]:.2f}" for coord in saved_coords])
    if coords_str:
        messagebox.showinfo("Координаты падения", coords_str)
    else:
        messagebox.showinfo("Координаты падения", "Нет записанных координат.")

saved_coords = []

# Создание окна Tkinter
root = tk.Tk()
root.title("Симуляция полета снаряда")

# Настройки для начальной скорости и угла
tk.Label(root, text="Начальная скорость (м/с):").pack()
speed_entry = tk.Entry(root)
speed_entry.pack()

tk.Label(root, text="Угол выстрела (градусы):").pack()
angle_entry = tk.Entry(root)
angle_entry.pack()

tk.Label(root, text="Угол наклона по оси Z (градусы):").pack()
phi_entry = tk.Entry(root)
phi_entry.pack()

# Настройки для максимальных значений осей
tk.Label(root, text="Макс. X (м):").pack()
max_x_entry = tk.Entry(root)
max_x_entry.pack()

tk.Label(root, text="Макс. Y (м):").pack()
max_y_entry = tk.Entry(root)
max_y_entry.pack()

tk.Label(root, text="Макс. Z (м):").pack()
max_z_entry = tk.Entry(root)
max_z_entry.pack()

# Кнопка для запуска анимации
start_button = tk.Button(root, text="Запустить анимацию", command=start_animation)
start_button.pack()

# Кнопка для отображения координат
show_button = tk.Button(root, text="Показать координаты", command=show_coordinates)
show_button.pack()

root.mainloop()