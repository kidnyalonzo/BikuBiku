import pygame
from bikubiku.dir import *
from bikubiku.constants import *
pygame.init()
screen=pygame.display.set_mode((640, 480))
light= pg.image.load(path.join(img_dir, LIGHT_MASK))
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: break
    else:
        screen.fill(pygame.color.Color('Red'))
        for x in (0, 640, 20):
            pygame.draw.line(screen, pygame.color.Color('Green'), (x, 0), (x, 480), 3)
        filter = pygame.Surface((640, 480))
        filter.fill(pygame.color.Color('Grey'))
        filter.blit(light, map(lambda x: x-50, pygame.mouse.get_pos()))
        screen.blit(filter, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        pygame.display.flip()
        continue
    break