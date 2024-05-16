import pygame


class UI:
    HOT_BUTTON = 0
    ACTIVE_BUTTON = 0
    mouse_pos = (0, 0)
    mouse_up = False
    mouse_down = False
    screen = 0


def button(ui, button_id, text, rect):
    result = False
    if ui.ACTIVE_BUTTON == button_id:
        if ui.mouse_up:
            if ui.HOT_BUTTON: 
                result = True
                ui.ACTIVE_BUTTON = 0
    elif ui.HOT_BUTTON == button_id:
        if ui.mouse_down:
            ui.ACTIVE_BUTTON = button_id

    if (rect.left <= mouse_pos[0] and mouse_pos[0] <= rect.right) and (rect.top <= mouse_pos[1] and mouse_pos[1] <= rect.bottom):
        ui.HOT_BUTTON = button_id

    pygame.draw.rect(screen, (255, 0, 0), rect)
    return result



pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
font = pygame.font.SysFont('./Roboto.ttf', 30)

ui = UI()
ui.screen = screen
is_running = True

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event == pygame.MOUSEBUTTONUP:
            ui.mouse_up = True
        elif event == pygame.MOUSEBUTTONDOWN:
            ui.mouse_down = True

    # Do logical updates here.
    mouse_pos = pygame.mouse.get_pos()
    ui.mouse_pos = mouse_pos

    screen.fill((255, 255, 255))

    # Render the graphics here.
    fps_text = font.render(f'FPS: {clock.get_fps():.0f}', True, (0, 255, 0))
    screen.blit(fps_text, (0,0))

    if button(ui, 'Hello###HELLO', pygame.Rect(100, 100, 200, 100)):
        print("LOOOL")

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
