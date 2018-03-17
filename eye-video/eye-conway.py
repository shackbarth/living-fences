from PIL import Image, ImageDraw
from random import *

# CALIBRATION
gridWidth = 19 # actually one less than you would think
gridHeight = 35 # actually one less than you would think
topLeftX = 10
topLeftY = 10
topRightX = 2800
topRightY = 10
bottomLeftX = 10
bottomLeftY = 6000
bottomRightX = 2800
bottomRightY = 6000

def toArt (i):
  if i == 0:
    return " "
  else:
    return "X"

def getNeighbors (x, y):
  neighbors = []
  if x > 1:
    neighbors.append([x - 2, y])
  if x > 0 and y > 0:
    neighbors.append([x - 1, y - 1])
  if y > 1:
    neighbors.append([x, y - 2])
  if x < gridWidth and y > 0:
    neighbors.append([x + 1, y - 1])
  if x + 1 < gridWidth:
    neighbors.append([x + 2, y])
  if x < gridWidth and y < gridHeight:
    neighbors.append([x + 1, y + 1])
  if y + 1 < gridHeight:
    neighbors.append([x, y + 2])
  if x > 0 and y < gridHeight:
    neighbors.append([x - 1, y + 1])
  return neighbors

def countLivingNeighbors (currentBoard, neighbors):
  count = 0
  for neighbor in neighbors:
    neighborX = neighbor[0]
    neighborY = neighbor[1]
    count += currentBoard[neighborY][neighborX]
  return count

def getNextBoard (currentBoard):
  nextBoard = [[0 for x in range(gridWidth + 1)] for y in range(gridHeight + 1)]
  livingCellCount = 0
  for xIndex in range(0, gridWidth + 1):
    for yIndex in range(0, gridHeight + 1):
      if xIndex % 2 != yIndex % 2:
        continue
      livingCellCount = livingCellCount + currentBoard[yIndex][xIndex]
      neighbors = getNeighbors(xIndex, yIndex)
      livingNeighborCount = countLivingNeighbors(currentBoard, neighbors)
      if livingNeighborCount < 2 or livingNeighborCount > 3:
        continue
      if livingNeighborCount == 2 and currentBoard[yIndex][xIndex] == 0:
        continue
      nextBoard[yIndex][xIndex] = 1
  return nextBoard

xExpansion = (bottomRightX - bottomLeftX) / (topRightX - topLeftX)
xExpansionPerRow = (xExpansion - 1) / gridHeight
xShiftPerRow = (bottomLeftX - topLeftX) / gridHeight
yExpansion = (bottomRightY - topRightY) / (bottomLeftY - topLeftY)
yExpansionPerRow = (yExpansion - 1) / gridWidth
yShiftPerRow = (topRightY - topLeftY) / gridHeight

def indicesToPixels (xIndex, yIndex):
  xExpansionFactor = 1 + xExpansionPerRow * yIndex
  xShiftFactor = xShiftPerRow * yIndex
  yExpansionFactor = 1 + yExpansionPerRow * xIndex
  yShiftFactor = yShiftPerRow * xIndex
  xPixel = topLeftX + xShiftFactor + ((topRightX - topLeftX) * xIndex / gridWidth) * xExpansionFactor
  yPixel = topLeftY + yShiftFactor + ((bottomLeftY - topLeftY) * yIndex / gridHeight) * yExpansionFactor
  return [xPixel, yPixel]



im = Image.open("./ChainLink.jpg").convert("RGBA")
openEye1 = Image.open("1.png").convert("RGBA")
openEye1 = openEye1.resize((200, 200), Image.ANTIALIAS)
openEye2 = Image.open("2.png").convert("RGBA")
openEye2 = openEye2.resize((200, 200), Image.ANTIALIAS)
openEye3 = Image.open("3.png").convert("RGBA")
openEye3 = openEye3.resize((200, 200), Image.ANTIALIAS)
openEye4 = Image.open("4.png").convert("RGBA")
openEye4 = openEye4.resize((200, 200), Image.ANTIALIAS)
openEye5 = Image.open("5.png").convert("RGBA")
openEye5 = openEye5.resize((200, 200), Image.ANTIALIAS)
closedEye = Image.open("6dot.png").convert("RGBA")

closedEye = closedEye.resize((200, 200), Image.ANTIALIAS)

def processPicture(currentBoard):
  for xIndex in range(0, gridWidth + 1):
    for yIndex in range(0, gridHeight + 1):
      if xIndex % 2 is yIndex % 2:
        [xPixel, yPixel] = indicesToPixels(xIndex, yIndex)

        if currentBoard[yIndex][xIndex] == 1:
          randomInt = randint(1, 5)
          if (randomInt == 1):
            im.paste(openEye1, (int(xPixel) - 100, int(yPixel) - 100), openEye1)
          if (randomInt == 2):
            im.paste(openEye2, (int(xPixel) - 100, int(yPixel) - 100), openEye2)
          if (randomInt == 3):
            im.paste(openEye3, (int(xPixel) - 100, int(yPixel) - 100), openEye3)
          if (randomInt == 4):
            im.paste(openEye4, (int(xPixel) - 100, int(yPixel) - 100), openEye4)
          if (randomInt == 5):
            im.paste(openEye5, (int(xPixel) - 100, int(yPixel) - 100), openEye5)
        else:
          im.paste(closedEye, (int(xPixel) - 100, int(yPixel) - 100), closedEye)
  return im

def makeVideo():
  currentBoard = [[0 for x in range(gridWidth + 1)] for y in range(gridHeight + 1)]
  for i in range(4, 12):
    currentBoard[i - 2][i] = 1

  print("Board:")
  for row in currentBoard:
    print("".join(map(toArt, row)))

  for index in range(0, 10):
    im = processPicture(currentBoard);
    im.save("output" + str(index).rjust(5, "0") + ".png")
    currentBoard = getNextBoard(currentBoard)
    print("Board:")
    for row in currentBoard:
      print("".join(map(toArt, row)))

makeVideo()

# $ ffmpeg -i output%05d.png -vcodec gif -y conway-eye.gif
