from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import abc
from typing import Iterable, Set, Sized, TypeVar

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


T = TypeVar('T')


class Drawable(Iterable[T], abc.ABC):
    """The base class for all drawable objects in the TTR library

    This class defines the core requirements of a generic drawable object, but
    cannot be instansiated, it is an iterable, and supports a number of basic
    functions once the member `__draw__` function is implemented, likely not
    the default class to subclass unless working on some very unique mechanics.
    """
    last_draw = None

    @abc.abstractmethod
    def __draw__(self) -> T:
        """Override with the rolling mechanism of your rollable"""
        pass

    def draw(self) -> T:
        """Returns a value corresponding to the next draw of the object

        This function will return a value of the type associated with the
        rollable generic and update the `last_draw` attrribute.
        """
        self.last_draw = self.__draw__()
        return self.last_draw

    def draws(self, n: int) -> Iterable[T]:
        """A generator equivalent to calling `draw` `n` times

        Parameters
        ----------
        n : int
            The number of draws requested

        Returns
        -------
        Iterable[T]
            A generator of results from draw
        """
        while n > 0:
            n -= 1
            yield self.draw()

    def __iter__(self) -> T:
        return self

    __next__ = draw


T = TypeVar('T')


class FiniteDrawable(Drawable[T], Sized):
    """The base class for finite drawable objects in the TTR library

    This class defines the core requirements of a finite drawable object, but
    cannot be instansiated, it is an iterable, and defines a number of basic
    functions. The `__draw__` function of a finite drawable is expected to
    raise a `StopIteration` when exhuasted.
    """

    def draws(self, n: int) -> Iterable[T]:
        """A generator equivalent to calling `draw` `n` times

        Parameters
        ----------
        n : int
            The number of draws requested

        Returns
        -------
        Iterable[T]
            A generator of results from draw
        """
        while n > 0:
            n -= 1
            try:
                yield self.draw()
            except StopIteration:
                return

    @property
    @abc.abstractmethod
    def drawn(self) -> Set[T]:
        """A property giving a set of elements from the drawable currently
        in the drawn state"""
        pass

    @property
    @abc.abstractmethod
    def pool(self) -> Set[T]:
        """A property giving a set of elements from the drawable currently
        in the undrawn, or drawable state"""
        pass

    @abc.abstractmethod
    def replace(self, T) -> Set[T]:
        """A function to replace a drawn object and return the resulting
        undrawn pool"""
        pass

    @abc.abstractmethod
    def replace_all(self) -> Set[T]:
        """A function to replace all drawn objects and return the resulting
        undrawn pool"""
        pass

    def draw_and_replace(self) -> T:
        """A function to draw an element with replacement"""
        self.replace(self.draw())
        return self.last_draw

    def __len__(self) -> int:
        return len(self.pool)
