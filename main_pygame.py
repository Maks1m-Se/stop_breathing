import pygame
import random
import sys
import os
import math
import time

# Initialize pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()
monster_move=True

# Constants for screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 45  # Frames per second


# Load music
# random_menu_sound = random.choice(os.listdir(os.path.join('assets', 'sounds','music')))
# menu_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'music', random_menu_sound))
game_music = pygame.mixer.Sound(os.path.join('assets', 'music', 'chopin_funeral_lento_cut_eq.mp3'))
breath_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'breathing.ogg'))
intro_creepy_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'intro_creepy.mp3'))
kill_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'kill.mp3'))
monster_start_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'monster_start.mp3'))
inhale_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'inhale.mp3'))
gasp_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'gasp2.wav'))
holding_breath_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'holding_breath.ogg'))
breath_sound.set_volume(.1)
intro_creepy_sound.set_volume(.5)
monster_start_sound.set_volume(.2)
holding_breath_sound.set_volume(.5)
game_music.set_volume(2)

intro_creepy_sound.play()
breath_sound.play()


# Load images
PLAYER_IMAGE = pygame.image.load("assets/images/player.png")  # Replace with your player image path
MONSTER_IMAGE = pygame.image.load("assets/images/monster.png")  # Replace with your monster image path
PLAYER_DEAD_IMAGE = pygame.image.load("assets/images/player_dead.png")

# Scale images (optional, adjust as needed)
PLAYER_SIZE = (50, 50)
MONSTER_SIZE = (60, 60)
PLAYER_IMAGE = pygame.transform.scale(PLAYER_IMAGE, PLAYER_SIZE)
PLAYER_DEAD_IMAGE = pygame.transform.scale(PLAYER_DEAD_IMAGE, PLAYER_SIZE)
MONSTER_IMAGE = pygame.transform.scale(MONSTER_IMAGE, MONSTER_SIZE)

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
LIGHTGREY = (247, 241, 247)
LIGHTRED = (255, 196, 205)
COLOR_BUTTON = LIGHTGREY

# Button properties
button_width = 200
button_height = 50
button_x = (SCREEN_WIDTH - button_width) // 2
button_y = SCREEN_HEIGHT - button_height - 20  # 20 pixels above the bottom
# Track if space is held
space_held = False

class Player:
    def __init__(self, x, y):
        self.original_image = PLAYER_IMAGE
        self.image = self.original_image  # Rotated image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 2  # Player movement speed
        self.target_pos = (x, y)

    def update(self):
        """Move player towards target position."""
        target_x, target_y = self.target_pos
        dx, dy = target_x - self.rect.centerx, target_y - self.rect.centery
        distance = max(1, (dx**2 + dy**2) ** 0.5)  # Avoid division by zero
        if distance > self.speed:
            move_x, move_y = (dx / distance) * self.speed, (dy / distance) * self.speed
            self.rect.x += round(move_x)
            self.rect.y += round(move_y)
            
            # Calculate angle & rotate
            angle = -math.degrees(math.atan2(dy, dx)) - 90
            self.image = pygame.transform.rotate(self.original_image, angle)
            self.rect = self.image.get_rect(center=self.rect.center)

        else:
            self.rect.center = self.target_pos

    def set_target(self, pos):
        """Set new target position when clicked."""
        self.target_pos = pos

    def draw(self, screen):
        """Draw the player on the screen."""
        screen.blit(self.image, self.rect)

class Monster:
    def __init__(self, x, y):
        self.original_image = MONSTER_IMAGE
        self.image = self.original_image  # Rotated image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 2

    def update(self, target_pos, move):
        """Move the monster towards the player's position."""
        target_x, target_y = target_pos
        dx, dy = target_x - self.rect.centerx, target_y - self.rect.centery
        distance = max(1, (dx**2 + dy**2) ** 0.5)
        
        if move and distance > 0:
            move_x, move_y = (dx / distance) * self.speed, (dy / distance) * self.speed
            #print('move_x, move_y', move_x, move_y)
            self.rect.x += round(move_x)
            self.rect.y += round(move_y)

            # Calculate angle & rotate
            angle = -math.degrees(math.atan2(dy, dx)) + 90
            self.image = pygame.transform.rotate(self.original_image, angle)
            self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, screen):
        """Draw the monster on the screen."""
        screen.blit(self.image, self.rect)



