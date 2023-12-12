import pygame

pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)

running = True
FPS = 100
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill('white')
    pygame.display.flip()
    clock.tick(FPS)
