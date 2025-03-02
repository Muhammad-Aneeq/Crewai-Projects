
import pygame
import random

# Initialize Pygame
pygame.init()

# Set window dimensions
window_width = 600
window_height = 400
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Snake Game")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# Snake initial settings
snake_block_size = 10
snake_speed = 15
snake_x = window_width / 2
snake_y = window_height / 2
snake_x_change = 0
snake_y_change = 0
snake_list = []
snake_length = 1

# Food initial settings
food_x = round(random.randrange(0, window_width - snake_block_size) / 10.0) * 10.0
food_y = round(random.randrange(0, window_height - snake_block_size) / 10.0) * 10.0

# Game variables
game_over = False
clock = pygame.time.Clock()
score = 0
font_style = pygame.font.SysFont(None, 30)

def display_score(score):
    value = font_style.render("Your Score: " + str(score), True, white)
    window.blit(value, [0, 0])

def draw_snake(snake_block_size, snake_list):
    for x in snake_list:
        pygame.draw.rect(window, green, [x[0], x[1], snake_block_size, snake_block_size])

def display_message(msg, color):
    mesg = font_style.render(msg, True, color)
    window.blit(mesg, [window_width / 6, window_height / 3])

# Game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and snake_x_change != snake_block_size:
                snake_x_change = -snake_block_size
                snake_y_change = 0
            elif event.key == pygame.K_RIGHT and snake_x_change != -snake_block_size:
                snake_x_change = snake_block_size
                snake_y_change = 0
            elif event.key == pygame.K_UP and snake_y_change != snake_block_size:
                snake_y_change = -snake_block_size
                snake_x_change = 0
            elif event.key == pygame.K_DOWN and snake_y_change != -snake_block_size:
                snake_y_change = snake_block_size
                snake_x_change = 0

    # Check for boundary collisions
    if snake_x >= window_width or snake_x < 0 or snake_y >= window_height or snake_y < 0:
        game_over = True

    snake_x += snake_x_change
    snake_y += snake_y_change
    window.fill(black)
    pygame.draw.rect(window, red, [food_x, food_y, snake_block_size, snake_block_size])

    snake_head = []
    snake_head.append(snake_x)
    snake_head.append(snake_y)
    snake_list.append(snake_head)

    if len(snake_list) > snake_length:
        del snake_list[0]

    for x in snake_list[:-1]:
        if x == snake_head:
            game_over = True

    draw_snake(snake_block_size, snake_list)
    display_score(score)
    pygame.display.update()

    if snake_x == food_x and snake_y == food_y:
        food_x = round(random.randrange(0, window_width - snake_block_size) / 10.0) * 10.0
        food_y = round(random.randrange(0, window_height - snake_block_size) / 10.0) * 10.0
        snake_length += 1
        score += 10

    clock.tick(snake_speed)

pygame.quit()
quit()