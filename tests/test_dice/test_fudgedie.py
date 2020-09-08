from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import unittest
import random
from tabletoprandom.dice.fudge import FudgeDie, FudgeValue


class FudgeDie_TestCase(unittest.TestCase):

    def setUp(self):
        self.dF = FudgeDie()

    def test_num_faces(self):
        self.assertEqual(self.dF.num_faces, 3)

    def test_sized(self):
        self.assertEqual(len(self.dF), 3)

    def test_type(self):
        self.assertIsInstance(self.dF, FudgeDie)

    def test_mean(self):
        self.assertEqual(self.dF.mean, FudgeValue.BLANK)

    def test_best_roll(self):
        self.assertEqual(self.dF.best_roll, FudgeValue.PLUS)

    def test_worst_roll(self):
        self.assertEqual(self.dF.worst_roll, FudgeValue.MINUS)

    def test_probability(self):
        for value in FudgeValue:
            with self.subTest(i=value):
                self.assertEqual(self.dF.probability(value), 1/3)
        self.assertEqual(self.dF.probability(2), 0)

    def test_faces(self):
        self.assertEqual(self.dF.faces, set(FudgeValue))

    def test_mode(self):
        self.assertEqual(self.dF.mode, set(FudgeValue))

    def test_last_roll(self):
        self.assertIsNone(self.dF.last_roll)
        for i in range(10):
            with self.subTest(i=i):
                dF_last = self.dF.roll()
                self.assertEqual(self.dF.last_roll, dF_last)

    def test_roll(self):
        for i in range(10):
            with self.subTest(i=i):
                self.assertEqual(
                    *self.seed_capture_repeat_capture(i, self.dF)
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
                    *self.seq_seed_capture_repeat_capture(i, self.dF, 3*i)
                )
        with self.assertRaises(StopIteration):
            next(self.dF.rolls(0))
        with self.assertRaises(StopIteration):
            next(self.dF.rolls(-1))
        with self.assertRaises(StopIteration):
            next(self.dF.rolls(-1000))

    def seq_seed_capture_repeat_capture(self, seed, die, n):
        repeat_captures = []
        random.seed(seed)
        die_captures = list(die.rolls(n))
        random.seed(seed)
        for i in range(n):
            repeat_captures.append(random.choice(tuple(die.faces)))
        return die_captures, repeat_captures

    def test_str(self):
        self.assertEqual(str(self.dF), "dF")

    def test_face_order(self):
        self.assertEqual(self.dF.face_order, sorted(list(FudgeValue)))


if __name__ == '__main__':
    unittest.main()
