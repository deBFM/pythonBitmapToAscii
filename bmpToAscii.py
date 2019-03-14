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
    return bytes[getPixelArrayOffset(bytes):]  #TODO, die Länge stimmt wohl noch nicht, irgendwie muss ich die Länge greifen/berechnen

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
    pixels = []
    for byte in getPixelArrayBytes(bytes):
        for bit in bin(byte)[2:]:
            pixels.append(bit)
    # Ok now we have ['1', '1', '1', '0', '0', '0', '0', '0', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0']
    return sortPixelsByRow(pixels, getWidth(bytes))

def paint():
    pass

def printMetaData(bytes):
    print("Width:  " + str(getWidth(bytes)))
    print("Height: " + str(getHeight(bytes)))

#############################
# Format: BMP (Monochrome)  #
#############################
bytes = readBytes("monochrom10x2.bmp")
printMetaData(bytes)
pixels = getPixels(bytes)
paint(pixels)



#print(bin(pixels[0]))


