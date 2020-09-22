from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import unittest
import random
from tabletoprandom.dice.enumdie import EnumDie, ElementValue


class EnumDie_TestCase(unittest.TestCase):

    def setUp(self):
        self.dE = EnumDie(ElementValue)

    def test_num_faces(self):
        self.assertEqual(self.dE.num_faces, 4)

    def test_sized(self):
        self.assertEqual(len(self.dE), 4)

    def test_type(self):
        self.assertIsInstance(self.dE, EnumDie)

    def test_probability(self):
        for value in ElementValue:
            with self.subTest(i=value):
                self.assertEqual(self.dE.probability(value), 1/4)
        self.assertEqual(self.dE.probability(2), 0)

    def test_faces(self):
        self.assertEqual(self.dE.faces, set(ElementValue))

    def test_mode(self):
        self.assertEqual(self.dE.mode, set(ElementValue))

    def test_last_roll(self):
        self.assertIsNone(self.dE.last_roll)
        for i in range(10):
            with self.subTest(i=i):
                dE_last = self.dE.roll()
                self.assertEqual(self.dE.last_roll, dE_last)

    def test_roll(self):
        for i in range(10):
            with self.subTest(i=i):
                self.assertEqual(
                    *self.seed_capture_repeat_capture(i, self.dE)
                )

    def seed_capture_repeat_capture(self, seed, die):
        random.seed(seed)
        die_capture = die.roll()
        random.seed(seed)
        repeat_capture = random.choice(tuple(die.faces))
        return die_capture, repeat_capture

    def test_rolls(self):
        for i in range(3):
            with self.subTest(i=i):
                self.assertListEqual(
                    *self.seq_seed_capture_repeat_capture(i, self.dE, 3*i)
                )
        with self.assertRaises(StopIteration):
            next(self.dE.rolls(0))
        with self.assertRaises(StopIteration):
            next(self.dE.rolls(-1))
        with self.assertRaises(StopIteration):
            next(self.dE.rolls(-1000))

    def seq_seed_capture_repeat_capture(self, seed, die, n):
        repeat_captures = []
        random.seed(seed)
        die_captures = list(die.rolls(n))
        random.seed(seed)
        for i in range(n):
            repeat_captures.append(random.choice(tuple(die.faces)))
        return die_captures, repeat_captures

    def test_str(self):
        self.assertEqual(str(self.dE), "dE")


if __name__ == '__main__':
    unittest.main()
