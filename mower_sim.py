import sys
import time
import json
import pygame
import math

# Constants
WINDOW_SIZE = 1000
BACKGROUND_IMAGE_FILE = "grass.jpg"
MOWER_COLOR = (255, 0, 0)  # Red mower
CIRCLE_DIAMETER = int(0.35 * (WINDOW_SIZE // 10))
CIRCLE_RADIUS = CIRCLE_DIAMETER // 2
DOT_DATA = "dot_data_0808_155538.json"

def load_path(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"No such file: '{filename}'. Ensure the file exists.")
        sys.exit()

def adjust_color(base_color, depth):
    lighten_factor = depth / 100
    # Ensure the lighter color is still a shade of green rather than white
    max_green_lightness = (144, 238, 144)  # Light green
    lighten_color = tuple(min(base_color[i] + int((max_green_lightness[i] - base_color[i]) * lighten_factor), 255) for i in range(3))
    return lighten_color

def draw_rounded_line(surface, color, start_pos, end_pos, radius):
    """Draw a rounded line by drawing overlapping circles along the path"""
    x1, y1 = int(start_pos[0]), int(start_pos[1])
    x2, y2 = int(end_pos[0]), int(end_pos[1])
    radius = int(radius)
    
    # Calculate distance and number of circles needed
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    
    if distance == 0:
        # If start and end are the same, just draw one circle
        if 0 <= x1 < WINDOW_SIZE and 0 <= y1 < WINDOW_SIZE:
            pygame.draw.circle(surface, color, (x1, y1), radius)
        return
    
    # Number of circles to draw (spacing them closer for smoother appearance)
    num_circles = max(1, int(distance / (radius * 0.3)))  # Reduced overlap for performance
    
    # Draw circles along the line
    for i in range(num_circles + 1):
        t = i / num_circles if num_circles > 0 else 0
        x = int(x1 + (x2 - x1) * t)
        y = int(y1 + (y2 - y1) * t)
        
        # Ensure coordinates are within screen bounds
        if 0 <= x < WINDOW_SIZE and 0 <= y < WINDOW_SIZE and radius > 0:
            pygame.draw.circle(surface, color, (x, y), radius)

def simulate_mowing():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Lawnmower Simulation")
    background_image = pygame.image.load(BACKGROUND_IMAGE_FILE)
    background_image = pygame.transform.scale(background_image, (WINDOW_SIZE, WINDOW_SIZE))
    
    # Create a persistent surface for cut paths to avoid redrawing everything each frame
    cut_surface = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE))
    cut_surface.set_colorkey((0, 0, 0))  # Make black transparent
    
    path_data = load_path(DOT_DATA)
    clock = pygame.time.Clock()
    previous_end_x, previous_end_y = None, None
    
    for group_index, group in enumerate(path_data):
        print(f"Processing group {group_index + 1}")
        dots = group['dots']
        depth = group['depth']
        cut_color = adjust_color((0, 128, 0), depth)
        
        # Handle movement between groups (non-cutting movement)
        if previous_end_x is not None and previous_end_y is not None:
            start_x, start_y = previous_end_x, previous_end_y
            end_x, end_y = int(dots[0][0] * WINDOW_SIZE / 10), int((10 - dots[0][1]) * WINDOW_SIZE / 10)
            
            # Animate movement without cutting
            for t in range(0, 101, 2):  # Smaller steps for smoother, slower movement
                interp_x = start_x + (end_x - start_x) * t // 100
                interp_y = start_y + (end_y - start_y) * t // 100
                
                # Draw everything efficiently
                screen.blit(background_image, (0, 0))
                screen.blit(cut_surface, (0, 0))  # Draw all cut paths at once
                pygame.draw.circle(screen, MOWER_COLOR, (interp_x, interp_y), CIRCLE_RADIUS)
                
                pygame.display.flip()
                clock.tick(60)  # Slower framerate for slower movement
                
                # Check for quit events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
        
        # Handle cutting within a group
        for i in range(1, len(dots)):
            start_x, start_y = int(dots[i-1][0] * WINDOW_SIZE / 10), int((10 - dots[i-1][1]) * WINDOW_SIZE / 10)
            end_x, end_y = int(dots[i][0] * WINDOW_SIZE / 10), int((10 - dots[i][1]) * WINDOW_SIZE / 10)
            
            for t in range(0, 101, 2):  # Smaller steps for smoother, slower movement
                interp_x = start_x + (end_x - start_x) * t // 100
                interp_y = start_y + (end_y - start_y) * t // 100
                
                # Draw everything efficiently
                screen.blit(background_image, (0, 0))
                screen.blit(cut_surface, (0, 0))  # Draw all previous cuts at once
                
                # Draw the current cutting path as the mower progresses
                if t > 0:
                    draw_rounded_line(screen, cut_color, (start_x, start_y), (interp_x, interp_y), CIRCLE_RADIUS)
                
                pygame.draw.circle(screen, MOWER_COLOR, (interp_x, interp_y), CIRCLE_RADIUS)
                pygame.display.flip()
                clock.tick(30)  # Slower framerate for slower movement
                time.sleep(0.02)  # Add small delay for even slower movement
                
                # Check for quit events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
            
            # Add the completed path to the persistent surface
            draw_rounded_line(cut_surface, cut_color, (start_x, start_y), (end_x, end_y), CIRCLE_RADIUS)
        
        previous_end_x, previous_end_y = end_x, end_y
    
    # Keep the window open after simulation
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # Redraw final state
        screen.blit(background_image, (0, 0))
        screen.blit(cut_surface, (0, 0))
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    simulate_mowing()
