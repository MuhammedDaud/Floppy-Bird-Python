import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Load images
background = pygame.image.load(r'C:\Users\Lenovo\Desktop\Floppy Bird Python\back.png')
bird_img = pygame.image.load(r'C:\Users\Lenovo\Desktop\Floppy Bird Python\bird.png')
pipe_img = pygame.image.load(r'C:\Users\Lenovo\Desktop\Floppy Bird Python\pipe.png')
ground_img = pygame.image.load(r'C:\Users\Lenovo\Desktop\Floppy Bird Python\ground.png')

# Scale images
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
bird_img = pygame.transform.scale(bird_img, (40, 40))
pipe_img = pygame.transform.scale(pipe_img, (60, 400))
ground_img = pygame.transform.scale(ground_img, (SCREEN_WIDTH, 100))

# Bird settings
bird_x = 60
bird_y = SCREEN_HEIGHT // 2
bird_y_speed = 0
gravity = 0.5
flap_strength = -10

# Pipe settings
pipe_gap = 150
pipe_speed = 3
pipe_frequency = 1500  # in milliseconds
pipe_heights = [200, 250, 300, 350]

# Ground settings
ground_y = SCREEN_HEIGHT - 100

# Colors
WHITE = (255, 255, 255)

# Game variables
pipes = []
score = 0
running = True
game_over = False

# Font
font = pygame.font.SysFont("Arial", 40)

def draw_bird():
    screen.blit(bird_img, (bird_x, bird_y))

def draw_pipes(pipes):
    for pipe in pipes:
        screen.blit(pipe_img, (pipe['x'], pipe['top']))
        screen.blit(pygame.transform.flip(pipe_img, False, True), (pipe['x'], pipe['bottom']))

def draw_ground():
    screen.blit(ground_img, (0, ground_y))

def check_collision(pipes):
    global bird_y, ground_y, game_over

    # Check ground collision
    if bird_y + bird_img.get_height() >= ground_y:
        game_over = True
        return True

    # Check pipe collision
    for pipe in pipes:
        if bird_x + bird_img.get_width() > pipe['x'] and bird_x < pipe['x'] + pipe_img.get_width():
            if bird_y < pipe['top'] + pipe_img.get_height() or bird_y + bird_img.get_height() > pipe['bottom']:
                game_over = True
                return True
    return False

def display_score(score):
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 50))

# Spawn initial pipes
def create_pipe():
    pipe_height = random.choice(pipe_heights)
    bottom_pipe_y = pipe_height + pipe_gap
    return {'x': SCREEN_WIDTH, 'top': pipe_height - pipe_img.get_height(), 'bottom': bottom_pipe_y}

# Game Loop
pipe_timer = pygame.USEREVENT + 1
pygame.time.set_timer(pipe_timer, pipe_frequency)

while running:
    screen.blit(background, (0, 0))  # Draw background
    draw_bird()                      # Draw bird
    draw_pipes(pipes)                # Draw pipes
    draw_ground()                    # Draw ground
    display_score(score)             # Display the score

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:  # Only flap if game is not over
                bird_y_speed = flap_strength  # Apply flap strength
                print("Space pressed!")  # Debugging statement to check if space is pressed

        if event.type == pipe_timer and not game_over:
            pipes.append(create_pipe())

    if not game_over:
        # Bird gravity effect
        bird_y_speed += gravity
        bird_y += bird_y_speed

        # Ensure bird doesn't go above the screen
        if bird_y < 0:
            bird_y = 0

        # Move pipes
        pipes = [{'x': pipe['x'] - pipe_speed, 'top': pipe['top'], 'bottom': pipe['bottom']} for pipe in pipes]
        pipes = [pipe for pipe in pipes if pipe['x'] > -pipe_img.get_width()]

        # Check for pipe passes and increment score
        for pipe in pipes:
            if pipe['x'] + pipe_img.get_width() < bird_x and not pipe.get('passed', False):
                pipe['passed'] = True
                score += 1

        # Check for collisions
        if check_collision(pipes):
            pass  # Game over, do nothing further

    # Update display
    pygame.display.update()
    clock.tick(60)

# End the game
pygame.quit()
