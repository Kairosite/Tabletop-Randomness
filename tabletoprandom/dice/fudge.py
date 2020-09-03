from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from typing import Set, List
from enum import IntEnum, unique
from tabletoprandom.abstract.dice import FairDie, NumericDie
import random


@unique
class FudgeValue(IntEnum):
    PLUS = 1
    BLANK = 0
    MINUS = -1


class FudgeDie(FairDie[FudgeValue], NumericDie[FudgeValue]):

    @property
    def faces(self) -> Set[FudgeValue]:
        return set(FudgeValue)

    @property
    def face_order(self) -> List[FudgeValue]:
        """Returns an ordered list of the die's faces"""
        return sorted(list(FudgeValue))

    @staticmethod
    def quick_roll() -> FudgeValue:
        return random.choice(FudgeValue)

    def __str__(self) -> str:
        return "dF"
