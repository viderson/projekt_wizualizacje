import pygame
import time

from ui import *

def toggle_fullscreen(screen):
  flags = screen.get_flags()
  if flags & pygame.FULLSCREEN:
      pygame.display.set_mode((640, 720))
  else:
      pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

########################################
# Init
pygame.init()
pygame.font.init()
pygame.event.set_grab(True)  # Capture all input

screen = pygame.display.set_mode(size=(720, 640))
clock  = pygame.time.Clock()
font   = pygame.font.SysFont('./Roboto.ttf', 30)

target_fps = 30
target_frame_time = 1/target_fps 
frame_time = 0
frame_begin_time = time.time()
frame_end_time   = time.time()

ui = UI()
ui.screen = screen
is_running = True

while is_running:
    ########################################
    # Inputs
    ui.mouse_up = ui.mouse_down = False

    alt_is_pressed = pygame.key.get_pressed()[pygame.K_LALT]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        elif event.type == pygame.MOUSEBUTTONUP:
            ui.mouse_up = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            ui.mouse_down = True

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

    ########################################
    # Render
    screen.fill((255, 255, 255))

    fps_text = font.render(f'FPS: {1/frame_time if frame_time != 0 else 0:.2f}', True, (0, 255, 0))
    screen.blit(fps_text, (0,0))

    # UI
    # TODO(Pawel Hermansdorfer): Get font with these symbols https://iconly.io/
    if button(ui, "-###SCALE_UP", pygame.Rect(screen_dim[0] - 25, screen_dim[1] - 25, 20, 20)):
        print("-")

    if button(ui, "+###SCALE_DOWN", pygame.Rect(screen_dim[0] - 50, screen_dim[1] - 25, 20, 20)):
        print("+")

    if button(ui, 'WIELKI KUTAS###1', pygame.Rect(10, 50, 200, 100)):
        print("Clicked")

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
