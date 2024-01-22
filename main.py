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


def start_screen(flag):
    global manager
    count = 0
    if flag:
        fon = pygame.transform.scale(load_image('developers.png'), (width, height))
        screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) or not flag:
                if count < 1:
                    music_slider.set_current_value(con.cursor().execute("""SELECT music_volume FROM statistics 
                    WHERE user_id = (SELECT id FROM user WHERE nickname = ?)""", (nickname,)).fetchone()[0])
                    pygame.mixer.music.load('sounds/ost.mp3')
                    pygame.mixer.music.set_volume(music_slider.current_value)
                    pygame.mixer.music.play(-1)
                    pygame.display.flip()
                    count += 1
                    fon = pygame.transform.scale(load_image('Start_scr.png'), (width, height))
                    screen.blit(fon, (0, 0))
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == play_button:
                    mainloop()
                if event.ui_element == settings_button:
                    manager = manager4
                if event.ui_element == back_button1:
                    con.cursor().execute("""UPDATE statistics SET music_volume = ? 
                    WHERE user_id = (SELECT id FROM user WHERE nickname = ?)""", (music_slider.current_value, nickname))
                    con.commit()
                    manager = manager3
                if event.ui_element == exit_button:
                    terminate()
                if event.ui_element == change_button:
                    con.cursor().execute("""UPDATE statistics SET player_pos = '15, 15', wood = 0, stone = 0, 
                    game_time = 0, music_volume = 0.2, hp = 20, damage = 1
                    WHERE user_id = (SELECT id FROM user WHERE nickname = ?)""",
                                         (nickname,))
                    con.commit()
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


def game_over():
    global manager
    manager = manager6
    fon = pygame.transform.scale(load_image('game_over.png'), (width, height))
    screen.blit(fon, (0, 0))
    pygame.mixer.music.load('sounds/game_over.mp3')
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == exit_button2:
                    con.cursor().execute("""UPDATE statistics SET player_pos = '15, 15', wood = 0, stone = 0, 
                                        game_time = 0, music_volume = 0.2, hp = 20, damage = 1
                                        WHERE user_id = (SELECT id FROM user WHERE nickname = ?)""",
                                         (nickname,))
                    con.commit()
                    terminate()
            manager.process_events(event)
        manager.update(time_delta)
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
                pos_x, pos_y = con.cursor().execute("""SELECT player_pos FROM statistics WHERE
                                                    user_id = (SELECT id FROM user WHERE nickname = ?)""",
                                                    (nickname,)).fetchone()[0].split(', ')
                new_player = Hero(int(pos_x), int(pos_y))
            elif level[y][x] == '-1':
                pass
            else:
                Tile(f'{level[y][x]}.jpg', x, y, group)
    return new_player, x, y


def statistics(timer):
    attack_time = 10 - timer // 100
    font = pygame.font.Font("data/Minecraft Rus NEW.otf", 30)
    if 1000 < timer < 1500:
        text = font.render(f'Внимание атака: {15 - timer // 100}', True, 'black')
        screen.blit(text, (20, 24))
    else:
        text = font.render(f'Время до следующей атаки: {attack_time}', True, 'black')
        screen.blit(text, (20, 24))

    res = font.render(f'Кол-во ресурсов, камень - {resources.stone}, дерево - {resources.wood}', True, 'black')
    screen.blit(res, (20, 74))


