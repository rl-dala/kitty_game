import pygame


class Player:
    def __init__(self, x, y, color, width=320, height=180):
        self.rect = pygame.Rect(x, y, width, height)
        self.original_image = pygame.image.load("kitty_1.jpg").convert_alpha()
        self.original_image = pygame.transform.scale(
            self.original_image, (width, height)
        )
        self.image = self.original_image.copy()
        self.color = color
        self.velocity_y = 0
        self.gravity = 0.1
        self.jump_power = -10
        self.on_ground = True
        self.jump_count = 0
        self.facing_right = True

    def draw(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.image, self.rect)  # DRAW IMAGE ON THE RECTANGLE

    def move(self, keys):
        if keys[pygame.K_SPACE] and self.on_ground:  # JUMP
            self.velocity_y = self.jump_power
            self.on_ground = False
            self.jump_count += 1
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-1, 0)
            if self.facing_right:
                self.facing_right = False
                self.image = pygame.transform.flip(self.original_image, True, False)
        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(1, 0)
            if not self.facing_right:
                self.facing_right = True
                self.image = self.original_image.copy()
        if keys[pygame.K_UP]:  # UP
            self.rect.move_ip(0, -1)
        if keys[pygame.K_DOWN]:  # DOWN
            self.rect.move_ip(0, 1)

    def apply_gravity(self, screen_height):
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        floor_y = screen_height - self.rect.height
        if self.rect.y >= floor_y:
            self.rect.y = floor_y
            self.velocity_y = 0
            self.on_ground = True


def main():
    pygame.init()

    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

    base_font = pygame.font.Font(None, 32)
    username = "I'm a Kitty :)"
    input_rect = pygame.Rect(200, 200, 140, 32)
    input_color_active = pygame.Color("lightskyblue3")
    input_color_passive = pygame.Color("gray15")
    input_color = input_color_passive
    active_typing = False

    fullscreen = False

    clock = pygame.time.Clock()
    FPS = 240

    player = Player(200, 150, (255, 255, 255))
    delta_time = 0.1

    game_running = True
    while game_running:
        screen.fill((0, 0, 0))

        keys = pygame.key.get_pressed()
        player.move(keys)  # MOVING
        player.apply_gravity(screen.get_height())  # JUMPING
        player.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # QUIT OUT
                game_running = False
            if event.type == pygame.VIDEORESIZE:  # RESIZE WINDOW
                if not fullscreen:
                    screen = pygame.display.set_mode(
                        (event.w, event.h), pygame.RESIZABLE
                    )
            if (
                event.type == pygame.MOUSEBUTTONDOWN
            ):  # CHECK IF THE PLAYA IS CLICKING ON THE TEXTBOX
                if input_rect.collidepoint(event.pos):
                    active_typing = True
                else:
                    active_typing = False

            if event.type == pygame.KEYDOWN:  # THE PLAYA IS PRESSING A KEY
                if event.key == pygame.K_ESCAPE:  # QUIT OUT
                    game_running = False
                if event.key == pygame.K_F12:  # FULLSCREEN / WINDOW
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode(
                            (monitor_size[0], monitor_size[1]), pygame.FULLSCREEN
                        )
                    else:
                        screen = pygame.display.set_mode(
                            (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE
                        )
                if active_typing:  # TYPING MODE (PLAYA CAN STILL MOVE)
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        username += event.unicode

        if active_typing:
            input_color = input_color_active
        else:
            input_color = input_color_passive
        pygame.draw.rect(screen, input_color, input_rect, 2, 100)
        text_surface = base_font.render(username, True, (255, 255, 255))
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

        input_rect.w = max(100, text_surface.get_width() + 10)

        pygame.display.flip()

        delta_time = clock.tick(FPS) / 1000
        delta_time = max(0.0001, delta_time)

    pygame.quit()


if __name__ == "__main__":
    main()
