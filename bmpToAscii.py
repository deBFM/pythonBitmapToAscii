import sys
import math
from argparse import ArgumentParser

def readFile(fileName):
    try:
        with open(fileName, "rb", 0) as file:
            bytes = file.read(-1)
    except FileNotFoundError as e:
        sys.exit(f"File '{fileName}' not found")
    return bytes

def getPixelArrayOffset(bytes):
    """
    :param bytes: whole image data
    :return: the position where the pixelArrayBytes starts
    """
    return int.from_bytes(bytes[0x0a:0x0e], 'little')

def getWidth(bytes):
    """
    :param bytes: whole image data
    :return: the width of the image
    """
    return int.from_bytes(bytes[0x12:0x16], 'little')

def getHeight(bytes):
    """
    :param bytes: whole image data
    :return: the height of the image
    """
    return int.from_bytes(bytes[0x16:0x1a], 'little')

def getPixelArrayBytes(bytes):
    """
    :param bytes: whole image data
    :return: raw section (bytes) of the image which contains the pixels
    """
    return bytes[getPixelArrayOffset(bytes):]

def getPixels(bytes):
    """
    :param bytes: whole image data
    :return: 2 dimensonal list of pixels
    """
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
    """
    Paints the pixels to the console
    :param pixels: 2 dimensional list with pixeldata
    """
    for row in pixels:
        for pixel in row:
            char = " " if (pixel == "1") else "\u25A0"
            print(char, end="")
        print()

def printMetaData(bytes, args):
    print("Size:\t\t{} x {:d}".format(getWidth(bytes), getHeight(bytes)))
    print(f"Filename:\t{args.file}")

def arguments():
    parser = ArgumentParser(description="Prints monochrom bitmaps to the console",
                            epilog="Just a Python learning project of mine",
                            usage="Try %(prog)s --help"
                            )
    parser.add_argument("-v", help="verbose", action="store_true", dest="verbose")
    parser.add_argument("file", help="Bitmap filename")
    return parser.parse_args()

def checkFormat(bytes):
    if not (bytes[0x00] == ord("B") and bytes[0x01] == ord("M")):
        sys.exit("Error: This is not a bitmap file")
    if not (bytes[0x1c] == 1):
        sys.exit("Error: Only monochrom bitmaps are supported yet")


args = arguments()
fileData = readFile(args.file)
checkFormat(fileData)
if args.verbose:
    printMetaData(fileData, args)
paint(getPixels(fileData))