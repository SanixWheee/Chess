import pygame
import sys

pygame.init()
pygame.font.init()

font = pygame.font.SysFont('Verdana', 30)
size = width, height = 800, 900

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Chess')

checkText = font.render('Some Text', False, (255, 255, 255))
checkRect = checkText.get_rect(center = (width//2, height-70))

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
    def __init__(self, xPos, yPos, tileColor, piece=None, occupied='none'):
        self.xPos = xPos
        self.yPos = yPos
        self.colPos = int(xPos/100)
        self.rowPos = int(yPos/100)
        self.tileColor = tileColor
        self.piece = piece
        self.occupied = occupied
        self.rect = pygame.Rect(xPos, yPos, 100, 100)

        pygame.draw.rect(screen, tileColor, (xPos, yPos, 100, 100))
    
    def __str__(self):
        return self.piece
    
    def updateName(self, piece):
        self.piece = piece
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.tileColor, (self.xPos, self.yPos, 100, 100))

class Piece:
    def __init__(self, id, tile, side, type="pawn", check=False):
        self.tile = tile
        self.side = side
        self.type = type
        self.id = id
        self.check = check
        self.image = self.loadImage()
        self.image = pygame.transform.smoothscale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (self.tile.xPos + 48, self.tile.yPos + 50)

        self.tile.occupied = side
        self.tile.piece = self

    def __str__(self):
        return self.type

    def loadImage(self):
        image_path = f'images/{self.type.capitalize()}{self.side[0].upper()}.png'
        return pygame.image.load(image_path).convert_alpha()
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def movePiece(self, xPos, yPos):
        self.rect.center = (xPos, yPos)

    def updateTile(self, tile):
        self.tile = tile
        self.rect.center = (self.tile.xPos + 48, self.tile.yPos + 50)

    def checkCheck(self):
        directions = [
            (-1, 0),  # straight up *rook, queen
            (-1, 1),  # upper right *bishop, queen
            (0, 1),   # straight right *rook queen
            (1, 1),   # bottom right *bishop queen
            (1, 0),   # straight down *rook queen
            (1, -1),  # bottom left *bishop queen
            (0, -1),  # straight left *rook queen
            (-1, -1)  # upper left *bishop queen
        ]
        knightDir = [
            (-2, -1),
            (-1, -2),
            (1, -2),
            (2, -1),
            (2, 1),
            (1, 2),
            (-1, 2),
            (-2, 1)
        ]
        pawnDir = [
            (-1, -1),
            (-1, 1),
        ]
        
        self.check = False

        for direction in directions:
            checkX, checkY = self.tile.colPos, self.tile.rowPos
            while True:
                checkX += direction[1]
                checkY += direction[0]
            
                if (0 <= checkX < 8) and (0 <= checkY < 8):
                    checkingTile = tiles[checkY][checkX]
                else:
                    break

                if checkingTile.occupied != 'none' and checkingTile.piece != None:
                    if direction == (-1, 0) or direction == (0, 1) or direction == (1, 0) or direction == (0, -1):
                        if checkingTile.piece.side != self.side:
                            if checkingTile.piece.type == 'queen' or checkingTile.piece.type == 'rook':
                                print(f"There is a {checkingTile.piece} at {checkingTile.colPos},{checkingTile.rowPos}")
                                self.check = True
                    elif direction == (-1, -1) or direction == (-1, 1) or direction == (1, 1) or direction == (1, -1):
                        if checkingTile.piece.side != self.side:
                            if checkingTile.piece.type == 'queen' or checkingTile.piece.type == 'bishop':
                                print(f"There is a {checkingTile.piece} at {checkingTile.colPos},{checkingTile.rowPos}")
                                self.check = True
                    else:
                        self.check = False
                    break
        
        for direction in knightDir:
            knightX, knightY = self.tile.colPos + direction[1], self.tile.rowPos + direction[0]

            if (0 <= knightX < 8) and (0 <= knightY < 8):
                checkingTile = tiles[knightY][knightX]
            else:
                break

            if checkingTile.occupied != 'none' and checkingTile.piece != None:
                    if direction in knightDir:
                        if checkingTile.piece.side != self.side and checkingTile.piece.type == 'knight':
                            print(f"There is a {checkingTile.piece} at {checkingTile.colPos},{checkingTile.rowPos}")
                            self.check = True

        for direction in pawnDir:
            if self.side == 'white':
                pawnX, pawnY = self.tile.colPos + direction[1], self.tile.rowPos + direction[0]  #(-1, -1), (-1, 1)
            elif self.side == 'black':
                pawnX, pawnY = self.tile.colPos - direction[1], self.tile.rowPos - direction[0]

            if (0 <= pawnX < 8) and (0 <= pawnY < 8):
                checkingTile = tiles[pawnY][pawnX]
            else:
                break

            if checkingTile.occupied != 'none' and checkingTile.piece != None:
                if checkingTile.piece.side != self.side and checkingTile.piece.type == 'pawn':
                    print(f"There is a {checkingTile.piece} at {checkingTile.colPos},{checkingTile.rowPos}")
                    self.check = True
    


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
pieces.append(Piece("wp1", tiles[6][0], 'white', 'pawn'))
pieces.append(Piece("wp2", tiles[6][1], 'white', 'pawn'))
pieces.append(Piece("wp3", tiles[6][2], 'white', 'pawn'))
pieces.append(Piece("wp4", tiles[6][3], 'white', 'pawn'))
pieces.append(Piece("wp5", tiles[6][4], 'white', 'pawn'))
pieces.append(Piece("wp6", tiles[6][5], 'white', 'pawn'))
pieces.append(Piece("wp7", tiles[6][6], 'white', 'pawn'))
pieces.append(Piece("wp8", tiles[6][7], 'white', 'pawn'))
pieces.append(Piece("wr1", tiles[7][0], 'white', 'rook'))
pieces.append(Piece("wn1", tiles[7][1], 'white', 'knight'))
pieces.append(Piece("wb1", tiles[7][2], 'white', 'bishop'))
pieces.append(Piece("wq", tiles[7][3], 'white', 'queen'))
pieces.append(Piece("wk", tiles[7][4], 'white', 'king'))
pieces.append(Piece("wb2", tiles[7][5], 'white', 'bishop'))
pieces.append(Piece("wn2", tiles[7][6], 'white', 'knight'))
pieces.append(Piece("wr2", tiles[7][7], 'white', 'rook'))

#black pieces
pieces.append(Piece("bp1", tiles[1][0], 'black', 'pawn'))
pieces.append(Piece("bp2", tiles[1][1], 'black', 'pawn'))
pieces.append(Piece("bp3", tiles[1][2], 'black', 'pawn'))
pieces.append(Piece("bp4", tiles[1][3], 'black', 'pawn'))
pieces.append(Piece("bp5", tiles[1][4], 'black', 'pawn'))
pieces.append(Piece("bp6", tiles[1][5], 'black', 'pawn'))
pieces.append(Piece("bp7", tiles[1][6], 'black', 'pawn'))
pieces.append(Piece("bp8", tiles[1][7], 'black', 'pawn'))
pieces.append(Piece("br1", tiles[0][0], 'black', 'rook'))
pieces.append(Piece("bn1", tiles[0][1], 'black', 'knight'))
pieces.append(Piece("bb1", tiles[0][2], 'black', 'bishop'))
pieces.append(Piece("bq", tiles[0][3], 'black', 'queen'))
pieces.append(Piece("bk", tiles[0][4], 'black', 'king'))
pieces.append(Piece("bp2", tiles[0][5], 'black', 'bishop'))
pieces.append(Piece("bn2", tiles[0][6], 'black', 'knight'))
pieces.append(Piece("br2", tiles[0][7], 'black', 'rook'))

running = True
selectedPiece = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #selects the piece that is being moved
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not selectedPiece:
                for piece in pieces:
                    if piece.rect.collidepoint(pygame.mouse.get_pos()):
                        selectedPiece = piece
                        break
        #check if you can move the piece there
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if selectedPiece:
                for row in tiles:
                    for tile in row:
                        if tile.rect.collidepoint(pygame.mouse.get_pos()) and tile.occupied == 'none':
                            selectedPiece.tile.occupied = 'none'
                            selectedPiece.tile.piece = 'none'
                            selectedPiece.updateTile(tile)
                            tile.piece = selectedPiece
                            tile.occupied = selectedPiece.side
                            break
                        else:
                            continue
                        break
                else:
                    selectedPiece.updateTile(selectedPiece.tile)
            selectedPiece = None

    screen.fill((0, 0, 0))

    #check for checks
    for piece in pieces:
        if piece.type == 'king':
            piece.checkCheck()
            if piece.check == True and piece.side == 'white':
                screen.fill((0, 0, 0), (0, 800, screen.get_width(), 900))
                checkText = font.render('You are in check', False, (255, 255, 255))
                checkRect = checkText.get_rect(center = (width//2, height-70))
            elif piece.check == False and piece.side == 'white':
                screen.fill((0, 0, 0), (0, 800, screen.get_width(), 900))
                checkText = font.render('You are not in check', False, (255, 255, 255))
                checkRect = checkText.get_rect(center = (width//2, height-70))

    #draws each tile onto the screen
    for row in tiles:
        for tile in row:
            tile.draw(screen)

    #draws each piece onto the screen
    for piece in pieces:
        piece.draw(screen)
        piece.tile.occupied = True

    #updates the selected piece to be at the mouse position
    ### NEED TO CHANGE THIS LATER SO THAT IT ALLOWS TO SELECT A PIECE WITHOUT DRAGGING IT
    if selectedPiece:
        mX, mY = pygame.mouse.get_pos()
        selectedPiece.movePiece(mX, mY)

    screen.blit(checkText, checkRect)

    pygame.display.flip()

pygame.quit()
sys.exit()