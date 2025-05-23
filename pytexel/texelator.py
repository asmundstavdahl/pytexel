
# %%
from PIL import Image, ImageEnhance
try:
    import numpy as np
except ImportError:
    np = None

from .texel import Texel

import pathlib
thidDir = pathlib.Path(__file__).parent.absolute()

# Characters used for ASCII rendering
CHARS = r""" !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"""


class Texelator:
    def __init__(self):

        image: Image.Image = Image.open(f"{thidDir}/ascii.png").convert("L")
        # Determine character cell size from the ascii.png glyph atlas
        self.charWidth = image.width // len(CHARS)
        self.charHeight = image.height

        self.texels = list()

        for i in range(len(CHARS)):
            chim = image.crop(
                (i*self.charWidth, 0, i*self.charWidth+self.charWidth, self.charHeight))
            pixels = list(chim.getdata(0))
            texel = Texel(CHARS[i], pixels,
                          width=chim.width, height=chim.height)
            self.texels.append(texel)

        if np is not None:
            self._texel_pixels = np.array([t.pixels for t in self.texels], dtype=np.int16)
            self._texel_chars = [t.char for t in self.texels]
        # cache for mapping tile patterns to characters
        self.tileCache: dict = self.loadTileCache()

    def render(self, image: Image.Image, width: int, height: int) -> str:
        image2 = image.resize((width * self.charWidth, height * self.charHeight))
        image2 = image2.convert("L")
        if np is not None:
            arr = np.asarray(image2, dtype=np.int16)
            arr = arr.reshape((height, self.charHeight, width, self.charWidth))
            arr = arr.transpose(0, 2, 1, 3)
            arr = arr.reshape((height, width, self.charHeight * self.charWidth))
            lines = []
            for row in arr:
                diff = np.abs(row[:, None, :] - self._texel_pixels[None, :, :])
                costs = diff.sum(axis=2)
                best = np.argmin(costs, axis=1)
                lines.append(''.join(self._texel_chars[idx] for idx in best))
            return '\n'.join(lines)

        lines = []
        for y in range(height):
            line_chars = []
            for x in range(width):
                tileBox = (
                    x * self.charWidth,
                    y * self.charHeight,
                    (x + 1) * self.charWidth,
                    (y + 1) * self.charHeight,
                )
                tile = image2.crop(tileBox).getdata(0)
                line_chars.append(self.getFittest(tile))
            lines.append(''.join(line_chars))
        return '\n'.join(lines)

    def getFittest(self, tile) -> str:
        key = bytes(tile)
        if key in self.tileCache:
            return self.tileCache[key]

        best = max(self.texels, key=lambda tx: tx.rateFitnessOfPixels(tile))
        result = best.char
        self.tileCache[key] = result
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
