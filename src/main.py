import pygame


class UI:
    HOT_BUTTON = None
    ACTIVE_BUTTON = None
    mouse_pos = (0, 0)
    mouse_up = False
    mouse_down = False
    screen = None

    def __init__(self):
        self.font = pygame.font.SysFont('./Roboto.ttf', 64)


def button(ui, text_with_id, rect):
    text, button_id = text_with_id.split("###")
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
    elif ui.HOT_BUTTON == button_id:
        ui.HOT_BUTTON = None

    # Draw bg
    color = (255, 0, 0)
    if ui.ACTIVE_BUTTON == button_id: color = (0, 255, 0)
    elif ui.HOT_BUTTON == button_id:  color = (0, 0, 255)
    pygame.draw.rect(screen, color, rect)

    # Draw text
    rendered_text = ui.font.render(text, True, (0, 255, 0))
    rect_size = (rect.right - rect.left, rect.bottom - rect.top)
    text_size = rendered_text.get_size()
    factor = min(rect_size[0] / text_size[0], rect_size[1] / text_size[1])
    target_text_size = (text_size[0] * factor, text_size[1] * factor)
    rendered_text = pygame.transform.smoothscale(rendered_text, target_text_size)
    ui.screen.blit(rendered_text, (rect.left + (rect_size[0] / 2) - (target_text_size[0] / 2),
                                   rect.top  + (rect_size[1] / 2) - (target_text_size[1] / 2)))
    
    return result


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

# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
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

    if button(ui, 'Hello###HELLO', pygame.Rect(100, 100, 200, 100)):
        print("Clicked")

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
