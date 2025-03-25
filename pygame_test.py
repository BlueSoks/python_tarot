import os
import pygame
from pygame import Rect
from pygame.math import Vector2
import random as rd

os.environ['SDL_VIDEO_CENTERED'] = '1'

class Trick():
    def __init__(self):
        self.played = []
        self.suit = None
        
    def setSuit(self, suit):
        self.suit = suit

class GameState():
    def __init__(self):
        self.worldSize = Vector2(20,20)
        self.tankPos = Vector2(0,0)
        self.deck = ['0E', '14H', '13H', '12H', '11H', '10H', '9H', '8H', '7H', '6H', '5H', '4H', '3H', '2H', '1H', '14C', '13C', '12C', '11C', '10C', '9C', '8C', '7C', '6C', '5C', '4C', '3C', '2C', '1C', '14D', '13D', '12D', '11D', '10D', '9D', '8D', '7D', '6D', '5D', '4D', '3D', '2D', '1D', '14S', '13S', '12S', '11S', '10S', '9S', '8S', '7S', '6S', '5S', '4S', '3S', '2S', '1S']
        for j in range(1, 22):
            self.deck += ['%sA' %j]
        rd.shuffle(self.deck)
        self.south = []
        self.north = []
        self.east = []
        self.west = []
        self.south_earned = []
        self.north_east_earned = []
        self.north_west_earned = []
        self.east_earned = []
        self.west_earned = []
        self.kitty = []
        self.remaining_contracts = ['None', 'Small', 'Guard', 'Guard without', 'Guard against']
        self.contract = None
        self.dealer_index = 0
        self.index_position = {0: 'South', 1: 'West', 2: 'North', 3: 'East'}
        self.players = [self.south, self.west, self.north, self.east]
        self.played_cards = [None, None, None, None]
        self.players_earned = [self.south_earned, self.west_earned, self.north_west_earned, self.north_east_earned, self.east_earned]
        self.caller_index = None
        self.deal()
        self.previous_trick_winner = (self.dealer_index + 1) % 4
        self.current_player = self.previous_trick_winner
        self.total_scores = 4*[0]
        self.trick = Trick()
        self.sprites = {}
        # x width on the sprite is 337 pixels and y height is 645 pixels
        # self.positions = {'0E': (5, 6), '14H': (3, 4), '13H': (3, 5), '12H': (2, 1), '11H': (3, 2), '10H': (3, 3), '9H': (2, 2), '8H': (2, 3), '7H': (2, 4), '6H': (2, 5), '5H': (10, 6), '4H': (9, 6), '3H': (8, 6), '2H': (7, 6), '1H': (6, 6), '14C': (3, 7), '13C': (2, 7), '12C': (1, 7), '11C': (5, 7), '10C': (4, 7), '9C': (10, 8), '8C': (9, 8), '7C': (8, 8), '6C': (7, 8), '5C': (6, 8), '4C': (5, 8), '3C': (4, 8), '2C': (3, 8), '1C': (2, 8), '14D': (2, 6), '13D': (1, 1), '12D': (1, 2), '11D': (4, 6), '10D': (3, 6), '9D': (1, 3), '8D': (1, 4), '7D': (1, 5), '6D': (1, 6), '5D': (10, 7), '4D': (9, 7), '3D': (8, 7), '2D': (7, 7), '1D': (6, 7), '14S': (4, 1), '13S': (4, 2), '12S': (4, 3), '11S': (5, 3), '10S': (5, 4), '9S': (4, 4), '8S': (10, 5), '7S': (9, 5), '6S': (8, 5), '5S': (7, 5), '4S': (6, 5), '3S': (5, 5), '2S': (4, 5), '1S': (3, 5), '1A': (5, 2), '2A': (5, 1), '3A': (6, 4), '4A': (7, 4), '5A': (8, 4), '6A': (9, 4), '7A': (10, 4), '8A': (6, 3), '9A': (6, 2), '10A': (6, 1), '11A': (7, 3), '12A': (7, 2), '13A': (7, 1), '14A': (8, 3), '15A': (9, 3), '16A': (10, 3), '17A': (8, 2), '18A': (8, 1), '19A': (9, 2), '20A': (9, 1), '21A': (10, 2)}
                    
            
    
    def deal(self):
        counter = 0
        current_player_index = (self.dealer_index + 1) % 4
        kitty_numbers = rd.sample(range(1, 20), 6)
        while self.deck:
            if counter in kitty_numbers:
                card = self.deck.pop()
                self.kitty += [card]
                counter += 1
            else:
                cards = []
                cards += [self.deck.pop()]
                cards += [self.deck.pop()]
                cards += [self.deck.pop()]
                # print(cards)
                self.players[current_player_index] += cards
                # print(self.players[current_player_index])
                current_player_index = (current_player_index + 1) % 4
                counter += 1
        self.previous_trick_winner = self.dealer_index + 1
        for k in range(len(self.players)):
            self.players[k] = [item for item in self.players[k] if item[-1] == 'C'] + [item for item in self.players[k] if item[-1] == 'S'] + [item for item in self.players[k] if item[-1] == 'D'] + [item for item in self.players[k] if item[-1] == 'H'] + [item for item in self.players[k] if item[-1] == 'A'] + [item for item in self.players[k] if item[-1] == 'E']
    
    def allowedCards(self):
        player = self.players[self.current_player]
        if self.trick.suit == None:
            return player
        elif self.trick.suit == 'A':
            if len([card for card in player if card[-1] == 'A']) > 0:
                return [card for card in player if card[-1] == 'A']
            else:
                return player
        else:
            if len([card for card in player if card[-1] == self.trick.suit]) > 0:
                return [card for card in player if card[-1] == self.trick.suit]
            else:
                if len([card for card in player if card[-1] == 'A']) > 0:
                    return [card for card in player if card[-1] == 'A']
                else:
                    return player
            
        
    def update(self, card):
        if played_card_position == None:
            pass
        else:
            x = played_card_position[0]
            y = played_card_position[1]
            for card in self.allowedCards():
                if self.sprites[card][0] <= x and x <= self.sprites[card][0] and self.sprites[card][1] <= y and y <= self.sprites[card][1] <= y:
                    self.played_cards[self.current_player] = card
            if self.current_player == 0:
                for card in self.allowedCards()
            elif self.current_player == 1:
                pass
            elif self.current_player == 2:
                pass
            elif self.current_player == 3:
                pass

