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
        return counter(self.deck)

    def __draw__(self) -> T:
        card = self.deck.popleft()
        self.drawn.update([card])
        return card

    def shuffle(self) -> None:
        deck_list = list(self.deck)
        random.shuffle(deck_list)
        self.deck = deque(deck_list)

    def return_cards(self, cards: Iterable[T], place_top: bool = False
                     ) -> Counter[T]:
        if place_top:
            self.deck.extendleft(cards)
        else:
            self.deck.extend(cards)
        self.drawn.subtract(cards)
        return self.pool

    def return_card(self, card: T, place_top: bool = False
                    ) -> Counter[T]:
        return self.return_cards([card], place_top)

    replace = return_card

    def replace_all(self) -> Counter[T]:
        pool = self.return_cards(self.drawn.elements())
        self.drawn = counter()
        return pool

    def peek(self, n: int = 1) -> List[T]:
        n = min(n, len(self.deck))
        return [self.deck[i] for i in range(n)]
