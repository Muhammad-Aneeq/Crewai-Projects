import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pacman")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

# Pacman class
class Pacman:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 20
        self.speed = 5
        self.lives = 3
        self.score = 0

    def draw(self):
        pygame.draw.circle(screen, yellow, (self.x, self.y), self.size)

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed

        # Keep pacman within screen bounds
        self.x = max(self.size, min(self.x, screen_width - self.size))
        self.y = max(self.size, min(self.y, screen_height - self.size))


# Ghost class
class Ghost:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.size = 20
        self.speed = 3
        self.color = color

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)

    def move(self):
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])
        self.x += dx * self.speed
        self.y += dy * self.speed

        # Keep ghost within screen bounds
        self.x = max(self.size, min(self.x, screen_width - self.size))
        self.y = max(self.size, min(self.y, screen_height - self.size))


# Food dot class
class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 5

    def draw(self):
        pygame.draw.circle(screen, white, (self.x, self.y), self.size)


# Create game objects
pacman = Pacman(50, 50)
ghosts = [Ghost(random.randint(50, 750), random.randint(50, 550), red) for _ in range(1)]
food_dots = []
num_dots = 100
for _ in range(num_dots):
    x = random.randint(10, screen_width - 10)
    y = random.randint(10, screen_height - 10)
    food_dots.append(Food(x, y))


# Game loop
running = True
clock = pygame.time.Clock()
level = 1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Pacman movement
    keys = pygame.key.get_pressed()
    dx = 0
    dy = 0
    if keys[pygame.K_LEFT]:
        dx = -1
    if keys[pygame.K_RIGHT]:
        dx = 1
    if keys[pygame.K_UP]:
        dy = -1
    if keys[pygame.K_DOWN]:
        dy = 1
    pacman.move(dx, dy)


    #Ghost Movement
    for ghost in ghosts:
        ghost.move()

        #Collision Detection
        distance = math.sqrt((pacman.x - ghost.x)**2 + (pacman.y - ghost.y)**2)
        if distance < pacman.size + ghost.size:
            pacman.lives -= 1
            if pacman.lives == 0:
                running = False

    # Eat food
    for dot in food_dots[:]: #Use slice to safely modify list during iteration
        distance = math.sqrt((pacman.x - dot.x)**2 + (pacman.y - dot.y)**2)
        if distance < pacman.size + dot.size:
            pacman.score += 1
            food_dots.remove(dot)


    #Level up
    if not food_dots:
        level += 1
        pacman.speed += 2
        ghosts.append(Ghost(random.randint(50,750), random.randint(50, 550), blue))
        num_dots += 50
        for _ in range(num_dots):
            x = random.randint(10, screen_width -10)
            y = random.randint(10, screen_height - 10)
            food_dots.append(Food(x,y))

    #Drawing
    screen.fill(black)
    pacman.draw()
    for ghost in ghosts:
        ghost.draw()
    for dot in food_dots:
        dot.draw()

    #Display score and lives
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {pacman.score}", True, white)
    lives_text = font.render(f"Lives: {pacman.lives}", True, white)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 50))

    pygame.display.update()
    clock.tick(30)

pygame.quit()
