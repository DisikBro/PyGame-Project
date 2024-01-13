import pygame
import pygame_gui

from consts import size

pygame.init()
manager1 = pygame_gui.UIManager(size, 'theme1.json')
registration_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((420 + 370, 330 + 100), (170, 50)),
                                                   text='Создать аккаунт',
                                                   manager=manager1)
entrance_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((420 + 370, 400 + 100), (170, 50)),
                                               text='Войти',
                                               manager=manager1)

manager2 = pygame_gui.UIManager(size, 'theme1.json')
label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((290 + 370, 330 + 100), (128, 30)),
                                    text='Введите никнейм:',
                                    manager=manager2)
message = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((660, 385), (300, 30)),
                                      text='',
                                      manager=manager2)
login_entry = pygame_gui.elements.UITextEntryLine(pygame.Rect((420 + 370, 330 + 100), (170, 30)), manager2)
accept_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((290 + 370, 365 + 100), (298, 30)),
                                             text='Подтвердить',
                                             manager=manager2)
back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((290 + 370, 240 + 100), (100, 40)),
                                           text='Назад',
                                           manager=manager2)
manager3 = pygame_gui.UIManager(size, 'theme2.json')
play_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((790, 360), (298, 30)),
                                           text='Играть',
                                           manager=manager3)
settings_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((790, 395), (298, 30)),
                                               text='Настройки',
                                               manager=manager3)
exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((790, 430), (298, 30)),
                                           text='Выход',
                                           manager=manager3)
manager4 = pygame_gui.UIManager(size, 'theme2.json')
music_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((790, 430), (298, 30)), start_value=0.2,
                                                      value_range=(0, 1), manager=manager4)
label1 = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((790, 395), (298, 30)),
                                     text='Громкость музыки',
                                     manager=manager4)
back_button1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((790, 480), (100, 40)),
                                            text='Назад',
                                            manager=manager4)
