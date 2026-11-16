
import pygame
import math
import sys

# =========================================================
# ELEGANT LOVE HEART
# Original animation faithfully recreated in Python
# =========================================================

pygame.init()

WIDTH, HEIGHT = 1000, 760
STAGE = 450
TOTAL_ITEMS = 100
FPS = 60
RENDER_SCALE = 2

BLACK = (0, 0, 0)

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT), pygame.RESIZABLE
)

pygame.display.set_caption("I Love You")
clock = pygame.time.Clock()

# =========================================================
# ORIGINAL VERTICAL KEYFRAMES
# =========================================================

KEYFRAMES = [
    (0, 180),
    (10, 45),
    (15, 4.5),
    (18, 0),
    (20, 4.5),
    (22, 34.61538),
    (24, 64.28571),
    (25, 112.5),
    (26, 64.28571),
    (28, 34.61538),
    (30, 4.5),
    (32, 0),
    (35, 4.5),
    (40, 45),
    (50, 180),
    (71, 428.57143),
    (72.5, 441.17647),
    (75, 450),
    (77.5, 441.17647),
    (79, 428.57143),
    (100, 180)
]


# =========================================================
# EASING
# CSS cubic-bezier(0.42, 0, 0.58, 1)
# =========================================================

def ease_in_out(t):

    low = 0.0
    high = 1.0

    for _ in range(24):

        u = (low + high) / 2
        v = 1 - u

        x = (
            3 * v * v * u * 0.42
            + 3 * v * u * u * 0.58
            + u ** 3
        )

        if x < t:
            low = u
        else:
            high = u

    u = (low + high) / 2
    v = 1 - u

    return (
        3 * v * v * u * 0
        + 3 * v * u * u
        + u ** 3
    )


# =========================================================
# HORIZONTAL ANIMATION
# 10 seconds, alternate, infinite
# =========================================================

def horizontal_position(t):

    phase = t % 20

    if phase <= 10:

        progress = ease_in_out(phase / 10)

    else:

        progress = 1 - ease_in_out(
            (phase - 10) / 10
        )

    return STAGE * progress


# =========================================================
# VERTICAL ANIMATION
# 20 seconds, linear, infinite
# =========================================================

def vertical_position(t):

    percent = (t % 20) * 5

    for i in range(len(KEYFRAMES) - 1):

        p1, y1 = KEYFRAMES[i]
        p2, y2 = KEYFRAMES[i + 1]

        if p1 <= percent <= p2:

            ratio = (percent - p1) / (p2 - p1)

            return y1 + (y2 - y1) * ratio

    return 180


# =========================================================
# FONT SELECTION
# =========================================================

def get_elegant_font(size):

    candidates = [
        "Georgia",
        "Palatino Linotype",
        "Palatino",
        "Times New Roman",
        "Liberation Serif",
        "DejaVu Serif"
    ]

    for name in candidates:

        path = pygame.font.match_font(
            name, italic=True
        )

        if path:

            font = pygame.font.Font(path, size)
            font.set_italic(True)
            return font

    font = pygame.font.SysFont(
        "serif", size, italic=True
    )

    return font


# =========================================================
# GRADIENT TYPOGRAPHY
# =========================================================

def create_gradient_text():

    phrase = "I love you"

    font = get_elegant_font(46)

    # Restrained blush-pink gradient

    start_color = (255, 218, 232)
    end_color = (238, 139, 177)

    letter_spacing = 3

    glyphs = []

    for i, char in enumerate(phrase):

        ratio = i / max(1, len(phrase) - 1)

        color = tuple(
            round(a + (b - a) * ratio)
            for a, b in zip(start_color, end_color)
        )

        glyph = font.render(
            char, True, color
        )

        glyphs.append(glyph)

    text_width = (
        sum(g.get_width() for g in glyphs)
        + letter_spacing * (len(glyphs) - 1)
    )

    text_height = max(
        g.get_height() for g in glyphs
    )

    text = pygame.Surface(
        (text_width, text_height),
        pygame.SRCALPHA
    )

    cursor = 0

    for glyph in glyphs:

        y = (text_height - glyph.get_height()) // 2

        text.blit(glyph, (cursor, y))

        cursor += glyph.get_width() + letter_spacing

    return text, text_width, text_height


# =========================================================
# TINT SURFACE
# =========================================================

def tint_surface(surface, color):

    result = surface.copy()

    tint = pygame.Surface(
        surface.get_size(),
        pygame.SRCALPHA
    )

    tint.fill((*color, 255))

    result.blit(
        tint,
        (0, 0),
        special_flags=pygame.BLEND_RGBA_MULT
    )

    return result


# =========================================================
# SOFT BLUR
# =========================================================

