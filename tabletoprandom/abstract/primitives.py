from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import abc
from typing import Iterable, TypeVar

T = TypeVar('T')


class Rollable(Iterable[T], abc.ABC):
    """The base class for all rollable objects in the TTR library

    This class defines the core requirements of a generic rollable object, but
    cannot be instansiated, it is an iterable, and supports a number of basic
    functions once the member `__roll__` function is implemented, likely not
    the default class to subclass unless working on some very unique mechanics.
    """
    last_roll = None

    @abc.abstractmethod
    def __roll__(self) -> T:
        """Override with the rolling mechanism of your rollable"""
        pass

    def roll(self) -> T:
        """Returns a value corresponding to the next roll of the object

        This function will return a value of the type associated with the
        rollable generic and update the `last_roll` attrribute.
        """
        self.last_roll = self.__roll__()
        return self.last_roll

    def rolls(self, n: int) -> Iterable[T]:
        """A generator equivalent to calling `roll` `n` times

        Parameters
        ----------
        n : int
            The number of rolls requested

        Returns
        -------
        Iterable[T]
            A generator of results from roll
        """
        while n > 0:
            n -= 1
            yield self.roll()

    def __iter__(self) -> T:
        return self

    __next__ = roll
