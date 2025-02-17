import pygame
import random
import sys
import os
import math
import time
import asyncio

# Initialize pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()


# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 800
FPS = 45

# Colors
BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (191, 4, 19)
GREY = (157, 151, 157)
LIGHTGREY = (247, 241, 247)
LIGHTRED = (255, 196, 205)
BLUE = (7, 136, 217)
LIGHTBLUE = (213, 231, 242)
COLORS_AIRBAR = [BLUE, LIGHTBLUE]
COLOR_BUTTON = [BLUE, LIGHTGREY]

font1 = pygame.font.Font(None, 200)  # Choose a large font
font2 = pygame.font.Font(None, 150)  # Choose a large font
font3 = pygame.font.Font(None, 30)  # Choose a large font

# Game State Variables
space_held = False
monster_move = True

                         
# Load music
# random_menu_sound = random.choice(os.listdir(os.path.join('assets', 'sounds','music')))
# menu_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'music', random_menu_sound))
game_music = pygame.mixer.Sound(os.path.join('assets', 'music', 'chopin_funeral_lento_cut_eq.mp3'))
breath_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'breathing.ogg'))
creepy_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'intro_creepy.mp3'))
kill_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'kill.mp3'))
monster_start_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'monster_start.mp3'))
inhale_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'inhale.mp3'))
gasp_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'gasp2.wav'))
holding_breath_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'holding_breath.ogg'))
poke_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'poke.wav'))
click_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'click.mp3'))

horror_hit_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'horror-hit.mp3'))
choke_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'choke.mp3'))

poke_sound.set_volume(.3)
breath_sound.set_volume(.1)
creepy_sound.set_volume(.5)
monster_start_sound.set_volume(.2)
holding_breath_sound.set_volume(.5)
game_music.set_volume(2)


breath_sound.play()


# Load images
PLAYER_IMAGE = pygame.image.load("assets/images/player.png")  # Replace with your player image path
MONSTER_IMAGE = pygame.image.load("assets/images/monster.png")  # Replace with your monster image path
PLAYER_DEAD_IMAGE = pygame.image.load("assets/images/player_dead.png")
DIZZY_IMAGE = pygame.image.load("assets/images/dizzy5.png")




# Scale images (optional, adjust as needed)

PLAYER_SIZE = (40, 40)
MONSTER_SIZE = (100, 100)
PLAYER_IMAGE = pygame.transform.scale(PLAYER_IMAGE, PLAYER_SIZE)
PLAYER_DEAD_IMAGE = pygame.transform.scale(PLAYER_DEAD_IMAGE, PLAYER_SIZE)
MONSTER_IMAGE = pygame.transform.scale(MONSTER_IMAGE, MONSTER_SIZE)
DIZZY_IMAGE = pygame.transform.scale(DIZZY_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))



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

