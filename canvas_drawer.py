import pygame
import sys
import json
from datetime import datetime

WINDOW_SIZE = 1000
BACKGROUND_IMAGE_FILE = "image.png"

def save_circle_data(circle_groups, window_size):
    grid_unit_size = window_size // 10
    save_data = []

    for index, (group, depth) in enumerate(circle_groups):
        if not group:
            continue
            
        grid_coordinates = [
            (round(x / grid_unit_size, 3), round(10 - y / grid_unit_size, 3)) for x, y in group
        ]
        save_data.append({"group": index + 1, "dots": grid_coordinates, "depth": depth})

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'dot_data_{timestamp}.json'

    with open(filename, 'w') as json_file:
        json.dump(save_data, json_file, indent=4)

    return filename

def undo_last_action(circles, current_group):
    if current_group:
        current_group.pop()
    elif circles:
        circles[-1][0].pop()
        if not circles[-1][0]:
            circles.pop()

def prompt_depth(font):
    depth = 100  # Default depth
    input_active = True
    input_box = pygame.Rect(10, 10, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_active if input_active else color_inactive
    text = ''
    
    screen = pygame.display.get_surface()
    
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        depth = int(text)
                        depth = max(1, min(depth, 100))  # Clamping depth between 1 and 100
                    except ValueError:
                        depth = 100
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

        screen.fill((30, 30, 30))
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)
        
        # Display prompt message below the input box
        prompt_text = font.render("Enter Depth (1-100):", True, color)
        screen.blit(prompt_text, (input_box.x+5, input_box.y+40))
        
        pygame.display.flip()
    
    return depth

def main():
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Interactive Drawing with Grid")

    background_image = pygame.image.load(BACKGROUND_IMAGE_FILE)
    background_image = pygame.transform.scale(background_image, (WINDOW_SIZE, WINDOW_SIZE))
    
    dim_surface = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE))
    dim_surface.set_alpha(100)
    dim_surface.fill((0, 0, 0))

    pygame.font.init()
    font = pygame.font.SysFont(None, 36)

    circles = []
    current_group = []
    current_depth = 100  # Default depth for new group

    grid_unit_size = WINDOW_SIZE // 10
    circle_diameter = int(0.35 * grid_unit_size)
    circle_radius = circle_diameter // 2

    space_down = False
    shift_down = False
    save_msg_display = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    space_down = True
                    shift_down = False
                    save_msg_display = False
                
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    shift_down = True
                    space_down = False

                if event.key == pygame.K_z and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    undo_last_action(circles, current_group)
                    
                if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    save_circle_data(circles + [(current_group, current_depth)], WINDOW_SIZE)
                    save_msg_display = True

                if event.key == pygame.K_w and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    current_depth = prompt_depth(font)  # Prompt for new depth

            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_SPACE, pygame.K_LSHIFT, pygame.K_RSHIFT):
                    space_down = False
                    shift_down = False
                    if event.key == pygame.K_SPACE:
                        if current_group:
                            circles.append((current_group, current_depth))
                            current_group = []

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if event.button == 1:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_SPACE]:
                        current_group.append((mouse_x, mouse_y))
                    elif keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                        if circles:
                            circles[-1][0].append((mouse_x, mouse_y))
                    elif not keys[pygame.K_SPACE]:
                        current_group = [(mouse_x, mouse_y)]
        
        screen.blit(background_image, (0, 0))
        screen.blit(dim_surface, (0, 0))

        for i in range(11):
            pos = i * grid_unit_size
            pygame.draw.line(screen, (255, 255, 255), (pos, 0), (pos, WINDOW_SIZE))
            pygame.draw.line(screen, (255, 255, 255), (0, pos), (WINDOW_SIZE, pos))

        all_groups = circles + [(current_group, current_depth)]
        for group, depth in all_groups:
            color_value = int(255 * (depth / 100))
            color = (color_value, 0, 0)
            for i in range(1, len(group)):
                pygame.draw.line(screen, color, group[i - 1], group[i], circle_diameter)

            for x, y in group:
                pygame.draw.circle(screen, color, (x, y), circle_radius)

            for x, y in group:
                pygame.draw.circle(screen, (0, 0, 0), (x, y), 3)

        current_depth_text = font.render(f"Current Depth: {current_depth}", True, (255, 255, 255))
        screen.blit(current_depth_text, (WINDOW_SIZE - current_depth_text.get_width() - 10, 10))

        mouse_x, mouse_y = pygame.mouse.get_pos()

        if space_down:
            label_text = font.render("space pressed", True, (255, 255, 255))
            screen.blit(label_text, (WINDOW_SIZE - label_text.get_width() - 10, WINDOW_SIZE - label_text.get_height() - 10))
        elif shift_down:
            label_text = font.render("shift pressed - editing previous group", True, (255, 255, 255))
            screen.blit(label_text, (WINDOW_SIZE - label_text.get_width() - 10, WINDOW_SIZE - label_text.get_height() - 10))
        
        if save_msg_display:
            save_label_text = font.render("dot coordinates saved", True, (255, 255, 255))
            screen.blit(save_label_text, (WINDOW_SIZE - save_label_text.get_width() - 10, WINDOW_SIZE - save_label_text.get_height() - 50))

        pygame.draw.circle(screen, (255, 0, 0), (mouse_x, mouse_y), circle_radius, 1)

        pygame.display.flip()

if __name__ == "__main__":
    main()
