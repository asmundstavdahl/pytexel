import unittest
from pytexel.texel import Texel, diffListOfInt

class TestDiffListOfInt(unittest.TestCase):
    def test_empty_lists(self):
        self.assertEqual(diffListOfInt([], []), 0)

    def test_identical_lists(self):
        self.assertEqual(diffListOfInt([1, 2, 3], [1, 2, 3]), 0)

    def test_different_lists(self):
        self.assertEqual(diffListOfInt([1, 2, 3], [1, 3, 5]), 3) # 0 + 1 + 2

    def test_negative_numbers(self):
        self.assertEqual(diffListOfInt([-1, -2, 0], [-1, 2, 3]), 7) # 0 + 4 + 3

    def test_mixed_sign_numbers(self):
        self.assertEqual(diffListOfInt([10, -5, 0], [5, 5, -5]), 20) # 5 + 10 + 5

    def test_lists_of_different_lengths(self):
        # zip stops at the shortest list
        self.assertEqual(diffListOfInt([1, 2, 3, 4], [1, 2, 3]), 0)
        self.assertEqual(diffListOfInt([1, 2, 3], [1, 2, 3, 4]), 0)


class TestTexel(unittest.TestCase):
    def setUp(self):
        self.char = 'A'
        self.pixels = [10, 20, 30] * 3 # 9 pixels: [10,20,30,10,20,30,10,20,30]
        self.width = 3
        self.height = 3
        self.texel = Texel(self.char, self.pixels, self.width, self.height)

    def test_texel_creation(self):
        self.assertEqual(self.texel.char, self.char)
        self.assertEqual(self.texel.pixels, self.pixels)
        self.assertEqual(self.texel.width, self.width)
        self.assertEqual(self.texel.height, self.height)

    def test_rate_fitness_perfect_match(self):
        # Perfect match, mismatch = 0, fitness = 1.0 / (1+0) = 1.0
        target_pixels = self.pixels[:]
        self.assertEqual(self.texel.rateFitnessOfPixels(target_pixels), 1.0)

    def test_rate_fitness_some_mismatch(self):
        target_pixels = [11, 22, 33, 11, 22, 33, 11, 22, 33]
        # diff for one set [10,20,30] vs [11,22,33] is 1+2+3 = 6. Repeated 3 times = 18.
        # fitness = 1.0 / (1 + 18) = 1.0 / 19
        expected_fitness = 1.0 / (1 + sum(abs(p1-p2) for p1,p2 in zip(self.pixels, target_pixels)))
        self.assertAlmostEqual(self.texel.rateFitnessOfPixels(target_pixels), expected_fitness)
        self.assertAlmostEqual(self.texel.rateFitnessOfPixels(target_pixels), 1.0 / 19.0)

    def test_rate_fitness_total_mismatch_example(self):
        texel_pixels = [0, 0, 0, 0]
        texel = Texel('X', texel_pixels, 2, 2)
        target_pixels = [255, 255, 255, 255]
        # Expected mismatch = 255*4 = 1020
        # Expected fitness = 1.0 / (1 + 1020) = 1.0 / 1021
        expected_fitness = 1.0 / (1 + 1020)
        self.assertAlmostEqual(texel.rateFitnessOfPixels(target_pixels), expected_fitness)

if __name__ == '__main__':
    unittest.main()