def show_blood_splatter(screen, player, player_pos, monster, monster_pos):
    """Displays blood splatter away from the direction the monster was coming, using stretched ellipses."""
    SPLATTER_COUNT = 100  # Number of splatter shapes
    SPLATTER_SPREAD = 80  # Max distance for splatter

    # Calculate direction away from the monster
    dx = player_pos[0] - monster_pos[0] #random.randint(-1, 1)
    dy = player_pos[1] - monster_pos[1] #random.randint(-1, 1)
    distance = max(1, (dx**2 + dy**2) ** 0.5)
    if distance > 0:
        dir_x = (dx / distance) 
        dir_y = (dy / distance)   # Unit direction vector
    else:
        dir_x, dir_y = 0, 0  # Avoid division by zero

    

    # Draw blood splatter in elongated ellipses
    for i in range(SPLATTER_COUNT):
        
        BLOOD_COLOR = (random.randint(150, 230), random.randint(0, 20), random.randint(0, 20))
        
        # Start splatter close to player
        start_x = player_pos[0] + random.randint(-2, 2)  
        start_y = player_pos[1] + random.randint(-2, 2)
        
        # Stretch outward from player in opposite direction of the monster
        splatter_x = start_x + (dir_x * random.randint(2, SPLATTER_SPREAD))
        splatter_y = start_y + (dir_y * random.randint(2, SPLATTER_SPREAD))
        print('splatter_x, splatter_y', splatter_x, splatter_y)

        # Rotate the ellipse to align with splatter direction
        angle = -math.degrees(math.atan2(dy, dx))
        print('angle', angle)


        # Create ellipse surface
        ellipse_width = random.randint(5, 12)
        ellipse_height = random.randint(2, 6)
        ellipse_surface = pygame.Surface((ellipse_width, ellipse_height), pygame.SRCALPHA)
        pygame.draw.ellipse(ellipse_surface, BLOOD_COLOR, (0, 0, ellipse_width, ellipse_height))
        
        # Rotate ellipse
        rotated_ellipse = pygame.transform.rotate(ellipse_surface, angle)
        
        # Get rect to position correctly
        ellipse_rect = rotated_ellipse.get_rect(center=(int(splatter_x), int(splatter_y)))
        
        # Draw splatter
        screen.blit(rotated_ellipse, ellipse_rect)
        
        # Draw game elements
        player.image = pygame.transform.rotate(PLAYER_DEAD_IMAGE, -math.degrees(math.atan2(dy, dx)+90))
        screen.blit(player.image, player.rect)
        monster.draw(screen)

        pygame.display.flip()
        #print(i)
        #print(0.0001*i)
        time.sleep(0.00002*i)



# Main game function
def main():
    global space_held, COLOR_BUTTON, button_x, button_y, button_width, button_height, monster_move

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Stop Breathing")
    clock = pygame.time.Clock()
    
    # Initialize player and monster
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    # Randomly select an edge for the monster to come from
    direction = random.choice(['top', 'bottom', 'left', 'right'])
    # Depending on the selected direction, set the monster's position
    if direction == 'top':
        x_monster_start = random.randint(0, SCREEN_WIDTH)  # Random x within screen width
        y_monster_start = -100  # Off the top of the screen
    elif direction == 'bottom':
        x_monster_start = random.randint(0, SCREEN_WIDTH)  # Random x within screen width
        y_monster_start = SCREEN_HEIGHT + 100  # Off the bottom of the screen
    elif direction == 'left':
        x_monster_start = -100  # Off the left side of the screen
        y_monster_start = random.randint(0, SCREEN_HEIGHT)  # Random y within screen height
    else:  # direction == 'right'
        x_monster_start = SCREEN_WIDTH + 100  # Off the right side of the screen
        y_monster_start = random.randint(0, SCREEN_HEIGHT)  # Random y within screen height

    monster = Monster(x_monster_start, y_monster_start)
    click_positions = []
    player_dead = False  # Track if player is dead
    # Draw everything initially
    screen.fill(WHITE)
    player.draw(screen)
    monster.draw(screen)
    pygame.display.flip()
    game_music.play()
    time.sleep(3)
    monster_start_sound.play()
    

    running = True
    
    while running:
        screen.fill(WHITE)  # Clear screen
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_positions.clear()
                click_pos = pygame.mouse.get_pos()
                player.set_target(click_pos)
                click_positions.append(click_pos)
            elif event.type == pygame.KEYDOWN:             
                if event.key == pygame.K_SPACE:
                    if not space_held:  # If space wasn't held, start holding
                        COLOR_BUTTON = LIGHTRED
                        space_held = True
                        monster_move = False

                        gasp_sound.stop()
                        breath_sound.stop()

                        inhale_sound.play()  # Play hold breath sound when space is pressed
                        holding_breath_sound.play()
                        
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    if space_held:  # If space was held, stop holding
                        COLOR_BUTTON = LIGHTGREY  
                        space_held = False
                        monster_move = True

                        inhale_sound.stop()
                        holding_breath_sound.stop()

                        gasp_sound.play()  # Play breath sound when space is released
                        breath_sound.play()
        
        # Update player movement towards last clicked position
        if not player_dead:  # Only update movement if alive
            player.update()
            monster.update(player.rect.center, monster_move)
        
        # Check collision
        if player.rect.colliderect(monster.rect):
            pygame.mixer.stop()
            kill_sound.play()
            player_dead = True  # Mark as dead
            show_blood_splatter(screen, player, player.rect.center, monster, monster.rect.center)
            print("Game Over! The monster caught you.")
            time.sleep(3)
            running = False
            break

        # Draw click positions
        for pos in click_positions:
            pygame.draw.circle(screen, RED, pos, 3)
        # Draw everything
        player.draw(screen)
        monster.draw(screen)

        # Draw "Hold Breath" button
        pygame.draw.rect(screen, COLOR_BUTTON, (button_x, button_y, button_width, button_height))
        font = pygame.font.Font(None, 36)
        text = font.render("Hold Breath", True, (0, 0, 0))
        screen.blit(text, (button_x + (button_width - text.get_width()) // 2, button_y + (button_height - text.get_height()) // 2))
        
        
        

        pygame.display.flip()
        clock.tick(FPS)  # Maintain FPS
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
