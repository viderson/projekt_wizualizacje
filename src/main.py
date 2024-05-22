import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' # Hide pygame welcome message
import pygame
import pandas
import time
# pip install openpyxl!!! for reading xlsx

from ui import *

def toggle_fullscreen(screen):
  flags = screen.get_flags()
  if flags & pygame.FULLSCREEN:
      pygame.display.set_mode((720, 640))
  else:
      pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

def scale_map(original_map, original_size, scale):
    target_size = (original_size[0] * scale, original_size[1] * scale)
    return pygame.transform.smoothscale(original_map, target_size)

########################################
# Init
pygame.init()
pygame.font.init()
pygame.event.set_grab(True)  # Capture all input (needed for alt)

screen = pygame.display.set_mode(size=(720, 640))
pygame.display.set_caption('TITLE ME!!!')
clock  = pygame.time.Clock()
font   = pygame.font.Font('./Roboto.ttf', 18)

font_icons = pygame.font.Font('./iconly.ttf', 64)
ICON_PLUS = '\uE000'
ICON_MINUS = '\uE001'

map_img = pygame.image.load("./mapa_gmina_fredropol.png").convert()
map_original_dim = map_img.get_size()
map_offset = (0, 0)
map_scale = 1
scaled_map = scale_map(map_img, map_original_dim, map_scale)
scaled_map_dim = scaled_map.get_size()
MAP_SCALE_FACTOR = 1.25

target_fps = 60
target_frame_time = 1/target_fps 
frame_time = 0
frame_begin_time = time.time()
frame_end_time   = time.time()

mouse_dragged = False
mouse_drag_start = pygame.mouse.get_pos()

ui = UI()
ui.screen = screen
is_running = True

places_excel = pandas.read_excel("./dane_gmina_fredropol.xlsx")


def parse_lat_long(lat_long):
    def degrees_from_dms(dms): # dms - degrees (°), minutes ('), seconds ('')
        # TODO(Pawel Hermansdorfer): Clean this
        degrees = int(dms.split('°')[0])
        minutes = int(dms.split('°')[1].split("'")[0])
        seconds = float(dms.split('°')[1].split("'")[1].split('"')[0])
        return (degrees) + (minutes / 60) + (seconds / 3600)
    split = lat_long.split(' ')
    return degrees_from_dms(split[0]), degrees_from_dms(split[1])

places_excel['lat'], places_excel['long'] = zip(*places_excel['współrzędne geograficzne'].apply(func=parse_lat_long))
min_lat,  max_lat  = min(places_excel['lat']),  max(places_excel['lat'])
min_long, max_long = min(places_excel['long']), max(places_excel['long'])

def render_name(lat, long, name):
    # TODO(Pawel Hermansdorfer): Finish
    def map(a, start1, stop1, start2, end2):
        return start2 + (((end2 - start2) / (stop1 -start1 )) * (a - start1))

    map_x = map(lat, min_lat, max_lat, 0, max_size[0])
    map_y = map(long, min_long, max_long, 0, max_size[1])



while is_running:
    ########################################
    # Inputs
    ui.mouse_up = ui.mouse_down = False

    alt_is_pressed = pygame.key.get_pressed()[pygame.K_LALT]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        # TODO(Pawel Hermansdorfer): Cleanup
        elif event.type == pygame.MOUSEBUTTONDOWN:
            ui.mouse_down = True
            if ui.HOT_BUTTON == None and ui.ACTIVE_BUTTON == None:
                mouse_dragged = True
                mouse_drag_start = pygame.mouse.get_pos()

        elif event.type == pygame.MOUSEBUTTONUP:
            ui.mouse_up = True
            mouse_dragged = False
            if ui.HOT_BUTTON == None and ui.ACTIVE_BUTTON == None:
                map_offset = (map_offset[0] + 1/map_scale * (mouse_pos[0] - mouse_drag_start[0]),
                              map_offset[1] + 1/map_scale * (mouse_pos[1] - mouse_drag_start[1]))

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and alt_is_pressed:
                toggle_fullscreen(screen)
            if event.key == pygame.K_q and alt_is_pressed:
                is_running = False

    ########################################
    # Update
    mouse_pos = pygame.mouse.get_pos()
    ui.mouse_pos = mouse_pos
    screen_dim = screen.get_size()

    if mouse_dragged:
        offset = (map_offset[0] + 1/map_scale * (mouse_pos[0] - mouse_drag_start[0]),
                  map_offset[1] + 1/map_scale * (mouse_pos[1] - mouse_drag_start[1]))
    else:
        offset = map_offset

    ########################################
    # Render
    screen.fill((50, 40, 40))

    blit_pos = (screen_dim[0]/2 - scaled_map_dim[0]/2 + offset[0]*map_scale,
                screen_dim[1]/2 - scaled_map_dim[1]/2 + offset[1]*map_scale)
    screen.blit(scaled_map,  blit_pos)

    fps_text = font.render(f'FPS: {1/frame_time if frame_time != 0 else 0:.2f}', True, (0, 255, 0))
    screen.blit(fps_text, (0,0))

    # UI
    if button(ui, ICON_MINUS + "###SCALE_DOWN", pygame.Rect(screen_dim[0] - 35, screen_dim[1] - 35, 30, 30), font_icons):
        map_scale /= MAP_SCALE_FACTOR
        scaled_map = scale_map(map_img, map_original_dim, map_scale)
        scaled_map_dim = scaled_map.get_size()

    if button(ui, ICON_PLUS + "###SCALE_UP", pygame.Rect(screen_dim[0] - 75, screen_dim[1] - 35, 30, 30), font_icons):
        map_scale *= MAP_SCALE_FACTOR
        scaled_map = scale_map(map_img, map_original_dim, map_scale)
        scaled_map_dim = scaled_map.get_size()

    if button(ui, 'RESET###RESET', pygame.Rect(screen_dim[0] - 185, screen_dim[1] - 35, 100, 30)):
        map_offset = (0, 0)
        map_scale = 1
        scaled_map = scale_map(map_img, map_original_dim, map_scale)
        scaled_map_dim = scaled_map.get_size()

    pygame.display.flip()

    ########################################
    # Limit frame rate
    elapsed_time = time.time() - frame_begin_time
    if elapsed_time < target_frame_time:
        time.sleep(target_frame_time - elapsed_time)
    frame_end_time = time.time()
    frame_time = frame_end_time - frame_begin_time
    frame_begin_time = frame_end_time

pygame.quit()
