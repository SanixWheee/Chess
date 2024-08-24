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



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    for row in tiles:
        for tile in row:
            tile.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()