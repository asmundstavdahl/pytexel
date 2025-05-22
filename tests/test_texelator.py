import unittest
from unittest.mock import patch, mock_open, MagicMock
import hashlib
import pickle
import pathlib

from PIL import Image # For type hinting and creating dummy images

from pytexel.texelator import Texelator
from pytexel.texel import Texel

# The actual CHARS string from Texelator's __init__
# This must be kept in sync if Texelator.py changes its CHARS constant
TEXELATOR_CHARS = r""" !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\ VFX_भ_ aggiunto_ VFX_भ_ aggiunto_ VFX_भ_ aggiunto_ VFX_भ_ aggiunto_ VFX_भ_ aggiunto_ VFX_भ_ aggiunto_ VFX_भ_ aggiunto_ VFX_भ_ aggiunto_ VFX_भ_ aggiunto_ VFX_भ_ aggiunto_ VFX_भ_ aggiunto_ VFX_भ_ aggiunto_ VFX_भ_ aggiunto_ VFX_भ_ aggiunto_ VFX_भ_ aggiunto_ VFX_भ_ aggiunto_ VFX_भ_ aggiunto_ VFX_भ_ aggiunto_ VFX_भ_ aggiunto_ VFX_भ_ aggiunto_]^_`abcdefghijklmnopqrstuvwxyz{|}~"""
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
            base_dir = pathlib.Path_ VFX_भ_ aggiunto_ VFX_भ_ aggiunto_ VFX_भ_ aggiunto_ VFX_भ_ aggiunto_ VFX_भ_ aggiunto_ VFX_भ_ aggiunto_ VFX_भ_ aggiunto_ VFX_भ_ aggiunto_ VFX_भ_ aggiunto_ VFX_भ_ aggiunto_ VFX_भ_ aggiunto_ VFX_भ_ aggiunto_ VFX_भ_ aggiunto_ VFX_भ_ aggiunto_ VFX_भ_ aggiunto_ VFX_भ_ aggiunto_ VFX_भ_ aggiunto_ VFX_भ_ aggiunto_ VFX_भ_ aggiunto_ VFX_भ_ aggiunto_(__file__).parent.parent # Assumes tests/ is sibling to pytexel/
            expected_ascii_path = str(base_dir / "pytexel" / "ascii.png")

        mock_image_open_ascii.assert_called_once_with(expected_ascii_path)

    def test_initialization(self):
        self.assertEqual(self.texelator.charWidth, CHAR_WIDTH)
        self.assertEqual(self.texelator.charHeight, CHAR_HEIGHT)
        self.assertEqual(len(self.texelator.texels), len(TEXELATOR_CHARS))
        
        if self.space_char_index != -1 and self.space_char_index < len(self.texelator.texels):
             self.assertEqual(self.texelator.texels[self.space_char_index].char, ' ')
             self.assertEqual(list(self.texelator.texels[self.space_char_index].pixels), list(self.space_pixels))
        if self.A_char_index != -1 and self.A_char_index < len(self.texelator.texels):
             self.assertEqual(self.texelator.texels[self.A_char_index].char, 'A')
             self.assertEqual(list(self.texelator.texels[self.A_char_index].pixels), list(self.A_pixels))

        self.assertEqual(self.texelator.tileCache, {})

    def test_render_simple(self):
        dummy_input_pil_image = MagicMock(spec=Image.Image)
        resized_mock_image = MagicMock(spec=Image.Image)
        converted_mock_image = MagicMock(spec=Image.Image)

        dummy_input_pil_image.resize.return_value = resized_mock_image
        resized_mock_image.convert.return_value = converted_mock_image
        
        def mock_crop_getdata_render(box):
            cropped_tile_mock = MagicMock(spec=Image.Image)
            if box == (0, 0, CHAR_WIDTH, CHAR_HEIGHT): 
                cropped_tile_mock.getdata.return_value = self.space_pixels 
            elif box == (CHAR_WIDTH, 0, 2 * CHAR_WIDTH, CHAR_HEIGHT):
                cropped_tile_mock.getdata.return_value = self.A_pixels
            else:
                raise ValueError(f"Unexpected crop box during render: {box}")
            return cropped_tile_mock

        converted_mock_image.crop.side_effect = mock_crop_getdata_render
        
        output = self.texelator.render(dummy_input_pil_image, width=2, height=1)
        
        dummy_input_pil_image.resize.assert_called_once_with((2 * CHAR_WIDTH, 1 * CHAR_HEIGHT))
        resized_mock_image.convert.assert_called_once_with("L")
        self.assertEqual(converted_mock_image.crop.call_count, 2)
        self.assertEqual(output, " A\n")

    def test_get_fittest_new_tile(self):
        tile_data = self.space_pixels 
        expected_char = ' '
        
        tile_hash = hashlib.md5(bytes(tile_data)).digest()
        if tile_hash in self.texelator.tileCache:
            del self.texelator.tileCache[tile_hash]

        char = self.texelator.getFittest(tile_data)
        self.assertEqual(char, expected_char)
        self.assertIn(tile_hash, self.texelator.tileCache)
        self.assertEqual(self.texelator.tileCache[tile_hash], expected_char)

    def test_get_fittest_cached_tile(self):
        tile_data = self.A_pixels 
        expected_char = 'A'
        tile_hash = hashlib.md5(bytes(tile_data)).digest()
        
        self.texelator.tileCache[tile_hash] = expected_char
        
        with patch.object(Texel, 'rateFitnessOfPixels') as mock_rate_fitness:
            char = self.texelator.getFittest(tile_data)
            self.assertEqual(char, expected_char)
            mock_rate_fitness.assert_not_called()

    @patch('builtins.open', new_callable=mock_open)
    @patch('pickle.dump')
    def test_save_tile_cache(self, mock_pickle_dump, mock_file_open):
        self.texelator.tileCache = {"testhash": "X"}
        self.texelator.saveTileCache()

        mock_file_open.assert_called_once_with("tileCache.pkl", "wb")
        mock_pickle_dump.assert_called_once_with({"testhash": "X"}, mock_file_open())
        mock_file_open().close.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    @patch('pickle.load')
    def test_load_tile_cache_exists(self, mock_pickle_load, mock_file_open):
        expected_cache_data = {"testhash_loaded": "Y"}
        mock_pickle_load.return_value = expected_cache_data
        
        # Create a new Texelator instance without __init__ for isolated test METHOD
        tex = Texelator.__new__(Texelator)
        tex.tileCache = {} # Explicitly initialize needed attribute

        loaded_cache = tex.loadTileCache()
        
        mock_file_open.assert_called_once_with("tileCache.pkl", "rb")
        mock_pickle_load.assert_called_once_with(mock_file_open())
        self.assertEqual(loaded_cache, expected_cache_data)

    @patch('builtins.open', side_effect=FileNotFoundError)
    @patch('builtins.print') 
    def test_load_tile_cache_not_found(self, mock_print, mock_file_open_notfound):
        tex = Texelator.__new__(Texelator)
        tex.tileCache = {}

        loaded_cache = tex.loadTileCache()
        
        mock_file_open_notfound.assert_called_once_with("tileCache.pkl", "rb")
        mock_print.assert_called_with("tileCache.pkl not found - starting clean")
        self.assertEqual(loaded_cache, {})

if __name__ == '__main__':
    unittest.main()
