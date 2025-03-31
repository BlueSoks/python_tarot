import os
import pygame
from pygame import Rect
from pygame.math import Vector2
import random as rd

pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)


os.environ['SDL_VIDEO_CENTERED'] = '1'

class Trick():
    def __init__(self):
        self.played = [None, None, None, None]
        self.suit = None
        
    def setSuit(self, suit):
        self.suit = suit
    
    def winner(self):
        if len([card for card in self.played if card[-1] == 'A']) > 0:
            trumps = [int(card[:-1]) for card in self.played if card[-1] == 'A']
            winner = str(max(trumps)) + 'A'
            index = self.played.index(winner)
            self.played = [None, None, None, None]
            return index
        else:
            suit_cards = [int(card[:-1]) for card in self.played if card[-1] == self.suit]
            winner = str(max(suit_cards)) + self.suit
            index = self.played.index(winner)
            return index
    
    def play_card(self, card, index):
        self.played[index] = card
        if self.suit == None and card != '0E':
            self.suit = card[-1]
            

class GameState():
    def __init__(self):
        self.worldSize = Vector2(26,26)
        self.deck = ['0E', '14H', '13H', '12H', '11H', '10H', '9H', '8H', '7H', '6H', '5H', '4H', '3H', '2H', '1H', '14C', '13C', '12C', '11C', '10C', '9C', '8C', '7C', '6C', '5C', '4C', '3C', '2C', '1C', '14D', '13D', '12D', '11D', '10D', '9D', '8D', '7D', '6D', '5D', '4D', '3D', '2D', '1D', '14S', '13S', '12S', '11S', '10S', '9S', '8S', '7S', '6S', '5S', '4S', '3S', '2S', '1S']
        for j in range(1, 22):
            self.deck += ['%sA' %j]
        rd.shuffle(self.deck)
        self.south = []
        self.north = []
        self.east = []
        self.west = []
        self.south_earned = []
        self.west_earned = []
        self.north_earned = []
        self.east_earned = []
        self.kitty = []
        self.kittyBuilding = False
        self.contracts = ['Small', 'Guard', 'Guard without', 'Guard against', 'pass']
        self.contract = None
        self.dealer_index = 0
        self.index_position = {0: 'South', 1: 'West', 2: 'North', 3: 'East'}
        self.players = [self.south, self.west, self.north, self.east]
        self.played_cards = [None, None, None, None]
        self.players_earned = [self.south_earned, self.west_earned, self.north_earned, self.east_earned]
        self.caller_index = None
        self.deal()
        self.previous_trick_winner = (self.dealer_index + 1) % 4
        self.current_player = self.previous_trick_winner
        self.roundStarted = False
        self.total_scores = 4*[0]
        self.trick = Trick()
        self.trickOver = False
        self.betOver = False
        self.roundOver = False
        # x width on the sprite is 337 pixels and y height is 645 pixels
        # self.positions = {'0E': (5, 6), '14H': (3, 4), '13H': (3, 5), '12H': (2, 1), '11H': (3, 2), '10H': (3, 3), '9H': (2, 2), '8H': (2, 3), '7H': (2, 4), '6H': (2, 5), '5H': (10, 6), '4H': (9, 6), '3H': (8, 6), '2H': (7, 6), '1H': (6, 6), '14C': (3, 7), '13C': (2, 7), '12C': (1, 7), '11C': (5, 7), '10C': (4, 7), '9C': (10, 8), '8C': (9, 8), '7C': (8, 8), '6C': (7, 8), '5C': (6, 8), '4C': (5, 8), '3C': (4, 8), '2C': (3, 8), '1C': (2, 8), '14D': (2, 6), '13D': (1, 1), '12D': (1, 2), '11D': (4, 6), '10D': (3, 6), '9D': (1, 3), '8D': (1, 4), '7D': (1, 5), '6D': (1, 6), '5D': (10, 7), '4D': (9, 7), '3D': (8, 7), '2D': (7, 7), '1D': (6, 7), '14S': (4, 1), '13S': (4, 2), '12S': (4, 3), '11S': (5, 3), '10S': (5, 4), '9S': (4, 4), '8S': (10, 5), '7S': (9, 5), '6S': (8, 5), '5S': (7, 5), '4S': (6, 5), '3S': (5, 5), '2S': (4, 5), '1S': (3, 5), '1A': (5, 2), '2A': (5, 1), '3A': (6, 4), '4A': (7, 4), '5A': (8, 4), '6A': (9, 4), '7A': (10, 4), '8A': (6, 3), '9A': (6, 2), '10A': (6, 1), '11A': (7, 3), '12A': (7, 2), '13A': (7, 1), '14A': (8, 3), '15A': (9, 3), '16A': (10, 3), '17A': (8, 2), '18A': (8, 1), '19A': (9, 2), '20A': (9, 1), '21A': (10, 2)}
                    
            
    
    def deal(self):
        self.deck = ['0E', '14H', '13H', '12H', '11H', '10H', '9H', '8H', '7H', '6H', '5H', '4H', '3H', '2H', '1H', '14C', '13C', '12C', '11C', '10C', '9C', '8C', '7C', '6C', '5C', '4C', '3C', '2C', '1C', '14D', '13D', '12D', '11D', '10D', '9D', '8D', '7D', '6D', '5D', '4D', '3D', '2D', '1D', '14S', '13S', '12S', '11S', '10S', '9S', '8S', '7S', '6S', '5S', '4S', '3S', '2S', '1S']
        for j in range(1, 22):
            self.deck += ['%sA' %j]
        rd.shuffle(self.deck)
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
                max_trump_played = max([int(card[:-1]) for card in self.trick.played if card != None and card[-1] == 'A'])
                if len([card for card in player if card[-1] == 'A' and int(card[:-1])>max_trump_played]) > 0:
                    return [card for card in player if card[-1] == 'A' and int(card[:-1])>max_trump_played]
                else:
                    return [card for card in player if card[-1] == 'A']
            else:
                return player
        else:
            if len([card for card in player if card[-1] == self.trick.suit]) > 0:
                return [card for card in player if card[-1] == self.trick.suit]
            else:
                if len([card for card in player if card[-1] == 'A']) > 0:
                    if len([int(card[:-1]) for card in self.trick.played if card != None and card[-1] == 'A']) > 0:
                        max_trump_played = max([int(card[:-1]) for card in self.trick.played if card != None and card[-1] == 'A'])
                        if len([card for card in player if card[-1] == 'A' and int(card[:-1])>max_trump_played]) > 0:
                            return [card for card in player if card[-1] == 'A' and int(card[:-1])>max_trump_played]
                        else:
                            return [card for card in player if card[-1] == 'A']
                    else:
                        return [card for card in player if card[-1] == 'A']
                else:
                    return player
            
        
    def update(self, card):
        
        # if card == 'betOver':
        #     self.betOver = False
        #     if self.contract == None:
        #         self.dealer_index += 1
        #         self.previous_trick_winner = (self.dealer_index + 1) % 4
        #         self.current_player = self.previous_trick_winner
        #         self.deal()
        #     else:
        #         self.kittyBuilding = True
        
        
        if self.roundStarted == False:
            if self.betOver == True and card == 'betOver':
                self.betOver = False
                if self.contract == None:
                    self.dealer_index += 1
                    self.previous_trick_winner = (self.dealer_index + 1) % 4
                    self.current_player = self.previous_trick_winner
                    self.deal()
                else:
                    self.kittyBuilding = True
                    self.roundStarted = True
            elif self.betOver == False:
                if card != 'pass':
                    self.caller_index = self.current_player
                    self.contract = card
                self.current_player = (self.current_player + 1) % 4
                if self.current_player == (self.dealer_index + 1) % 4:
                    self.betOver = True
        else:
            if self.kittyBuilding:
                self.players[self.caller_index] += self.kitty
                self.kitty = []
            if self.trickOver == True and card == 'nextTrick':
                self.trickOver = False
                self.previous_trick_winner = self.trick.winner()
                self.players_earned[self.previous_trick_winner] += self.trick.played
                self.trick = Trick()
                self.played_cards = [None, None, None, None]
                self.current_player = self.previous_trick_winner
            if card in self.allowedCards():
                self.players[self.current_player].remove(card)
                self.played_cards[self.current_player] = card
                self.trick.play_card(card, self.current_player)
                if len([card for card in self.trick.played if card != None]) == 4:
                    self.trickOver = True
                else:
                    self.current_player = (self.current_player + 1) % 4
                flag = True
                for player in self.players:
                    if len(player) > 0:
                        flag = False
                if flag:
                    self.roundOver = True
            if self.roundOver and card == 'nextRound':
                self.roundOver = False
                self.contract = None
                self.roundStarted = False
                self.dealer_index += 1
                self.previous_trick_winner = (self.dealer_index + 1) % 4
                self.current_player = self.previous_trick_winner
                self.deal()
            

