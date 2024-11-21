import pygame
import random
import math

# Inicializar pygame
pygame.init()

# Definir colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Definir la pantalla del juego
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids")

# Reloj para controlar los FPS
clock = pygame.time.Clock()

# Variables del jugador
player_image = pygame.Surface((50, 50), pygame.SRCALPHA)
pygame.draw.polygon(player_image, WHITE, [(25, 0), (50, 50), (0, 50)])
player_rect = player_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
player_speed = 5
player_angle = 0
player_velocity = pygame.Vector2(0, 0)

# Variables de los asteroides
asteroid_image = pygame.Surface((40, 40), pygame.SRCALPHA)
pygame.draw.circle(asteroid_image, WHITE, (20, 20), 20)
asteroids = []
asteroid_speed = 2

# Variables de los disparos
bullet_image = pygame.Surface((5, 15))
bullet_image.fill(RED)
bullets = []
bullet_speed = 7

# Iniciar el mezclador de sonido
pygame.mixer.init()

# Cargar música de fondo y efectos de sonido
pygame.mixer.music.load("shiny-smily-story.mp3")  # Música de fondo
pygame.mixer.music.set_volume(0.5)  # Establecer volumen de la música
pygame.mixer.music.play(-1, 0.0)  # Reproducir música en bucle


# Cargar efectos de sonido
shot_sound = pygame.mixer.Sound("umu.mp3")  # Sonido del disparo
explosion_sound = pygame.mixer.Sound("sonic-boom.mp3")  # Sonido de la colisión

# Variables del sistema de vidas
lives = 3
font = pygame.font.SysFont("Arial", 30)

# Variables del sistema de puntuación
score = 0



# Función para crear asteroides
def create_asteroid():
    size = random.randint(30, 60)
    x = random.choice([random.randint(-size, 0), random.randint(WIDTH, WIDTH + size)])
    y = random.choice([random.randint(-size, 0), random.randint(HEIGHT, HEIGHT + size)])
    speed = random.uniform(asteroid_speed, asteroid_speed + 2)
    angle = random.uniform(0, 2 * math.pi)
    asteroid = {'rect': pygame.Rect(x, y, size, size), 'speed': speed, 'angle': angle}
    asteroids.append(asteroid)

# Función para mover al jugador
def move_player():
    global player_angle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_angle -= 5
    if keys[pygame.K_RIGHT]:
        player_angle += 5
    #if keys[pygame.K_UP]:
        #player_velocity.x += math.cos(math.radians(player_angle)) * player_speed
        # player_velocity.y += math.sin(math.radians(player_angle)) * player_speed

    player_rect.x += player_velocity.x
    player_rect.y += player_velocity.y

    # Mantener al jugador dentro de los límites de la pantalla
    if player_rect.left < 0:
        player_rect.left = 0
    if player_rect.right > WIDTH:
        player_rect.right = WIDTH
    if player_rect.top < 0:
        player_rect.top = 0
    if player_rect.bottom > HEIGHT:
        player_rect.bottom = HEIGHT

# Función para mover asteroides
def move_asteroids():
    global asteroids
    for asteroid in asteroids:
        asteroid['rect'].x += math.cos(asteroid['angle']) * asteroid['speed']
        asteroid['rect'].y += math.sin(asteroid['angle']) * asteroid['speed']

        # Reaparecer asteroides fuera de la pantalla
        if asteroid['rect'].x < -asteroid['rect'].width:
            asteroid['rect'].x = WIDTH
        elif asteroid['rect'].x > WIDTH:
            asteroid['rect'].x = -asteroid['rect'].width
        if asteroid['rect'].y < -asteroid['rect'].height:
            asteroid['rect'].y = HEIGHT
        elif asteroid['rect'].y > HEIGHT:
            asteroid['rect'].y = -asteroid['rect'].height

# Función para disparar
def shoot_bullet():
    global player_angle
    angle_rad = math.radians(-player_angle-90)
    bullet_velocity = pygame.Vector2(math.cos(angle_rad) * bullet_speed, math.sin(angle_rad) * bullet_speed)
    bullet = {'rect': bullet_image.get_rect(center=player_rect.center), 'velocity': bullet_velocity}
    bullets.append(bullet)
    
    # Reproducir sonido de disparo
    shot_sound.play()
    
    move_bullets()

# Función para mover los disparos
def move_bullets():
    global bullets
    for bullet in bullets[:]:
        bullet['rect'].x += bullet['velocity'].x
        bullet['rect'].y += bullet['velocity'].y

        # Eliminar balas fuera de la pantalla
        if not (0 <= bullet['rect'].x <= WIDTH and 0 <= bullet['rect'].y <= HEIGHT):
            bullets.remove(bullet)

# Función para detectar colisiones
def check_collisions():
    global asteroids, bullets, player_rect, lives, score
    for asteroid in asteroids[:]:
        if player_rect.colliderect(asteroid['rect']):
            lives -= 1  # Perder una vida si colisiona
            asteroids.remove(asteroid)  # Eliminar el asteroide
            if lives <= 0:
                return False  # Game over si no quedan vidas
            break
    for bullet in bullets[:]:
        for asteroid in asteroids[:]:
            if bullet['rect'].colliderect(asteroid['rect']):
                bullets.remove(bullet)
                asteroids.remove(asteroid)
                explosion_sound.play()  # Reproducir sonido de colisión
                score += 10  # Incrementar la puntuación al destruir un asteroide
                break

# Función para mostrar el texto en la pantalla
def display_text(text, color, x, y):
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, (x, y))

# Función para dibujar el juego
def draw():
    screen.fill(BLACK)

    # Dibujar asteroides
    for asteroid in asteroids:
        screen.blit(asteroid_image, asteroid['rect'])

    # Dibujar balas
    for bullet in bullets:
        screen.blit(bullet_image, bullet['rect'])

    # Dibujar jugador
    rotated_player = pygame.transform.rotate(player_image, player_angle)
    new_rect = rotated_player.get_rect(center=player_rect.center)
    screen.blit(rotated_player, new_rect.topleft)
    # Mostrar número de vidas
    display_text(f"Lives: {lives}", WHITE, 10, 10)
    display_text(f"Score: {score}", WHITE, 150, 10)

    pygame.display.flip()

# Función para mostrar Game Over
def show_game_over():
    display_text("GAME OVER", RED, WIDTH // 3, HEIGHT // 4)
    display_text(f"Final Score: {score}", WHITE, WIDTH // 3, HEIGHT // 3)
    display_text("Press R to Restart", WHITE, WIDTH // 3, HEIGHT // 2)

    pygame.display.flip()

# Función principal del juego
def game():
    global asteroids, lives, score
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shoot_bullet()
                if event.key == pygame.K_r and lives <= 0:
                    # Reiniciar juego
                    lives = 3
                    score = 0
                    asteroids.clear()
                    

        if lives <= 0:  # Si el jugador se quedó sin vidas, muestra Game Over
            show_game_over()
            continue  # No actualizar el juego mientras está en Game Over

        move_player()
        move_asteroids()
        move_bullets()
        check_collisions()
    
        

        # Crear asteroides aleatorios
        if random.random() < 0.02:
            create_asteroid()

        draw()

    pygame.quit()

if __name__ == "__main__":
    game()