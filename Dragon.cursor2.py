import pygame
import math

pygame.init()


WIDTH = 1000
HEIGHT = 650

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dragon Mouse Cursor")

clock = pygame.time.Clock()


BLACK = (5, 5, 10)
WHITE = (240, 240, 240)
RED = (220, 50, 50)
DARK_RED = (120, 20, 20)
ORANGE = (255, 120, 20)
YELLOW = (255, 220, 50)


SEGMENTS = 30
DISTANCE = 13

body = []

mouse_x, mouse_y = WIDTH // 2, HEIGHT // 2

for i in range(SEGMENTS):
    body.append([
        mouse_x - i * DISTANCE,
        mouse_y
    ])


# -----------------------------
# Make body follow mouse
# -----------------------------
def follow(parent, child, distance):

    dx = parent[0] - child[0]
    dy = parent[1] - child[1]

    length = math.sqrt(dx * dx + dy * dy)

    if length == 0:
        return

    dx /= length
    dy /= length

    child[0] = parent[0] - dx * distance
    child[1] = parent[1] - dy * distance



def draw_wing(x, y, side):

    points = [
        (x, y),
        (x + side * 35, y - 50),
        (x + side * 80, y - 75),
        (x + side * 55, y - 25),
        (x + side * 90, y + 5),
        (x + side * 35, y + 10)
    ]

    pygame.draw.polygon(
        screen,
        DARK_RED,
        points
    )

    pygame.draw.lines(
        screen,
        RED,
        True,
        points,
        2
    )



def draw_head():

    x = body[0][0]
    y = body[0][1]

    # Head
    pygame.draw.circle(
        screen,
        DARK_RED,
        (int(x), int(y)),
        16
    )

    # Snout
    pygame.draw.line(
        screen,
        RED,
        (int(x), int(y)),
        (int(x + 25), int(y)),
        5
    )

    # Horn 1
    pygame.draw.line(
        screen,
        WHITE,
        (int(x - 8), int(y - 12)),
        (int(x - 18), int(y - 30)),
        4
    )

    # Horn 2
    pygame.draw.line(
        screen,
        WHITE,
        (int(x + 2), int(y - 13)),
        (int(x + 8), int(y - 32)),
        4
    )

    # Eye
    pygame.draw.circle(
        screen,
        YELLOW,
        (int(x + 7), int(y - 5)),
        4
    )

    # Pupil
    pygame.draw.circle(
        screen,
        BLACK,
        (int(x + 8), int(y - 5)),
        2
    )



def draw_leg(point, side):

    x = point[0]
    y = point[1]

    x2 = x + side * 18
    y2 = y + 20

    x3 = x2 + side * 15
    y3 = y2 + 8

    pygame.draw.line(
        screen,
        WHITE,
        (int(x), int(y)),
        (int(x2), int(y2)),
        3
    )

    pygame.draw.line(
        screen,
        WHITE,
        (int(x2), int(y2)),
        (int(x3), int(y3)),
        3
    )

    # Claw
    pygame.draw.line(
        screen,
        WHITE,
        (int(x3), int(y3)),
        (int(x3 + side * 7), int(y3 + 5)),
        2
    )



def draw_fire():

    x = body[-1][0]
    y = body[-1][1]

    # Fire changes size over time
    pulse = math.sin(pygame.time.get_ticks() * 0.015) * 5

    points = [
        (int(x), int(y)),
        (int(x - 18 - pulse), int(y + 8)),
        (int(x - 28), int(y)),
        (int(x - 18 - pulse), int(y - 8))
    ]

    pygame.draw.polygon(
        screen,
        ORANGE,
        points
    )

    pygame.draw.circle(
        screen,
        YELLOW,
        (int(x - 12), int(y)),
        5
    )



def draw_dragon():

    # Body
    for i in range(len(body) - 1):

        # Front is thicker
        thickness = max(3, 12 - i // 4)

        pygame.draw.line(
            screen,
            DARK_RED,
            (
                int(body[i][0]),
                int(body[i][1])
            ),
            (
                int(body[i + 1][0]),
                int(body[i + 1][1])
            ),
            thickness
        )

    # Body scales
    for i in range(2, 25, 3):

        pygame.draw.circle(
            screen,
            RED,
            (
                int(body[i][0]),
                int(body[i][1])
            ),
            4
        )

    # Wings
    draw_wing(
        body[5][0],
        body[5][1],
        -1
    )

    draw_wing(
        body[5][0],
        body[5][1],
        1
    )

    # Legs
    for i in range(7, 24, 5):

        draw_leg(body[i], -1)
        draw_leg(body[i], 1)

    # Head
    draw_head()

    # Fire tail
    draw_fire()



running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False


    mouse_x, mouse_y = pygame.mouse.get_pos()


    body[0][0] = mouse_x
    body[0][1] = mouse_y


    for i in range(1, len(body)):

        follow(
            body[i - 1],
            body[i],
            DISTANCE
        )


    screen.fill(BLACK)


    draw_dragon()

    pygame.display.flip()

    clock.tick(60)


pygame.quit()