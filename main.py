import pygame as pg
import random
from timer import Timer

colors = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), 
          (127, 127, 255), (127, 255, 127), (255, 127, 127), 
          (255, 255, 0), (255, 0, 255), (0, 255, 255), 
          (255, 127, 0), (127, 255, 0), (0, 127, 255), (255, 0, 127), (0, 255, 127), (127, 0, 255)
]
blocks = [
    [
        [1, 1, 1, 1]
    ],
    [
        [1], 
        [1], 
        [1], 
        [1]
    ],
    [
        [1, 1],
        [1, 1]
    ],
    [
        [1, 0, 0],
        [1, 1, 0],
        [0, 1, 1]
    ],
    [
        [1, 0, 0],
        [1, 0, 0],
        [1, 1, 1]
    ],
    [
        [0, 0, 1],
        [0, 0, 1],
        [1, 1, 1]
    ],
    [
        [1, 1, 1],
        [1, 0, 0],
        [1, 0, 0]
    ],
    [
        [1, 1, 1],
        [0, 0, 1],
        [0, 0, 1]
    ],
    [
        [1]
    ],
    [
        [1, 1]
    ],
    [
        [1, 1],
        [0, 1],
        [0, 1]
    ],
    [
        [1, 1],
        [1, 0],
        [1, 0]
    ],
    [
        [1, 0],
        [1, 0],
        [1, 1]
    ],
    [
        [0, 1],
        [0, 1],
        [1, 1]
    ],
    [
        [1, 1, 1],
        [1]
    ],
    [
        [1],
        [1, 1, 1]
    ],
    [
        [1, 1, 1],
        [0, 0, 1]
    ],
    [
        [0, 0, 1],
        [1, 1, 1]
    ],
    [
        [1], [1]
    ],
    [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0]
    ],
    [
        [0, 1],
        [1, 1],
        [0, 1]
    ],
    [
        [0, 1, 0],
        [1, 1, 1]
    ],
    [
        [1, 0],
        [1, 1],
        [1, 0]
    ],
    [
        [1, 1, 1],
        [0, 1, 0]
    ],
    [
        [0, 1],
        [1, 1],
        [1, 0]
    ],
    [
        [1, 1, 0],
        [0, 1, 1]
    ],
    [
        [1, 0],
        [1, 1],
        [0, 1]
    ],
    [
        [1, 1, 0],
        [0, 1, 1]
    ]
]


def rand_color():
    return random.randint(1, len(colors)-1)


def draw_block(screen, x, y, w, block: list[list[bool]], color: int):
    for i, row in enumerate(block):
        for j, cell in enumerate(row):
            if cell:
                pg.draw.rect(screen, colors[color], (x + i*w, y + j*w, w, w))
                pg.draw.rect(screen, (255, 255, 255), (x + i*w, y + j*w, w, w), 5)


class Grid:
    def __init__(self, w, h):
        self.grid = [[colors[0] for _ in range(h)] for __ in range(w)] # grid[x][y]
    
    def add(self, x, y, block: list[list[bool]], color: int):
        for i, row in enumerate(block):
            for j, cell in enumerate(row):
                if cell:
                    self.grid[x + i][y + j] = color

    def can_add(self, x, y, block: list[list[bool]]) -> bool:
        if len(self.grid) < x + len(block) or len(self.grid[0]) < y + len(block[0]) or x < 0 or y < 0:
            return False
        for i, row in enumerate(block):
            for j, cell in enumerate(row):
                if cell and self.grid[x + i][y + j]:
                    return False
        return True

    def update(self):
        for col in self.grid:
            if all(col):
                for i in range(len(col)):
                    col[i] = 0
        for i in range(len(self.grid[0])):
            line = [self.grid[j][i] for j in range(len(self.grid))]
            if all(line):
                for col in self.grid:
                    col[i] = 0

    def draw(self, screen, w):
        for x in range(len(self.grid)):
            for y in range(len(self.grid[0])):
                pg.draw.rect(screen, colors[self.grid[x][y]], (x * w, y * w, w, w))


def main():
    pg.init()

    res = 1000, 600 # initial resolution of the window
    w, h = 12, 6 # grid size

    square_w = min(res[0]//w, res[1]//h)

    res = square_w*w, square_w*h # resize window to only include grid
    screen = pg.display.set_mode(res, pg.RESIZABLE)

    clock = pg.time.Clock()
    delta_time = 0

    animation_timer = Timer(seconds=0.3)
    animation_sub_timer = Timer(seconds=0.1)
    key_timers = (Timer(seconds=0.15), Timer(seconds=0.15), Timer(seconds=0.15), Timer(seconds=0.15))
    n_click = -1
    lf_lmb = False
    dragging = False

    grid = Grid(w, h)
    block = None
    block_color = None
    block_x, block_y = 0, 0

    lf_mx, lf_my = 0, 0
    mx, my = 0, 0

    run = 1
    while run:
        if res != screen.get_size():
            res = screen.get_size()
            square_w = min(res[0]//w, res[1]//h)
        for e in pg.event.get():
            if e.type == pg.QUIT:
                run = 0
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    run = 0
                elif e.key == pg.K_SPACE or e.key == pg.K_RETURN:
                    n_click = (n_click + 1) % 2
                    animation_timer.restart()

        keys = pg.key.get_pressed()
        if (keys[pg.K_z] or keys[pg.K_w]) and not key_timers[0].is_running():
            block_y -= square_w
            key_timers[0].restart()
        if keys[pg.K_s] and not key_timers[1].is_running():
            block_y += square_w
            key_timers[1].restart()
        if (keys[pg.K_q] or keys[pg.K_a]) and not key_timers[2].is_running():
            block_x -= square_w
            key_timers[2].restart()
        if keys[pg.K_d] and not key_timers[3].is_running():
            block_x += square_w
            key_timers[3].restart()

        delta_time = clock.tick(500)
        pg.display.set_caption(f'BlockSpace FPS: {clock.get_fps():.1f}')

        lmb = pg.mouse.get_pressed()[0]
        mx, my = pg.mouse.get_pos()

        if lmb and not lf_lmb:
            n_click = (n_click + 1) % 2
            animation_timer.restart()

        if (mx, my) != (lf_mx, lf_my):
            block_x, block_y = mx // square_w * square_w, my // square_w * square_w

        if n_click == 0 and animation_timer.is_running():
            dragging = True
            # take block
            block = blocks[random.randint(0, len(blocks)-1)]
            block_color = rand_color()

        if n_click == 1 and dragging:
            dragging = False
            # drop block
            x, y = block_x // square_w, block_y // square_w
            if grid.can_add(x, y, block):
                grid.add(x, y, block, block_color)
            block = None
            block_color = None


        grid.update()
        animation_timer.manual_update(delta_time)
        [key_timer.manual_update(delta_time) for key_timer in key_timers]

        screen.fill((30, 0, 30))

        grid.draw(screen, square_w)
        if block is not None:
            draw_block(screen, block_x, block_y, square_w, block, block_color)

        pg.display.flip()

        lf_lmb = lmb
        lf_mx, lf_my = mx, my


    return 0


if __name__ == '__main__':
    main()
