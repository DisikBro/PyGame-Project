import os
import random
import sys
import csv
import sqlite3

from UI import *
from consts import *
from groups import *


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
    global manager
    count = 0
    fon = pygame.transform.scale(load_image('developers.png'), (width, height))
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                if count < 1:
                    music_slider.set_current_value(con.cursor().execute("""SELECT music_volume FROM statistics 
                    WHERE user_id = (SELECT id FROM user WHERE nickname = ?)""", (nickname, )).fetchone()[0])
                    pygame.mixer.music.load('ost.mp3')
                    pygame.mixer.music.set_volume(music_slider.current_value)
                    pygame.mixer.music.play(-1)
                    pygame.display.flip()
                    count += 1
                    fon = pygame.transform.scale(load_image('Start_scr.png'), (width, height))
                    screen.blit(fon, (0, 0))
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == play_button:
                    return  # начинаем игру
                if event.ui_element == settings_button:
                    manager = manager4
                if event.ui_element == back_button1:
                    con.cursor().execute("""UPDATE statistics SET music_volume = ? 
                    WHERE user_id = (SELECT id FROM user WHERE nickname = ?)""", (music_slider.current_value, nickname))
                    con.commit()
                    print(con.cursor().execute("""SELECT music_volume FROM statistics 
                                        WHERE user_id = (SELECT id FROM user WHERE nickname = ?)""",
                                               (nickname,)).fetchone()[0])
                    manager = manager3
                if event.ui_element == exit_button:
                    terminate()
            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == music_slider:
                    pygame.mixer.music.set_volume(music_slider.current_value)
            manager.process_events(event)
        manager.update(time_delta)
        if count == 1:
            screen.blit(fon, (0, 0))
            manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "map/" + filename
    with open(filename, encoding="utf8") as mapFile:
        level_map = list(csv.reader(mapFile, delimiter=',', quotechar='"'))
    return level_map


def generate_level(level, group):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '33':
                Tile('33.jpg', x, y, group)
                # with sqlite3.connect('crack_db.sqlite') as con:
                #     pos_x, pos_y = con.cursor().execute("""SELECT player_pos FROM statistics WHERE
                #                                         user_id = (SELECT id FROM user WHERE nickname = ?)""",
                #                                         ())
                new_player = Hero(15, 15)
            elif level[y][x] == '-1':
                pass
            else:
                Tile(f'{level[y][x]}.jpg', x, y, group)
    return new_player, x, y


def statistics(timer):
    attack_time = 10 - timer // 100
    if 1000 < timer < 1500:
        font = pygame.font.SysFont(None, 20)
        img = font.render(f'Внимание атака: {15 - timer // 100}', True, 'black')
        screen.blit(img, (20, 20))
    else:
        font = pygame.font.SysFont(None, 20)
        img = font.render(f'Время до следующей атаки: {attack_time}', True, 'black')
        screen.blit(img, (20, 20))
    font = pygame.font.SysFont(None, 20)
    img = font.render(f'Кол-во ресурсов, камень - {resources.rock}, дерево - {resources.wood}', True, 'black')
    screen.blit(img, (20, 40))


def terminate():
    pygame.quit()
    sys.exit()


class Map:
    def __init__(self):
        self.layers = []
        self.player = None
        for i in list_of_groups:
            layer = load_level(f'karta._Слой тайлов {list_of_groups.index(i) + 1}.csv')
            self.layers.append(layer)
            player1, level_x, level_y = generate_level(layer, i)
            if player1:
                self.player = player1

    def check_tile(self, x, y):
        for j in self.layers:
            if j[y][x] not in permitted:
                return False
        return True


