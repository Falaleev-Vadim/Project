import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import tkinter as tk
from tkinter import messagebox

def calculate_trajectory(v0, angle, g=9.81, time_step=0.01):
    angle_rad = np.radians(angle)
    
    v0x = v0 * np.cos(angle_rad)
    v0y = v0 * np.sin(angle_rad)
    
    t_max = 2 * v0y / g
    time_points = np.arange(0, t_max, time_step)
    
    x = v0x * time_points
    y = v0y * time_points - 0.5 * g * time_points**2
    
    return x[y >= 0], y[y >= 0]

def update(frame, x, y, line, time_text, coords_text):
    if frame < len(x):
        line.set_data(x[:frame], y[:frame])
        time_text.set_text(f"Time: {frame * 0.01:.2f} s")
        coords_text.set_text(f"Coords: ({x[frame]:.2f}, {y[frame]:.2f})")
    return line, time_text, coords_text

def start_animation():
    global line, time_text, coords_text, x, y, anim

    try:
        speed = float(speed_entry.get())
        angle = float(angle_entry.get())
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректные значения скорости и угла.")
        return

    x, y = calculate_trajectory(speed, angle)

    fig, ax = plt.subplots()
    ax.set_xlim(0, 65000)
    ax.set_ylim(0, max(y) + 10)
    ax.set_title("Траектория полета снаряда")
    ax.set_xlabel("X (м)")
    ax.set_ylabel("Y (м)")
    
    line, = ax.plot([], [], lw=2)
    time_text = ax.text(0.7, 0.9, "", transform=ax.transAxes)
    coords_text = ax.text(0.7, 0.85, "", transform=ax.transAxes)

    anim = FuncAnimation(fig, update, frames=len(x), fargs=(x, y, line, time_text, coords_text), interval=10, blit=True)
    plt.show()

    saved_coords.append((x[-1], y[-1]))

def show_coordinates():
    coords_str = "\n".join([f"X: {coord[0]:.2f}, Y: {coord[1]:.2f}" for coord in saved_coords])
    if coords_str:
        messagebox.showinfo("Координаты падения", coords_str)
    else:
        messagebox.showinfo("Координаты падения", "Нет записанных координат.")

saved_coords = []

root = tk.Tk()
root.title("Симуляция полета снаряда")

tk.Label(root, text="Начальная скорость (м/с):").pack()
speed_entry = tk.Entry(root)
speed_entry.pack()

tk.Label(root, text="Угол выстрела (градусы):").pack()
angle_entry = tk.Entry(root)
angle_entry.pack()

start_button = tk.Button(root, text="Запустить анимацию", command=start_animation)
start_button.pack()

show_button = tk.Button(root, text="Показать координаты", command=show_coordinates)
show_button.pack()

root.mainloop()