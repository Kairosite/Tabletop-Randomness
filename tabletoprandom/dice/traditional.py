from typing import Set, Final
from ..abstract.dice import NumericDie, FairDie


class TraditionalDie(NumericDie[int], FairDie[int]):

    num_faces: Final[int]

    def __init__(self, n=6) -> None:
        if n < 1:
            raise ValueError("A die must have at least one side")
        self.num_faces = n

    @property
    def faces(self) -> Set[int]:
        return set(range(1, self.num_faces+1))
