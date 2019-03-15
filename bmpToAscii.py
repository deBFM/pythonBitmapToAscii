import math
from argparse import ArgumentParser

def readBytes(fileName):
    #TODO as Context
    #TODO catch Exception
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
        rowBytes = pixelArrayBytes[(i * bytesPerRow):(i * bytesPerRow + bytesPerRow)]
        pixelRow = []
        for rowByte in rowBytes:
            for bit in bin(rowByte)[2:].rjust(8,"0"):
                pixelRow.append(bit)
        pixels.append(pixelRow[:getWidth(bytes)])
    return reversed(pixels)

def paint(pixels):
    for row in pixels:
        for pixel in row:
            if(pixel == "1"):
                print(" ", end="")
            else:
                print("\u25A0", end="")
        print()

def printMetaData(bytes, args):
    print("Size: {:>8d} x {:d}".format(getWidth(bytes), getHeight(bytes)))
    print(f"Filename: {args.file:>19}")

def arguments():
    parser = ArgumentParser(description="Prints monochrom bitmaps to the console",
                            epilog="Just a Python learning project of mine",
                            usage="Try %(prog)s --help"
                            )
    parser.add_argument("-v", help="verbose", action="store_true", dest="verbose")
    parser.add_argument("file", help="Bitmap filename")
    return parser.parse_args()


#############################
# Format: BMP (Monochrome)  #
#############################
#TODO Check for monochrome Bitmap (see Headers)
args = arguments()
bytes = readBytes(args.file)
if args.verbose:
    printMetaData(bytes, args)
paint(getPixels(bytes))