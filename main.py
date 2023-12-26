import os
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


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '33':
                Tile('33.jpg', x, y)
                new_player = Hero(x, y)
            else:
                Tile(f'{level[y][x]}.jpg', x, y)
    return new_player, x, y


def terminate():
    pygame.quit()
    sys.exit()


class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(load_image("hero.png"), 8, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 0.2) % len(self.frames)
        self.image = self.frames[int(self.cur_frame)]
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= 5
        if keys[pygame.K_d]:
            self.rect.x += 5
        if keys[pygame.K_w]:
            self.rect.y -= 5
        if keys[pygame.K_s]:
            self.rect.y += 5


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = load_image(tile)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


def mainloop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            all_sprites.update()
        screen.fill('black')
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1920, 1080
    screen = pygame.display.set_mode(size)
    manager1 = pygame_gui.UIManager((1920, 1080))
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
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    tile_width = tile_height = 32
    level = load_level('karta._Слой тайлов 1.csv')
    player, level_x, level_y = generate_level(level)
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
        manager.update(time_delta)
        screen.fill('black')
        manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(FPS)
