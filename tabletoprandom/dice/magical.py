from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from tabletoprandom.dice.traditional import TraditionalDie


class MagicalDie(TraditionalDie):

    charge: int

    def __init__(self, n=6, charge=0) -> None:
        if charge < 0:
            raise ValueError("A magical die cannot have negative charge")
        self.charge = charge

        super().__init__(n)

    def __roll__(self) -> int:
        if self.charge:
            self.charge -= 1
            return self.best_roll

        return super().__roll__()

    def empower(self, charge=1) -> int:
        if charge < 0:
            raise ValueError("A magical die cannot have negative charge")
        self.charge += charge
        return self.charge

    def dispell(self) -> None:
        self.charge = 0

    def __str__(self) -> str:
        return super().__str__() + f"({self.charge})"
