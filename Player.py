from Card import Card
from pygame import Surface
import copy

class Player:
    cards: list[Card]
    name: str
    is_burdened: bool

    def __init__(self, name):
        self.cards = []
        self.name = name
        self.is_burdened = False

    def take_card(self, card: Card):
        card.position = len(self.cards)
        self.cards.append(card)

    def remove_card(self, card_index: int):
        card = self.cards[card_index]
        del self.cards[card_index]

        for i, remaining_card in enumerate(self.cards):
            remaining_card.position = i
        return card

    def draw_cards(self, screen: Surface, reveal: int):
        for card in self.cards:
            card.draw(screen, reveal)