import pygame

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
clock = pygame.time.Clock()
font = pygame.font.SysFont('./Roboto.ttf', 30)

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

    ########################################
    # Render
    screen.fill((255, 255, 255))

    fps_g = font.render(f'FPS: {clock.get_fps():.0f}', True, (0, 255, 0))
    screen.blit(fps_g, (0,0))

    if button(ui, 'WIELKI KUTAS###1', pygame.Rect(100, 100, 200, 100)):
        print("Clicked")

    if button(ui, 'WIELKI KUTAS###2', pygame.Rect(300, 300, 200, 100)):
        print("Clicked")

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
