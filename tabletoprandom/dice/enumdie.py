from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from typing import Set, List, Final
from enum import EnumMeta, IntEnum, Enum, unique, auto
from tabletoprandom.abstract.dice import FairDie, NumericDie
import random


@unique
class ElementValue(Enum):
    FIRE = auto()
    WATER = auto()
    AIR = auto()
    EARTH = auto()

    @staticmethod
    def die_string() -> str:
        return "E"


@unique
class FudgeValue(IntEnum):
    PLUS = 1
    BLANK = 0
    MINUS = -1

    @staticmethod
    def die_string() -> str:
        return "F"


class EnumDie(FairDie[Enum]):

    face_enum: Final[EnumMeta]

    def __init__(self, face_enum: EnumMeta) -> None:
        self.face_enum = face_enum

    @property
    def faces(self) -> Set[Enum]:
        return set(self.face_enum)

    @property
    def num_faces(self) -> int:
        return len(self.face_enum)

    @staticmethod
    def quick_roll(face_enum: EnumMeta) -> Enum:
        return random.choice(face_enum)

    def __str__(self) -> str:
        try:
            return f"d{self.face_enum.die_string()}"
        except AttributeError:
            return f"d({self.face_enum.__name__})"


class IntEnumDie(EnumDie, NumericDie[IntEnum]):

    face_enum: Final[EnumMeta]

    def __init__(self, face_enum: EnumMeta) -> None:
        if not IntEnum.__subclasscheck__(face_enum):
            raise ValueError("An IntEnum has not been given")
        self.face_enum = face_enum

    @property
    def face_order(self) -> List[IntEnum]:
        """Returns an ordered list of the die's faces"""
        return sorted(list(self.face_enum))

    @staticmethod
    def quick_roll(face_enum: EnumMeta) -> IntEnum:
        if not IntEnum.__subclasscheck__(face_enum):
            raise ValueError("An IntEnum has not been given")
        return random.choice(face_enum)