def simulated_store():
    font = pygame.font.Font("data/Minecraft Rus NEW.otf", 30)
    button_font = pygame.font.Font("data/Minecraft Rus NEW.otf", 15)

    text = button_font.render('Улучшения персонажа - 50 дерева и камня; турель - 80 дерева и камня',
                       True, 'black')
    screen.blit(text, (20, 114))

    damage = font.render(f'Урон - {player.damage}', True, 'black')
    damage2 = button_font.render('Улучшить', True, 'black')
    screen.blit(damage, (1630, 24))
    screen.blit(damage2, (1807, 30))
    pygame.draw.rect(screen, 'black', (1800, 19, 100, 40), 3)

    movement = font.render(f'Скорость передвижения - {player.speed_increase + 5}', True, 'black')
    movement2 = button_font.render('Улучшить', True, 'black')
    screen.blit(movement, (1255, 74))
    screen.blit(movement2, (1807, 80))
    pygame.draw.rect(screen, 'black', (1800, 69, 100, 40), 3)

    tur = font.render(f'Турели - {turret.amount}', True, 'black')
    tur2 = button_font.render('Купить', True, 'black')
    screen.blit(tur, (1585, 124))
    screen.blit(tur2, (1817, 130))
    pygame.draw.rect(screen, 'black', (1800, 119, 100, 40), 3)


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
        self.damage, self.hp = con.cursor().execute("""SELECT damage, hp FROM statistics 
        WHERE user_id = (SELECT id FROM user WHERE nickname = ?)""", (nickname,)).fetchone()
        self.speed_increase = 0
        self.image = pygame.image.load('stand/1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.pos_x, self.pos_y = pos_x, pos_y
        self.rect.x, self.rect.y = tile_width * pos_x, tile_height * pos_y
        self.inventory = []
        self.hit_sound = pygame.mixer.Sound('sounds/hit.ogg')
        self.hit_enemy_sound = pygame.mixer.Sound('sounds/hit_enemy.ogg')
        self.run_right = False
        self.run_left = False
        self.attack1 = False
        self.hit = False
        self.item = None
        self.frames = ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png', '7.png', '8.png']

    def update(self):
        if not self.attack1:
            if self.run_right:
                self.cur_frame += 0.3
                if self.cur_frame > 7:
                    self.cur_frame = 0
                self.image = pygame.image.load(f'run_right/{self.frames[int(self.cur_frame)]}')
            elif self.run_left:
                self.cur_frame += 0.3
                if self.cur_frame > 7:
                    self.cur_frame = 0
                self.image = pygame.image.load(f'run_left/{self.frames[int(self.cur_frame)]}')
            else:
                self.cur_frame += 0.3
                if self.cur_frame > 7:
                    self.cur_frame = 0
                self.image = pygame.image.load(f'stand/{self.frames[int(self.cur_frame)]}')

    def moving(self):
        if not self.attack1:
            x, y = 0, 0
            keys = pygame.key.get_pressed()
            if keys[pygame.K_x]:
                resources.wood += 50
                resources.stone += 50
            if keys[pygame.K_a]:
                x = -5 - self.speed_increase
                self.run_left = True
            if keys[pygame.K_d]:
                x = 5 + self.speed_increase
                self.run_right = True
            if keys[pygame.K_w]:
                if self.run_left:
                    pass
                elif self.run_right:
                    pass
                else:
                    self.run_right = True
                y = -5 - self.speed_increase
            if keys[pygame.K_s]:
                if self.run_left:
                    pass
                elif self.run_right:
                    pass
                else:
                    self.run_right = True
                y = 5 + self.speed_increase
            if game_map.check_tile((self.rect.bottomleft[0] + x) // tile_width,
                                   (self.rect.bottomleft[1] + y) // tile_height) and \
                    game_map.check_tile((self.rect.bottomright[0] + x) // tile_width,
                                        (self.rect.bottomright[1] + y) // tile_height):
                self.rect.move_ip(x, y)
                self.pos_x, self.pos_y = self.rect.x // tile_width, self.rect.y // tile_height
                if self.item:
                    for j in self.inventory:
                        j.rect.move_ip(x, y)

    def attack(self, evt):
        if self.attack1:
            spr = pygame.sprite.spritecollide(self, crackling_group, False)
            if self.frames[int(self.cur_frame1) % 4] == '3.png':
                self.hit = True
                if spr:
                    self.hit_enemy_sound.play(0)
                    for i in spr:
                        i.damaged(self.damage)
                        i.death()
                else:
                    self.hit_sound.play(0)
            else:
                self.hit = False
            if evt.pos[0] >= self.rect.x + self.rect.w / 2:
                self.image = pygame.image.load(f'attack/{self.frames[int(self.cur_frame1) % 4]}').convert_alpha()
            else:
                img = pygame.image.load(f'attack/{self.frames[int(self.cur_frame1) % 4]}')
                self.image = pygame.transform.flip(img, True, False)
            self.cur_frame1 += 1

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
        self.crackling_spawn = pygame.mixer.Sound('sounds/crackling_spawn.ogg')
        self.crackling_spawn.set_volume(0.2)
        self.crackling_spawn.play(0)
        self.crackling_death = pygame.mixer.Sound('sounds/crackling_death.ogg')
        self.crackling_death.set_volume(0.2)
        self.crackling_damage = pygame.mixer.Sound('sounds/crackling_damage.ogg')
        self.crackling_damage.set_volume(0.2)
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

    def move(self):
        if self.live and self.rect.x >= 435:
            self.rect.x -= self.speed_x
            if self.rect.y > 480 and self.rect.x < 847:
                self.rect.y -= 1
            elif self.rect.y < 480 and self.rect.x < 847:
                self.rect.y += 1

    def attack(self):
        if self.rect.x <= 435 and self.live:
            objective.damaged(self.damage)

    def death(self):
        if self.hp <= 0:
            self.crackling_death.play(0)
            self.live = False
            self.kill()

    def damaged(self, damage):
        self.crackling_damage.play(0)
        self.hp -= damage

    def get_top_pos(self):
        return self.rect.x // tile_width, self.rect.y // tile_height

    def get_bottom_pos(self):
        return self.rect.bottomleft[0] // tile_width, self.rect.bottomleft[1] // tile_height


class Objective(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(objective_group, all_sprites)
        self.image = load_image('image_2_3.png')
        self.death_sound = pygame.mixer.Sound('sounds/clash-royale-king-cry.ogg')
        self.death_sound.set_volume(0.2)
        self.rect = self.image.get_rect()
        self.count = 0
        self.functions = [lambda x: x + 1, lambda x: x - 1]
        self.rect.x, self.rect.y = 390, 450
        self.hp = 15

    def update(self):
        self.rect.y = self.functions[int(self.count) % 2](self.rect.y)
        self.count += 0.07
        self.death()

    def damaged(self, damage):
        self.hp -= damage

    def death(self):
        if self.hp <= 0:
            self.death_sound.play(0)
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
        self.functions = [lambda x: x + 4, lambda x: x - 4]
        self.count = 0
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = tile_width * pos_x + 25, tile_height * pos_y + 20

    def update(self):
        self.rect.y = self.functions[int(self.count) % 2](self.rect.y)
        self.count += 1


class Sword(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(sword_group, all_sprites)
        self.image = load_image('sword.png')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = tile_width * pos_x + 30, tile_height * pos_y + 15


class Resources:
    def __init__(self):
        self.stone, self.wood = con.cursor().execute("""SELECT stone, wood FROM statistics 
        WHERE user_id = (SELECT id FROM user WHERE nickname = ?)""", (nickname,)).fetchone()

    def update(self, rock_mine, wood_mine):
        if rock_mine and not wood_mine:
            self.stone += 1
        elif wood_mine and not rock_mine:
            self.wood += 1


class Turret(pygame.sprite.Sprite):
    def __init__(self, hp, mouse_x, mouse_y):
        super().__init__(all_sprites, turret_group)
        self.cur_frame = 0
        self.image = pygame.image.load('turret/1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = mouse_x - 26, mouse_y - 24
        self.hp = hp
        self.amount = 0
        self.alive = True
        self.frames = ['1.png', '2.png', '3.png', '1.png']

    def update(self):
        self.cur_frame += 0.11
        if self.cur_frame > 3:
            self.cur_frame = 0
        self.image = pygame.image.load(f'turret/{self.frames[int(self.cur_frame)]}').convert_alpha()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, damage, speed, x, y):
        super().__init__(all_sprites, bullet_group)
        self.cur_frame = 0
        self.image = pygame.image.load('bullet/1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x + 40, y + 7
        self.speed = speed
        self.damage = damage
        self.frames = ['1.png', '2.png', '3.png', '4.png']

    def update(self):
        self.cur_frame += 0.10
        if self.cur_frame > 4:
            self.cur_frame = 0
        self.image = pygame.image.load(f'bullet/{self.frames[int(self.cur_frame)]}').convert_alpha()

    def move(self):
        self.rect.x += self.speed

    def get_pos(self):
        return self.rect.x // tile_width, self.rect.y // tile_height


def mainloop():
    global manager
    timer = 0
    count = 0
    count1 = 0
    evt = None
    pause = False
    while True:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYUP:
                player.run_right = False
                player.run_left = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_WHEELUP and not pause:
                player.previous_item()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_WHEELDOWN and not pause:
                player.next_item()
            if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
                player.attack1 = False
                player.hit = False
            if event.type == pygame.MOUSEBUTTONDOWN and not pause:
                if (event.button == pygame.BUTTON_LEFT and isinstance(player.item, Pickaxe) and
                        27 <= player.pos_x <= 31 and 7 <= player.pos_y <= 8 and
                        867 <= mouse_x <= 1055 and 209 <= mouse_y <= 317):
                    resources.update(rock_mine=True, wood_mine=False)
                    pickaxe.update()
                if (event.button == pygame.BUTTON_LEFT and isinstance(player.item, Pickaxe) and
                        30 <= player.pos_x <= 34 and player.pos_y == 17 and
                        1000 <= mouse_x <= 1113 and 643 <= mouse_y <= 758):
                    resources.update(rock_mine=False, wood_mine=True)
                    pickaxe.update()
                if (event.button == pygame.BUTTON_LEFT and
                        isinstance(player.item, Sword)):
                    evt = event
                    player.attack1 = True
                    player.run_right = False
                    player.run_left = False
                if (event.button == pygame.BUTTON_LEFT and
                        20 <= mouse_x <= 60 <= mouse_y <= 120):
                    turret.selected = True
                if 1800 <= mouse_x <= 1900 and 119 <= mouse_y <= 159 and resources.wood >= 80 and resources.stone >= 80:
                    resources.wood -= 80
                    resources.stone -= 80
                    turret.amount += 1
                if 1800 <= mouse_x <= 1900 and 19 <= mouse_y <= 59 and resources.wood >= 50 and resources.stone >= 50:
                    resources.wood -= 50
                    resources.stone -= 50
                    player.damage += 1
                if 1800 <= mouse_x <= 1900 and 69 <= mouse_y <= 109 and resources.wood >= 50 and resources.stone >= 50:
                    resources.wood -= 50
                    resources.stone -= 50
                    player.speed_increase += 1
                if (event.button == pygame.BUTTON_RIGHT and turret.amount > 0
                        and 322 <= mouse_x <= 835 and 288 <= mouse_y <= 792):
                    turret.amount -= 1
                    new_turret = Turret(5, mouse_x, mouse_y)
                    turrets.append(new_turret)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause = True
                manager = manager5
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == continue_button:
                    pause = False
                if event.ui_element == settings_button1:
                    manager = manager4
                if event.ui_element == back_button1:
                    con.cursor().execute("""UPDATE statistics SET music_volume = ? 
                                        WHERE user_id = (SELECT id FROM user WHERE nickname = ?)""",
                                         (music_slider.current_value, nickname))
                    con.commit()
                    manager = manager5
                if event.ui_element == exit_button1:
                    con.cursor().execute("""UPDATE statistics 
                    SET player_pos = ?, wood = ?, stone = ?, hp = ?, damage = ? 
                    WHERE user_id = (SELECT id FROM user WHERE nickname = ?)""",
                                         (f'{player.pos_x}, {player.pos_y}', resources.wood, resources.stone,
                                          player.hp, player.damage, nickname))
                    con.commit()
                    manager = manager3
                    start_screen(False)
                    break
            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == music_slider:
                    pygame.mixer.music.set_volume(music_slider.current_value)
            manager.process_events(event)
        manager.update(time_delta)
        if not pause:
            player.moving()
            if player.attack1:
                if int(count) % 5 == 0:
                    player.attack(evt)
                count += 1
            if int(count1) % 50 == 0:
                for i in enemies:
                    i.attack()
                    if objective.hp <= 0:
                        game_over()
                        break
            count1 += 1
            # camera.update(player)
            # for sprite in all_sprites:
            #     camera.apply(sprite)
            timer += 1
            player_group.update()
            crackling_group.update()
            objective_group.update()
            screen.fill('black')
            for i in list_of_groups:
                i.draw(screen)
            if 1000 < timer < 1500:
                if timer % 100 == 0:
                    enemy = Enemy(2)
                    enemies.append(enemy)
            for i in enemies:
                i.move()
                i.update()
                crackling_group.draw(screen)
                for t in turrets:
                    if ((t.rect.y + 7) // tile_height in range(i.get_top_pos()[1], i.get_bottom_pos()[1]) and
                            timer % 30 == 0):
                        bullet = Bullet(1, 3, t.rect.x, t.rect.y)
                        bullets.append(bullet)
                for j in bullets:
                    j.move()
                    j.update()
                    bullet_group.draw(screen)
                    if j.get_pos()[1] in range(i.get_top_pos()[1], i.get_bottom_pos()[1]):
                        spr = pygame.sprite.spritecollide(j, crackling_group, False)
                        if spr:
                            for k in spr:
                                k.damaged(j.damage)
                                k.death()
                                if not k.live:
                                    enemies.remove(k)
                                bullets.remove(j)
                                j.kill()
                    if j.rect.x >= 1700:
                        j.kill()
                        bullets.remove(j)
            if timer > 1500:
                timer = 0
            if not enemies:
                for i in bullets:
                    i.kill()
                bullets.clear()


            objective_group.draw(screen)
            player_group.draw(screen)
            turret_group.draw(screen)
            if not player.run_left and not player.run_right and not player.attack1:
                player.item.groups()[0].draw(screen)
        else:
            screen.fill('black')
            for i in list_of_groups:
                i.draw(screen)
            crackling_group.draw(screen)
            objective_group.draw(screen)
            player_group.draw(screen)
            if not player.run_left and not player.run_right and not player.attack1:
                player.item.groups()[0].draw(screen)
            manager.draw_ui(screen)
        statistics(timer)
        simulated_store()
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()
    screen = pygame.display.set_mode(size)
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
                                    objective = Objective()
                                    game_map = Map()
                                    resources = Resources()
                                    player = game_map.player
                                    sword = Sword(player.pos_x, player.pos_y)
                                    player.add_item(sword)
                                    pickaxe = Pickaxe(player.pos_x, player.pos_y)
                                    turret = Turret(10, 11693, 11462)
                                    player.add_item(pickaxe)
                                    enemies = []
                                    bullets = []
                                    turrets = []
                                    manager = manager3
                                    start_screen(True)
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
                                    (user_id, player_pos, wood, stone, game_time, music_volume, hp, damage)
                                    VALUES ((SELECT id FROM user WHERE nickname = ?), '15, 15', 0, 0, 0, 0.2, 20, 1)""",
                                                         (nickname,))
                                    con.commit()
                                    objective = Objective()
                                    game_map = Map()
                                    resources = Resources()
                                    player = game_map.player
                                    sword = Sword(player.pos_x, player.pos_y)
                                    player.add_item(sword)
                                    pickaxe = Pickaxe(player.pos_x, player.pos_y)
                                    turret = Turret(10, 11693, 11462)
                                    player.add_item(pickaxe)
                                    enemies = []
                                    bullets = []
                                    turrets = []
                                    manager = manager3
                                    start_screen(True)
            manager.process_events(event)
        manager.update(time_delta)
        screen.fill('black')
        manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(FPS)
