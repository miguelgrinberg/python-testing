import sys
import pygame
from life import Life

SCREEN_SIZE = 500
FPS = 5

life = Life()


def initialize_game(pattern_file=None):
    pygame.init()
    pygame.display.set_caption('Game of Life')
    screen = pygame.display.set_mode([SCREEN_SIZE, SCREEN_SIZE])

    if pattern_file:
        life.load(pattern_file)

    return screen


def center(scale):
    cell_count = SCREEN_SIZE // scale
    minx, miny, maxx, maxy = life.bounding_box()

    basex = minx - (cell_count - (maxx - minx + 1)) // 2
    basey = miny - (cell_count - (maxy - miny + 1)) // 2
    return basex, basey


def game_loop(screen):
    running = True
    paused = False
    scale = 20
    basex, basey = center(scale)
    interval = 1000 // FPS

    while running:
        start_time = pygame.time.get_ticks()

        screen.fill((255, 255, 255))
        for i in range(0, SCREEN_SIZE, scale):
            pygame.draw.line(screen, (0, 0, 0), (i, 0), (i, SCREEN_SIZE))
            pygame.draw.line(screen, (0, 0, 0), (0, i), (SCREEN_SIZE, i))
        for cell in life.alive:
            x = cell[0]
            y = cell[1]
            pygame.draw.rect(screen, (80, 80, 192),
                             ((x - basex) * scale + 2, (y - basey) * scale + 2,
                              scale - 3, scale - 3))

        pygame.display.flip()
        if not paused:
            life.advance()

        wait_time = 1
        while wait_time > 0:
            event = pygame.event.wait(timeout=wait_time)
            while event:
                if event.type == pygame.QUIT:
                    running = False
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_LEFT:
                        basex -= 2
                    elif event.key == pygame.K_RIGHT:
                        basex += 2
                    elif event.key == pygame.K_UP:
                        basey -= 2
                    elif event.key == pygame.K_DOWN:
                        basey += 2
                    elif event.unicode == ' ':
                        paused = not paused
                        if paused:
                            pygame.display.set_caption('Game of Life (paused)')
                        else:
                            pygame.display.set_caption('Game of Life')
                    elif event.unicode == '+':
                        if scale < 50:
                            scale += 5
                    elif event.unicode == '-':
                        if scale > 10:
                            scale -= 5
                    elif event.unicode == 'c':
                        basex, basey = center(scale)
                    break
                elif event.type == pygame.MOUSEBUTTONUP:
                    mx, my = pygame.mouse.get_pos()
                    x = mx // scale + basex
                    y = my // scale + basey
                    life.alive.set(x, y)
                    break
                event = pygame.event.poll()
            if event:
                break

            current_time = pygame.time.get_ticks()
            wait_time = interval - (current_time - start_time)


if __name__ == '__main__':
    pattern_file = sys.argv[1] if len(sys.argv) > 1 else None
    screen = initialize_game(pattern_file)
    print('''
Press: Arrows to scroll
       Space to pause/resume the simulation
       +/- to zoom in/out
       c to re-center
       mouse click to toggle the state of a cell
       Esc to exit''')
    game_loop(screen)
    pygame.quit()
