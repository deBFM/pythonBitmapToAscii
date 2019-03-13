def readBytes():
    file = open("mono.bmp", "rb", 0)
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

def getPixelArray(bytes):
    return bytes[getPixelArrayOffset(bytes):]  #TODO, die Länge stimmt wohl noch nicht, irgendwie muss ich die Länge greifen/berechnen

def printMetaData(bytes):
    print("Width:  " + str(getWidth(bytes)))
    print("Height: " + str(getHeight(bytes)))

#############################
# Format: BMP (Monochrome)  #
#############################
bytes = readBytes()
printMetaData(bytes)
pixels = getPixelArray(bytes)


#print(bin(pixels[0]))


