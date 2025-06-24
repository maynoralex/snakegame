import pygame
import sys
import random

# --- Initialization ---
# Initialize all imported pygame modules
pygame.init()

# --- Game Settings and Constants ---
# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (50, 153, 213) # A nice blue for the background

# Snake properties
SNAKE_SIZE = 20
SNAKE_SPEED = 15 # The number of frames per second, controls game speed

# Setup the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Python Snake Game')

# Game clock to control the frame rate
clock = pygame.time.Clock()

# --- Font and Text Handling ---
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def display_score(score):
    """Renders and displays the current score."""
    value = score_font.render(f"Score: {score}", True, WHITE)
    screen.blit(value, [10, 10])

def draw_snake(snake_size, snake_list):
    """Draws all segments of the snake."""
    for x in snake_list:
        pygame.draw.rect(screen, GREEN, [x[0], x[1], snake_size, snake_size])

def display_message(msg, color, y_displace=0):
    """Displays a message on the screen."""
    mesg = font_style.render(msg, True, color)
    mesg_rect = mesg.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + y_displace))
    screen.blit(mesg, mesg_rect)

# --- Main Game Loop ---
def game_loop():
    game_over = False
    game_close = False

    # Snake's starting position in the center of the screen
    x1 = SCREEN_WIDTH / 2
    y1 = SCREEN_HEIGHT / 2

    # Change in position
    x1_change = 0
    y1_change = 0

    # Snake body represented as a list of coordinates
    snake_list = []
    length_of_snake = 1

    # Randomly place the first food item
    food_x = round(random.randrange(0, SCREEN_WIDTH - SNAKE_SIZE) / SNAKE_SIZE) * SNAKE_SIZE
    food_y = round(random.randrange(0, SCREEN_HEIGHT - SNAKE_SIZE) / SNAKE_SIZE) * SNAKE_SIZE

    # --- The Core Game Loop ---
    while not game_over:

        # --- Game Over Screen Loop ---
        while game_close:
            screen.fill(BLUE)
            display_message("You Lost! Press 'C' to Play Again or 'Q' to Quit", RED, y_displace=-50)
            display_score(length_of_snake - 1)
            pygame.display.update()

            # Check for user input to restart or quit
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop() # Restart the game by calling the main loop again

        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -SNAKE_SIZE
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = SNAKE_SIZE
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -SNAKE_SIZE
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = SNAKE_SIZE
                    x1_change = 0

        # --- Collision Detection (Walls) ---
        if x1 >= SCREEN_WIDTH or x1 < 0 or y1 >= SCREEN_HEIGHT or y1 < 0:
            game_close = True

        # Update snake's position
        x1 += x1_change
        y1 += y1_change

        # --- Drawing and Screen Updates ---
        screen.fill(BLUE)
        pygame.draw.rect(screen, RED, [food_x, food_y, SNAKE_SIZE, SNAKE_SIZE])

        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)

        # Ensure the snake's length is maintained
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # --- Collision Detection (Self) ---
        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        # Draw the snake and score
        draw_snake(SNAKE_SIZE, snake_list)
        display_score(length_of_snake - 1)

        # Update the full display Surface to the screen
        pygame.display.update()

        # --- Food Consumption and Growth ---
        if x1 == food_x and y1 == food_y:
            # Generate new food coordinates
            food_x = round(random.randrange(0, SCREEN_WIDTH - SNAKE_SIZE) / SNAKE_SIZE) * SNAKE_SIZE
            food_y = round(random.randrange(0, SCREEN_HEIGHT - SNAKE_SIZE) / SNAKE_SIZE) * SNAKE_SIZE
            length_of_snake += 1

        # Control the speed of the game
        clock.tick(SNAKE_SPEED)

    # --- Uninitialize and Quit ---
    pygame.quit()
    sys.exit()

# --- Start the game ---
if __name__ == '__main__':
    game_loop()