
# %%
import cProfile
from PIL import Image
from pytexel.texelator import Texelator


def renderImagesFromArgs(texelator_instance, cli_args, width, height):
    first = True

    for filename in cli_args.images:
        image: Image.Image = Image.open(filename)
        overlayImage: Image.Image = Image.new(image.mode, image.size, color=-1)
        preppedImage: Image.Image = Image.blend(image, overlayImage, 0.35)
        output = texelator_instance.render(preppedImage, width, height)

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
    args_ns: argparse.Namespace = argparser.parse_args()

    texelator_main = Texelator()

    width_main: int = int(args_ns.width)
    height_main: int = int(args_ns.height)

    import cProfile
    cProfile.run('renderImagesFromArgs(texelator_main, args_ns, width_main, height_main)', "profile")

    texelator_main.saveTileCache()

else:
    pass
