import os
import random
import sys
import pygame_gui
import csv
import pygame


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def start_screen():
    count = 0
    fon = pygame.transform.scale(load_image('developers.png'), (width, height))
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                pygame.display.flip()
                count += 1
                fon = pygame.transform.scale(load_image('Start_scr.png'), (width, height))
                screen.blit(fon, (0, 0))
            elif count == 2:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "map/" + filename
    with open(filename, encoding="utf8") as mapFile:
        level_map = list(csv.reader(mapFile, delimiter=',', quotechar='"'))
    return level_map


def generate_level(level, group,  flag=False):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '33':
                Tile('33.jpg', x, y, group)
                new_player = Hero((x - 1.6) * tile_width, (y - 3.2) * tile_height)
            elif level[y][x] == '-1':
                pass
            else:
                Tile(f'{level[y][x]}.jpg', x, y, group)
    if not flag:
        return new_player, x, y


def terminate():
    pygame.quit()
    sys.exit()


class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(player_group, all_sprites)
        self.cur_frame = 0
        self.image = pygame.image.load('stand/1.png')
        self.rect = self.image.get_rect(center=(x, y))
        self.run_right = False
        self.run_left = False
        self.frames = ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png', '7.png', '8.png']

    def update(self):
        if self.run_right:
            self.cur_frame += 0.15
            if self.cur_frame > 7:
                self.cur_frame = 0
            self.image = pygame.image.load(f'run_right/{self.frames[int(self.cur_frame)]}')
        elif self.run_left:
            self.cur_frame += 0.15
            if self.cur_frame > 7:
                self.cur_frame = 0
            self.image = pygame.image.load(f'run_left/{self.frames[int(self.cur_frame)]}')
        else:
            self.cur_frame += 0.15
            if self.cur_frame > 7:
                self.cur_frame = 0
            self.image = pygame.image.load(f'stand/{self.frames[int(self.cur_frame)]}')


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile, pos_x, pos_y, group):
        super().__init__(group, all_sprites)
        self.image = load_image(tile)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, rect_x1, rect_y1, rect_x2, rect_y2, speed):
        super().__init__(crackling_group, all_sprites)
        self.cur_frame = 0
        self.image = pygame.image.load('crackling/idle.png')
        self.rect_x1 = rect_x1
        self.rect_x2 = rect_x2
        self.rect_y1 = rect_y1
        self.rect_y2 = rect_y2
        self.spawn_x = random.choice(range(rect_x1, rect_x2))
        self.spawn_y = random.choice(range(rect_y1, rect_y2))
        self.spawn_point = (self.spawn_x, self.spawn_y)
        self.speed = speed



def mainloop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYUP:
                player.run_right = False
                player.run_left = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player.rect.x -= 5
            player.run_left = True
        if keys[pygame.K_d]:
            player.rect.x += 5
            player.run_right = True
        if keys[pygame.K_w]:
            if player.run_left:
                pass
            elif player.run_right:
                pass
            else:
                player.run_right = True
            player.rect.y -= 5
        if keys[pygame.K_s]:
            if player.run_left:
                pass
            elif player.run_right:
                pass
            else:
                player.run_right = True
            player.rect.y += 5
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        player.update()
        all_sprites.update()
        screen.fill('black')
        for i in list_of_groups:
            i.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1064, 768
    screen = pygame.display.set_mode(size)
    manager1 = pygame_gui.UIManager((1064, 768))
    registration_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((320, 230), (170, 50)),
                                                       text='Создать аккаунт',
                                                       manager=manager1)
    entrance_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((320, 300), (170, 50)),
                                                   text='Войти',
                                                   manager=manager1)

    manager2 = pygame_gui.UIManager((1920, 1080))
    label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((190, 230), (128, 30)), text='Введите никнейм:',
                                        manager=manager2)
    login_entry = pygame_gui.elements.UITextEntryLine(pygame.Rect((320, 230), (170, 30)), manager2)
    accept_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((190, 265), (298, 30)),
                                                 text='Подтвердить',
                                                 manager=manager2)
    back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((190, 140), (100, 40)),
                                               text='Назад',
                                               manager=manager2)
    all_sprites = pygame.sprite.Group()
    tiles_group1 = pygame.sprite.Group()
    tiles_group2 = pygame.sprite.Group()
    tiles_group3 = pygame.sprite.Group()
    tiles_group4 = pygame.sprite.Group()
    tiles_group5 = pygame.sprite.Group()
    list_of_groups = [tiles_group1, tiles_group2, tiles_group3, tiles_group4, tiles_group5]
    player_group = pygame.sprite.Group()
    crackling_group = pygame.sprite.Group()
    tile_width = tile_height = 32
    player, level_x, level_y = generate_level(load_level('karta._Слой тайлов 1.csv'), tiles_group1)
    for i in list_of_groups[1:]:
        generate_level(load_level(f'karta._Слой тайлов {list_of_groups.index(i) + 1}.csv'), i, True)
    running = True
    manager = manager1
    FPS = 60
    clock = pygame.time.Clock()
    while running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == registration_button:
                    manager = manager2
                if event.ui_element == entrance_button:
                    manager = manager2
                if event.ui_element == back_button:
                    manager = manager1
                if event.ui_element == accept_button:
                    start_screen()
                    mainloop()
            manager.process_events(event)
        camera = Camera()
        manager.update(time_delta)
        screen.fill('black')
        manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(FPS)
