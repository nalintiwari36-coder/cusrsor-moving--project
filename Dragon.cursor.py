import pygame
import math
import random

pygame.init()



WIDTH = 1200
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Realistic Dragon Mouse")

clock = pygame.time.Clock()



BG = (4, 5, 10)

DRAGON = (75, 82, 92)
DRAGON_DARK = (35, 40, 48)
DRAGON_LIGHT = (125, 135, 145)

WING = (45, 48, 58)
WING_BONE = (115, 120, 130)

HORN = (190, 190, 175)

EYE = (255, 190, 20)
EYE_GLOW = (255, 90, 10)

FIRE_RED = (255, 50, 10)
FIRE_ORANGE = (255, 130, 10)
FIRE_YELLOW = (255, 230, 60)

WHITE = (235, 235, 235)



SEGMENTS = 42
DISTANCE = 12

body = []

mx = WIDTH // 2
my = HEIGHT // 2

for i in range(SEGMENTS):
    body.append([
        mx - i * DISTANCE,
        my
    ])


particles = []


def create_particle(x, y):
    particles.append({
        "x": x,
        "y": y,
        "vx": random.uniform(-1.5, 1.5),
        "vy": random.uniform(-2.5, -0.5),
        "life": random.randint(15, 35),
        "size": random.randint(2, 5)
    })


def update_particles():

    for p in particles[:]:

        p["x"] += p["vx"]
        p["y"] += p["vy"]

        p["life"] -= 1

        if p["life"] <= 0:
            particles.remove(p)


def draw_particles():

    for p in particles:

        pygame.draw.circle(
            screen,
            FIRE_ORANGE,
            (int(p["x"]), int(p["y"])),
            p["size"]
        )




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




def draw_wing(index, side):

    x = body[index][0]
    y = body[index][1]

    # Wing movement
    flap = math.sin(pygame.time.get_ticks() * 0.004) * 12

    points = [
        (int(x), int(y)),
        (int(x + side * 65), int(y - 65 - flap)),
        (int(x + side * 150), int(y - 115 - flap)),
        (int(x + side * 220), int(y - 75 - flap)),
        (int(x + side * 180), int(y - 10)),
        (int(x + side * 110), int(y + 15)),
    ]

    pygame.draw.polygon(
        screen,
        WING,
        points
    )

    # Wing bones

    pygame.draw.line(
        screen,
        WING_BONE,
        points[0],
        points[2],
        4
    )

    pygame.draw.line(
        screen,
        WING_BONE,
        points[0],
        points[3],
        4
    )

    pygame.draw.line(
        screen,
        WING_BONE,
        points[0],
        points[4],
        3
    )

    # Wing membrane lines

    pygame.draw.line(
        screen,
        DRAGON_DARK,
        points[2],
        points[1],
        2
    )

    pygame.draw.line(
        screen,
        DRAGON_DARK,
        points[3],
        points[2],
        2
    )




def draw_horn(x, y, side):

    points = [
        (x, y),
        (x + side * 12, y - 25),
        (x + side * 18, y - 48),
        (x + side * 8, y - 32)
    ]

    pygame.draw.polygon(
        screen,
        HORN,
        points
    )



