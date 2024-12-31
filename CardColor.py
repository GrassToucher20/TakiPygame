from enum import Enum

class CardColor(Enum):
    Blue = 1
    Red = 2
    Green = 3
    Yellow = 4
    White = 5

    def __str__(self):
        return '%s' % self.value