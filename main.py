import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import sys
import random
import time

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF | pygame.OPENGL)
pygame.display.set_caption('Pac-Man')

# Set up OpenGL
glViewport(0, 0, 800, 500)
glMatrixMode(GL_PROJECTION)
gluOrtho2D(0, 900, 500, 0)
glMatrixMode(GL_MODELVIEW)

# Set up clock
clock = pygame.time.Clock()

# Set the initial time to 0
start_time = time.time()

# Load sounds
win_sound = pygame.mixer.Sound("ostora.mp3")
lose_sound = pygame.mixer.Sound("motna.mp3")
start_sound = pygame.mixer.Sound("run.mp3")

# Create sound channels
sound_channel = pygame.mixer.Channel(0)

# Play start sound
start_sound.play()

# Create maze
maze = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

# Set up player
player_x = 1
player_y = 1

# Set up enemy1
enemy_x = 16
enemy_y = 6
enemy_dx = 0
enemy_dy = 0

# Set up enemy1
enemy_x2 = 16
enemy_y2 = 1
enemy_dx2 = 0
enemy_dy2 = 0

# Define variables for score
score = 0

# Define variables for timer
time_limit = 20  # 180 seconds = 3 minutes

def check_game_over():
    global score
    global time_limit

    if player_x == enemy_x and player_y == enemy_y:
        print("Collision with enemy 1")
        font = pygame.font.SysFont(None, 64)
        text = font.render("Game Over", True, (255, 0, 0))
        screen.blit(text, (300, 250))
        pygame.display.flip()
        if sound_channel.get_busy():
            sound_channel.stop()
        lose_sound.play()
        pygame.time.delay(3000)  # Delay for 2 seconds before quitting
        pygame.quit()
        sys.exit()

    if player_x == enemy_x2 and player_y == enemy_y2:
        print("Collision with enemy 2")
        font = pygame.font.SysFont(None, 64)
        text = font.render("Game Over", True, (255, 0, 0))
        screen.blit(text, (300, 250))
        pygame.display.flip()
        if sound_channel.get_busy():
            sound_channel.stop()
        lose_sound.play()
        pygame.time.delay(3000)  # Delay for 2 seconds before quitting
        pygame.quit()
        sys.exit()

    # Calculate the elapsed time
    elapsed_time = time.time() - start_time
    remaining_time = time_limit - int(elapsed_time)

    # Check if the elapsed time is greater than 60 seconds
    if remaining_time <= 0:
        print("You Won! ^_^")
        font = pygame.font.SysFont(None, 64)
        text = font.render("You Won!", True, (255, 255, 255))
        screen.blit(text, (300, 250))
        pygame.display.flip()
        if sound_channel.get_busy():
            sound_channel.stop()
        win_sound.play()
        pygame.time.delay(3000)  # Delay for 2 seconds before quitting
        pygame.quit()
        sys.exit()

# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Handle input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if maze[player_y][player_x - 1] == 0:
            player_x -= 1
    if keys[pygame.K_RIGHT]:
        if maze[player_y][player_x + 1] == 0:
            player_x += 1
    if keys[pygame.K_UP]:
        if maze[player_y - 1][player_x] == 0:
            player_y -= 1
    if keys[pygame.K_DOWN]:
        if maze[player_y + 1][player_x] == 0:
            player_y += 1

    # Move enemy1
    if random.random() < 0.1:
        enemy_dx, enemy_dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
    if maze[enemy_y + enemy_dy][enemy_x + enemy_dx] == 0:
        enemy_x += enemy_dx
        enemy_y += enemy_dy

    # Move enemy2
    if random.random() < 0.1:
        enemy_dx2, enemy_dy2 = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
    if maze[enemy_y2 + enemy_dy2][enemy_x2 + enemy_dx2] == 0:
        enemy_x2 += enemy_dx2
        enemy_y2 += enemy_dy2

    # Check for collision and game over conditions
    check_game_over()

    # Clear screen
    screen.fill((255, 255, 255))

    # Draw maze
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if maze[y][x] == 1:
                glColor3f(1, 1, 1)
            else:
                glColor3f(0, 0, 0)
            glBegin(GL_QUADS)
            glVertex2f(x * 50, y * 50)
            glVertex2f(x * 50 + 50, y * 50)
            glVertex2f(x * 50 + 50, y * 50 + 50)
            glVertex2f(x * 50, y * 50 + 50)
            glEnd()

    # Draw player
    glColor3f(0, 255, 0)
    glBegin(GL_QUADS)
    glVertex2f(player_x * 50 + 10, player_y * 50 + 10)
    glVertex2f(player_x * 50 + 40, player_y * 50 + 10)
    glVertex2f(player_x * 50 + 40, player_y * 50 + 40)
    glVertex2f(player_x * 50 + 10, player_y * 50 + 40)
    glEnd()

    # Draw enemy1
    glColor3f(255, 0, 0)
    glBegin(GL_QUADS)
    glVertex2f(enemy_x * 50 + 10, enemy_y * 50 + 10)
    glVertex2f(enemy_x * 50 + 40, enemy_y * 50 + 10)
    glVertex2f(enemy_x * 50 + 40, enemy_y * 50 + 40)
    glVertex2f(enemy_x * 50 + 10, enemy_y * 50 + 40)
    glEnd()

    # Draw enemy2
    glColor3f(255, 255, 0)
    glBegin(GL_QUADS)
    glVertex2f(enemy_x2 * 50 + 10, enemy_y2 * 50 + 10)
    glVertex2f(enemy_x2 * 50 + 40, enemy_y2 * 50 + 10)
    glVertex2f(enemy_x2 * 50 + 40, enemy_y2 * 50 + 40)
    glVertex2f(enemy_x2 * 50 + 10, enemy_y2 * 50 + 40)
    glEnd()

    # Render score
    font = pygame.font.SysFont(None, 36)
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Render timer
    elapsed_time = time.time() - start_time
    remaining_time = time_limit - int(elapsed_time)
    timer_text = font.render("Time: " + str(max(0, remaining_time)), True, (255, 255, 255))
    screen.blit(timer_text, (10, 50))

    # Render mini-map
    mini_map_size = (200, 200)
    mini_map_surface = pygame.Surface(mini_map_size)
    mini_map_surface.fill((0, 0, 0))

    # Draw maze elements on the mini-map
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if maze[y][x] == 1:
                pygame.draw.rect(mini_map_surface, (255, 255, 255), (x * 10, y * 10, 10, 10))
            else:
                pygame.draw.rect(mini_map_surface, (0, 0, 0), (x * 10, y * 10, 10, 10))

    # Mark player's position on the mini-map
    pygame.draw.rect(mini_map_surface, (0, 255, 0), (player_x * 10, player_y * 10, 10, 10))

    # Scale and blit the mini-map onto the main screen
    scaled_mini_map = pygame.transform.scale(mini_map_surface, (100, 100))
    screen.blit(scaled_mini_map, (10, 100))

    # Update screen
    pygame.display.flip()

    # Regulate frame rate
    clock.tick(8)