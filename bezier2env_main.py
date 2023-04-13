import pygame
import sys
import numpy as np
from math import comb
import tkinter as tk
from reapy_boost import reascript_api as RPR

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

def set_intersection_count():
    global intersection_count
    try:
        intersection_count = int(entry.get())
        root.destroy()
    except ValueError:
        pass

root = tk.Tk()
root.title("Set Intersection Count")

label = tk.Label(root, text="Enter Intersection Count (2-500):")
label.pack()

entry = tk.Entry(root)
entry.pack()

submit_button = tk.Button(root, text="Submit", command=set_intersection_count)
submit_button.pack()

center_window(root)
root.mainloop()

intersection_count = min(max(intersection_count, 2), 500)
intersection_coords = []

pygame.init()

screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Bezier Curve")

start_point = (0, 250)
end_point = (500, 250)
control_points = [start_point, (250, 250), end_point]

go_button = pygame.Rect(450, 450, 50, 50)
go_button_color = (102, 204, 102)
go_button_pressed = False

reset_button = pygame.Rect(350, 450, 50, 50)
reset_button_color = (204, 102, 102)
reset_button_pressed = False

flip_ud_button = pygame.Rect(400, 450, 50, 50)
flip_ud_button_color = (102, 102, 204)
flip_ud_button_pressed = False

points_button = pygame.Rect(280, 450, 70, 50)
points_button_color = (153, 153, 255)
points_button_pressed = False

def bezier_point(t, control_points):
    n = len(control_points) - 1
    x = sum((1 - t) ** (n - i) * t ** i * p[0] * comb(n, i) for i, p in enumerate(control_points))
    y = sum((1 - t) ** (n - i) * t ** i * p[1] * comb(n, i) for i, p in enumerate(control_points))
    return x, y

running = True
dragging = False
dragged_point_idx = None

while running:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for idx, point in enumerate(control_points):
                    if abs(event.pos[0] - point[0]) < 10 and abs(event.pos[1] - point[1]) < 10:
                        dragging = True
                        dragged_point_idx = idx
            if go_button.collidepoint(event.pos):
                go_button_pressed = True
            if reset_button.collidepoint(event.pos):
                reset_button_pressed = True
            if flip_ud_button.collidepoint(event.pos):
                flip_ud_button_pressed = True
            if points_button.collidepoint(event.pos):
                points_button_pressed = True
            
            elif event.button == 3:
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    control_points.insert(-1, event.pos)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for idx, point in enumerate(control_points):
                    if abs(event.pos[0] - point[0]) < 10 and abs(event.pos[1] - point[1]) < 10:
                        dragging = True
                        dragged_point_idx = idx
            if go_button.collidepoint(event.pos):
                go_button_pressed = True
            if reset_button.collidepoint(event.pos):
                reset_button_pressed = True
            if flip_ud_button.collidepoint(event.pos):
                flip_ud_button_pressed = True
            if points_button.collidepoint(event.pos):
                points_button_pressed = True

    if event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
            dragging = False
            dragged_point_idx = None

            if go_button_pressed and go_button.collidepoint(event.pos):
                
                env = RPR.GetSelectedTrackEnvelope(0)

                is_set, is_loop, start_time, end_time, allow_auto_seek = RPR.GetSet_LoopTimeRange(False, False, 0, 0, False)

                RPR.DeleteEnvelopePointRange(env, start_time, end_time)

                for t in np.linspace(0, 1, intersection_count):
                    x, y = bezier_point(t, control_points)
                    time = start_time + t * (end_time - start_time)
                    value = 1 - (y / 500)
                    RPR.InsertEnvelopePoint(env, time, value, 0, 0, True, True)

                RPR.Envelope_SortPoints(env)

                go_button_pressed = False

            if reset_button_pressed and reset_button.collidepoint(event.pos):
                control_points = [start_point, (250, 250), end_point]
                reset_button_pressed = False
                flip_ud_active = False  

            if flip_ud_button_pressed and flip_ud_button.collidepoint(event.pos):
                control_points = [(p[0], 500 - p[1]) for p in control_points]
                flip_ud_button_pressed = False

            if points_button_pressed and points_button.collidepoint(event.pos):
                root = tk.Tk()
                root.title("Set Intersection Count")

                label = tk.Label(root, text="Enter Intersection Count (2-500):")
                label.pack()

                entry = tk.Entry(root)
                entry.pack()

                submit_button = tk.Button(root, text="Submit", command=set_intersection_count)
                submit_button.pack()

                center_window(root)
                root.mainloop()

                intersection_count = min(max(intersection_count, 2), 500)
                points_button_pressed = False

    if event.type == pygame.MOUSEMOTION:
        if dragging:
            new_pos = event.pos
            if dragged_point_idx == 0 or dragged_point_idx == len(control_points) - 1:
                new_pos = (control_points[dragged_point_idx][0], event.pos[1])
            control_points[dragged_point_idx] = new_pos

    grid_size = 10
    grid_step = 50
    for i in range(grid_size + 1):
        x = i * grid_step
        pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, 500))
        pygame.draw.line(screen, (200, 200, 200), (0, x), (500, x))
        font = pygame.font.SysFont('Arial', 12)  
        text_surface = font.render(f"{1 - i / 10:.1f}", True, (32, 32, 32))
        screen.blit(text_surface, (0, i * grid_step - 7))

    for point in control_points:
        pygame.draw.circle(screen, (255, 0, 0), point, 5)

    for t in np.linspace(0, 1, 1000):
        x, y = bezier_point(t, control_points)
        pygame.draw.circle(screen, (0, 0, 0), (int(x), int(y)), 1)

    for t in np.linspace(0, 1, intersection_count):
        x, y = bezier_point(t, control_points)
        pygame.draw.circle(screen, (128, 128, 128), (int(x), int(y)), 3)

    description_text = (
    "RIGHTCLICK+SHIFT = ADD POINT\n"
    )

    description_font = pygame.font.SysFont("Arial", 12)
    description_lines = description_text.split("\n")
    description_y = 480

    for line in description_lines:
        description_surface = description_font.render(line, True, (0, 0, 0))
        screen.blit(description_surface, (10, description_y))
        description_y += 15

    pygame.draw.rect(screen, go_button_color, go_button)
    pygame.draw.rect(screen, reset_button_color, reset_button)
    pygame.draw.rect(screen, flip_ud_button_color, flip_ud_button)
    pygame.draw.rect(screen, points_button_color, points_button)

    font = pygame.font.SysFont('Arial', 14)
    go_text = font.render("GO", True, (0, 0, 0))
    reset_text = font.render("Reset", True, (0, 0, 0))
    flip_ud_text = font.render("UD", True, (0, 0, 0))
    points_text = font.render("Points", True, (0, 0, 0))

    go_text_rect = go_text.get_rect(center=go_button.center)
    reset_text_rect = reset_text.get_rect(center=reset_button.center)
    flip_ud_text_rect = flip_ud_text.get_rect(center=flip_ud_button.center)
    points_text_rect = points_text.get_rect(center=points_button.center)

    screen.blit(go_text, go_text_rect)
    screen.blit(reset_text, reset_text_rect)
    screen.blit(flip_ud_text, flip_ud_text_rect)
    screen.blit(points_text, points_text_rect)


    pygame.display.flip()

pygame.quit()

