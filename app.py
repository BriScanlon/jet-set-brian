import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Code Jumpers")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)

# Define fonts
font = pygame.font.Font(None, 74)
hello_world_font = pygame.font.Font(None, 150)  # Larger font for "Hello World!"

# Define character properties
character_size = 50
character_speed = 5
character_y_velocity = 0

# Gravity and Jump properties
gravity = 0.8
jump_power = -15
is_jumping = False

# Define game variables
lives = 3
score = 0
total_collectibles = 4
all_collectibles_collected = False
fade_alpha = 0  # Alpha value for the fade effect
fade_complete = False  # Flag to track if the fade is done
message_displayed = False  # Track if "Hello World!" has been displayed

# Ground level (where the character "lands")
ground_level = screen_height - character_size

# Define borders and gaps
border_thickness = 10

# Define some example layouts
maps = [
    # Map 1: Only right door (leads to Map 2)
    {
        "platforms": [
            pygame.Rect(100, 400, 200, 20),
            pygame.Rect(400, 300, 200, 20),
            pygame.Rect(600, 500, 150, 20),
        ],
        "enemies": [
            {
                "rect": pygame.Rect(150, 380, 30, 30),
                "speed": 2,
                "direction": 1,
                "range": (100, 300),
            }
        ],
        "collectibles": [pygame.Rect(700, 470, 30, 30)],
        "gaps": {"left": False, "right": True},  # Door on the right side
    },
    # Map 2: Left door (to Map 1), right door (to Map 3)
    {
        "platforms": [pygame.Rect(150, 450, 250, 20), pygame.Rect(350, 200, 150, 20)],
        "enemies": [
            {
                "rect": pygame.Rect(350, 180, 30, 30),
                "speed": 2,
                "direction": -1,
                "range": (350, 500),
            }
        ],
        "collectibles": [pygame.Rect(300, 470, 30, 30)],
        "gaps": {"left": True, "right": True},  # Doors on both sides
    },
    # Map 3: Left door (to Map 2), right door (to Map 4)
    {
        "platforms": [pygame.Rect(200, 350, 200, 20), pygame.Rect(500, 250, 150, 20), pygame.Rect(150, 450, 150, 20)],
        "enemies": [
            {
                "rect": pygame.Rect(500, 230, 30, 30),
                "speed": 2,
                "direction": -1,
                "range": (500, 650),
            }
        ],
        "collectibles": [pygame.Rect(600, 200, 30, 30)],
        "gaps": {"left": True, "right": True},  # Doors on both sides
    },
    # Map 4: Only left door (leads to Map 3)
    {
        "platforms": [pygame.Rect(300, 400, 200, 20), pygame.Rect(600, 200, 150, 20), pygame.Rect(150, 450, 150, 20)],
        "enemies": [
            {
                "rect": pygame.Rect(350, 380, 30, 30),
                "speed": 2,
                "direction": 1,
                "range": (300, 500),
            }
        ],
        "collectibles": [pygame.Rect(650, 300, 30, 30)],
        "gaps": {"left": True, "right": False},  # Door on the left side
    },
]


current_map_index = 0
character_x = screen_width // 2
character_y = ground_level

def reset_character():
    """Resets the character's position when moving to a new map"""
    global character_x, character_y
    character_x = screen_width // 2
    character_y = ground_level


def check_for_map_transition():
    """Checks if the character is moving through a gap to a new map"""
    global current_map_index
    current_map = maps[current_map_index]

    # If character moves through a gap, switch map
    if current_map["gaps"]["left"] and character_x < 0:
        current_map_index = max(current_map_index - 1, 0)  # Move to previous map but don't go below 0
        reset_character()
    elif current_map["gaps"]["right"] and character_x + character_size > screen_width:
        current_map_index = min(current_map_index + 1, len(maps) - 1)  # Move to next map but don't exceed max index
        reset_character()

def draw_borders():
    """Draw the borders and orange doors (gaps) on the left or right sides only"""
    current_map = maps[current_map_index]
    gaps = current_map["gaps"]

    # Draw the borders with no gaps at the top or bottom
    pygame.draw.rect(screen, BLACK, pygame.Rect(0, 0, screen_width, border_thickness))  # Top border
    pygame.draw.rect(screen, BLACK, pygame.Rect(0, screen_height - border_thickness, screen_width, border_thickness))  # Bottom border

    # Draw the left border, leaving a gap if 'left' is True
    if not gaps["left"]:
        pygame.draw.rect(screen, BLACK, pygame.Rect(0, 0, border_thickness, screen_height))  # Solid left border
    else:
        # Draw an orange door on the left side
        pygame.draw.rect(screen, ORANGE, pygame.Rect(0, screen_height, border_thickness, 100))  # Door on the left

    # Draw the right border, leaving a gap if 'right' is True
    if not gaps["right"]:
        pygame.draw.rect(screen, BLACK, pygame.Rect(screen_width - border_thickness, 0, border_thickness, screen_height))  # Solid right border
    else:
        # Draw an orange door on the right side
        pygame.draw.rect(screen, ORANGE, pygame.Rect(screen_width - border_thickness, screen_height, border_thickness, 100))  # Door on the right


