import serial.tools.list_ports
import serial
import pygame


for port in serial.tools.list_ports.comports():
    if port.description.startswith("STM"):
        ser = serial.Serial(
            port=port.device,  # ou "/dev/ttyUSB0"
            baudrate=115200,  # doit correspondre à l'émetteur
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1  # secondes, évite le blocage infini
        )
        print(port.device, "-", port.description)


CELL_SIZE = 16   # taille d'une texture d'origine en pixels
ZOOM = 3            # agrandissement (entier, pour garder des pixels nets)

VISIBLE_COLUMNS = 26    # nombre de blocs affichés en largeur
SCROLL_SPEED = 400      # vitesse de défilement (pixels écran par seconde)
FPS = 40

BACKGROUND = pygame.Color("#7CA3EA")

MODE = "fichiers"   # "fichiers" ou "spritesheet"

# --- Mode "fichiers" : numéro -> chemin de l'image --------------------------
FILES = {
    1: "textures/dirt.png",
    2: "textures/grass.png",
    3: "textures/brick.png",
    4: "textures/file_block.png",
    5: "textures/block.png",
    6: "textures/chimney_left.png",
    7: "textures/chimney_right.png",
    8: "textures/chimney_left_top.png",
    9: "textures/chimney_right_top.png",
    10: "textures/millitary_unit.png",
    11: "textures/Ramio.png",
    12: "textures/Guili.png",
}

# --- Mode "spritesheet" : image unique, tuiles numérotées ligne par ligne ---
# (la tuile en haut à gauche = 0, celle d'à côté = 1, etc.)
SPRITESHEET = "textures/tileset.png"

# --- Votre tableau -----------------------------------------------------------

TABLEAU = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,10,0,10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,3,3,3,3,0,0,0,3,3,3,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,3,3,3,0,0,0,0,3,4,4,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,5,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,5,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,3,4,3,4,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,9,0,0,0,0,0,0,0,0,0,8,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,4,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,3,3,0,0,0,0,4,0,0,4,0,0,4,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,3,3,0,0,0,0,0,0,5,0,0,5,0,0,0,0,0,0,0,0,0,0,5,5,0,0,5,0,0,0,0,0,0,0,0,0,0,0,0,3,3,4,3,0,0,0,0,0,0,0,0,0,0,0,0,5,5,5,5,5,5,0,0,0,0,0,0,0,0,0,0,0,5,5,3,3,3,5,5],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,9,0,0,0,0,0,0,6,7,0,0,0,0,0,0,0,0,0,6,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,0,0,5,5,0,0,0,0,0,0,0,0,5,5,5,0,0,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,5,5,5,5,5,0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,3,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,9,0,0,0,0,0,0,0,0,6,7,0,0,0,0,0,0,6,7,0,0,0,0,0,0,0,0,0,6,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,5,0,0,5,5,5,0,0,0,0,0,0,5,5,5,5,0,0,5,5,5,0,0,0,0,0,8,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,9,0,5,5,5,5,5,5,5,5,0,0,0,0,0,0,0,0,0,0,0,0,3,3,0,3,3,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,10,0,0,0,0,0,6,7,0,0,0,0,0,0,0,0,6,7,10,0,0,0,0,0,6,7,0,0,0,10,10,0,0,0,0,6,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,10,0,10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,10,0,10,0,0,0,0,0,0,0,10,10,0,0,10,10,0,0,0,0,5,5,5,5,0,0,5,5,5,5,0,0,0,0,5,5,5,5,5,0,0,5,5,5,5,0,0,0,0,6,7,0,0,0,0,0,0,0,0,0,10,0,10,0,0,6,7,5,5,5,5,5,5,5,5,5,0,0,0,0,0,0,0,0,5,0,0,0,3,3,0,3,3,0],
    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

car_col = 3
car_row = 3
car_col_offset, car_row_offset = 0, 0


def scale_up(surface):
    """Agrandit sans lissage : transform.scale = plus proche voisin,
    donc les pixels restent nets (ne PAS utiliser smoothscale)."""
    size = CELL_SIZE * ZOOM
    return pygame.transform.scale(surface, (size, size))


def load_files():
    """Charge une image PNG par numéro de texture."""
    textures = {}
    for number, path in FILES.items():
        img = pygame.image.load(path).convert_alpha()  # garde la transparence
        if img.get_size() != (CELL_SIZE, CELL_SIZE):
            print(f"Attention : {path} fait {img.get_size()}, "
                  f"attendu {CELL_SIZE}x{CELL_SIZE}")
            img = pygame.transform.scale(img, (CELL_SIZE, CELL_SIZE))
        textures[number] = scale_up(img)
    return textures


def load_spritesheet():
    """Découpe une image unique en tuiles 16x16, numérotées ligne par ligne."""
    sheet = pygame.image.load(SPRITESHEET).convert_alpha()
    width, height = sheet.get_size()
    textures = {}
    number = 0
    for y in range(0, height - CELL_SIZE + 1, CELL_SIZE):
        for x in range(0, width - CELL_SIZE + 1, CELL_SIZE):
            tuile = sheet.subsurface((x, y, CELL_SIZE, CELL_SIZE))
            textures[number] = scale_up(tuile)
            number += 1
    return textures


def draw(screen, board, textures, scroll_x):
    """Dessine uniquement les colonnes visibles, décalées de scroll_x pixels."""
    screen.fill(BACKGROUND)
    size = CELL_SIZE * ZOOM

    first_column = scroll_x // size      # première colonne (partiellement) visible
    offset = scroll_x % size             # décalage en pixels de cette colonne
    last_column = first_column + VISIBLE_COLUMNS + 1   # +1 : colonne coupée à droite

    for line, row in enumerate(board):
        for column in range(first_column, min(last_column + 1, len(row))):
            number = row[column]
            if not number:
                continue
            position = ((column - first_column) * size - offset, line * size)
            texture = textures.get(number)
            if texture is None:
                # Numéro sans texture : case magenta pour repérer l'erreur
                pygame.draw.rect(screen, (255, 0, 255), (*position, size, size))
            else:
                screen.blit(texture, position)
    draw_Ramio_Guili(screen, textures)

def draw_Ramio_Guili(screen, textures):
    size = CELL_SIZE * ZOOM
    position = ((car_col*size), (15-car_row)*size)
    texture = textures.get(11)
    screen.blit(texture, position)


def main():
    pygame.init()

    size = CELL_SIZE * ZOOM
    total_columns = max(len(r) for r in TABLEAU)
    width = VISIBLE_COLUMNS * size
    height = len(TABLEAU) * size
    max_scroll = max(0, (total_columns - VISIBLE_COLUMNS) * size)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("ULTRA RAMIO FAMILY")

    # convert_alpha() a besoin que la fenêtre existe : on charge après set_mode
    textures = load_files() if MODE == "fichiers" else load_spritesheet()

    clock = pygame.time.Clock()
    scroll_x = 0.0   # position de la "caméra" en pixels écran
    running = True
    while running:
        dt = clock.tick(FPS) / 1000   # durée de l'image précédente en secondes

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Flèches maintenues = défilement continu
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            scroll_x += SCROLL_SPEED * dt
        if keys[pygame.K_LEFT]:
            scroll_x -= SCROLL_SPEED * dt
        scroll_x = max(0, min(scroll_x, max_scroll))   # reste dans le niveau

        draw(screen, TABLEAU, textures, int(scroll_x))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
