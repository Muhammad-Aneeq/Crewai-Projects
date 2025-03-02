import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
TILE_SIZE = 30
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
PINK = (255, 105, 180)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
BLUE = (0, 0, 255)

# Maze layout (0: empty, 1: wall, 2: pellet, 3: power pellet)
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

pellets = []
power_pellets = [(1,1),(18,1),(1,9),(18,9)]
for y, row in enumerate(maze):
    for x, tile in enumerate(row):
        if tile == 2:
            pellets.append((x,y))



class Pacman:
    def __init__(self):
        self.x = 1
        self.y = 1
        self.direction = "right"
        self.speed = 1
        self.lives = 3


    def move(self):
        new_x = self.x
        new_y = self.y
        if self.direction == "right":
            new_x += self.speed
        elif self.direction == "left":
            new_x -= self.speed
        elif self.direction == "up":
            new_y -= self.speed
        elif self.direction == "down":
            new_y += self.speed

        if 0 <= new_x < len(maze[0]) and 0 <= new_y < len(maze) and maze[int(new_y)][int(new_x)] != 1:
            self.x = new_x
            self.y = new_y

        # Warp tunnels
        if self.x < 0:
            self.x = len(maze[0]) - 2
        elif self.x >= len(maze[0]):
            self.x = 1


class Ghost:
    def __init__(self, color, x, y):
        self.x = x
        self.y = y
        self.color = color
        self.speed = 0.5
        self.target_x = 0
        self.target_y = 0

    def move(self, pacman):
        # Basic ghost AI (replace with more sophisticated AI if desired)
        dx = pacman.x - self.x
        dy = pacman.y - self.y
        if abs(dx) > abs(dy):
            self.x += self.speed * (1 if dx > 0 else -1)
        else:
            self.y += self.speed * (1 if dy > 0 else -1)
        self.x = int(self.x)
        self.y = int(self.y)

# Initialize game objects
pacman = Pacman()
ghosts = [
    Ghost(RED, 10, 10),
    Ghost(PINK, 10, 12),
    Ghost(CYAN, 12, 10),
    Ghost(ORANGE, 12, 12)
]
score = 0

# Game loop
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")
clock = pygame.time.Clock()
running = True
font = pygame.font.Font(None, 36)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pacman.direction = "left"
            elif event.key == pygame.K_RIGHT:
                pacman.direction = "right"
            elif event.key == pygame.K_UP:
                pacman.direction = "up"
            elif event.key == pygame.K_DOWN:
                pacman.direction = "down"

    pacman.move()
    for ghost in ghosts:
        ghost.move(pacman)

    #Pellet and power pellet collision
    for pellet in pellets[:]:
        if int(pacman.x) == pellet[0] and int(pacman.y) == pellet[1]:
            pellets.remove(pellet)
            score +=10

    for power_pellet in power_pellets[:]:
        if int(pacman.x) == power_pellet[0] and int(pacman.y) == power_pellet[1]:
            power_pellets.remove(power_pellet)
            score +=50



    #Ghost collision
    for ghost in ghosts:
        if int(pacman.x) == int(ghost.x) and int(pacman.y) == int(ghost.y):
            pacman.lives -= 1
            if pacman.lives == 0:
                running = False


    screen.fill(BLACK)
    # Draw maze
    for y, row in enumerate(maze):
        for x, tile in enumerate(row):
            if tile == 1:
                pygame.draw.rect(screen, WHITE, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            elif tile == 2:
                pygame.draw.circle(screen, WHITE, (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2), 3)
            elif tile == 3:
                pygame.draw.circle(screen, WHITE, (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2), 7)

    # Draw pacman
    pygame.draw.circle(screen, YELLOW, (int(pacman.x * TILE_SIZE + TILE_SIZE / 2), int(pacman.y * TILE_SIZE + TILE_SIZE / 2)), TILE_SIZE // 2)
    # Draw ghosts
    for ghost in ghosts:
        pygame.draw.circle(screen, ghost.color, (int(ghost.x * TILE_SIZE + TILE_SIZE / 2), int(ghost.y * TILE_SIZE + TILE_SIZE / 2)), TILE_SIZE // 2)

    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

#Game Over Screen
game_over_text = font.render("GAME OVER", True, WHITE)
score_text = font.render(f"Final Score: {score}", True, WHITE)
screen.blit(game_over_text,(WIDTH//2 - 100, HEIGHT//2 - 50))
screen.blit(score_text,(WIDTH//2 - 100, HEIGHT//2))
pygame.display.flip()
pygame.time.delay(3000)

pygame.quit()
