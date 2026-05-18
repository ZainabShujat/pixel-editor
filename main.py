import pygame
import sys

pygame.init()

# Window settings
WIDTH = 1000
HEIGHT = 900

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tiny Pixel Editor")

clock = pygame.time.Clock()

# Grid settings
GRID_SIZE = 32
CELL_SIZE = 20

# Drawing area offset
OFFSET_X = 50
OFFSET_Y = 50

# Colors
BACKGROUND = (20, 20, 20)
GRID_COLOR = (50, 50, 50)

palette = [
    (255, 255, 255),  # White
    (255, 0, 0),      # Red
    (0, 255, 0),      # Green
    (0, 0, 255),      # Blue
    (255, 255, 0),    # Yellow
    (255, 165, 0),    # Orange
    (255, 105, 180),  # Pink
    (128, 0, 255),    # Purple
    (0, 255, 255),    # Cyan
    (0, 0, 0),        # Black
]

current_color = palette[0]

# Pixel data
pixels = {}

# Undo / Redo stacks
undo_stack = []
redo_stack = []

font = pygame.font.SysFont("arial", 18)

def save_state():
    undo_stack.append(pixels.copy())

    # Limit memory usage
    if len(undo_stack) > 100:
        undo_stack.pop(0)

def undo():
    global pixels

    if undo_stack:
        redo_stack.append(pixels.copy())
        pixels = undo_stack.pop()

def redo():
    global pixels

    if redo_stack:
        undo_stack.append(pixels.copy())
        pixels = redo_stack.pop()

def clear_canvas():
    global pixels
    save_state()
    pixels = {}

def save_image():
    surface = pygame.Surface(
        (GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE)
    )

    surface.fill(BACKGROUND)

    for (x, y), color in pixels.items():

        rect = pygame.Rect(
            x * CELL_SIZE,
            y * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )

        pygame.draw.rect(surface, color, rect)

    pygame.image.save(surface, "pixel_art.png")

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Mouse drawing
        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Palette selection
            for i, color in enumerate(palette):

                palette_rect = pygame.Rect(
                    750,
                    50 + i * 50,
                    40,
                    40
                )

                if palette_rect.collidepoint(mouse_x, mouse_y):
                    current_color = color

            # Grid drawing
            grid_x = (mouse_x - OFFSET_X) // CELL_SIZE
            grid_y = (mouse_y - OFFSET_Y) // CELL_SIZE

            if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:

                save_state()

                pixels[(grid_x, grid_y)] = current_color

                redo_stack.clear()

        # Keyboard shortcuts
        if event.type == pygame.KEYDOWN:

            # Undo
            if event.key == pygame.K_z:
                undo()

            # Redo
            if event.key == pygame.K_y:
                redo()

            # Clear
            if event.key == pygame.K_c:
                clear_canvas()

            # Save image
            if event.key == pygame.K_s:
                save_image()

    # Background
    screen.fill(BACKGROUND)

    # Draw pixels
    for (x, y), color in pixels.items():

        rect = pygame.Rect(
            OFFSET_X + x * CELL_SIZE,
            OFFSET_Y + y * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )

        pygame.draw.rect(screen, color, rect)

    # Draw grid
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):

            rect = pygame.Rect(
                OFFSET_X + col * CELL_SIZE,
                OFFSET_Y + row * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )

            pygame.draw.rect(screen, GRID_COLOR, rect, 1)

    # Draw palette
    for i, color in enumerate(palette):

        rect = pygame.Rect(
            750,
            50 + i * 50,
            40,
            40
        )

        pygame.draw.rect(screen, color, rect)

        if color == current_color:
            pygame.draw.rect(screen, (255, 255, 255), rect, 3)

    # Instructions
    instructions = [
        "Z = Undo",
        "Y = Redo",
        "C = Clear",
        "S = Save Image"
    ]

    for i, text in enumerate(instructions):

        label = font.render(text, True, (220, 220, 220))

        screen.blit(label, (750, 650 + i * 30))

    pygame.display.flip()

    clock.tick(60)
