import pygame

class UI:
    HOT_BUTTON    = None
    ACTIVE_BUTTON = None
    mouse_pos  = (0, 0)
    mouse_up   = False
    mouse_down = False
    screen = None
    font   = None

    def __init__(self):
        self.font = pygame.font.SysFont('./Roboto.ttf', 64)

def draw_ui_element(ui, text_with_id, rect,
                    draw_bg=False,
                    draw_text=False,
                    draw_border=False,
                    draw_shadow=False):
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

    if (rect.left <= ui.mouse_pos[0] and ui.mouse_pos[0] <= rect.right) and (rect.top <= ui.mouse_pos[1] and ui.mouse_pos[1] <= rect.bottom):
        ui.HOT_BUTTON = button_id
    elif ui.HOT_BUTTON == button_id:
        ui.HOT_BUTTON = None

    # Draw shadow
    if draw_shadow:
        shadow_color = (10, 10, 10)
        pygame.draw.rect(ui.screen, shadow_color, pygame.Rect(rect.left + 2, rect.top + 2, rect.width, rect.height),
                         border_radius=10)

    # Draw bg
    if draw_bg:
        bg_color = (80, 80, 80)
        if ui.ACTIVE_BUTTON == button_id: bg_color = (40, 40, 40)
        elif ui.HOT_BUTTON == button_id:  bg_color = (60, 60, 60)
        pygame.draw.rect(ui.screen, bg_color, rect, border_radius=10)

    if draw_border:
        border_color = (110, 110, 110)
        pygame.draw.rect(ui.screen, border_color, rect, width=2, border_radius=10)

    # Draw text
    if draw_text:
        rendered_text = ui.font.render(text, True, (255, 255, 255))
        rect_size = (rect.right - rect.left, rect.bottom - rect.top)
        text_size = rendered_text.get_size()
        margin = (rect_size[0] * 0.1, rect_size[1] * 0.1)
        factor = min((rect_size[0] - margin[0]) / text_size[0],
                     (rect_size[1] - margin[1]) / text_size[1])
        target_text_size = (text_size[0] * factor, text_size[1] * factor)
        rendered_text = pygame.transform.smoothscale(rendered_text, target_text_size)
        ui.screen.blit(rendered_text, (rect.left + (rect_size[0] / 2) - (target_text_size[0] / 2),
                                       rect.top  + (rect_size[1] / 2) - (target_text_size[1] / 2)))
    
    return result

def button(ui, text_with_id, rect):
    draw_ui_element(ui, text_with_id, rect, draw_bg=True,
                                            draw_text=True,
                                            draw_shadow=True,
                                            draw_border=True)
