import unittest
from PIL import Image
from pytexel.texelator import Texelator


class TestImageGeneration(unittest.TestCase):
    def test_half_black_white_horizontal(self):
        width, height = 3, 2
        img = Image.new('L', (width, height))
        pixel_values = [255] * width + [0] * width
        img.putdata(pixel_values)

        tex = Texelator()
        output = tex.render(img, width, height)

        expected_lines = [
            ' ' * width,
            '█' * width,
        ]
        self.assertEqual(output.splitlines(), expected_lines)