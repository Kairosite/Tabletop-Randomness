from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import unittest
import random
from tabletoprandom.dice.magical import MagicalDie


class MagicalDie_TestCase(unittest.TestCase):

    def setUp(self):
        self.d3 = MagicalDie(3)
        self.d6 = MagicalDie(6)
        self.d20 = MagicalDie(20)

    def test_num_faces(self):
        self.assertEqual(self.d3.num_faces, 3)
        self.assertEqual(self.d6.num_faces, 6)
        self.assertEqual(self.d20.num_faces, 20)
        default = MagicalDie()
        self.assertEqual(default.num_faces, 6)

    def test_sized(self):
        self.assertEqual(len(self.d3), 3)
        self.assertEqual(len(self.d6), 6)
        self.assertEqual(len(self.d20), 20)

    def test_type(self):
        self.assertIsInstance(self.d3, MagicalDie)
        self.assertIsInstance(self.d6, MagicalDie)
        self.assertIsInstance(self.d20, MagicalDie)

    def test_mean(self):
        self.assertEqual(self.d3.mean, 2.0)
        self.assertEqual(self.d6.mean, 3.5)
        self.assertEqual(self.d20.mean, 10.5)

    def test_best_roll(self):
        self.assertEqual(self.d3.best_roll, 3)
        self.assertEqual(self.d6.best_roll, 6)
        self.assertEqual(self.d20.best_roll, 20)

    def test_worst_roll(self):
        self.assertEqual(self.d3.worst_roll, 1)
        self.assertEqual(self.d6.worst_roll, 1)
        self.assertEqual(self.d20.worst_roll, 1)

    def test_probability(self):
        for i in range(22):
            with self.subTest(i=i):
                d3target = d6target = d20target = 0
                if i in range(1, 4):
                    d3target = 1/3
                if i in range(1, 7):
                    d6target = 1/6
                if i in range(1, 21):
                    d20target = 1/20
                self.assertEqual(self.d3.probability(i), d3target)
                self.assertEqual(self.d6.probability(i), d6target)
                self.assertEqual(self.d20.probability(i), d20target)

    def test_faces(self):
        self.assertEqual(self.d3.faces, set(range(1, 4)))
        self.assertEqual(self.d6.faces, set(range(1, 7)))
        self.assertEqual(self.d20.faces, set(range(1, 21)))

    def test_mode(self):
        self.assertEqual(self.d3.mode, set(range(1, 4)))
        self.assertEqual(self.d6.mode, set(range(1, 7)))
        self.assertEqual(self.d20.mode, set(range(1, 21)))

    def test_last_roll(self):
        self.assertIsNone(self.d3.last_roll)
        self.assertIsNone(self.d6.last_roll)
        self.assertIsNone(self.d20.last_roll)
        for i in range(10):
            with self.subTest(i=i):
                d3_last = self.d3.roll()
                d6_last = self.d6.roll()
                d20_last = self.d20.roll()
                self.assertEqual(self.d3.last_roll, d3_last)
                self.assertEqual(self.d6.last_roll, d6_last)
                self.assertEqual(self.d20.last_roll, d20_last)

    def test_roll(self):
        for i in range(10):
            with self.subTest(i=i):
                self.assertEqual(
                    *self.seed_capture_repeat_capture(i, self.d3)
                )
                self.assertEqual(
                    *self.seed_capture_repeat_capture(i, self.d6)
                )
                self.assertEqual(
                    *self.seed_capture_repeat_capture(i, self.d20)
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
                    *self.seq_seed_capture_repeat_capture(i, self.d3, 3*i)
                )
                self.assertListEqual(
                    *self.seq_seed_capture_repeat_capture(i, self.d6, 3*i)
                )
                self.assertListEqual(
                    *self.seq_seed_capture_repeat_capture(i, self.d20, 3*i)
                )
        with self.assertRaises(StopIteration):
            next(self.d3.rolls(0))
        with self.assertRaises(StopIteration):
            next(self.d3.rolls(-1))
        with self.assertRaises(StopIteration):
            next(self.d3.rolls(-1000))

    def seq_seed_capture_repeat_capture(self, seed, die, n):
        repeat_captures = []
        random.seed(seed)
        die_captures = list(die.rolls(n))
        random.seed(seed)
        for i in range(n):
            repeat_captures.append(random.choice(tuple(die.faces)))
        return die_captures, repeat_captures

    def test_bad_initiation(self):
        with self.assertRaises(ValueError):
            MagicalDie(0)
        with self.assertRaises(ValueError):
            MagicalDie(-1000)
        with self.assertRaises(ValueError):
            MagicalDie(charge=-1)
        with self.assertRaises(ValueError):
            MagicalDie(charge=-1000)

    def test_str(self):
        self.assertEqual(str(self.d3), "d3(0)")
        test_value_1 = 5
        self.d6.empower(test_value_1)
        self.assertEqual(str(self.d6), f"d6({test_value_1})")
        test_value_2 = 3
        self.d20.empower(test_value_2)
        self.assertEqual(str(self.d20), f"d20({test_value_2})")

    def test_initiation(self):
        self.assertEqual(self.d3.charge, 0)
        test_value_1 = 1
        test_die_1 = MagicalDie(charge=test_value_1)
        self.assertEqual(test_die_1.charge, test_value_1)
        test_value_2 = 100
        test_die_2 = MagicalDie(20, test_value_2)
        self.assertEqual(test_die_2.charge, test_value_2)

    def test_empower(self):
        test_value_1 = 2
        self.d3.empower(test_value_1)
        self.assertEqual(self.d3.charge, test_value_1)
        test_value_2 = 4
        self.d3.empower(test_value_2)
        self.assertEqual(self.d3.charge, test_value_1 + test_value_2)
        self.d6.empower(test_value_2)
        self.assertEqual(self.d6.charge, test_value_2)
        self.d20.empower()
        self.assertEqual(self.d20.charge, 1)

    def test_dispell(self):
        self.d3.empower()
        self.d3.dispell()
        self.assertEqual(self.d3.charge, 0)
        self.d3.dispell()
        self.assertEqual(self.d3.charge, 0)
        self.d6.empower(3)
        test_value_1 = 5
        self.d20.empower(test_value_1)
        self.d6.dispell()
        self.assertEqual(self.d6.charge, 0)
        self.assertEqual(self.d20.charge, test_value_1)

    def test_empowered_roll(self):
        test_value_1 = 5
        self.d3.empower(test_value_1)
        for i in range(test_value_1):
            with self.subTest(i=i):
                self.assertEqual(self.d3.charge, test_value_1 - i)
                self.d3.roll()
                self.assertEqual(self.d3.charge, test_value_1 - i - 1)

        self.d3.empower(3)
        self.d6.empower(6)
        self.d20.empower(9)
        for i in range(10):
            with self.subTest(i=i):
                if self.d3.charge:
                    self.assertEqual(self.d3.roll(), self.d3.best_roll)
                else:
                    self.assertEqual(
                        *self.seed_capture_repeat_capture(i, self.d3)
                    )
                if self.d6.charge:
                    self.assertEqual(self.d6.roll(), self.d6.best_roll)
                else:
                    self.assertEqual(
                        *self.seed_capture_repeat_capture(i, self.d6)
                    )
                if self.d20.charge:
                    self.assertEqual(self.d20.roll(), self.d20.best_roll)
                else:
                    self.assertEqual(
                        *self.seed_capture_repeat_capture(i, self.d20)
                    )

    def test_face_order(self):
        self.assertEqual(self.d3.face_order, list(range(1, 4)))
        self.assertEqual(self.d6.face_order, list(range(1, 7)))
        self.assertEqual(self.d20.face_order, list(range(1, 21)))


if __name__ == '__main__':
    unittest.main()
