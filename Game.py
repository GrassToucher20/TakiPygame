# Checklist
# -What to do when the player wins
# -Replay functionality
# -Other player card size is the same as the current player card size
# -Card position not updated after adding to placed cards pile
# -Creating a dest when drawing instead of using the one from the card
# -Center the cards on the screen

from Player import Player
from Pile import Pile
import pygame
from pygame import Rect
import sys
from Card import Card
from CardColor import CardColor

class Game:
    WIDTH, HEIGHT = 1280, 720
    FPS = 60
    TITLE = "Taki"
    BACKGROUND_COLOR = (30, 30, 30)
    NUM_STARTING_CARDS = 8

    is_game_over = False
    cards_placed = []
    pile: Pile

    player1: Player
    player2: Player

    current_player: Player
    other_player: Player

    take_card: pygame.Rect
    font: any

    plus_two_burden = 0

    turn_over = False
    selecting_color = False

    taki_active = False
    taki_color: CardColor

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(self.TITLE)

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()

        self.pile = Pile()

        self.player1 = Player('Player 1')
        self.player2 = Player('Player 2')

        self.current_player = self.player1
        self.other_player = self.player2

        self.take_card = pygame.Rect(Rect(300, 250, Card.WIDTH, Card.HEIGHT))
        self.font = pygame.font.SysFont('Comic Sans MS', 30)

        self.red_changer = pygame.Rect(Rect(300 + Card.GAP, 250, Card.WIDTH, Card.HEIGHT))
        self.yellow_changer = pygame.Rect(Rect(300 + Card.WIDTH + Card.GAP + Card.GAP, 250, Card.WIDTH, Card.HEIGHT))
        self.green_changer = pygame.Rect(Rect(300 + Card.GAP, 250 + Card.HEIGHT + Card.GAP, Card.WIDTH, Card.HEIGHT))
        self.blue_changer = pygame.Rect(Rect(300 + Card.GAP + Card.WIDTH + Card.GAP, 250 + Card.HEIGHT + Card.GAP, Card.WIDTH, Card.HEIGHT))


    def run(self):
        self.cards_placed.append(self.pile.draw_card())

        green = (0, 255, 0)
        blue = (0, 0, 128)
        color = (255, 0, 0)

        for _ in range(1):
            self.player1.take_card(self.pile.draw_card())
            self.player2.take_card(self.pile.draw_card())

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos

                    # The player is trying to select a color cube
                    if self.selecting_color:
                        self.determine_color_changer(x, y)
                        break

                    # The player is drawing a card, or a +2 burden
                    if self.take_card.collidepoint(x, y):
                        self.draw_card()
                        break

                    # Loop to see what the player wants to place
                    for i, card in enumerate(self.current_player.cards):
                        rect = pygame.Rect(card.x_position, card.Y_POSITION, Card.WIDTH, Card.HEIGHT)

                        if rect.collidepoint(x, y):
                            requested_card = self.current_player.cards[i]
                            top_card = self.cards_placed[-1]

                            if self.current_player.is_burdened:
                                if requested_card.is_plus_two():
                                    self.plus_two_burden += 2
                                    self.cards_placed.append(self.current_player.remove_card(i))
                                    print(f"{self.current_player.name} => {requested_card.display_string()}")
                                    self.other_player.is_burdened = True
                                    self.change_turns()
                                break

                            if requested_card.color == top_card.color:
                                if requested_card.is_plus_two() and not self.taki_active:
                                    print(f"{self.current_player.name} => {requested_card.display_string()}")
                                    self.plus_two_burden += 2
                                    self.cards_placed.append(self.current_player.remove_card(i))
                                    self.other_player.is_burdened = True
                                    self.change_turns()
                                    break

                            if requested_card.is_color_changer() and not self.taki_active:
                                self.selecting_color = True
                                self.cards_placed.append(self.current_player.remove_card(i))
                                print(f"{self.current_player.name} => {card.display_string()}")
                                break

                            if (requested_card.value == top_card.value or
                                    requested_card.color == top_card.color or
                                    (requested_card.is_stop() and top_card.is_stop())):
                                print(f"{self.current_player.name} => {card.display_string()}")

                                if requested_card.is_taki():
                                    self.taki_active = True
                                    self.taki_color = requested_card.color
                                if self.taki_active:
                                    if requested_card.color == top_card.color:
                                        self.cards_placed.append(self.current_player.remove_card(i))
                                else:
                                    self.cards_placed.append(self.current_player.remove_card(i))

                                if self.taki_active:
                                    if not any(card.color == self.taki_color for card in self.current_player.cards):
                                        self.taki_active = False




                                if not requested_card.is_stop() and not requested_card.is_change_direction() and not self.taki_active:
                                    if len(self.current_player.cards) == 0:
                                        is_game_over = True
                                    else:
                                        self.change_turns()

                                break

                # Clear the screen
            self.screen.fill(self.BACKGROUND_COLOR)

            # Draw the last card in the pile
            self.screen.blit(self.cards_placed[-1].image, (200, 250))

            if self.selecting_color:
                pygame.draw.rect(self.screen, pygame.Color('red'), self.red_changer)
                pygame.draw.rect(self.screen, pygame.Color('green'), self.green_changer)
                pygame.draw.rect(self.screen, pygame.Color('yellow'), self.yellow_changer)
                pygame.draw.rect(self.screen, pygame.Color('blue'), self.blue_changer)
            else:
                pygame.draw.rect(self.screen, (255, 0, 0), self.take_card)

            if not self.is_game_over:

                #for i in range(len(self.other_player.cards)):
                    #pygame.draw.rect(self.screen, color, pygame.Rect(100 * i + 30, 30, Card.WIDTH, Card.HEIGHT))
                self.other_player.draw_cards(self.screen, Card.HIDE)

                # Draw the current player's cards
                self.current_player.draw_cards(self.screen, Card.REVEAL)

                # Display current player's name

                text = self.font.render(self.current_player.name, True, green, blue)
                text_rect = text.get_rect(center=(450, 650))
                self.screen.blit(text, text_rect)
            else:
                text = self.font.render(f"{self.current_player.name} won", True, green, blue)
                text_rect = text.get_rect(center=(450, 650))
                self.screen.blit(text, text_rect)
            # Update the display
            pygame.display.flip()

            # Limit the frame rate
            self.clock.tick(self.FPS)

        # Quit Pygame
        pygame.quit()
        sys.exit()
    def change_turns(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
            self.other_player = self.player1
        else:
            self.current_player = self.player1
            self.other_player = self.player2

    def determine_color_changer(self, x, y):
        if self.yellow_changer.collidepoint(x, y):
            self.cards_placed[-1].turn_into_color_cube(CardColor.Yellow, f"assets/cards/yellow/color_changer.png")
            self.selecting_color = False
            print(f"{self.current_player.name} => Color changer: Yellow")

            self.change_turns()
        elif self.red_changer.collidepoint(x, y):
            self.cards_placed[-1].turn_into_color_cube(CardColor.Red, f"assets/cards/red/color_changer.png")
            self.selecting_color = False
            print(f"{self.current_player.name} => Color changer: Red")
            self.change_turns()
        elif self.green_changer.collidepoint(x, y):
            self.cards_placed[-1].turn_into_color_cube(CardColor.Green, f"assets/cards/green/color_changer.png")
            self.selecting_color = False
            print(f"{self.current_player.name} => Color changer: Green")
            self.change_turns()
        elif self.blue_changer.collidepoint(x, y):
            self.cards_placed[-1].turn_into_color_cube(CardColor.Blue, f"assets/cards/blue/color_changer.png")
            self.selecting_color = False
            print(f"{self.current_player.name} => Color changer: Blue")
            self.change_turns()

    def draw_card(self):
        if self.current_player.is_burdened:
            for i in range(self.plus_two_burden):
                self.current_player.take_card(self.pile.draw_card())
            print(f"{self.current_player.name} => Took {self.plus_two_burden} cards")
            self.plus_two_burden = 0
            self.current_player.is_burdened = False
            self.other_player.is_burdened = False
        else:
            print(f"{self.current_player.name} => Took from the pile")
            self.current_player.take_card(self.pile.draw_card())

        self.change_turns()