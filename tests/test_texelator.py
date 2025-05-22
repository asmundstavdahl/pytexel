import unittest
from unittest.mock import patch, mock_open, MagicMock
import hashlib
import pickle
import pathlib

from PIL import Image # For type hinting and creating dummy images

from pytexel.texelator import Texelator
from pytexel.texel import Texel

# Use dynamic import for CHARS constant
from pytexel.texelator import CHARS as TEXELATOR_CHARS

CHAR_WIDTH = 7
CHAR_HEIGHT = 14

class TestTexelator(unittest.TestCase):

    def _get_mock_pil_image_for_ascii_png(self):
        mock_image = MagicMock(spec=Image.Image)
        mock_image.width = len(TEXELATOR_CHARS) * CHAR_WIDTH
        mock_image.height = CHAR_HEIGHT
        mock_image.convert.return_value = mock_image

        self.space_char_index = TEXELATOR_CHARS.find(' ')
        self.A_char_index = TEXELATOR_CHARS.find('A')
        
        self.space_pixels = tuple([0] * (CHAR_WIDTH * CHAR_HEIGHT))  # All black for space
        self.A_pixels = tuple([255] * (CHAR_WIDTH * CHAR_HEIGHT)) # All white for 'A'

        def mock_crop_getdata_for_ascii(box):
            mock_cropped_image = MagicMock(spec=Image.Image)
            mock_cropped_image.width = box[2] - box[0]
            mock_cropped_image.height = box[3] - box[1]
            
            char_index_from_box = box[0] // CHAR_WIDTH

            if char_index_from_box == self.space_char_index:
                mock_cropped_image.getdata.return_value = self.space_pixels
            elif char_index_from_box == self.A_char_index:
                mock_cropped_image.getdata.return_value = self.A_pixels
            else:
                num_pixels_in_char = CHAR_WIDTH * CHAR_HEIGHT
                default_pixels = [100] + [50] * (num_pixels_in_char -1) # A distinct default pattern
                mock_cropped_image.getdata.return_value = tuple(default_pixels)
            return mock_cropped_image

        mock_image.crop.side_effect = mock_crop_getdata_for_ascii
        return mock_image

    @patch('pytexel.texelator.Image.open')
    @patch('pytexel.texelator.Texelator.loadTileCache', return_value={}) # Start with empty cache
    def setUp(self, mock_load_cache, mock_image_open_ascii):
        self.mock_ascii_pil_image = self._get_mock_pil_image_for_ascii_png()
        mock_image_open_ascii.return_value = self.mock_ascii_pil_image
        
        self.texelator = Texelator()
        
        # Use pathlib to get the texelator.py's directory for ascii.png path construction
        texelator_module_path = pathlib.Path(Texelator.__module__.replace('.', '/') + '.py')
        if not texelator_module_path.exists(): # Fallback for different execution contexts
            texelator_module_path = pathlib.Path(self.texelator.__class__.__module__.replace('.', '/') + '.py')
        
        try:
            # This expects pytexel/texelator.py structure
            path_to_texelator_dir = pathlib.Path(__file__).parent.parent / "pytexel" 
            if not (path_to_texelator_dir / "texelator.py").exists(): # try another common structure
                 path_to_texelator_dir = pathlib.Path(Texelator.__file__).parent.absolute()
            expected_ascii_path = str(path_to_texelator_dir / "ascii.png")
        except (AttributeError, TypeError):
            # Fallback if __file__ is not available or Texelator.__file__ fails
                        base_dir = pathlib.Path(__file__).parent.parent  # Assumes tests/ is sibling to pytexel/