
# %%
from PIL import Image, ImageEnhance
import hashlib

from .texel import Texel

import pathlib
thidDir = pathlib.Path(__file__).parent.absolute()


class Texelator:
    def __init__(self):
        CHARS = r""" !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"""
        image: Image.Image = Image.open(f"{thidDir}/ascii.png").convert("L")
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
        self.tileCache: dict = self.loadTileCache()

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
            output += "\n"

        return output

    def getFittest(self, tile: Image.Image) -> str:
        hash = hashlib.md5(bytes(tile)).digest()
        if hash in self.tileCache:
            return self.tileCache[hash]

        fitnesses = [(tx.char, tx.rateFitnessOfPixels(tile))
                     for tx in self.texels]
        fitnesses.sort(key=lambda tx: tx[1])

        result = fitnesses.pop()[0]

        self.tileCache[hash] = result
        return result

    def saveTileCache(self):
        with open("tileCache.pkl", "wb") as f:
            import pickle
            pickle.dump(self.tileCache, f)
            f.close()

    def loadTileCache(self) -> dict:
        try:
            with open("tileCache.pkl", "rb") as f:
                import pickle
                return pickle.load(f)
        except FileNotFoundError:
            print("tileCache.pkl not found - starting clean")
            return {}
