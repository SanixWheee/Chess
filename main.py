import pygame
import sys

pygame.init()

size = width, height = 800, 800

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Chess')

whiteTile = '#E6D5BB'
greenTile = '#355745'

tiles = []

'''
    For Reference
    [0][0] is a8
    [0][7] is h8
    [7][0] is a1
    [7][7] is h1
'''

class Tile:
    def __init__(self, xPos, yPos, tileColor, name='none', occupied=False):
        self.xPos = xPos
        self.yPos = yPos
        self.tileColor = tileColor
        self.name = name
        self.occupied = occupied

        pygame.draw.rect(screen, tileColor, (xPos, yPos, 100, 100))
    
    def __str__(self):
        return self.name
    
    def updateName(self, name):
        self.name = name
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.tileColor, (self.xPos, self.yPos, 100, 100))

class Piece:
    def __init__(self, id, tile, side, type="pawn"):
        self.tile = tile
        self.side = side
        self.type = type
        self.id = id
        self.image = self.load_image()
        self.image = pygame.transform.smoothscale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (self.tile.xPos + 48, self.tile.yPos + 50)

    def __str__(self):
        return self.type

    def load_image(self):
        image_path = f'images/{self.type.capitalize()}{self.side[0].upper()}.png'
        return pygame.image.load(image_path).convert_alpha()
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

for y in range(8):
    row = []
    for x in range(8):
        xPos = x * 100
        yPos = y * 100
        if ((x + y) % 2 == 1):
            row.append(Tile(xPos, yPos, greenTile))
        else:
            row.append(Tile(xPos, yPos, whiteTile))
    tiles.append(row)

pieces = []
#white pieces
pieces.append(Piece("pw1", tiles[6][0], 'white', 'pawn'))
pieces.append(Piece("pw2", tiles[6][1], 'white', 'pawn'))
pieces.append(Piece("pw3", tiles[6][2], 'white', 'pawn'))
pieces.append(Piece("pw4", tiles[6][3], 'white', 'pawn'))
pieces.append(Piece("pw5", tiles[6][4], 'white', 'pawn'))
pieces.append(Piece("pw6", tiles[6][5], 'white', 'pawn'))
pieces.append(Piece("pw7", tiles[6][6], 'white', 'pawn'))
pieces.append(Piece("pw8", tiles[6][7], 'white', 'pawn'))
pieces.append(Piece("rw1", tiles[7][0], 'white', 'rook'))
pieces.append(Piece("rk1", tiles[7][1], 'white', 'knight'))
pieces.append(Piece("rb1", tiles[7][2], 'white', 'bishop'))
pieces.append(Piece("qw", tiles[7][3], 'white', 'queen'))
pieces.append(Piece("kw", tiles[7][4], 'white', 'king'))
pieces.append(Piece("bw2", tiles[7][5], 'white', 'bishop'))
pieces.append(Piece("kw2", tiles[7][6], 'white', 'knight'))
pieces.append(Piece("rw2", tiles[7][7], 'white', 'rook'))

#black pieces
pieces.append(Piece("pb1", tiles[1][0], 'black', 'pawn'))
pieces.append(Piece("pb2", tiles[1][1], 'black', 'pawn'))
pieces.append(Piece("pb3", tiles[1][2], 'black', 'pawn'))
pieces.append(Piece("pb4", tiles[1][3], 'black', 'pawn'))
pieces.append(Piece("pb5", tiles[1][4], 'black', 'pawn'))
pieces.append(Piece("pb6", tiles[1][5], 'black', 'pawn'))
pieces.append(Piece("pb7", tiles[1][6], 'black', 'pawn'))
pieces.append(Piece("pb8", tiles[1][7], 'black', 'pawn'))
pieces.append(Piece("rb1", tiles[0][0], 'black', 'rook'))
pieces.append(Piece("kb1", tiles[0][1], 'black', 'knight'))
pieces.append(Piece("bb1", tiles[0][2], 'black', 'bishop'))
pieces.append(Piece("pq", tiles[0][3], 'black', 'queen'))
pieces.append(Piece("pk", tiles[0][4], 'black', 'king'))
pieces.append(Piece("pb2", tiles[0][5], 'black', 'bishop'))
pieces.append(Piece("pk2", tiles[0][6], 'black', 'knight'))
pieces.append(Piece("pr2", tiles[0][7], 'black', 'rook'))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    for row in tiles:
        for tile in row:
            tile.draw(screen)

    for piece in pieces:
        piece.draw(screen)
        if pygame.mouse.get_pressed()[0] and piece.rect.collidepoint(pygame.mouse.get_pos()):
            print (piece.id)
    

    pygame.display.flip()

pygame.quit()
sys.exit()