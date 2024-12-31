from CardColor import CardColor
from Card import Card
import random

class Pile:
    NUM_CHANGE_COLOR = 4
    cards = []
    index = 0

    def __init__(self):
        for i in range(2):
            for j in range(9):
                if j + 1 == 2:
                    continue

                self.cards.append(Card(j + 1, CardColor.Blue,  f"assets/cards/blue/{j + 1}.png"))
                self.cards.append(Card(j + 1, CardColor.Green, f"assets/cards/green/{(j + 1)}.png"))
                self.cards.append(Card(j + 1, CardColor.Yellow, f"assets/cards/yellow/{(j + 1)}.png"))
                self.cards.append(Card(j + 1, CardColor.Red,  f"assets/cards/red/{(j + 1)}.png"))

            for j in range(2):
                self.cards.append(Card(None, CardColor.Blue, f"assets/cards/blue/stop.png"))
                self.cards.append(Card(None, CardColor.Green, f"assets/cards/green/stop.png"))
                self.cards.append(Card(None, CardColor.Yellow, f"assets/cards/yellow/stop.png"))
                self.cards.append(Card(None, CardColor.Red, f"assets/cards/red/stop.png"))

                self.cards.append(Card(None, CardColor.Blue, f"assets/cards/blue/plus_two.png"))
                self.cards.append(Card(None, CardColor.Green, f"assets/cards/green/plus_two.png"))
                self.cards.append(Card(None, CardColor.Yellow, f"assets/cards/yellow/plus_two.png"))
                self.cards.append(Card(None, CardColor.Red, f"assets/cards/red/plus_two.png"))

                self.cards.append(Card(None, CardColor.Blue, f"assets/cards/blue/change_direction.png"))
                self.cards.append(Card(None, CardColor.Green, f"assets/cards/green/change_direction.png"))
                self.cards.append(Card(None, CardColor.Yellow, f"assets/cards/yellow/change_direction.png"))
                self.cards.append(Card(None, CardColor.Red, f"assets/cards/red/change_direction.png"))

                self.cards.append(Card(None, CardColor.Blue, f"assets/cards/blue/taki.png"))
                self.cards.append(Card(None, CardColor.Green, f"assets/cards/green/taki.png"))
                self.cards.append(Card(None, CardColor.Yellow, f"assets/cards/yellow/taki.png"))
                self.cards.append(Card(None, CardColor.Red, f"assets/cards/red/taki.png"))

                # Forgot to add plus card for each color

            for k in range(self.NUM_CHANGE_COLOR):
                self.cards.append(Card(None, CardColor.White, f"assets/cards/color_changer.png"))

        random.shuffle(self.cards)

        while not self.cards[-1].is_number():
            random.shuffle(self.cards)

    def draw_card(self):

        return self.cards.pop()