def draw_head():

    x = body[0][0]
    y = body[0][1]

    # Neck
    pygame.draw.circle(
        screen,
        DRAGON_DARK,
        (int(x - 15), int(y)),
        30
    )

    # Main head
    pygame.draw.ellipse(
        screen,
        DRAGON,
        (
            int(x - 28),
            int(y - 25),
            65,
            55
        )
    )

    # Snout
    pygame.draw.polygon(
        screen,
        DRAGON_LIGHT,
        [
            (int(x + 20), int(y - 12)),
            (int(x + 65), int(y - 5)),
            (int(x + 70), int(y + 12)),
            (int(x + 20), int(y + 18))
        ]
    )

    # Lower jaw
    pygame.draw.polygon(
        screen,
        DRAGON_DARK,
        [
            (int(x + 25), int(y + 15)),
            (int(x + 65), int(y + 12)),
            (int(x + 48), int(y + 28)),
            (int(x + 15), int(y + 22))
        ]
    )

    # Horns
    draw_horn(x - 12, y - 18, -1)
    draw_horn(x + 8, y - 20, 1)

    # Eyes
    pygame.draw.circle(
        screen,
        EYE_GLOW,
        (int(x + 12), int(y - 8)),
        8
    )

    pygame.draw.circle(
        screen,
        EYE,
        (int(x + 12), int(y - 8)),
        4
    )

    # Eye pupil
    pygame.draw.line(
        screen,
        (0, 0, 0),
        (int(x + 12), int(y - 13)),
        (int(x + 12), int(y - 3)),
        2
    )

    # Nostril
    pygame.draw.circle(
        screen,
        (10, 10, 10),
        (int(x + 52), int(y + 2)),
        3
    )

    # Teeth

    for i in range(4):

        tx = x + 30 + i * 8

        pygame.draw.polygon(
            screen,
            WHITE,
            [
                (int(tx), int(y + 14)),
                (int(tx + 5), int(y + 14)),
                (int(tx + 2), int(y + 23))
            ]
        )




def draw_scales():

    for i in range(3, 32, 2):

        x = body[i][0]
        y = body[i][1]

        radius = max(
            3,
            int(9 - i * 0.12)
        )

        pygame.draw.arc(
            screen,
            DRAGON_LIGHT,
            (
                int(x - radius),
                int(y - radius),
                radius * 2,
                radius * 2
            ),
            0,
            math.pi,
            2
        )



def draw_leg(index, side):

    x = body[index][0]
    y = body[index][1]


    x2 = x + side * 25
    y2 = y + 28


    x3 = x2 + side * 15
    y3 = y2 + 25

    pygame.draw.line(
        screen,
        DRAGON_DARK,
        (int(x), int(y)),
        (int(x2), int(y2)),
        8
    )

    pygame.draw.line(
        screen,
        DRAGON,
        (int(x2), int(y2)),
        (int(x3), int(y3)),
        6
    )


    pygame.draw.line(
        screen,
        DRAGON_LIGHT,
        (int(x3), int(y3)),
        (int(x3 + side * 15), int(y3)),
        4
    )


    for i in range(3):

        claw_x = x3 + side * (12 + i * 5)

        pygame.draw.line(
            screen,
            HORN,
            (int(claw_x), int(y3)),
            (int(claw_x + side * 5), int(y3 + 7)),
            2
        )




def draw_tail():

    for i in range(25, SEGMENTS - 1):

        thickness = max(
            2,
            10 - (i - 25) // 2
        )

        pygame.draw.line(
            screen,
            DRAGON_DARK,
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





def draw_fire():

    x = body[-1][0]
    y = body[-1][1]

    # Tail fire
    for i in range(3):

        size = random.randint(8, 15)

        create_particle(
            x - random.randint(0, 15),
            y + random.randint(-5, 5)
        )

        pygame.draw.circle(
            screen,
            FIRE_ORANGE,
            (
                int(x - i * 12),
                int(y)
            ),
            size
        )

    pygame.draw.circle(
        screen,
        FIRE_YELLOW,
        (int(x), int(y)),
        7
    )





def draw_dragon():

    # Wings behind body
    draw_wing(6, -1)
    draw_wing(6, 1)


    draw_tail()


    for i in range(SEGMENTS - 1):

        thickness = max(
            3,
            int(14 - i * 0.25)
        )

        pygame.draw.line(
            screen,
            DRAGON,
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


    draw_scales()

    # Legs
    draw_leg(9, -1)
    draw_leg(9, 1)

    draw_leg(17, -1)
    draw_leg(17, 1)

    # Head
    draw_head()

    # Fire
    draw_fire()




running = True

while running:

    # Events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    # Mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()


    body[0][0] = mouse_x
    body[0][1] = mouse_y


    for i in range(1, SEGMENTS):

        follow(
            body[i - 1],
            body[i],
            DISTANCE
        )


    update_particles()


    screen.fill(BG)

    draw_dragon()


    draw_particles()

    pygame.display.flip()

    clock.tick(60)


pygame.quit()