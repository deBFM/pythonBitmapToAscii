import math

def readBytes(fileName):
    file = open(fileName, "rb", 0)
    bytes = file.read(-1)
    file.close()
    return bytes


def getPixelArrayOffset(bytes):
    """
    PixelArrayOffset: 0x0A (4Bytes)
    """
    return int.from_bytes(bytes[0x0a:0x0e], 'little')


def getWidth(bytes):
    """
    Width:  0x12 (4Bytes)
    """
    return int.from_bytes(bytes[0x12:0x16], 'little')


def getHeight(bytes):
    """
    Height: 0x16 (4Bytes)
    """
    return int.from_bytes(bytes[0x16:0x1a], 'little')

def getPixelArrayBytes(bytes):
    return bytes[getPixelArrayOffset(bytes):]

#Obsolete Funktion
def sortPixelsByRow(pixels, rowLength):
    rows = []
    row = []
    count = 1
    for pixel in pixels:
        row.append(pixel)
        if count % rowLength == 0:
            rows.append(row)
            row = []
        count += 1
    return rows

def getPixels(bytes):
    #Todo: Die Bits werden Zeilenweise geschrieben. Eine neue Zeile fängt mit einem neuen Byte an.
    #      Wieviele Bytes eine Zeile hat, ergibt sich aus der width des Bildes!
    #      Bytes kommen nur in 4er Sequenzen vor (4Bytes, 8Bytes, 12 Bytes ...)
    #      Bsp.: Width 10 => 4 Bytes | (RoundUp(10 / 8)) = 2  -> 4er Byte Blocks: RoundUp(2/4) * 4 = 4
    #            Width 30 => 4 Bytes | (RoundUp(30 / 8)  = 4  -> 4er Byte Blocks: RoundUp(4/4) * 4 = 4
    #            Width 33 => 8 Bytes | (RoundUp(33 / 8)  = 5  -> 4er Byte Blocks: RoundUp(5/4) * 4 = 8
    pixels = []
    requiredBytesPerRow = math.ceil(getWidth(bytes) / 8)
    bytesPerRow = math.ceil(requiredBytesPerRow / 4) * 4
    rowCount = getHeight(bytes)
    pixelArrayBytes = getPixelArrayBytes(bytes)
    for i in range(0, rowCount):
        sliceStart = (i * bytesPerRow)
        sliceStop = sliceStart + bytesPerRow
        rowBytes = pixelArrayBytes[sliceStart:sliceStop]
        pixelRow = []
        for rowByte in rowBytes:
            for bit in bin(rowByte)[2:].rjust(8,"0"):
                pixelRow.append(bit)
        pixels.append(pixelRow[:getWidth(bytes)])
    pixels = reversed(pixels)
    return pixels

def paint(pixels):
    for row in pixels:
        for pixel in row:
            if(pixel == "1"):
                print("\u25a1", end="") #White square
            else:
                print("\u2b1b", end="") #Black square
        print()

def printMetaData(bytes):
    print("Size: " + str(getWidth(bytes)) + " x " + str(getHeight(bytes)))


#############################
# Format: BMP (Monochrome)  #
#############################
#TODO Check for monochrome Bitmap (see Headers)
bytes = readBytes("monochromHelloWorld.bmp")
printMetaData(bytes)
pixels = getPixels(bytes)
paint(pixels)

