
# %%
import cProfile
from PIL import Image, ImageEnhance
import hashlib


def diffListOfInt(l1: list, l2: list) -> int:
    return sum(abs(i1 - i2) for i1, i2 in zip(l1, l2))


class Texel:
    def __init__(self, char: str, pixels: list, width: int, height: int):
        self.char = char
        self.pixels = pixels
        self.width = width
        self.height = height

    def rateFitnessOfPixels(self, pixels: list) -> float:
        mismatch = diffListOfInt(pixels, self.pixels)
        return 1.0 / (1 + mismatch)


class Texelator:
    def __init__(self):
        CHARS = """ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"""
        image: Image.Image = Image.open("./ascii.png").convert("L")
        self.charWidth = 7
        self.charHeight = 14

        self.texels = list()

        for i in range(len(CHARS)):
            chim = image.crop(
                (i*self.charWidth, 0, i*self.charWidth+self.charWidth, self.charHeight))
            pixels = list(chim.getdata(0))
            texel = Texel(CHARS[i], pixels,
                          width=chim.width, height=chim.height)
            self.texels.append(texel)

        # hash to resulting character
        self.cheatSheet: dict = {}

    def render(self, image: Image.Image, width: int, height: int) -> str:
        image2: Image.Image = image.resize((width * self.charWidth,
                                            height * self.charHeight))
        image2 = image2.convert("L")
        tileRows = []
        for y in range(height):
            tiles = []
            for x in range(width):
                tileBox = (
                    x*self.charWidth,
                    y*self.charHeight,
                    (x+1)*self.charWidth,
                    (y+1)*self.charHeight,
                )
                tile = image2.crop(tileBox).getdata(0)
                tiles.append(tile)
            tileRows.append(tiles)

        output: str = ""
        for tiles in tileRows:
            for tile in tiles:
                char = self.getFittest(tile)
                output += char
                print(char, end="")
            output += "\n"
            print("", end="\n")

        return output

    def getFittest(self, tile: Image.Image) -> str:
        hash = hashlib.md5(bytes(tile)).digest()
        if hash in self.cheatSheet:
            return self.cheatSheet[hash]

        fitnesses = [(tx.char, tx.rateFitnessOfPixels(tile))
                     for tx in self.texels]
        fitnesses.sort(key=lambda tx: tx[1])

        result = fitnesses.pop()[0]

        self.cheatSheet[hash] = result
        return result


# texelator = Texelator()
#
# width: int = 40
# height: int = 20
# filename: str = "../pokeball-color.png"
# filename: str = "../fiolin.jpg"
#
# image: Image.Image = Image.open(filename)
# cProfile.run("texelator.render(image, width, height)", "profile")

# %%


def renderImagesFromArgs(width, height):
    for filename in args.images:
        image: Image.Image = Image.open(filename)
        overlayImage: Image.Image = Image.new(image.mode, image.size, color=-1)
        preppedImage: Image.Image = Image.blend(image, overlayImage, 0.35)
        texelator.render(preppedImage, width, height)
        # output = texelator.render(image, width, height)
        # print(output)


if __name__ == "__main__":
    import argparse

    argparser = argparse.ArgumentParser()
    argparser.add_argument("-W", "--width", dest="width", default=80)
    argparser.add_argument("-H", "--height", dest="height", default=40)
    argparser.add_argument("images", nargs="+")
    args: argparse.Namespace = argparser.parse_args()

    texelator = Texelator()

    width: int = int(args.width)
    height: int = int(args.height)

    import cProfile
    cProfile.run("renderImagesFromArgs(width, height)", "profile")

else:
    pass


# %%
