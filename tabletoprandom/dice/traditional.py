from typing import Set, Final
from ..abstract.dice import NumericDie, FairDie


class TraditionalDie(NumericDie[int], FairDie[int]):
    """A fair `n` sided die that defaults to 6 sides

    Attributes:
        num_faces: the number of faces on the die
        faces: set of all the faces on the die
        mode: set of all the most common faces to be rolled
        mean: geometric average roll of the die
        is_fair: boolean describing whether or not a die is fair
        best_roll: the numberical best/highest roll on the die
        worst_roll: the numberical worst/lowest roll on the die """

    num_faces: Final[int]

    def __init__(self, n=6) -> None:
        if n < 1:
            raise ValueError("A die must have at least one side")
        self.num_faces = n

    @property
    def faces(self) -> Set[int]:
        return set(range(1, self.num_faces+1))

    def __str__(self) -> str:
        return f"d{self.num_faces}"
