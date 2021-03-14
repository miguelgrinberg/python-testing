import sys
import pygame
from life import Life

SCREEN_SIZE = 500
FPS = 5

life = Life()


def initialize_game(pattern_file=None, x=None, y=None):
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_SIZE, SCREEN_SIZE])

    if pattern_file:
        life.load(pattern_file, None or 0, None or 0)

    return screen


def center(scale):
    cell_count = SCREEN_SIZE // scale
    min_x, min_y, max_x, max_y = life.bounding_box()

    basex = min_x - (cell_count - (max_x - min_x + 1)) // 2
    basey = min_y - (cell_count - (max_y - min_y + 1)) // 2
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
                        basex += 2
                    elif event.key == pygame.K_RIGHT:
                        basex -= 2
                    elif event.key == pygame.K_UP:
                        basey += 2
                    elif event.key == pygame.K_DOWN:
                        basey -= 2
                    elif event.unicode == ' ':
                        paused = not paused
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
    game_loop(screen)
    pygame.quit()
