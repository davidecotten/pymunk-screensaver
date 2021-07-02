import os
import sys
import math
import time
import pymunk
import pyglet
import random
import pickle
import hashlib
import pygame
from pyglet.window import key
from pymunk.pyglet_util import DrawOptions

# Config
ESCAPED_KEYS = [key.LALT, key.RALT, key.F9]
RECALCULATE = True
GRAVITY = 0
FRICTION = 0.1
ELASTICITY = 0.8


def sha_256(file_path):
    with open(file_path, 'rb') as file:
        sha = hashlib.sha256()
        while True:
            file_buffer = file.read(4096)
            sha.update(file_buffer)
            if len(file_buffer) == 0:
                break
        return sha.hexdigest()


def get_rgba_pixel(img, x, y):
    img_data = img.get_region(x, y, 1, 1).get_image_data()
    pixel_data = img_data.get_data("RGBA", 4)
    return [n for n in pixel_data]


def get_vertices(img_path):
    img_hash = sha_256(img_path)
    vertex_file = f"{img_hash}.dat"
    vertex_path = os.path.join(sys.path[0], "vertices", vertex_file)
    if os.path.exists(vertex_path) and not RECALCULATE:
        with open(vertex_path, "rb") as file:
            return pickle.load(file)
    img = pyglet.image.load(img_path)
    pygame_img = pygame.image.load(img_path)
    center_x = img.width // 2
    center_y = img.height // 2
    largest = img.width
    if img.height > largest:
        largest = img.height
    vertices = []
    interval = int(largest / 100)
    if interval == 0:
        interval = 1
    surface.fill((0, 0, 0))
    pygame_x = (pygame_width // 2) - (img.width // 2)
    pygame_y = (pygame_height // 2) - (img.height // 2)
    surface.blit(pygame_img, (pygame_x, pygame_y))
    for theta in range(0, 360, 5):
        for i in range(0, largest, interval):
            x = int(center_x + (math.cos(math.radians(theta)) * i))
            y = int(center_y + (math.sin(math.radians(theta)) * i))
            try:
                pixel = get_rgba_pixel(img, x, y)
                if pixel[-1] == 0:
                    break
            except IndexError:
                x = int(center_x + (math.cos(math.radians(theta)) * (i - interval)))
                y = int(center_y + (math.sin(math.radians(theta)) * (i - interval)))
                break
        pygame.draw.circle(surface, (255, 0, 0), (pygame_x + x, pygame_y - y + img.height), 5)
        pygame.display.update()
        vertices.append((x, y))
        with open(vertex_path, "wb") as file:
            pickle.dump(vertices, file)
    return vertices


window = pyglet.window.Window(fullscreen=True)
window.set_mouse_visible(False)
fps_display = pyglet.window.FPSDisplay(window=window)
batch = pyglet.graphics.Batch()
options = DrawOptions()
debug = False
first_move = True

smallest = window.height
if window.width < smallest:
    smallest = window.width

space = pymunk.Space()
space.gravity = 0, GRAVITY
margin = -1
friction = FRICTION
elasticity = ELASTICITY
spawn_margin = 200
spawn_x_min = spawn_margin
spawn_x_max = window.width - spawn_margin
spawn_y_min = spawn_margin
spawn_y_max = window.height - spawn_margin
min_speed = 50
max_speed = 300
mass = 1
face_bodies = []
face_sprites = []

segments = [
    [(margin, margin), (window.width - margin, margin)],
    [(window.width - margin, margin), (window.width - margin, window.height - margin)],
    [(window.width - margin, window.height - margin), (margin, window.height - margin)],
    [(margin, window.height - margin), (margin, margin)]
]

for segment in segments:
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    segment = pymunk.Segment(body, segment[0], segment[1], 1)
    segment.elasticity = elasticity
    segment.friction = friction
    space.add(body, segment)

pygame.init()
surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
info = pygame.display.Info()
pygame_width = info.current_w
pygame_height = info.current_h
surface.fill((0, 0, 0))
pygame.display.update()


faces_path = os.path.join(sys.path[0], "png", "faces")
for face_file in os.listdir(faces_path):
    if not face_file.endswith(".png"):
        continue
    face_path = os.path.join(faces_path, face_file)
    face_img = pyglet.image.load(face_path)
    vertices = get_vertices(face_path)
    face_body = pymunk.Body(1, 1000, pymunk.Body.DYNAMIC)
    face_poly = pymunk.Poly(face_body, vertices)
    face_poly.density = 3
    face_poly.elasticity = elasticity
    face_poly.friction = friction
    face_body.position = random.randint(spawn_x_min, spawn_x_max), random.randint(spawn_y_min, spawn_y_max)
    face_body.velocity = random.randint(min_speed, max_speed), random.randint(min_speed, max_speed)
    face_body.angle = random.randint(0, 360)
    face_sprite = pyglet.sprite.Sprite(face_img, x=face_body.position.x, y=face_body.position.y, batch=batch)
    face_bodies.append(face_body)
    face_sprites.append(face_sprite)
    space.add(face_body, face_poly)

logo_path = os.path.join(sys.path[0], "png", "logo.png")
logo_img = pyglet.image.load(logo_path)
vertices = get_vertices(logo_path)
logo_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
logo_poly = pymunk.Poly(logo_body, vertices)
logo_poly.cache_bb()
logo_width = logo_poly.bb.right - logo_poly.bb.left
logo_height = logo_poly.bb.top - logo_poly.bb.bottom
logo_poly.elasticity = 1.0
logo_poly.friction = friction
logo_x = random.randint(spawn_x_min, spawn_x_min + logo_width // 2)
logo_y = random.randint(spawn_y_min, spawn_y_min + logo_height // 2)
logo_body.position = logo_x, logo_y
logo_body.velocity = 200, 200
logo_sprite = pyglet.sprite.Sprite(logo_img, x=logo_body.position.x, y=logo_body.position.y, batch=batch)
space.add(logo_body, logo_poly)


@ window.event
def on_key_press(symbol, modifiers):
    global debug
    if symbol == key.F1:
        debug = not debug
    elif symbol in ESCAPED_KEYS:
        pass
    else:
        pyglet.app.exit()


@ window.event
def on_mouse_motion(x, y, dx, dy):
    global first_move
    if first_move:
        first_move = False
    else:
        pyglet.app.exit()


@ window.event
def on_draw():
    window.clear()
    if debug:
        space.debug_draw(options)
        fps_display.draw()
    batch.draw()
    logo_sprite.draw()


def update(dt):
    space.step(dt)
    for index, face_sprite in enumerate(face_sprites):
        face_body = face_bodies[index]
        face_sprite.position = face_body.position
        face_sprite.rotation = math.degrees(-face_body.angle)

        x = face_body.position.x
        y = face_body.position.y
        if x < -200 or x > window.width + 200 or y < -200 or y > window.height + 200:
            face_body.position = random.randint(spawn_x_min, spawn_x_max), random.randint(spawn_y_min, spawn_y_max)
            face_body.velocity = random.randint(-50, 50), random.randint(-50, 50)
            face_body.angular_velocity = random.randint(10, 100)

    logo_sprite.position = logo_body.position

    if logo_body.position.x < 0:
        logo_body.velocity = abs(logo_body.velocity.x), logo_body.velocity.y
    if logo_body.position.x + logo_width > window.width:
        logo_body.velocity = -abs(logo_body.velocity.x), logo_body.velocity.y
    if logo_body.position.y < 0:
        logo_body.velocity = logo_body.velocity.x, abs(logo_body.velocity.y)
    if logo_body.position.y + logo_height > window.height:
        logo_body.velocity = logo_body.velocity[0], -abs(logo_body.velocity.y)


pygame.quit()
pyglet.clock.schedule_interval(update, 1.0 / 120)
pyglet.app.run()
