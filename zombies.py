import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

# Get the user's screen resolution
SCREEN_INFO = pygame.display.Info()
SCREEN_WIDTH = SCREEN_INFO.current_w
SCREEN_HEIGHT = SCREEN_INFO.current_h

# Constants
PLAYER_SIZE = 40
ZOMBIE_SIZE = 40
WEAPON_SIZE = 20
BULLET_PACK_SIZE = 20
HEALTH_PACK_SIZE = 20
POWER_UP_SIZE = 20
MONEY_SIZE = 10  # Size of money items
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)  # Color for money
MENU_FONT_SIZE = 48

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Hunters vs Zombies")

# Create player and initial position
player = pygame.Rect(SCREEN_WIDTH // 2 - PLAYER_SIZE // 2, SCREEN_HEIGHT // 2 - PLAYER_SIZE // 2, PLAYER_SIZE, PLAYER_SIZE)
player_speed = 7
player_velocity = [0, 0]

# Create lists for zombies, bullets, bullet packs, health packs, power-ups, and money
zombies = []
bullets = []
bullet_packs = []
health_packs = []
power_ups = []
money_items = []

# Create fonts for displaying score, bullet count, health, money, and menu
font = pygame.font.Font(None, 36)
menu_font = pygame.font.Font(None, MENU_FONT_SIZE)

# File path for saving and loading money
money_file_path = "money.txt"

# Function to save the player's money to a file
def save_money():
    with open(money_file_path, "w") as file:
        file.write(str(money))

# Function to load the player's money from a file
def load_money():
    try:
        with open(money_file_path, "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0  # Return 0 if the file doesn't exist

# Initialize money with the loaded value or 0 if the file doesn't exist
money = load_money()

# Initialize score, bullet count, health, and power-up counter
score = 0
bullet_count = 22  # Initial bullet count
health = 100  # Initial health
power_up_counter = 0

# Initialize available weapons and their prices
weapons = {
    "Pistol": 100,
    "Shotgun": 200,
    "Machine Gun": 300,
}
selected_weapon = "Pistol"  # Initial selected weapon
equipped_weapon = "Pistol"  # Initial equipped weapon

# Define weapon properties (damage, bullet speed, bullet count, etc.) for different weapons
weapon_properties = {
    "Pistol": {"damage": 10, "bullet_speed": 10, "bullet_count": 20},
    "Shotgun": {"damage": 20, "bullet_speed": 8, "bullet_count": 10},
    "Machine Gun": {"damage": 5, "bullet_speed": 12, "bullet_count": 30},
}

# Initialize selected weapon and money
selected_weapon = "Pistol"
money = 0

# Menu options
start_option = menu_font.render("Start Game", True, BLUE)
shop_option = menu_font.render("Shop", True, BLUE)
menu_options = [start_option, shop_option]
selected_option = 0

# Create a function to save the player's money to a file
def save_money():
    with open(money_file_path, "w") as file:
        file.write(str(money))

# Create a function to load the player's money from a file
def load_money():
    try:
        with open(money_file_path, "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0  # Return 0 if the file doesn't exist

# Initialize money with the loaded value or 0 if the file doesn't exist
money = load_money()

def create_zombie():
    x = random.randint(0, SCREEN_WIDTH - ZOMBIE_SIZE)
    y = random.randint(0, SCREEN_HEIGHT - ZOMBIE_SIZE)
    zombie = pygame.Rect(x, y, ZOMBIE_SIZE, ZOMBIE_SIZE)
    zombies.append(zombie)

def create_bullet(angle, bullet_speed, bullet_damage):
    global bullet_count
    if bullet_count > 0:
        dx = bullet_speed * math.cos(angle)
        dy = bullet_speed * math.sin(angle)
        bullet = [player.centerx - 5, player.centery - 5, dx, dy, bullet_damage]  # Add bullet damage
        bullets.append(bullet)
        bullet_count -= 1

def create_bullet_pack():
    x = random.randint(0, SCREEN_WIDTH - BULLET_PACK_SIZE)
    y = random.randint(0, SCREEN_HEIGHT - BULLET_PACK_SIZE)
    bullet_pack = pygame.Rect(x, y, BULLET_PACK_SIZE, BULLET_PACK_SIZE)
    bullet_packs.append(bullet_pack)

def create_health_pack():
    x = random.randint(0, SCREEN_WIDTH - HEALTH_PACK_SIZE)
    y = random.randint(0, SCREEN_HEIGHT - HEALTH_PACK_SIZE)
    health_pack = pygame.Rect(x, y, HEALTH_PACK_SIZE, HEALTH_PACK_SIZE)
    health_packs.append(health_pack)

def create_power_up():
    x = random.randint(0, SCREEN_WIDTH - POWER_UP_SIZE)
    y = random.randint(0, SCREEN_HEIGHT - POWER_UP_SIZE)
    power_up = pygame.Rect(x, y, POWER_UP_SIZE, POWER_UP_SIZE)
    power_ups.append(power_up)

def create_money():
    x = random.randint(0, SCREEN_WIDTH - MONEY_SIZE)
    y = random.randint(0, SCREEN_HEIGHT - MONEY_SIZE)
    money_item = pygame.Rect(x, y, MONEY_SIZE, MONEY_SIZE)
    money_items.append(money_item)

def move_zombies():
    for zombie in zombies:
        if zombie.x < player.x:
            zombie.x += 1
        elif zombie.x > player.x:
            zombie.x -= 1
        if zombie.y < player.y:
            zombie.y += 1
        elif zombie.y > player.y:
            zombie.y -= 1

def move_bullets():
    for bullet in bullets:
        bullet[0] += bullet[2]  # Update x position
        bullet[1] += bullet[3]  # Update y position
        if bullet[0] > SCREEN_WIDTH or bullet[0] < 0 or bullet[1] > SCREEN_HEIGHT or bullet[1] < 0:
            bullets.remove(bullet)

def main_menu():
    global selected_option
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        game_loop()
                    elif selected_option == 1:
                        shop_menu()

        screen.fill(WHITE)
        menu_y = SCREEN_HEIGHT // 2 - (len(menu_options) * MENU_FONT_SIZE) // 2
        for i, option in enumerate(menu_options):
            if i == selected_option:
                pygame.draw.circle(screen, BLUE, (SCREEN_WIDTH // 2, menu_y + MENU_FONT_SIZE // 2), 5)
            screen.blit(option, (SCREEN_WIDTH // 2 - MENU_FONT_SIZE, menu_y))
            menu_y += MENU_FONT_SIZE

        pygame.display.flip()

def shop_menu():
    global money, selected_weapon, equipped_weapon
    weapon_list = list(weapons.keys())
    selected_index = weapon_list.index(selected_weapon)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # Return to the main menu

        screen.fill(WHITE)
        shop_text = menu_font.render("Shop", True, BLUE)
        money_text = font.render(f"Money: ${money}", True, GOLD)

        weapon_y = SCREEN_HEIGHT // 2 - (len(weapons) * MENU_FONT_SIZE) // 2
        for i, weapon in enumerate(weapon_list):
            if i == selected_index:
                pygame.draw.circle(screen, BLUE, (SCREEN_WIDTH // 2, weapon_y + MENU_FONT_SIZE // 2), 5)
            weapon_text = menu_font.render(f"{weapon} - ${weapons[weapon]}", True, BLUE)
            screen.blit(weapon_text, (SCREEN_WIDTH // 2 - MENU_FONT_SIZE, weapon_y))
            weapon_y += MENU_FONT_SIZE

        screen.blit(shop_text, (SCREEN_WIDTH // 2 - 100, 50))
        screen.blit(money_text, (10, 10))

        pygame.display.flip()

        # Check if the player wants to navigate through available weapons
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            selected_index = (selected_index - 1) % len(weapon_list)
        if keys[pygame.K_DOWN]:
            selected_index = (selected_index + 1) % len(weapon_list)

        if keys[pygame.K_RETURN]:
            selected_weapon = weapon_list[selected_index]
            price = weapons[selected_weapon]
            if money >= price:
                money -= price
                equipped_weapon = selected_weapon  # Equip the selected weapon
                bullet_count = weapon_properties[selected_weapon]["bullet_count"]  # Set initial bullet count

def game_over_screen():
    global score
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Restart the game
                    return
                elif event.key == pygame.K_ESCAPE:
                    # Quit the game
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_m:
                    # Return to the main menu
                    main_menu()

        screen.fill(WHITE)
        game_over_text = font.render("Game Over", True, RED)
        score_text = font.render(f"Score: {score}", True, BLUE)
        restart_text = font.render("Press Enter to Restart", True, BLUE)
        quit_text = font.render("Press Escape to Quit", True, BLUE)
        main_menu_text = font.render("Press 'M' for Main Menu", True, BLUE)  # Add main menu button text

        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 + 50))
        screen.blit(quit_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100))
        screen.blit(main_menu_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 150))  # Display main menu button text

        pygame.display.flip()

def activate_power_up():
    global bullet_count, power_up_counter
    # Add your power-up logic here
    # For example, you can increase the player's bullet count based on the power-up_counter
    bullet_count += power_up_counter
    power_up_counter = 0
    health = 100

def game_loop():
    global score, money, bullet_count, health, power_up_counter, equipped_weapon

    clock = pygame.time.Clock()
    game_over = False

    last_bullet_pack_spawn_time = pygame.time.get_ticks()
    last_health_pack_spawn_time = pygame.time.get_ticks()
    last_power_up_spawn_time = pygame.time.get_ticks()
    last_money_spawn_time = pygame.time.get_ticks()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        keys = pygame.key.get_pressed()
        if not game_over:
            # Reset the player's velocity
            player_velocity = [0, 0]

            # Handle player movement
            if keys[pygame.K_w]:  # Move up
                player_velocity[1] = -player_speed
            if keys[pygame.K_s]:  # Move down
                player_velocity[1] = player_speed
            if keys[pygame.K_a]:  # Move left
                player_velocity[0] = -player_speed
            if keys[pygame.K_d]:  # Move right
                player_velocity[0] = player_speed

            # Handle player shooting
            if pygame.mouse.get_pressed()[0]:  # Left mouse button
                mouse_x, mouse_y = pygame.mouse.get_pos()
                angle = math.atan2(mouse_y - player.centery, mouse_x - player.centerx)
                
                # Use equipped weapon's properties
                weapon_properties_current = weapon_properties[equipped_weapon]
                bullet_speed = weapon_properties_current["bullet_speed"]
                bullet_damage = weapon_properties_current["damage"]
                
                create_bullet(angle, bullet_speed, bullet_damage)

            player.x += player_velocity[0]
            player.y += player_velocity[1]

            screen.fill(WHITE)

            # Move zombies towards the player
            move_zombies()

            # Move bullets
            move_bullets()

            # Check for collisions with zombies
            for zombie in zombies[:]:
                if player.colliderect(zombie):
                    health -= random.randint(12,34)  # Decrease health when hit by a zombie
                    zombies.remove(zombie)
                    if health <= 0:
                        game_over = True
                    break

            # Check for collisions with bullets
            for bullet in bullets[:]:
                for zombie in zombies[:]:
                    bullet_rect = pygame.Rect(bullet[0], bullet[1], 10, 10)
                    if bullet_rect.colliderect(zombie):
                        if bullet in bullets:  # Check if the bullet is still in the list
                            bullets.remove(bullet)
                        zombies.remove(zombie)
                        score += 10
                        power_up_counter += 1

            # Create new zombies
            if len(zombies) < 5:
                create_zombie()

            # Draw zombies
            for zombie in zombies:
                pygame.draw.rect(screen, RED, zombie)

            # Draw bullets
            for bullet in bullets:
                pygame.draw.rect(screen, BLUE, (bullet[0], bullet[1], 10, 10))

            # Draw player
            pygame.draw.rect(screen, BLUE, player)

            # Display score
            score_text = font.render(f"Score: {score}", True, BLUE)
            screen.blit(score_text, (10, 10))

            # Check for bullet pack spawns
            current_time = pygame.time.get_ticks()
            if current_time - last_bullet_pack_spawn_time > 10000:  # Spawn every 10 seconds
                create_bullet_pack()
                last_bullet_pack_spawn_time = current_time

            # Check for health pack spawns
            if current_time - last_health_pack_spawn_time > 15000:  # Spawn every 15 seconds
                create_health_pack()
                last_health_pack_spawn_time = current_time

            # Check for power-up spawns and activation
            if current_time - last_power_up_spawn_time > 20000:  # Spawn every 20 seconds
                create_power_up()
                last_power_up_spawn_time = current_time

            # Check for money item spawns
            if current_time - last_money_spawn_time > 8000:  # Spawn every 8 seconds
                create_money()
                last_money_spawn_time = current_time

            # Draw bullet packs
            for bullet_pack in bullet_packs:
                pygame.draw.rect(screen, GREEN, bullet_pack)

            # Check for collisions with bullet packs
            for bullet_pack in bullet_packs[:]:
                if player.colliderect(bullet_pack):
                    bullet_packs.remove(bullet_pack)
                    bullet_count += 5  # Increase bullet count

            # Draw health packs
            for health_pack in health_packs:
                pygame.draw.rect(screen, GREEN, health_pack)

            # Check for collisions with health packs
            for health_pack in health_packs[:]:
                if player.colliderect(health_pack):
                    health_packs.remove(health_pack)
                    health = min(100, health + 20)  # Increase health (up to a maximum of 100)

            # Draw power-ups
            for power_up in power_ups:
                pygame.draw.rect(screen, YELLOW, power_up)

            # Check for collisions with power-ups
            for power_up in power_ups[:]:
                if player.colliderect(power_up):
                    power_ups.remove(power_up)
                    activate_power_up()

            # Draw money items
            for money_item in money_items:
                pygame.draw.rect(screen, GOLD, money_item)

            # Check for collisions with money items
            for money_item in money_items[:]:
                if player.colliderect(money_item):
                    money_items.remove(money_item)
                    money += 10  # Add 10 money to the player's balance

            # Display bullet count, health, and power-up counter
            bullet_count_text = font.render(f"Bullets: {bullet_count}", True, BLUE)
            health_text = font.render(f"Health: {health}", True, GREEN)
            power_up_text = font.render(f"Power-Up: {power_up_counter}", True, YELLOW)
            money_text = font.render(f"Money: ${money}", True, GOLD)

            screen.blit(bullet_count_text, (10, 40))
            screen.blit(health_text, (10, 70))
            screen.blit(power_up_text, (10, 100))
            screen.blit(money_text, (10, 130))

            # Draw equipped weapon
            equipped_weapon_text = font.render(f"Equipped: {equipped_weapon}", True, BLUE)
            screen.blit(equipped_weapon_text, (10, SCREEN_HEIGHT - 40))

            pygame.display.flip()

            clock.tick(60)

    # Save the player's money when the game is over
    save_money()

    game_over_screen()

# Start the main menu
main_menu()
