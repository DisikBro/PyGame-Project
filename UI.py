import pygame
import pygame_gui

from consts import size

pygame.init()
manager1 = pygame_gui.UIManager(size)
registration_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((320, 230), (170, 50)),
                                                   text='Создать аккаунт',
                                                   manager=manager1)
entrance_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((320, 300), (170, 50)),
                                               text='Войти',
                                               manager=manager1)

manager2 = pygame_gui.UIManager(size)
label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((190, 230), (128, 30)), text='Введите никнейм:',
                                    manager=manager2)
login_entry = pygame_gui.elements.UITextEntryLine(pygame.Rect((320, 230), (170, 30)), manager2)
accept_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((190, 265), (298, 30)),
                                             text='Подтвердить',
                                             manager=manager2)
back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((190, 140), (100, 40)),
                                           text='Назад',
                                           manager=manager2)
