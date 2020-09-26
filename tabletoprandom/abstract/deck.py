from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from typing import Counter, TypeVar, Deque, List, Iterable
import random
from collections import deque
from tabletoprandom.abstract.primitives import FiniteDrawable

T = TypeVar('T')


class Deck(FiniteDrawable[T]):
    deck: Deque[T]

    def shuffle(self) -> None:
        deck_list = list(self.deck)
        random.shuffle(deck_list)
        self.deck = deque(deck_list)

    def return_card(self, cards: Iterable[T], place_top: bool = False
                    ) -> Counter[T]:
        if place_top:
            self.deck.extendleft(cards)
        else:
            self.deck.extend(cards)
        return self.pool

    def peek(self, n: int = 1) -> List[T]:
        n = min(n, len(self.deck))
        return [self.deck[i] for i in range(n)]
