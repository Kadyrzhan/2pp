import pygame
pygame.init()
screen = pygame.display.set_mode((600, 300))
pygame.display.set_caption('a')
running = True
while running:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
