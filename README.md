# pytexel

pytexel is a Python library and set of utilities for rendering pixel graphics as ASCII text art.
It uses the actual bitmap shapes of characters to approximate the original pixel grid as closely as possible,
and supports both static image conversion and live terminal demos.

## Features

- Pixel-accurate ASCII art rendering using Pillow for image processing.
- Tile-based caching for fast repeated conversions using NumPy arrays.
- Command-line tools (`texelate.py` and `texelate.sh`) for quick one-off conversions.
- Python API via `Texelator` and `Texel` classes for integration into custom scripts.
- Live Pygame-based demos for animated ASCII output.
- Utilities for visualizing the ASCII glyph set and profiling performance.

## Installation

Requires Python 3.6+ and the following Python packages:

- [Pillow](https://pypi.org/project/Pillow/) (image processing)
- [pygame](https://pypi.org/project/pygame/) and [numpy](https://pypi.org/project/numpy/) (for demos)

Install pytexel as a library from PyPI or from source:

```bash
# Install the latest release from PyPI
pip install pytexel

# Or install from local source
git clone <repository-url>
cd pytexel
pip install .
```

## Quickstart

### Command-Line Usage

Convert images to ASCII art in your terminal:

```bash
python texelate.py -W <columns> -H <rows> image1.png [image2.jpg ...]
```

- `-W`, `--width`: number of character columns (default: 80)
- `-H`, `--height`: number of character rows (default: 40)

Alternatively, use the provided shell wrapper to match your terminal size:

```bash
bash texelate.sh image.png
```

Persistent dict-based caching has been replaced by in-memory NumPy arrays for faster conversions.

### Python API

Use `Texelator` directly in your own scripts:

```python
from texelator import Texelator
from PIL import Image

tex = Texelator()
img = Image.open("marie.png")
ascii_art = tex.render(img, width=80, height=40)
print(ascii_art)
```

## Demos

Two live demos using Pygame are included:

- `demo-pygame-line.py`: animated line drawing.
- `demo-pygame-bounce.py`: bouncing ball simulation.

Run them with:

```bash
python demo-pygame-line.py
python demo-pygame-bounce.py
```

Press Ctrl+C to exit.

## Utilities

- `ascii-glyphs.py`: generate `ascii.png` font atlas from a monospace TrueType font using Pillow.
- `ascii-print.py`: display the first 255 ASCII characters.
- `view-profile.py`: analyze and display profiling data from the last run (`profile` file).

## Resources and Files

- `ascii.png` / `ascii.xcf`: bitmap and GIMP source of character glyphs used for rendering (regenerate via `ascii-glyphs.py`).
- `ascii-glyphs.py`: programmatic generator for `ascii.png` using Pillow and a monospace font.
- `texel.py`, `texelator.py`: core library code defining `Texel` and `Texelator`.
- `texelate.py`, `texelate.sh`: command-line front ends.
- `demo-pygame-*.py`: live terminal animation demos.
- `ascii-print.py`: ASCII table utility.
- `view-profile.py`: performance profiling utility.
- Sample images (`marie.png`, `pokeball.png`, etc.) for testing.

## Customizing Glyphs

Edit `ascii.xcf` in GIMP and export to `ascii.png` to change the appearance of the rendered text art,
or regenerate `ascii.png` programmatically using `ascii-glyphs.py`.
