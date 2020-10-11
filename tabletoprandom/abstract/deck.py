from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from typing import Counter, TypeVar, Deque, List, Iterable
import random
from collections import deque
from collections import Counter as counter
from tabletoprandom.abstract.primitives import FiniteDrawable

T = TypeVar('T')


class Deck(FiniteDrawable[T]):
    deck: Deque[T]
    drawn: Counter[T]

    @property
    def pool(self) -> Counter[T]:
        """Returns all the drawable, i.e. undrawn elements as an unordered
        set"""
        return counter(self.deck)

    def __draw__(self) -> T:
        """Draws a card from the top of the deck"""
        card = self.deck.popleft()
        self.drawn.update([card])
        return card

    def shuffle(self) -> None:
        """Shuffles the deck in place"""
        deck_list = list(self.deck)
        random.shuffle(deck_list)
        self.deck = deque(deck_list)

    def return_cards(self, cards: Iterable[T], place_top: bool = False
                     ) -> Counter[T]:
        """Returns an iterable of cards to the deck, they are returned to the
        bottom of the deck unless the `place_top` flag is set"""
        if place_top:
            self.deck.extendleft(cards)
        else:
            self.deck.extend(cards)
        self.drawn.subtract(cards)
        return self.pool

    def return_card(self, card: T, place_top: bool = False
                    ) -> Counter[T]:
        """Returns a single card to the deck, it is returned to the bottom of
        the deck unless the `place_top` flag is set"""
        return self.return_cards([card], place_top)

    replace = return_card

    def replace_all(self) -> Counter[T]:
        """Returns all drawn cards to the bottom of the deck and refreshes the
        drawn counter"""
        pool = self.return_cards(self.drawn.elements())
        self.drawn = counter()
        return pool

    def peek(self, n: int = 1) -> List[T]:
        """Returns the top N elements of the list"""
        n = min(n, len(self.deck))
        return [self.deck[i] for i in range(n)]