class UserInterface():
    def __init__(self):
        pygame.init()

        # Game state
        self.gameState = GameState()

        # Rendering properties
        self.cellSizex = 50
        self.cellSizey = 50
        self.cellSize = Vector2(self.cellSizex, self.cellSizey)
        self.unitsTexture = pygame.image.load("units.png")
        self.cardsTexture = pygame.image.load("cards.png")
        self.cardsTexture = pygame.transform.scale(self.cardsTexture, (20*self.cellSizex, 16*self.cellSizey))
        # Position of the card sprites within the sprite image
        self.positions = {'0E': (5, 6), '14H': (3, 4), '13H': (3, 5), '12H': (2, 1), '11H': (3, 2), '10H': (3, 3), '9H': (2, 2), '8H': (2, 3), '7H': (2, 4), '6H': (2, 5), '5H': (10, 6), '4H': (9, 6), '3H': (8, 6), '2H': (7, 6), '1H': (6, 6), '14C': (3, 7), '13C': (2, 7), '12C': (1, 7), '11C': (5, 7), '10C': (4, 7), '9C': (10, 8), '8C': (9, 8), '7C': (8, 8), '6C': (7, 8), '5C': (6, 8), '4C': (5, 8), '3C': (4, 8), '2C': (3, 8), '1C': (2, 8), '14D': (2, 6), '13D': (1, 1), '12D': (1, 2), '11D': (4, 6), '10D': (3, 6), '9D': (1, 3), '8D': (1, 4), '7D': (1, 5), '6D': (1, 6), '5D': (10, 7), '4D': (9, 7), '3D': (8, 7), '2D': (7, 7), '1D': (6, 7), '14S': (4, 1), '13S': (4, 2), '12S': (4, 3), '11S': (5, 3), '10S': (5, 4), '9S': (4, 4), '8S': (10, 5), '7S': (9, 5), '6S': (8, 5), '5S': (7, 5), '4S': (6, 5), '3S': (5, 5), '2S': (4, 5), '1S': (3, 5), '1A': (5, 2), '2A': (5, 1), '3A': (6, 4), '4A': (7, 4), '5A': (8, 4), '6A': (9, 4), '7A': (10, 4), '8A': (6, 3), '9A': (6, 2), '10A': (6, 1), '11A': (7, 3), '12A': (7, 2), '13A': (7, 1), '14A': (8, 3), '15A': (9, 3), '16A': (10, 3), '17A': (8, 2), '18A': (8, 1), '19A': (9, 2), '20A': (9, 1), '21A': (10, 2)}
        self.played_card_position = None
        
        # Window
        windowSize = self.gameState.worldSize.elementwise() * self.cellSize
        self.window = pygame.display.set_mode((int(windowSize.x),int(windowSize.y)))
        pygame.display.set_caption("Discover Python & Patterns - https://www.patternsgameprog.com")
        pygame.display.set_icon(pygame.image.load("icon.png"))
        self.moveTankCommand = Vector2(0,0)

        # Loop properties
        self.clock = pygame.time.Clock()
        self.running = True


    def processInput(self):
        self.moveTankCommand = Vector2(0,0)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                self.played_card_position = pos
                print(pos)
            elif event.type == pygame.QUIT:
                self.running = False
                break
            # elif event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_ESCAPE:
            #         self.running = False
            #         break
            #     elif event.key == pygame.K_RIGHT:
            #         self.moveTankCommand.x = 1
            #     elif event.key == pygame.K_LEFT:
            #         self.moveTankCommand.x = -1
            #     elif event.key == pygame.K_DOWN:
            #         self.moveTankCommand.y = 1
            #     elif event.key == pygame.K_UP:
            #         self.moveTankCommand.y = -1

    def update(self):
        self.gameState.update(self.played_card_position)

    def render(self):
        self.window.fill((0, 0, 0))
        for k,player in enumerate(self.gameState.players):
            if k == 0 and self.gameState.current_player != k:
                for i, card in enumerate(player):
                    handSize = len(player)
                    x, y = self.positions[card]
                    y = 2*(8-y)
                    x = 2*(x-1)
                    textureRect = pygame.Rect(x*self.cellSizex, y*self.cellSizey, self.cellSizex, self.cellSizey)
                    spritePoint = Vector2(10-handSize//2+i,19).elementwise()*self.cellSize
                    self.gameState.sprites[card] = spritePoint
                    self.window.blit(self.cardsTexture, spritePoint, textureRect)
            elif k == 0 and self.gameState.current_player == k:
                allowedCards = self.gameState.allowedCards()
                for i, card in enumerate(player):
                    handSize = len(player)
                    x, y = self.positions[card]
                    y = 2*(8-y)
                    x = 2*(x-1)
                    textureRect = pygame.Rect(x*self.cellSizex, y*self.cellSizey, self.cellSizex, self.cellSizey)
                    if card in allowedCards:
                        spritePoint = Vector2(10-handSize//2+i,18).elementwise()*self.cellSize
                    else:
                        spritePoint = Vector2(10-handSize//2+i,19).elementwise()*self.cellSize
                    self.gameState.sprites[card] = spritePoint
                    self.window.blit(self.cardsTexture, spritePoint, textureRect)
            elif k == 1 and self.gameState.current_player != k:
                for i, card in enumerate(player):
                    x, y = self.positions[card]
                    y = 2*(8-y)
                    x = 2*(x-1)
                    textureRect = pygame.Rect(x*self.cellSizex, y*self.cellSizey, self.cellSizex, self.cellSizey)
                    spritePoint = Vector2(0,10-handSize//2+i).elementwise()*self.cellSize
                    self.gameState.sprites[card] = spritePoint
                    self.window.blit(self.cardsTexture, spritePoint, textureRect)
            elif k == 1 and self.gameState.current_player == k:
                allowedCards = self.gameState.allowedCards()
                for i, card in enumerate(player):
                    handSize = len(player)
                    x, y = self.positions[card]
                    y = 2*(8-y)
                    x = 2*(x-1)
                    textureRect = pygame.Rect(x*self.cellSizex, y*self.cellSizey, self.cellSizex, self.cellSizey)
                    if card in allowedCards:
                        spritePoint = Vector2(1,10-handSize//2+i).elementwise()*self.cellSize
                    else:
                        spritePoint = Vector2(0,10-handSize//2+i).elementwise()*self.cellSize
                    self.gameState.sprites[card] = spritePoint
                    self.window.blit(self.cardsTexture, spritePoint, textureRect)
            elif k == 2 and self.gameState.current_player != k:
                for i, card in enumerate(player):
                    x, y = self.positions[card]
                    y = 2*(8-y)
                    x = 2*(x-1)
                    textureRect = pygame.Rect(x*self.cellSizex, y*self.cellSizey, self.cellSizex, self.cellSizey)
                    spritePoint = Vector2(10-handSize//2+i,0).elementwise()*self.cellSize
                    self.gameState.sprites[card] = spritePoint
                    self.window.blit(self.cardsTexture, spritePoint, textureRect)
            elif k == 2 and self.gameState.current_player == k:
                allowedCards = self.gameState.allowedCards()
                for i, card in enumerate(player):
                    handSize = len(player)
                    x, y = self.positions[card]
                    y = 2*(8-y)
                    x = 2*(x-1)
                    textureRect = pygame.Rect(x*self.cellSizex, y*self.cellSizey, self.cellSizex, self.cellSizey)
                    if card in allowedCards:
                        spritePoint = Vector2(10-handSize//2+i,1).elementwise()*self.cellSize
                    else:
                        spritePoint = Vector2(10-handSize//2+i,0).elementwise()*self.cellSize
                    self.gameState.sprites[card] = spritePoint
                    self.window.blit(self.cardsTexture, spritePoint, textureRect)
            elif k == 3 and self.gameState.current_player != k:
                for i, card in enumerate(player):
                    x, y = self.positions[card]
                    y = 2*(8-y)
                    x = 2*(x-1)
                    textureRect = pygame.Rect(x*self.cellSizex, y*self.cellSizey, self.cellSizex, self.cellSizey)
                    spritePoint = Vector2(19,10-handSize//2+i).elementwise()*self.cellSize
                    self.gameState.sprites[card] = spritePoint
                    self.window.blit(self.cardsTexture, spritePoint, textureRect)
            elif k == 3 and self.gameState.current_player == k:
                allowedCards = self.gameState.allowedCards()
                for i, card in enumerate(player):
                    handSize = len(player)
                    x, y = self.positions[card]
                    y = 2*(8-y)
                    x = 2*(x-1)
                    textureRect = pygame.Rect(x*self.cellSizex, y*self.cellSizey, self.cellSizex, self.cellSizey)
                    if card in allowedCards:
                        spritePoint = Vector2(18,10-handSize//2+i).elementwise()*self.cellSize
                    else:
                        spritePoint = Vector2(19,10-handSize//2+i).elementwise()*self.cellSize
                    self.gameState.sprites[card] = spritePoint
                    self.window.blit(self.cardsTexture, spritePoint, textureRect)

        pygame.display.update()    

    def run(self):
        while self.running:
            self.processInput()
            self.update()
            self.render()
            self.clock.tick(60)

userInterface = UserInterface()
userInterface.run()

pygame.quit()