def create_soft_blur(surface, divisor, color, alpha):

    w, h = surface.get_size()

    small_size = (
        max(1, w // divisor),
        max(1, h // divisor)
    )

    reduced = pygame.transform.smoothscale(
        surface, small_size
    )

    blurred = pygame.transform.smoothscale(
        reduced, (w, h)
    )

    blurred = tint_surface(
        blurred, color
    )

    blurred.set_alpha(alpha)

    return blurred


# =========================================================
# FINAL TYPOGRAPHY COMPOSITION
# =========================================================

def create_final_text():

    text, text_width, text_height = (
        create_gradient_text()
    )

    padding = 30

    canvas = pygame.Surface(
        (
            text_width + padding * 2,
            text_height + padding * 2
        ),
        pygame.SRCALPHA
    )

    # Layer 1: wide, very soft pink glow

    wide_glow = create_soft_blur(
        text,
        10,
        (255, 105, 165),
        34
    )

    canvas.blit(
        wide_glow,
        (padding, padding)
    )

    # Layer 2: tighter glow

    tight_glow = create_soft_blur(
        text,
        5,
        (255, 135, 185),
        45
    )

    canvas.blit(
        tight_glow,
        (padding, padding)
    )

    # Layer 3: delicate natural shadow

    shadow = tint_surface(
        text,
        (105, 35, 65)
    )

    shadow.set_alpha(65)

    canvas.blit(
        shadow,
        (padding + 1, padding + 3)
    )

    # Layer 4: sharp original typography

    canvas.blit(
        text,
        (padding, padding)
    )

    # Downsample for refined antialiasing

    final_surface = pygame.transform.smoothscale(
        canvas,
        (
            canvas.get_width() // RENDER_SCALE,
            canvas.get_height() // RENDER_SCALE
        )
    )

    # Original 30-degree rotation

    final_surface = pygame.transform.rotozoom(
        final_surface,
        -30,
        1.0
    )

    logical_width = text_width / RENDER_SCALE
    logical_height = text_height / RENDER_SCALE

    return (
        final_surface,
        logical_width,
        logical_height
    )


# =========================================================
# CREATE THE 100 ORIGINAL ANIMATION ELEMENTS
# =========================================================

love_text, text_width, text_height = (
    create_final_text()
)

love_items = []

for i in range(1, TOTAL_ITEMS + 1):

    love_items.append({
        "index": i,
        "delay": i * 0.3
    })


# =========================================================
# MAIN ANIMATION LOOP
# =========================================================

elapsed = 0.0
paused = False
last_scale = None
display_text = love_text

running = True

while running:

    dt = clock.tick(FPS) / 1000

    # -----------------------------------------------------
    # EVENTS
    # -----------------------------------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                running = False

            elif event.key == pygame.K_SPACE:

                paused = not paused

        elif event.type == pygame.VIDEORESIZE:

            screen = pygame.display.set_mode(
                (event.w, event.h),
                pygame.RESIZABLE
            )

    # -----------------------------------------------------
    # TIME
    # -----------------------------------------------------

    if not paused:

        elapsed += dt

    # -----------------------------------------------------
    # CLEAN BACKGROUND
    # -----------------------------------------------------

    screen.fill(BLACK)

    screen_width, screen_height = screen.get_size()

    # Responsive stage scaling

    scale = min(
        1.0,
        (screen_width - 50) / STAGE,
        (screen_height - 50) / STAGE
    )

    scale = max(0.1, scale)

    stage_size = STAGE * scale

    stage_x = (screen_width - stage_size) / 2
    stage_y = (screen_height - stage_size) / 2

    # Rebuild scaled text only when window size changes

    if scale != last_scale:

        display_size = (
            max(1, round(love_text.get_width() * scale)),
            max(1, round(love_text.get_height() * scale))
        )

        display_text = pygame.transform.smoothscale(
            love_text,
            display_size
        )

        last_scale = scale

    # -----------------------------------------------------
    # ORIGINAL 100-TEXT HEART ANIMATION
    # -----------------------------------------------------

    for item in love_items:

        # Individual negative CSS animation delay

        t = elapsed + item["delay"]

        # Horizontal movement

        x = horizontal_position(t)

        # Vertical movement

        y = vertical_position(t)

        # Position relative to responsive stage

        center_x = (
            stage_x
            + (x + text_width / 2) * scale
        )

        center_y = (
            stage_y
            + (y - text_height / 2) * scale
        )

        # Center-anchored rotated typography

        rect = display_text.get_rect(
            center=(
                round(center_x),
                round(center_y)
            )
        )

        screen.blit(
            display_text,
            rect
        )

    # -----------------------------------------------------
    # DISPLAY
    # -----------------------------------------------------

    pygame.display.flip()


# =========================================================
# EXIT
# =========================================================

pygame.quit()
sys.exit()
