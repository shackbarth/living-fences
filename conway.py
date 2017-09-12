from PIL import Image, ImageDraw
from time import gmtime, strftime
import picamera
camera = picamera.PiCamera()
camera.resolution = (1920, 1200)

# CALIBRATION
gridWidth = 38 # actually one less than you would think
gridHeight = 33 # actually one less than you would think
topLeftX = 460 
topLeftY = 220
topRightX = 1250
topRightY = 250
bottomLeftX = 430
bottomLeftY = 1065
bottomRightX = 1225
bottomRightY = 1070

def isPixelYellow (r, g, b):
  return r > 160 and g > 160 and r + g >= b * 2


def isYellow (pix, xPixel, yPixel):
  yellowCount = 0
  for x in range(7):
    for y in range(7):
      r, g, b = pix[xPixel + x - 3, yPixel + y - 3]
      if isPixelYellow(r, g, b):
        yellowCount = yellowCount + 1
  return yellowCount > 10 

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

  if livingCellCount == 0:
    i = 16
    offset = -2
    nextBoard[i + offset][i] = 1
    i = i + 1
    nextBoard[i + offset][i] = 1
    i = i + 1
    nextBoard[i + offset][i] = 1
    i = i + 1
    nextBoard[i + offset][i] = 1
    i = i + 1
    nextBoard[i + offset][i] = 1
    i = i + 1
    nextBoard[i + offset][i] = 1
    i = i + 1
    nextBoard[i + offset][i] = 1
    i = i + 1
    nextBoard[i + offset][i] = 1

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

def processPicture(): 
  camera.capture("conway-raw.jpg")
  im = Image.open("conway-raw.jpg")
  im = im.transpose(Image.ROTATE_180)
  pix = im.load()
    
  draw = ImageDraw.Draw(im)

  currentBoard = [[0 for x in range(gridWidth + 1)] for y in range(gridHeight + 1)]

  for xIndex in range(0, gridWidth + 1):
    for yIndex in range(0, gridHeight + 1):
      if xIndex % 2 is yIndex % 2:
        [xPixel, yPixel] = indicesToPixels(xIndex, yIndex)
        if isYellow(pix, xPixel, yPixel):
          currentBoard[yIndex][xIndex] = 1
          draw.ellipse((xPixel - 15, yPixel - 15, xPixel + 15, yPixel + 15), fill=(80,60,60,255))
          draw.ellipse((xPixel - 2, yPixel - 2, xPixel + 2, yPixel + 2), fill=(255,0,0,255))
        else: 
          currentBoard[yIndex][xIndex] = 0
          draw.ellipse((xPixel - 2, yPixel - 2, xPixel + 2, yPixel + 2), fill=(255,0,0,255))
       
  #print("Current Board:")
  #for row in currentBoard:
  #  print("".join(map(toArt, row)))

  nextBoard = getNextBoard(currentBoard)
  #print("Next Board:")
  #for row in nextBoard:
  #  print("".join(map(toArt, row)))
  for xIndex in range(0, gridWidth + 1):
    for yIndex in range(0, gridHeight + 1):
      if xIndex % 2 is yIndex % 2:
        [xPixel, yPixel] = indicesToPixels(xIndex, yIndex)
        if nextBoard[yIndex][xIndex] == 1:
          draw.ellipse((xPixel - 15, yPixel - 15, xPixel + 15, yPixel + 15), fill=(255,255,0,255))
        
  draw.ellipse((topLeftX - 5, topLeftY - 5, topLeftX + 5, topLeftY + 5), fill=(0,255,0,255))
  draw.ellipse((topRightX - 5, topRightY - 5, topRightX + 5, topRightY + 5), fill=(0,255,0,255))
  draw.ellipse((bottomLeftX - 5, bottomLeftY - 5, bottomLeftX + 5, bottomLeftY + 5), fill=(0,255,0,255))
  draw.ellipse((bottomRightX - 5, bottomRightY - 5, bottomRightX + 5, bottomRightY + 5), fill=(0,255,0,255))

  im = im.rotate(2)
  im = im.crop((topLeftX - 50, topLeftY - 50, bottomRightX + 100, bottomRightY + 50))
  im.save("www/conway.jpg")

  currentStateFile = open("current-state.txt", "r") 
  currentStateText = currentStateFile.read()
  if str(currentStateText) != str(currentBoard):
    print("state has changed")
    timestamp = strftime("%Y-%m-%d-%H-%M-%S", gmtime())
    im.save("www/archive-" + timestamp + ".jpg")
  else: 
    print("state has not changed")
  currentStateFile.close()
 
  currentStateFile = open("current-state.txt", "w")
  currentStateFile.write(str(currentBoard))
  currentStateFile.close()
 
processPicture()  