class UserInterface():
    def __init__(self):
        pygame.init()

        # Game state
        self.gameState = GameState()

        # Rendering properties
        self.cellSizex = 35
        self.cellSizey = 35
        self.cellSize = Vector2(self.cellSizex, self.cellSizey)
        # self.buttonNextTrickTexture = my_font.render('Next trick', False, (255, 255, 255))
        # self.buttonNextTrickTexture = pygame.transform.scale(self.buttonNextTrickTexture, (self.cellSizex, self.cellSizey))
        self.passTexture = my_font.render('Pass', False, (255, 255, 255))
        self.passTexture = pygame.transform.scale(self.passTexture, (self.cellSizex, self.cellSizey))
        self.smallTexture = my_font.render('Small', False, (255, 255, 255))
        self.smallTexture = pygame.transform.scale(self.smallTexture, (self.cellSizex, self.cellSizey))
        self.guardTexture = my_font.render('Guard', False, (255, 255, 255))
        self.guardTexture = pygame.transform.scale(self.guardTexture, (self.cellSizex, self.cellSizey))
        self.withoutTexture = my_font.render('Without', False, (255, 255, 255))
        self.withoutTexture = pygame.transform.scale(self.withoutTexture, (self.cellSizex, self.cellSizey))
        self.againstTexture = my_font.render('Against', False, (255, 255, 255))
        self.againstTexture = pygame.transform.scale(self.againstTexture, (self.cellSizex, self.cellSizey))
        self.contractSprites = [self.smallTexture, self.guardTexture, self.withoutTexture, self.againstTexture, self.passTexture]
        
        self.unitsTexture = pygame.image.load("units.png")
        self.cardsTexture = pygame.image.load("cards.png")
        self.cardsTexture = pygame.transform.scale(self.cardsTexture, (20*self.cellSizex, 16*self.cellSizey))
        
        self.buttonNextTrickTexture = pygame.image.load("nextTrick.png")
        self.buttonNextTrickTexture = pygame.transform.scale(self.buttonNextTrickTexture, (self.cellSizex, self.cellSizey))
        
        self.buttonBetOverTexture = pygame.image.load("betOver.png")
        self.buttonBetOverTexture = pygame.transform.scale(self.buttonBetOverTexture, (self.cellSizex, self.cellSizey))
        
        # Position of the card sprites within the sprite image
        self.positions = {'0E': (5, 6), '14H': (3, 4), '13H': (3, 5), '12H': (2, 1), '11H': (3, 2), '10H': (3, 3), '9H': (2, 2), '8H': (2, 3), '7H': (2, 4), '6H': (2, 5), '5H': (10, 6), '4H': (9, 6), '3H': (8, 6), '2H': (7, 6), '1H': (6, 6), '14C': (3, 7), '13C': (2, 7), '12C': (1, 7), '11C': (5, 7), '10C': (4, 7), '9C': (10, 8), '8C': (9, 8), '7C': (8, 8), '6C': (7, 8), '5C': (6, 8), '4C': (5, 8), '3C': (4, 8), '2C': (3, 8), '1C': (2, 8), '14D': (2, 6), '13D': (1, 1), '12D': (1, 2), '11D': (4, 6), '10D': (3, 6), '9D': (1, 3), '8D': (1, 4), '7D': (1, 5), '6D': (1, 6), '5D': (10, 7), '4D': (9, 7), '3D': (8, 7), '2D': (7, 7), '1D': (6, 7), '14S': (4, 1), '13S': (4, 2), '12S': (4, 3), '11S': (5, 3), '10S': (5, 4), '9S': (4, 4), '8S': (10, 5), '7S': (9, 5), '6S': (8, 5), '5S': (7, 5), '4S': (6, 5), '3S': (5, 5), '2S': (4, 5), '1S': (1, 3), '1A': (5, 2), '2A': (5, 1), '3A': (6, 4), '4A': (7, 4), '5A': (8, 4), '6A': (9, 4), '7A': (10, 4), '8A': (6, 3), '9A': (6, 2), '10A': (6, 1), '11A': (7, 3), '12A': (7, 2), '13A': (7, 1), '14A': (8, 3), '15A': (9, 3), '16A': (10, 3), '17A': (8, 2), '18A': (8, 1), '19A': (9, 2), '20A': (9, 1), '21A': (10, 2)}
        self.played_card_position = None
        
        # Window
        windowSize = self.gameState.worldSize.elementwise() * self.cellSize
        self.window = pygame.display.set_mode((int(windowSize.x),int(windowSize.y)))
        pygame.display.set_caption("Discover Python & Patterns - https://www.patternsgameprog.com")
        pygame.display.set_icon(pygame.image.load("icon.png"))
        self.moveTankCommand = Vector2(0,0)
        self.sprites = {}

        # Loop properties
        self.clock = pygame.time.Clock()
        self.running = True


    def processInput(self):
        self.played_card_position = None
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                self.played_card_position = pos
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
        if self.played_card_position == None:
            pass
        else:
            x = self.played_card_position[0]
            y = self.played_card_position[1]
            for card, position in self.sprites.items():
                if x >= position[0] and x <= position[0]+50 and y >= position[1] and y <= position[1] + 50:
                    self.gameState.update(card)
            else:
                pass

    def render(self):
        self.window.fill((0, 0, 0))
        self.sprites = {}
        
        if not self.gameState.roundStarted and not self.gameState.betOver:
            if self.gameState.contract == None:
                k = -1
            else:
                k = self.gameState.contracts.index(self.gameState.contract)
            for l in range(k + 1, len(self.gameState.contracts)):
                contract = self.gameState.contracts[l]
                textureRect = pygame.Rect(0, 0, self.cellSizex, self.cellSizey)
                spritePoint = Vector2(6+2*l,15).elementwise()*self.cellSize
                self.sprites[contract] = spritePoint
                self.window.blit(self.contractSprites[l], spritePoint, textureRect)
        
        if self.gameState.betOver == True:
            textureRect = pygame.Rect(0, 0, self.cellSizex, self.cellSizey)
            spritePoint = Vector2(13,17).elementwise()*self.cellSize
            self.sprites['betOver'] = spritePoint
            # self.window.blit(self.button_next_trick_texture, spritePoint, textureRect)
            self.window.blit(self.buttonNextTrickTexture, spritePoint, textureRect)
        
        if self.gameState.kittyBuilding:
            for k, card in enumerate(self.gameState.kitty):
                x, y = self.positions[card]
                y = 2*(8-y)
                x = 2*(x-1)
                textureRect = pygame.Rect(x*self.cellSizex, y*self.cellSizey, self.cellSizex, self.cellSizey)
                spritePoint = Vector2(9+k, 13).elementwise()*self.cellSize
                self.sprites[card] = spritePoint
                self.window.blit(self.cardsTexture, spritePoint, textureRect)
            textureRect = pygame.Rect(0, 0, self.cellSizex, self.cellSizey)
            spritePoint = Vector2(13,17).elementwise()*self.cellSize
            self.sprites['kittySeen'] = spritePoint
            self.window.blit(self.buttonNextTrickTexture, spritePoint, textureRect)
        
        if self.gameState.trickOver == True:
            textureRect = pygame.Rect(0, 0, self.cellSizex, self.cellSizey)
            spritePoint = Vector2(13,17).elementwise()*self.cellSize
            self.sprites['nextTrick'] = spritePoint
            # self.window.blit(self.button_next_trick_texture, spritePoint, textureRect)
            self.window.blit(self.buttonNextTrickTexture, spritePoint, textureRect)
        
        if self.gameState.roundOver == True:
            textureRect = pygame.Rect(0, 0, self.cellSizex, self.cellSizey)
            spritePoint = Vector2(13,17).elementwise()*self.cellSize
            self.sprites['nextRound'] = spritePoint
            # self.window.blit(self.button_next_trick_texture, spritePoint, textureRect)
            self.window.blit(self.buttonNextTrickTexture, spritePoint, textureRect)
        
        for i,card in enumerate(self.gameState.played_cards):
            if card != None:
                if i == 0:
                    x, y = self.positions[card]
                    y = 2*(8-y)
                    x = 2*(x-1)
                    textureRect = pygame.Rect(x*self.cellSizex, y*self.cellSizey, self.cellSizex, self.cellSizey)
                    spritePoint = Vector2(13,14).elementwise()*self.cellSize
                    self.sprites[card] = spritePoint
                    self.window.blit(self.cardsTexture, spritePoint, textureRect)
                elif i == 1:
                    x, y = self.positions[card]
                    y = 2*(8-y)
                    x = 2*(x-1)
                    textureRect = pygame.Rect(x*self.cellSizex, y*self.cellSizey, self.cellSizex, self.cellSizey)
                    spritePoint = Vector2(12,13).elementwise()*self.cellSize
                    self.sprites[card] = spritePoint
                    self.window.blit(self.cardsTexture, spritePoint, textureRect)
                elif i == 2:
                    x, y = self.positions[card]
                    y = 2*(8-y)
                    x = 2*(x-1)
                    textureRect = pygame.Rect(x*self.cellSizex, y*self.cellSizey, self.cellSizex, self.cellSizey)
                    spritePoint = Vector2(13,12).elementwise()*self.cellSize
                    self.sprites[card] = spritePoint
                    self.window.blit(self.cardsTexture, spritePoint, textureRect)
                elif i == 3:
                    x, y = self.positions[card]
                    y = 2*(8-y)
                    x = 2*(x-1)
                    textureRect = pygame.Rect(x*self.cellSizex, y*self.cellSizey, self.cellSizex, self.cellSizey)
                    spritePoint = Vector2(14,13).elementwise()*self.cellSize
                    self.sprites[card] = spritePoint
                    self.window.blit(self.cardsTexture, spritePoint, textureRect)
        
        
        for k,player in enumerate(self.gameState.players):
            if k == 0 and self.gameState.current_player != k:
                for i, card in enumerate(player):
                    handSize = len(player)
                    x, y = self.positions[card]
                    y = 2*(8-y)
                    x = 2*(x-1)
                    textureRect = pygame.Rect(x*self.cellSizex, y*self.cellSizey, self.cellSizex, self.cellSizey)
                    spritePoint = Vector2(13-handSize//2+i,25).elementwise()*self.cellSize
                    self.sprites[card] = spritePoint
                    self.window.blit(self.cardsTexture, spritePoint, textureRect)
            elif k == 0 and self.gameState.current_player == k and self.gameState.kittyBuilding == False:
                allowedCards = self.gameState.allowedCards()
                for i, card in enumerate(player):
                    handSize = len(player)
                    x, y = self.positions[card]
                    y = 2*(8-y)
                    x = 2*(x-1)
                    textureRect = pygame.Rect(x*self.cellSizex, y*self.cellSizey, self.cellSizex, self.cellSizey)
                    if card in allowedCards and not(self.gameState.trickOver) and self.gameState.roundStarted:
                        spritePoint = Vector2(13-handSize//2+i,24).elementwise()*self.cellSize
                    else:
                        spritePoint = Vector2(13-handSize//2+i,25).elementwise()*self.cellSize
                    self.sprites[card] = spritePoint
                    self.window.blit(self.cardsTexture, spritePoint, textureRect)
            elif k == 0 and self.gameState.current_player == k and self.gameState.kittyBuilding:
                allowedCards = self.gameState.allowedCards()
                for i, card in enumerate(player):
                    handSize = len(player)
                    x, y = self.positions[card]
                    y = 2*(8-y)
                    x = 2*(x-1)
                    textureRect = pygame.Rect(x*self.cellSizex, y*self.cellSizey, self.cellSizex, self.cellSizey)
                    if card in allowedCards and not(self.gameState.trickOver) and self.gameState.roundStarted:
                        spritePoint = Vector2(13-handSize//2+i,24).elementwise()*self.cellSize
                    else:
                        spritePoint = Vector2(13-handSize//2+i,25).elementwise()*self.cellSize
                    self.sprites[card] = spritePoint
                    self.window.blit(self.cardsTexture, spritePoint, textureRect)
            elif k == 1 and self.gameState.current_player != k:
                for i, card in enumerate(player):
                    handSize = len(player)
                    x, y = self.positions[card]
                    y = 2*(8-y)
                    x = 2*(x-1)
                    textureRect = pygame.Rect(x*self.cellSizex, y*self.cellSizey, self.cellSizex, self.cellSizey)
                    spritePoint = Vector2(0,13-handSize//2+i).elementwise()*self.cellSize
                    self.sprites[card] = spritePoint
                    self.window.blit(self.cardsTexture, spritePoint, textureRect)
            elif k == 1 and self.gameState.current_player == k and self.gameState.kittyBuilding == False:
                allowedCards = self.gameState.allowedCards()
                for i, card in enumerate(player):
                    handSize = len(player)
                    x, y = self.positions[card]
                    y = 2*(8-y)
                    x = 2*(x-1)
                    textureRect = pygame.Rect(x*self.cellSizex, y*self.cellSizey, self.cellSizex, self.cellSizey)
                    if card in allowedCards and not(self.gameState.trickOver) and self.gameState.roundStarted:
                        spritePoint = Vector2(1,13-handSize//2+i).elementwise()*self.cellSize
                    else:
                        spritePoint = Vector2(0,13-handSize//2+i).elementwise()*self.cellSize
                    self.sprites[card] = spritePoint
                    self.window.blit(self.cardsTexture, spritePoint, textureRect)
            elif k == 1 and self.gameState.current_player == k and self.gameState.kittyBuilding:
                allowedCards = self.gameState.allowedCards()
                for i, card in enumerate(player):
                    handSize = len(player)
                    x, y = self.positions[card]
                    y = 2*(8-y)
                    x = 2*(x-1)
                    textureRect = pygame.Rect(x*self.cellSizex, y*self.cellSizey, self.cellSizex, self.cellSizey)
                    if card in allowedCards and not(self.gameState.trickOver) and self.gameState.roundStarted:
                        spritePoint = Vector2(1,13-handSize//2+i).elementwise()*self.cellSize
                    else:
                        spritePoint = Vector2(0,13-handSize//2+i).elementwise()*self.cellSize
                    self.sprites[card] = spritePoint
                    self.window.blit(self.cardsTexture, spritePoint, textureRect)
            elif k == 2 and self.gameState.current_player != k:
                for i, card in enumerate(player):
                    handSize = len(player)
                    x, y = self.positions[card]
                    y = 2*(8-y)
                    x = 2*(x-1)
                    textureRect = pygame.Rect(x*self.cellSizex, y*self.cellSizey, self.cellSizex, self.cellSizey)
                    spritePoint = Vector2(13-handSize//2+i,0).elementwise()*self.cellSize
                    self.sprites[card] = spritePoint
                    self.window.blit(self.cardsTexture, spritePoint, textureRect)
            elif k == 2 and self.gameState.current_player == k and self.gameState.kittyBuilding == False:
                allowedCards = self.gameState.allowedCards()
                for i, card in enumerate(player):
                    handSize = len(player)
                    x, y = self.positions[card]
                    y = 2*(8-y)
                    x = 2*(x-1)
                    textureRect = pygame.Rect(x*self.cellSizex, y*self.cellSizey, self.cellSizex, self.cellSizey)
                    if card in allowedCards and not(self.gameState.trickOver) and self.gameState.roundStarted:
                        spritePoint = Vector2(13-handSize//2+i,1).elementwise()*self.cellSize
                    else:
                        spritePoint = Vector2(13-handSize//2+i,0).elementwise()*self.cellSize
                    self.sprites[card] = spritePoint
                    self.window.blit(self.cardsTexture, spritePoint, textureRect)
            elif k == 2 and self.gameState.current_player == k and self.gameState.kittyBuilding:
                allowedCards = self.gameState.allowedCards()
                for i, card in enumerate(player):
                    handSize = len(player)
                    x, y = self.positions[card]
                    y = 2*(8-y)
                    x = 2*(x-1)
                    textureRect = pygame.Rect(x*self.cellSizex, y*self.cellSizey, self.cellSizex, self.cellSizey)
                    if card in allowedCards and not(self.gameState.trickOver) and self.gameState.roundStarted:
                        spritePoint = Vector2(13-handSize//2+i,1).elementwise()*self.cellSize
                    else:
                        spritePoint = Vector2(13-handSize//2+i,0).elementwise()*self.cellSize
                    self.sprites[card] = spritePoint
                    self.window.blit(self.cardsTexture, spritePoint, textureRect)
            elif k == 3 and self.gameState.current_player != k:
                for i, card in enumerate(player):
                    handSize = len(player)
                    x, y = self.positions[card]
                    y = 2*(8-y)
                    x = 2*(x-1)
                    textureRect = pygame.Rect(x*self.cellSizex, y*self.cellSizey, self.cellSizex, self.cellSizey)
                    spritePoint = Vector2(25,13-handSize//2+i).elementwise()*self.cellSize
                    self.sprites[card] = spritePoint
                    self.window.blit(self.cardsTexture, spritePoint, textureRect)
            elif k == 3 and self.gameState.current_player == k and self.gameState.kittyBuilding == False:
                allowedCards = self.gameState.allowedCards()
                for i, card in enumerate(player):
                    handSize = len(player)
                    x, y = self.positions[card]
                    y = 2*(8-y)
                    x = 2*(x-1)
                    textureRect = pygame.Rect(x*self.cellSizex, y*self.cellSizey, self.cellSizex, self.cellSizey)
                    if card in allowedCards and not(self.gameState.trickOver) and self.gameState.roundStarted:
                        spritePoint = Vector2(24,13-handSize//2+i).elementwise()*self.cellSize
                    else:
                        spritePoint = Vector2(25,13-handSize//2+i).elementwise()*self.cellSize
                    self.sprites[card] = spritePoint
                    self.window.blit(self.cardsTexture, spritePoint, textureRect)
            elif k == 3 and self.gameState.current_player == k and self.gameState.kittyBuilding:
                allowedCards = self.gameState.allowedCards()
                for i, card in enumerate(player):
                    handSize = len(player)
                    x, y = self.positions[card]
                    y = 2*(8-y)
                    x = 2*(x-1)
                    textureRect = pygame.Rect(x*self.cellSizex, y*self.cellSizey, self.cellSizex, self.cellSizey)
                    if card in allowedCards and not(self.gameState.trickOver) and self.gameState.roundStarted:
                        spritePoint = Vector2(24,13-handSize//2+i).elementwise()*self.cellSize
                    else:
                        spritePoint = Vector2(25,13-handSize//2+i).elementwise()*self.cellSize
                    self.sprites[card] = spritePoint
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