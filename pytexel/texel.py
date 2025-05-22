# %%

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

# %%