class Hero(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.cur_frame = 0
        self.cur_frame1 = 0
        self.damage = 1
        self.image = pygame.image.load('stand/1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.pos_x, self.pos_y = pos_x, pos_y
        self.rect.x, self.rect.y = tile_width * pos_x, tile_height * pos_y
        self.inventory = []
        self.run_right = False
        self.run_left = False
        self.attack1 = False
        self.hit = False
        self.item = None
        self.frames = ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png', '7.png', '8.png']

    def update(self):
        if not self.attack1:
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

    def moving(self):
        if not self.attack1:
            x, y = 0, 0
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                x = -5
                self.run_left = True
            if keys[pygame.K_d]:
                x = 5
                self.run_right = True
            if keys[pygame.K_w]:
                if self.run_left:
                    pass
                elif self.run_right:
                    pass
                else:
                    self.run_right = True
                y = -5
            if keys[pygame.K_s]:
                if self.run_left:
                    pass
                elif self.run_right:
                    pass
                else:
                    self.run_right = True
                y = 5
            if game_map.check_tile((self.rect.bottomleft[0] + x) // tile_width,
                                   (self.rect.bottomleft[1] + y) // tile_height) and \
                    game_map.check_tile((self.rect.bottomright[0] + x) // tile_width,
                                        (self.rect.bottomright[1] + y) // tile_height):
                self.rect.move_ip(x, y)
                self.pos_x, self.pos_y = self.rect.x // tile_width, self.rect.y // tile_height
                print(self.pos_x, self.pos_y)
                if self.item:
                    for j in self.inventory:
                        j.rect.move_ip(x, y)

    def attack(self, evt):
        if self.attack1:
            if self.frames[int(self.cur_frame1) % 4] == '3.png':
                self.hit = True
            else:
                self.hit = False
            if evt.pos[0] >= self.rect.x + self.rect.w / 2:
                self.image = pygame.image.load(f'attack/{self.frames[int(self.cur_frame1) % 4]}').convert_alpha()
            else:
                img = pygame.image.load(f'attack/{self.frames[int(self.cur_frame1) % 4]}')
                self.image = pygame.transform.flip(img, True, False)
            self.cur_frame1 += 0.2
            spr = pygame.sprite.spritecollide(self, crackling_group, False)
            if self.hit:
                if spr:
                    for i in spr:
                        i.damaged(self.damage)

    def add_item(self, item):
        self.inventory.append(item)
        if len(self.inventory) == 1:
            self.item = item

    def next_item(self):
        if len(self.inventory) > 1:
            self.item = self.inventory[(self.inventory.index(self.item) + 1) %
                                       len(self.inventory)]

    def previous_item(self):
        if len(self.inventory) > 1:
            if self.inventory[self.inventory.index(self.item)] == 0:
                self.item = self.inventory[-1]
            else:
                self.item = self.inventory[self.inventory.index(self.item) - 1]


class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__(crackling_group, all_sprites)
        self.cur_frame = 0
        self.image = pygame.image.load('m_run/1.png')
        self.rect = self.image.get_rect()
        self.rect.x = 1500
        self.rect.y = random.randint(375, 525)
        self.hp = 10
        self.speed_x = speed
        self.speed_y = None
        self.live = True
        self.objective = False
        self.object_coords = 429, 480
        self.frames = ['1.png', '2.png', '3.png']
        self.damage = 1
        self.speed_y = (self.speed_x * (self.rect.y - 480)) / (self.rect.x - 429)

    def update(self):
        self.cur_frame += 0.15
        if self.cur_frame > 3:
            self.cur_frame = 0
        self.image = pygame.image.load(f'm_run/{self.frames[int(self.cur_frame)]}').convert_alpha()
        self.death()
        self.attack()

    def move(self):
        if self.live:
            if self.rect.y == 480 and self.rect.x > 429:
                self.rect.x -= self.speed_x
            if self.rect.y > 480 and self.rect.x > 429:
                distance = ((self.rect.x - 429) ** 2 + (self.rect.y - 480) ** 2) ** 0.5
                self.speed_y = abs((self.rect.y - 480) / distance)
                self.rect.x -= self.speed_x
                self.rect.y -= self.speed_y
            if self.rect.y < 480 and self.rect.x > 429:
                distance = ((self.rect.x - 429) ** 2 + (480 - self.rect.y) ** 2) ** 0.5
                self.speed_y = -abs((480 - self.rect.y) / distance)
                self.rect.x -= self.speed_x
                self.rect.y -= self.speed_y

    def attack(self):
        if self.rect.x <= 435:
            objective.damaged(self.damage)

    def death(self):
        if self.hp <= 0:
            self.kill()

    def damaged(self, damage):
        self.hp -= damage


class Objective(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(objective_group, all_sprites)
        self.image = load_image('image_2_3.png')
        self.rect = self.image.get_rect()
        self.count = 0
        self.functions = [lambda x: x + 10, lambda x: x - 10]
        self.rect.x, self.rect.y = 390, 450
        self.hp = 15

    def update(self):
        self.functions[int(self.count) % 2](self.rect.y)
        self.count += 0.2
        self.death()

    def damaged(self, damage):
        self.hp -= damage

    def death(self):
        if self.hp <= 0:
            self.kill()


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


class Pickaxe(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(pickaxe_group, all_sprites)
        self.image = load_image('pickaxe.png')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = tile_width * pos_x + 25, tile_height * pos_y + 20


class Sword(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(sword_group, all_sprites)
        self.image = load_image('sword.png')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = tile_width * pos_x + 30, tile_height * pos_y + 15


class Resources:
    def __init__(self):
        self.rock = 0
        self.wood = 0

    def update(self, rock_mine, wood_mine):
        if rock_mine and not wood_mine:
            self.rock += 1
        elif wood_mine and not rock_mine:
            self.wood += 1


def mainloop():
    timer = 0
    evt = None
    while True:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYUP:
                player.run_right = False
                player.run_left = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_WHEELUP:
                player.previous_item()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_WHEELDOWN:
                player.next_item()
            if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
                player.attack1 = False
                player.hit = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (event.button == pygame.BUTTON_LEFT and isinstance(player.item, Pickaxe) and
                        27 <= player.pos_x <= 31 and 7 <= player.pos_y <= 8 and
                        867 <= mouse_x <= 1055 and 209 <= mouse_y <= 317):
                    resources.update(rock_mine=True, wood_mine=False)
                elif (event.button == pygame.BUTTON_LEFT and isinstance(player.item, Pickaxe) and
                      30 <= player.pos_x <= 34 and player.pos_y == 17 and
                      1000 <= mouse_x <= 1113 and 643 <= mouse_y <= 758):
                    resources.update(rock_mine=False, wood_mine=True)
                elif (event.button == pygame.BUTTON_LEFT and
                      isinstance(player.item, Sword)):
                    evt = event
                    player.attack1 = True
                    player.run_right = False
                    player.run_left = False
        player.moving()
        player.attack(evt)
        # camera.update(player)
        # for sprite in all_sprites:
        #     camera.apply(sprite)
        timer += 1
        player.update()
        all_sprites.update()
        screen.fill('black')
        for i in list_of_groups:
            i.draw(screen)
        if 1000 < timer < 1500:
            if timer % 100 == 0:
                enemy = Enemy(2)
                enemies.append(enemy)
        for i in enemies:
            i.move()
            crackling_group.draw(screen)
        if timer > 1500:
            timer = 0
        objective_group.draw(screen)
        player_group.draw(screen)
        if not player.run_left and not player.run_right and not player.attack1:
            player.item.groups()[0].draw(screen)
        statistics(timer)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(size)
    objective = Objective()
    game_map = Map()
    resources = Resources()
    player = game_map.player
    sword = Sword(player.pos_x, player.pos_y)
    player.add_item(sword)
    pickaxe = Pickaxe(player.pos_x, player.pos_y)
    player.add_item(pickaxe)
    enemies = []
    running = True
    entr = False
    reg = False
    manager = manager1
    clock = pygame.time.Clock()
    while running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == registration_button:
                    manager = manager2
                    reg = True
                if event.ui_element == entrance_button:
                    manager = manager2
                    entr = True
                if event.ui_element == back_button:
                    message.set_text('')
                    manager = manager1
                    entr = False
                    reg = False
                if event.ui_element == accept_button:
                    with sqlite3.connect('crack_db.sqlite') as con:
                        check = con.cursor().execute("""SELECT id FROM user
                                                WHERE nickname = ?""", (login_entry.text,)).fetchone()
                        if entr:
                            if login_entry.text == '':
                                message.set_text('Введите имя!')
                            else:
                                if check is not None:
                                    nickname = login_entry.text
                                    manager = manager3
                                    start_screen()
                                    mainloop()
                                else:
                                    message.set_text('Неверное имя пользователя!')
                        elif reg:
                            if login_entry.text == '':
                                message.set_text('Введите имя!')
                            else:
                                if check is not None:
                                    message.set_text('Имя пользователя уже занято.')
                                else:
                                    nickname = login_entry.text
                                    con.cursor().execute("""INSERT INTO user (nickname) 
                                    VALUES (?)""", (nickname,))
                                    con.cursor().execute("""INSERT INTO statistics 
                                    (user_id, player_pos, wood, stone, game_time, music_volume)
                                    VALUES ((SELECT id FROM user WHERE nickname = ?), '15, 15', 0, 0, 0, 0.2)""",
                                                         (nickname, ))
                                    con.commit()
                                    manager = manager3
                                    start_screen()
                                    mainloop()
            manager.process_events(event)
        manager.update(time_delta)
        screen.fill('black')
        manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(FPS)