class AirBar():
    def __init__(self, x, y, width, height, max_air):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.air = max_air
        self.max_air = max_air
    
    def draw(self, surface):
        if self.air > self.max_air:
            self.air = self.max_air
        if self.air < 0:
            self.air = 0
            
        ratio = self.air / self.max_air
        pygame.draw.rect(surface, COLORS_AIRBAR[1], (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, COLORS_AIRBAR[0], (self.x, self.y, self.width  * ratio, self.height))

def display_announcement(screen, text1, text2, show_replay=False):
    
    text1_surface = font1.render(text1, True, RED)  # Main message
    text2_surface = font2.render(text2, True, RED)  # Sub message
    text1_rect = text1_surface.get_rect(center=(SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * .33)))
    text2_rect = text2_surface.get_rect(center=(SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * .66)))
    
    # fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    # fade_surface.fill((0,0,0))
    # fade_surface.set_alpha(100)
    # screen.blit(fade_surface, (0, 0)) # Black background
    screen.blit(text1_surface, text1_rect)  # Draw title text
    screen.blit(text2_surface, text2_rect)  # Draw subtitle text
    

    time.sleep(1)
    # Draw replay button if needed
    if show_replay:
        # replay_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT * 0.8, 200, 60)
        # pygame.draw.rect(screen, COLOR_BUTTON[1], replay_rect)
        # font = pygame.font.Font(None, 50)
        # text = font.render("Replay", True, COLOR_BUTTON[0])
        # screen.blit(text, (replay_rect.x + (200 - text.get_width()) // 2, replay_rect.y + (60 - text.get_height()) // 2))
        # ##
        button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT * 0.8, 200, 60)
        color = GREY
        pygame.draw.rect(screen, color, button_rect, border_radius=10)  
        label_surface = font3.render("RESTART", True, BLACK)
        screen.blit(label_surface, (button_rect.x + (200 - label_surface.get_width()) // 2, button_rect.y + (60 - label_surface.get_height()) // 2))     

    creepy_sound.play()
    pygame.display.flip()
    
    return button_rect if show_replay else None

def wait_for_replay_click(screen, button_rect):
    """Waits for user to click replay button or quit the game."""
    while True:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        color = GREY if button_rect.collidepoint(mouse_x, mouse_y) else LIGHTGREY  
        pygame.draw.rect(screen, color, button_rect, border_radius=10)  
        label_surface = font3.render("RESTART", True, BLACK)
        screen.blit(label_surface, (button_rect.x + (200 - label_surface.get_width()) // 2, button_rect.y + (60 - label_surface.get_height()) // 2))     
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    click_sound.play()
                    return  # Restart the game

        #pygame.time.delay(100)  # Small delay to avoid CPU overload

def player_dying(screen, player, player_pos, monster, monster_pos, display_blood=True):
    """Dying of player. Displays blood splatter away from the direction the monster was coming, using stretched ellipses."""
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
        if display_blood:
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
async def main():
    global space_held, COLOR_BUTTON, button_x, button_y, button_width, button_height, monster_move, COLORS_AIRBAR, COLOR_BUTTON

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Stop Breathing")
    clock = pygame.time.Clock()

    airbar = AirBar(SCREEN_WIDTH*0.02, SCREEN_WIDTH*0.01, SCREEN_WIDTH*0.96, 5, 1000)
    
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
    #airbar.draw(screen)
    player.draw(screen)
    monster.draw(screen)

    # Display game title
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill((0,0,0))
    fade_surface.set_alpha(200)
    screen.blit(fade_surface, (0, 0))
    pygame.display.flip()

    await asyncio.sleep(2)

    display_announcement(screen, 'STOP', 'BREATHING')
  
    await asyncio.sleep(3)

    game_music.play()
    monster_start_sound.play()
    

    running = True
    
    while running:
        screen.fill(WHITE)  # Clear screen
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                poke_sound.play()
                click_positions.clear()
                click_pos = pygame.mouse.get_pos()
                player.set_target(click_pos)
                click_positions.append(click_pos)
            elif event.type == pygame.KEYDOWN:             
                if event.key == pygame.K_SPACE:
                    if not space_held:  # If space wasn't held, start holding
                        space_held = True
                        monster_move = False
                        COLORS_AIRBAR = [RED, LIGHTRED]
                        COLOR_BUTTON = [RED, LIGHTRED]

                        gasp_sound.stop()
                        breath_sound.stop()

                        inhale_sound.play()  # Play hold breath sound when space is pressed
                        holding_breath_sound.play()
                        
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    if space_held:  # If space was held, stop holding 
                        space_held = False
                        monster_move = True
                        COLORS_AIRBAR = [BLUE, LIGHTBLUE]
                        COLOR_BUTTON = [BLUE, LIGHTGREY]

                        inhale_sound.stop()
                        holding_breath_sound.stop()

                        gasp_sound.play()  # Play breath sound when space is released
                        breath_sound.play()
        
        if not space_held:
            airbar.air += 1
        else:
            airbar.air -= 1
        DIZZY_IMAGE.set_alpha(255-255*airbar.air/airbar.max_air)
        print('air', airbar.air)
        print('dizzy alpha', 255-255*airbar.air/airbar.max_air)

        # Update player movement towards last clicked position
        if not player_dead:  # Only update movement if alive
            player.update()
            monster.update(player.rect.center, monster_move)
        

        # Collision Monster Player 
        player_mask = pygame.mask.from_surface(player.image)
        monster_mask = pygame.mask.from_surface(monster.image)
        offset = (monster.rect.x - player.rect.x, monster.rect.y - player.rect.y)

        if player_mask.overlap(monster_mask, offset):  # Checks exact shape collision
            pygame.mixer.stop()
            horror_hit_sound.play()
            kill_sound.play()
            player_dead = True  # Mark as dead
            player_dying(screen, player, player.rect.center, monster, monster.rect.center, display_blood=True)
            print("Game Over! The monster caught you.")
            await asyncio.sleep(2)
            button_rect = display_announcement(screen, "GAME OVER", "Caught", show_replay=True)
            wait_for_replay_click(screen, button_rect)  # Wait for replay click
            await main()  # Restart game
            await asyncio.sleep(6)
            running = False
            break

        # Out of air
        if airbar.air <= 0:
            pygame.mixer.stop()
            horror_hit_sound.play()
            choke_sound.play()

            player_dying(screen, player, player.rect.center, monster, monster.rect.center, display_blood=False)
            print("Game Over! You suffocated")
            await asyncio.sleep(2)
            button_rect = display_announcement(screen, "GAME OVER", "Suffocated", show_replay=True)
            wait_for_replay_click(screen, button_rect)
            await main()
            await asyncio.sleep(6)
            running = False
            break


        # Draw click positions
        for pos in click_positions:
            pygame.draw.circle(screen, BLACK, pos, 3)
        # Draw everything
        airbar.draw(screen)
        player.draw(screen)
        monster.draw(screen)


        # Draw "Hold Breath" button
        pygame.draw.rect(screen, COLOR_BUTTON[1], (button_x, button_y, button_width, button_height))
        font = pygame.font.Font(None, 36)
        text = font.render("Hold Breath", True, COLOR_BUTTON[0])
        screen.blit(text, (button_x + (button_width - text.get_width()) // 2, button_y + (button_height - text.get_height()) // 2))
        
        # DIZZY
        screen.blit(DIZZY_IMAGE, (0,0))
        

        pygame.display.flip()
        clock.tick(FPS)  # Maintain FPS
        await asyncio.sleep(0)
    
    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())
