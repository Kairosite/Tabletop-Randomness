import abc
import random
from typing import Set, Sized, TypeVar
from .primitives import Rollable

T = TypeVar('T')


class Die(Rollable[T], Sized, abc.ABC):
    """A base class for dice to inherit from, defining some expectations

    Adds the basic die class with `faces`, `mode` and `probability` functions.
    """
    @property
    @abc.abstractmethod
    def faces(self) -> Set[T]:
        """Returns a set containing all the faces of the die"""
        pass

    @property
    @abc.abstractmethod
    def mode(self) -> Set[T]:
        """Returns a set containing the most commonly rolled side(s)"""
        pass

    @abc.abstractmethod
    def probability(self, face: T) -> float:
        """Returns the probability of a given value, or face, being rolled

        Parameters
        ----------
        face : T
            The potential face value to be tested

        Returns
        -------
        float
            The probablity of `roll` returning that face

        Note: This should return `0.0` on values not on the face of the die,
        to test if a face is on the die `face in Die.faces` should be used
        instead"""
        pass

    def __len__(self) -> int:
        return self.num_faces


T = TypeVar('T')


class FairDie(Die[T]):
    """An inheritable class that implements the behaviour of a fair die"""
    isFair = True

    def __roll__(self) -> T:
        """Returns a face from a fair roll of the die"""
        return random.choice(tuple(self.faces))

    def probability(self, face: T) -> float:
        """Returns the probability of a given value, or face, being rolled

        Parameters
        ----------
        face : T
            The potential face value to be tested

        Returns
        -------
        float
            The probablity of `roll` returning that face

        Note: This should return `0.0` on values not on the face of the die,
        to test if a face is on the die `face in Die.faces` should be used
        instead"""
        if face in self.faces:
            return 1/self.num_faces
        else:
            return 0.0

    @property
    def mode(self) -> Set[T]:
        """Returns a set containing the most commonly rolled side(s)"""
        return self.faces


T = TypeVar('T')


class MonotonicDie(Die[T]):
    """A base class for Monotonic Dice, those with orderable sides defining
    expectations"""

    @property
    @abc.abstractmethod
    def best_roll(self) -> T:
        """Returns the worst roll of the die"""
        pass

    @property
    @abc.abstractmethod
    def worst_roll(self) -> T:
        """Returns the worst roll of the die"""
        pass


N = TypeVar('N', float, int)


class NumericDie(MonotonicDie[N]):
    """A base class for Numeric Dice to inherit from that provides relevant
    definitions"""

    @property
    def mean(self) -> float:
        """Calculates and returns the geometric mean of the die"""
        return sum([self.probability(x) * x for x in self.faces])

    @property
    def best_roll(self) -> N:
        """Returns the best, maximum, roll of the die"""
        return max(self.faces)

    @property
    def worst_roll(self) -> N:
        """Returns the worst, minimum, roll of the die"""
        return min(self.faces)