def display_lives():
    """Display lives at the top-left of the screen"""
    lives_text = font.render(f"Lives: {lives}", True, BLACK)
    screen.blit(lives_text, (20, 20))


def display_score():
    """Display the current score and collectible counter"""
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (20, 100))


def handle_collectibles(character_rect):
    """Check if player collects any collectibles and update the score"""
    global score, total_collectibles, all_collectibles_collected
    current_map = maps[current_map_index]
    if len(current_map["collectibles"]) == 0 and total_collectibles == 0:
        all_collectibles_collected = True
    else:
        for collectible in current_map["collectibles"][:]:  # Iterate over a copy of the list
            if character_rect.colliderect(collectible):
                current_map["collectibles"].remove(collectible)  # Remove the collected item
                score += 10  # Add 10 points for each collectible
                total_collectibles -= 1


def update_enemies():
    """Update enemy positions smoothly"""
    current_map = maps[current_map_index]
    for enemy in current_map["enemies"]:
        enemy_rect = enemy["rect"]

        # Update the enemy's position based on its speed and direction
        enemy_rect.x += enemy["speed"] * enemy["direction"]

        # Reverse direction if the enemy hits the edge of its movement range
        if enemy_rect.x <= enemy["range"][0]:
            enemy["rect"].x = enemy["range"][0]  # Snap to range start to avoid jitter
            enemy["direction"] = 1  # Move right
        elif enemy_rect.x >= enemy["range"][1] - enemy_rect.width:
            enemy["rect"].x = enemy["range"][1] - enemy_rect.width  # Snap to range end to avoid jitter
            enemy["direction"] = -1  # Move left


def fade_to_black():
    """ Fades the screen to black by gradually increasing a black surface's alpha """
    global fade_alpha, fade_complete
    fade_surface = pygame.Surface((screen_width, screen_height))
    fade_surface.fill(BLACK)
    if fade_alpha < 255:  # Keep increasing the alpha value until fully opaque
        fade_alpha += 5  # Increase the fade speed
        fade_surface.set_alpha(fade_alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
    else:
        fade_complete = True  # Fade is complete when alpha reaches 255


def display_hello_world():
    """ Displays 'Hello World!' in blocky 8-bit style """
    global message_displayed
    screen.fill(BLACK)  # Fully black background after the fade
    message = "HELLO WORLD!"
    message_surface = hello_world_font.render(message, True, RED)
    screen.blit(message_surface, (screen_width // 2 - message_surface.get_width() // 2, screen_height // 2 - message_surface.get_height() // 2))
    pygame.display.flip()
    message_displayed = True  # Set flag to avoid redrawing message continuously


# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # If all collectibles are gathered, start the fade and display process
    if score == 40 and not fade_complete:
        fade_to_black()  # Gradually fade to black
    elif fade_complete and not message_displayed:
        display_hello_world()  # Show the "Hello World!" message after fade is done

    if all_collectibles_collected:
        display_hello_world()  # Ensure "Hello World!" is displayed when all collectibles are gathered
    else:
        # Movement logic
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            character_x -= character_speed
        if keys[pygame.K_RIGHT]:
            character_x += character_speed
        if keys[pygame.K_SPACE] and not is_jumping:
            character_y_velocity = jump_power
            is_jumping = True

        # Apply gravity
        character_y_velocity += gravity
        character_y += character_y_velocity

        # Check for landing on platforms
        character_rect = pygame.Rect(character_x, character_y, character_size, character_size)
        on_platform = False
        current_map = maps[current_map_index]
        for platform in current_map["platforms"]:
            if character_rect.colliderect(platform) and character_y_velocity >= 0:
                character_y = platform.y - character_size
                character_y_velocity = 0
                is_jumping = False
                on_platform = True

        # If not on a platform, apply gravity
        if not on_platform and character_y >= ground_level:
            character_y = ground_level
            character_y_velocity = 0
            is_jumping = False

        # Check for map transitions through gaps
        check_for_map_transition()

        # Handle collectibles
        handle_collectibles(character_rect)

        # Update enemies
        update_enemies()

        # Fill the screen with white
        screen.fill(WHITE)

        # Draw borders with gaps
        draw_borders()

        # Draw the platforms
        for platform in current_map["platforms"]:
            pygame.draw.rect(screen, GREEN, platform)

        # Draw the character (a simple red rectangle for now)
        pygame.draw.rect(screen, RED, character_rect)

        # Draw the enemies (blue rectangles)
        for enemy in current_map["enemies"]:
            pygame.draw.rect(screen, BLUE, enemy["rect"])

        # Draw the collectibles (yellow rectangles)
        for collectible in current_map["collectibles"]:
            pygame.draw.rect(screen, YELLOW, collectible)

        # Display lives and score
        display_lives()
        display_score()

        # Update the display
        pygame.display.flip()

    # Set the frame rate
    pygame.time.Clock().tick(60)
