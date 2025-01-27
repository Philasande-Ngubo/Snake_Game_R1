import pygame
import random
import math
import time

# Initialize Pygame
pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BROWN = (139, 69, 19)
LEAF_GREEN = (50, 205, 50)

# Game settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CELL_SIZE = 20
BASE_SPEED = 5
SPEED_INCREASE = 0.5
MAX_SPEED = 15

# Initialize display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

def draw_apple(pos):
    # Apple body
    pygame.draw.circle(screen, RED, (pos[0]+10, pos[1]+10), 10)
    # Stem
    pygame.draw.rect(screen, BROWN, (pos[0]+8, pos[1]-4, 4, 8))
    # Leaf
    pygame.draw.polygon(screen, LEAF_GREEN, [
        (pos[0]+14, pos[1]-2),
        (pos[0]+20, pos[1]-8),
        (pos[0]+24, pos[1]-2)
    ])

def draw_worm(snake, direction):
    for i, segment in enumerate(snake):
        # Worm body
        pygame.draw.circle(screen, GREEN, (segment[0]+10, segment[1]+10), 10)
        
        # Draw eyes on head
        if i == 0:
            dx, dy = direction
            angle = math.atan2(dy, dx) if dx != 0 or dy != 0 else 0
            eye_distance = 6
            
            # Left eye
            eye1_x = segment[0]+10 + math.cos(angle + math.pi/6) * eye_distance
            eye1_y = segment[1]+10 + math.sin(angle + math.pi/6) * eye_distance
            pygame.draw.circle(screen, WHITE, (int(eye1_x), int(eye1_y)), 4)
            pygame.draw.circle(screen, BLACK, (int(eye1_x), int(eye1_y)), 2)
            
            # Right eye
            eye2_x = segment[0]+10 + math.cos(angle - math.pi/6) * eye_distance
            eye2_y = segment[1]+10 + math.sin(angle - math.pi/6) * eye_distance
            pygame.draw.circle(screen, WHITE, (int(eye2_x), int(eye2_y)), 4)
            pygame.draw.circle(screen, BLACK, (int(eye2_x), int(eye2_y)), 2)

def display_score(score, speed):
    font = pygame.font.SysFont('Arial', 24)
    text = font.render(f"Score: {score}  Speed: {speed:.1f}", True, WHITE)
    screen.blit(text, (10, 10))

def game_over():
    font = pygame.font.SysFont('Arial', 72)
    text = font.render("Game Over!", True, RED)
    screen.blit(text, (WINDOW_WIDTH//2 - text.get_width()//2, WINDOW_HEIGHT//2 - text.get_height()//2))
    pygame.display.flip()
    time.sleep(2)

def main():
    running = True
    game_active = True
    snake = [[WINDOW_WIDTH//2, WINDOW_HEIGHT//2]]
    dx, dy = CELL_SIZE, 0
    food = [random.randrange(0, WINDOW_WIDTH, CELL_SIZE), 
            random.randrange(0, WINDOW_HEIGHT, CELL_SIZE)]
    score = 0
    current_speed = BASE_SPEED

    while running:
        screen.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and game_active:
                if event.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -CELL_SIZE
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, CELL_SIZE
                elif event.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -CELL_SIZE, 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = CELL_SIZE, 0

        if game_active:
            new_head = [snake[0][0] + dx, snake[0][1] + dy]
            
            # Collision detection
            if (new_head[0] < 0 or new_head[0] >= WINDOW_WIDTH or
                new_head[1] < 0 or new_head[1] >= WINDOW_HEIGHT or
                new_head in snake):
                game_active = False
                game_over()

            snake.insert(0, new_head)

            # Food collision
            if snake[0] == food:
                score += 1
                current_speed = min(MAX_SPEED, BASE_SPEED + score * SPEED_INCREASE)
                food = [random.randrange(0, WINDOW_WIDTH, CELL_SIZE),
                        random.randrange(0, WINDOW_HEIGHT, CELL_SIZE)]
                while food in snake:
                    food = [random.randrange(0, WINDOW_WIDTH, CELL_SIZE),
                            random.randrange(0, WINDOW_HEIGHT, CELL_SIZE)]
            else:
                snake.pop()

        # Draw game elements
        draw_worm(snake, (dx, dy))
        draw_apple(food)
        display_score(score, current_speed)

        if not game_active:
            font = pygame.font.SysFont('Arial', 36)
            text = font.render("Press SPACE to restart or Q to quit", True, WHITE)
            screen.blit(text, (WINDOW_WIDTH//2 - text.get_width()//2, WINDOW_HEIGHT//2 - text.get_height()//2))

        pygame.display.flip()
        clock.tick(current_speed)

        # Handle game over state
        if not game_active:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                main()
            elif keys[pygame.K_q]:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()