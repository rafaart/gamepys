import pygame
from pygame.locals import *
pygame.init()

clock = pygame.time.Clock()
fps = 60

# pega uma lista de todas as resoluções suportadas
resolutions = pygame.display.list_modes()

# pega a primeira resolução da lista
first_resolution = resolutions[0]
width, height = first_resolution

# modifica a resolução da screen para ser quadrada
width = height*0.5
height = height*0.5

# define as variavéis do jogo
brick_size = width * 0.05
game_over = 0
main_menu = True

print("Resolução da tela atual:", width, "x", height)
print("tamanho do brick: ", brick_size)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Parkour')

# carregar imagens
sun_img = pygame.image.load('img/sun.png')
bg_img = pygame.image.load('img/sky.png')
restart_img = pygame.image.load('img/restart.png')
start_img = pygame.image.load('img/start.png')
exit_img = pygame.image.load('img/exit.png')


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):

        action = False

        # pega a posição do cursor
        pos = pygame.mouse.get_pos()

        # checka colisão do cursor
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        # desenha o butão
        screen.blit(self.image, self.rect)

        return action


class Player():
    def __init__(self, x, y):
        self.reset(x, y)

        print("a largura e a altura da imagem: ",
              self.width, " x ", self.height)

    def update(self, game_over):

        dx = 0
        dy = 0
        walk_delay = 2

        if game_over == 0:
            # pegando teclado
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                self.vel_y = -5
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 5
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1
                self.direction = 1
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # animação do sprite
            if self.counter > walk_delay:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # gravidade
            self.vel_y += 0.1
            if self.vel_y > 5:
                self.vel_y = 5
            dy += self.vel_y

            # checar colisão
            self.in_air = True
            for tile in world.tile_list:

                # chequar colisão na direção x
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0

                # chequar por colisão na direção y
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # chequar se abaixo do solo (pulando)
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    # chequar se acima do solo (caindo)
                    elif self.vel_y > 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

            # checkar por colisões com o inimigo
            if pygame.sprite.spritecollide(self, snail_group, False):
                # game_over = -1
                pass

                # checkar por colisões com a saida
            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1

            # atualizar posição do jogador
            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            self.image = self.hurt_image
            if self.rect.y > 0:
                self.rect.y += 5

        elif game_over == 1:
            self.image = self.p1_duck

        # desenha o jogador na tela
        screen.blit(self.image, self.rect)
        return game_over

    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 12):
            img_right = pygame.image.load(f'img/p1_walk{num}.png')
            img_right = pygame.transform.scale(
                img_right, (brick_size*0.9, brick_size * 2))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.hurt_image = pygame.image.load('img/p1_hurt.png')
        self.p1_duck = pygame.image.load('img/p1_duck.png')
        self.p1_duck = pygame.transform.scale(
            self.p1_duck, (brick_size*0.9, brick_size * 2))
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/snailwalk1.png')
        self.image = pygame.transform.scale(
            self.image, (brick_size, brick_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > brick_size:
            self.move_direction *= -1
            self.move_counter *= -1


class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/door_lock.png')
        self.image = pygame.transform.scale(
            self.image, (brick_size, brick_size * 1.5))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class World():
    def __init__(self, data):
        self.tile_list = []

        # load images
        dirt_img = pygame.image.load('img/wall.png')
        grass_img = pygame.image.load('img/ground.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(
                        dirt_img, (brick_size, brick_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * brick_size
                    img_rect.y = row_count * brick_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(
                        grass_img, (brick_size, brick_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * brick_size
                    img_rect.y = row_count * brick_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    snail = Enemy(col_count * brick_size,
                                  row_count * brick_size)
                    snail_group.add(snail)
                if tile == 8:
                    exit = Exit(col_count * brick_size,
                                row_count * brick_size - (brick_size // 2))
                    exit_group.add(exit)

                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


world_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1],
    [1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1],
    [1, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1],
    [1, 0, 2, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1],
    [1, 0, 0, 0, 0, 0, 2, 2, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

player = Player(100, height - (brick_size + brick_size*2))

snail_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

world = World(world_data)

# cria os butões
restart_button = Button(width // 2 - (brick_size * 3),
                        height // 2, restart_img)
start_button = Button(width // 2 - (brick_size * 8), height // 2, start_img)
exit_button = Button(width // 2 + brick_size, height // 2, exit_img)
run = True
while run:

    clock.tick(fps)
    screen.blit(bg_img, (0, 0))
    screen.blit(sun_img, (100, 100))

    if main_menu:
        if exit_button.draw():
            run = False
        if start_button.draw():
            main_menu = False
    else:

        world.draw()

        if game_over == 0:
            snail_group.update()

        snail_group.draw(screen)
        exit_group.draw(screen)

        game_over = player.update(game_over)

        if game_over == -1:
            if restart_button.draw():
                player.reset(100, height - (brick_size + brick_size*2))
                game_over = 0

        if game_over == 1:
            if restart_button.draw():
                player.reset(100, height - (brick_size + brick_size*2))
                game_over = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
