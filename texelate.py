
# %%
import cProfile
from PIL import Image, ImageEnhance

from texelator import Texelator


def renderImagesFromArgs(width, height):
    first = True

    for filename in args.images:
        image: Image.Image = Image.open(filename)
        overlayImage: Image.Image = Image.new(image.mode, image.size, color=-1)
        preppedImage: Image.Image = Image.blend(image, overlayImage, 0.35)
        output = texelator.render(preppedImage, width, height)

        if not first:
            print(f"\x1b[{height+1}A", end="")

        print(output)
        first = False


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

    texelator.saveTileCache()

else:
    pass
