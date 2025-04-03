import os
import pygame
from pygame import Rect
from pygame.math import Vector2
import random as rd

pygame.font.init()
my_font = pygame.font.SysFont('Arial', 30)


def sortHand(player):
    clubsValues = [int(item[:-1]) for item in player if item[-1] == 'C']
    clubsValues.sort()
    spadesValues = [int(item[:-1]) for item in player if item[-1] == 'S']
    spadesValues.sort()
    diamondsValues = [int(item[:-1]) for item in player if item[-1] == 'D']
    diamondsValues.sort()
    heartsValues = [int(item[:-1]) for item in player if item[-1] == 'H']
    heartsValues.sort()
    trumpsValues = [int(item[:-1]) for item in player if item[-1] == 'A']
    trumpsValues.sort()
    excuse = [item for item in player if item[-1] == 'E']
    clubs = [str(item) + 'C' for item in clubsValues]
    spades = [str(item) + 'S' for item in spadesValues]
    diamonds = [str(item) + 'D' for item in diamondsValues]
    hearts = [str(item) + 'H' for item in heartsValues]
    trumps = [str(item) + 'A' for item in trumpsValues]
    return (clubs + spades + diamonds + hearts + trumps + excuse)
    
    

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
        self.players = [self.south, self.west, self.north, self.east]
        self.southEarned = []
        self.westEarned = []
        self.northEarned = []
        self.eastEarned = []
        self.playersEarned = [self.southEarned, self.westEarned, self.northEarned, self.eastEarned]
        self.southScore = 0
        self.westScore = 0
        self.northScore = 0
        self.eastScore = 0
        self.scores = [self.southScore, self.westScore, self.northScore, self.eastScore]
        self.kitty = []
        self.contracts = ['Small', 'Guard', 'Without', 'Against', 'pass']
        self.contract = None
        self.dealerIndex = 0
        self.indexPosition = {0: 'South', 1: 'West', 2: 'North', 3: 'East'}
        self.playedCards = [None, None, None, None]
        self.callerIndex = None
        self.oudlers = 0
        self.deal()
        self.excusePlayer = None
        self.petitAuBout = None
        
        # Attribute to adjust the final score based on who played the excuse
        # 1 means the attack played the excuse and the defense won the trick, 0 means nothing needds to be adjusted, -1 means defense played the excuse and the attack won the trick
        self.adjustScore = 0
        self.previousTrickWinner = (self.dealerIndex + 1) % 4
        self.currentPlayer = self.previousTrickWinner
        self.trick = Trick()
        self.attackScore = 0
        self.defenseScore = 0
        self.winner = None
        
        # Variables describing the game state. Only one should be true at a time
        self.betStarted = True
        self.betOver = False
        self.kittyRevealed = False
        self.kittyBuilding = False
        self.kittyOver = False
        self.roundStarted = False
        self.trickOver = False
        self.roundOver = False
        self.roundSummary = False
        self.scoreDisplayed = False
        
        # x width on the sprite is 337 pixels and y height is 645 pixels
        # self.positions = {'0E': (5, 6), '14H': (3, 4), '13H': (3, 5), '12H': (2, 1), '11H': (3, 2), '10H': (3, 3), '9H': (2, 2), '8H': (2, 3), '7H': (2, 4), '6H': (2, 5), '5H': (10, 6), '4H': (9, 6), '3H': (8, 6), '2H': (7, 6), '1H': (6, 6), '14C': (3, 7), '13C': (2, 7), '12C': (1, 7), '11C': (5, 7), '10C': (4, 7), '9C': (10, 8), '8C': (9, 8), '7C': (8, 8), '6C': (7, 8), '5C': (6, 8), '4C': (5, 8), '3C': (4, 8), '2C': (3, 8), '1C': (2, 8), '14D': (2, 6), '13D': (1, 1), '12D': (1, 2), '11D': (4, 6), '10D': (3, 6), '9D': (1, 3), '8D': (1, 4), '7D': (1, 5), '6D': (1, 6), '5D': (10, 7), '4D': (9, 7), '3D': (8, 7), '2D': (7, 7), '1D': (6, 7), '14S': (4, 1), '13S': (4, 2), '12S': (4, 3), '11S': (5, 3), '10S': (5, 4), '9S': (4, 4), '8S': (10, 5), '7S': (9, 5), '6S': (8, 5), '5S': (7, 5), '4S': (6, 5), '3S': (5, 5), '2S': (4, 5), '1S': (3, 5), '1A': (5, 2), '2A': (5, 1), '3A': (6, 4), '4A': (7, 4), '5A': (8, 4), '6A': (9, 4), '7A': (10, 4), '8A': (6, 3), '9A': (6, 2), '10A': (6, 1), '11A': (7, 3), '12A': (7, 2), '13A': (7, 1), '14A': (8, 3), '15A': (9, 3), '16A': (10, 3), '17A': (8, 2), '18A': (8, 1), '19A': (9, 2), '20A': (9, 1), '21A': (10, 2)}
                    
            
    
    def deal(self):
        self.deck = ['0E', '14H', '13H', '12H', '11H', '10H', '9H', '8H', '7H', '6H', '5H', '4H', '3H', '2H', '1H', '14C', '13C', '12C', '11C', '10C', '9C', '8C', '7C', '6C', '5C', '4C', '3C', '2C', '1C', '14D', '13D', '12D', '11D', '10D', '9D', '8D', '7D', '6D', '5D', '4D', '3D', '2D', '1D', '14S', '13S', '12S', '11S', '10S', '9S', '8S', '7S', '6S', '5S', '4S', '3S', '2S', '1S']
        for j in range(1, 22):
            self.deck += ['%sA' %j]
        rd.shuffle(self.deck)
        counter = 0
        currentPlayerIndex = (self.dealerIndex + 1) % 4
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
                self.players[currentPlayerIndex] += cards
                # print(self.players[currentPlayerIndex])
                currentPlayerIndex = (currentPlayerIndex + 1) % 4
                counter += 1
        self.previousTrickWinner = self.dealerIndex + 1
        for k in range(len(self.players)):
            # self.players[k] = [item for item in self.players[k] if item[-1] == 'C'] + [item for item in self.players[k] if item[-1] == 'S'] + [item for item in self.players[k] if item[-1] == 'D'] + [item for item in self.players[k] if item[-1] == 'H'] + [item for item in self.players[k] if item[-1] == 'A'] + [item for item in self.players[k] if item[-1] == 'E']
            self.players[k] = sortHand(self.players[k])
    
    def allowedCards(self):
        player = self.players[self.currentPlayer]
        if self.trick.suit == None:
            return player
        elif self.trick.suit == 'A':
            if len([card for card in player if card[-1] == 'A']) > 0:
                max_trump_played = max([int(card[:-1]) for card in self.trick.played if card != None and card[-1] == 'A'])
                if len([card for card in player if card[-1] == 'A' and int(card[:-1])>max_trump_played]) > 0:
                    return [card for card in player if card[-1] == 'A' and int(card[:-1])>max_trump_played] + ['0E']
                else:
                    return [card for card in player if card[-1] == 'A'] + ['0E']
            else:
                return player
        else:
            if len([card for card in player if card[-1] == self.trick.suit]) > 0:
                return [card for card in player if card[-1] == self.trick.suit] + ['0E']
            else:
                if len([card for card in player if card[-1] == 'A']) > 0:
                    if len([int(card[:-1]) for card in self.trick.played if card != None and card[-1] == 'A']) > 0:
                        max_trump_played = max([int(card[:-1]) for card in self.trick.played if card != None and card[-1] == 'A'])
                        if len([card for card in player if card[-1] == 'A' and int(card[:-1])>max_trump_played]) > 0:
                            return [card for card in player if card[-1] == 'A' and int(card[:-1])>max_trump_played] + ['0E']
                        else:
                            return [card for card in player if card[-1] == 'A'] + ['0E']
                    else:
                        return [card for card in player if card[-1] == 'A'] + ['0E']
                else:
                    return player
            
    
    def calculateScore(self):
        self.attackScore = 0
        self.defenseScore = 0
        for k,player in enumerate(self.playersEarned):
            if k == self.callerIndex:
                for card in player:
                    # print(player)
                    if card == '0E' or card == '1A' or card == '21A' or (card[:-1] == '14' and card[-1] != 'A'):
                        self.attackScore += 4.5
                    elif card[:-1] == '13' and card[-1] != 'A':
                        self.attackScore += 3.5
                    elif card[:-1] == '12' and card[-1] != 'A':
                        self.attackScore += 2.5
                    elif card[:-1] == '11' and card[-1] != 'A':
                        self.attackScore += 1.5
                    else:
                        self.attackScore += 0.5
            else:
                for card in player:
                    if card == '0E' or card == '1A' or card == '21A' or (card[:-1] == '14' and card[-1] != 'A'):
                        self.defenseScore += 4.5
                    elif card[:-1] == '13' and card[-1] != 'A':
                        self.defenseScore += 3.5
                    elif card[:-1] == '12' and card[-1] != 'A':
                        self.defenseScore += 2.5
                    elif card[:-1] == '11' and card[-1] != 'A':
                        self.defenseScore += 1.5
                    else:
                        self.defenseScore += 0.5
    
    def addKitty(self):
        if self.contract in ['Small', 'Guard', 'Without']:
            self.playersEarned[self.callerIndex] += self.kitty
        elif self.contract == 'Against':
            self.playersEarned[(self.callerIndex + 1) % 4] += self.kitty
        else:
            pass
    
    
    
    def calculateTotalScore(self):
        if self.petitAuBout == 'attack':
            petit = 10
        elif self.petitAuBout == 'defense':
            petit = -10
        self.petitAuBout = None
        if self.contract == 'Small':
            multiplier = 1
        elif self.contract == 'Guard':
            multiplier = 2
        elif self.contract == 'Without':
            multiplier = 4
        elif self.contract == 'Against':
            multiplier = 6
        result = self.winnings()
        if result > 0:
            self.winner = 'Attack'
            score = (25 + result + petit)*multiplier
        else:
            self.winner = 'Defense'
            score = -(25 - result + petit)*multiplier
        for j in range(4):
            if j == self.callerIndex:
                self.scores[j] += 3*score
            else:
                self.scores[j] -= score
    
    def winnings(self):
        callerEarned = self.playersEarned[self.callerIndex]
        self.oudlers = 0
        for card in callerEarned:
            if card in ['0E', '1A', '21A']:
                self.oudlers += 1
        if self.oudlers == 0:
            return (self.attackScore - 56)
        elif self.oudlers == 1:
            return (self.attackScore - 51)
        elif self.oudlers == 2:
            return (self.attackScore - 41)
        elif self.oudlers == 3:
            return (self.attackScore - 36)
        
        
    
    def update(self, card):
        
        # Betting phase of the game: updating current contract
        
        if self.betStarted:
            if card != 'pass':
                self.callerIndex = self.currentPlayer
                self.contract = card
            self.currentPlayer = (self.currentPlayer + 1) % 4
            if self.currentPlayer == (self.dealerIndex + 1) % 4:
                self.betOver = True
                self.betStarted = False
        
        if self.betOver:
            if card == 'betOver':
                print(self.contract)
                if self.contract == None:
                    self.dealerIndex += 1
                    self.previousTrickWinner = (self.dealerIndex + 1) % 4
                    self.currentPlayer = self.previousTrickWinner
                    self.deal()
                    self.betStarted = True
                    self.betOver = False
                elif self.contract in ['Small', 'Guard']:
                    self.betOver = False
                    self.kittyRevealed = True
                elif self.contract in ['Without', 'Against']:
                    self.betOver = False
                    self.roundStarted = True
        
        # Confirmation that the kitty was seen before kitty building phase
        
        if self.kittyRevealed:
            if card == 'kittySeen':
                self.players[self.callerIndex] += self.kitty
                self.players[self.callerIndex] = sortHand(self.players[self.callerIndex])
                self.kitty = []
                self.kittyRevealed = False
                self.kittyBuilding = True
        
        # Kitty building by selecting up to 6 cards from the current caller hand
        
        if self.kittyBuilding:
            if len(self.kitty) < 6:
                if card in self.players[self.callerIndex]:
                    self.kitty += [card]
                    self.players[self.callerIndex].remove(card)
                    if len(self.kitty) == 6:
                        self.kittyOver = True
                elif card in self.kitty:
                    self.kitty.remove(card)
                    self.players[self.callerIndex] += [card]
                    self.players[self.callerIndex] = sortHand(self.players[self.callerIndex])
                    if len(self.kitty) < 6:
                        self.kittyOver = False
            elif len(self.kitty) == 6:
                if card in self.kitty:
                    self.kitty.remove(card)
                    self.players[self.callerIndex] += [card]
                    self.players[self.callerIndex] = sortHand(self.players[self.callerIndex])
            if card == 'kittyOver':
                self.kittyBuilding = False
                self.kittyOver = False
                self.roundStarted = True
        
        
        # Main gameplay loop when the round is started
        
        
        if self.roundStarted:
        
            if self.trickOver == True and card == 'nextTrick':
                self.trickOver = False
                self.previousTrickWinner = self.trick.winner()
                self.playersEarned[self.previousTrickWinner] += self.trick.played
                if '0E' in self.trick.played:
                    self.excusePlayer = self.playedCards.index('0E')
                    if self.excusePlayer != self.callerIndex and self.previousTrickWinner != self.callerIndex:
                        pass
                    elif self.excusePlayer == self.callerIndex and self.previousTrickWinner != self.callerIndex:
                        self.playersEarned[self.previousTrickWinner].remove('0E')
                        self.playersEarned[self.excusePlayer] += ['0E']
                        self.adjustScore = 1
                    elif self.excusePlayer != self.callerIndex and self.previousTrickWinner == self.callerIndex:
                        self.playersEarned[self.previousTrickWinner].remove('0E')
                        self.playersEarned[self.excusePlayer] += ['0E']
                        self.adjustScore = -1
                self.calculateScore()
                flag = True
                for player in self.players:
                    if len(player) > 0:
                        flag = False
                if flag:
                    if '1A' in self.playedCards:
                        if self.callerIndex == self.previousTrickWinner:
                            self.petitAuBout = 'attack'
                        else:
                            self.petitAuBout = 'defense'
                    self.roundOver = True
                    self.trickOver = False
                self.trick = Trick()
                self.playedCards = [None, None, None, None]
                self.currentPlayer = self.previousTrickWinner
                
            if card in self.allowedCards():
                self.players[self.currentPlayer].remove(card)
                self.playedCards[self.currentPlayer] = card
                self.trick.play_card(card, self.currentPlayer)
                if len([card for card in self.trick.played if card != None]) == 4:
                    self.trickOver = True
                else:
                    self.currentPlayer = (self.currentPlayer + 1) % 4
                # flag = True
                # for player in self.players:
                #     if len(player) > 0:
                #         flag = False
                # if flag:
                #     self.roundOver = True
                #     self.trickOver = False
                
            if self.roundOver and card == 'nextRound':
                self.addKitty()
                self.roundOver = False
                self.roundStarted = False
                self.roundSummary = True
            
                
        if self.roundSummary:
            self.calculateScore()
            if self.adjustScore == 1:
                self.attackScore -= 0.5
                self.defenseScore += 0.5
            elif self.adjustScore == -1:
                self.attackScore += 0.5
                self.defenseScore -= 0.5
            self.adjustScore = 0
            self.excusePlayer = None
            self.calculateTotalScore()
            self.kitty = []
            if card == 'roundSeen':
                self.scoreDisplayed = True
                self.roundSummary = False
        
        
        if self.scoreDisplayed:
            if card == 'scoreSeen':
                self.scoreDisplayed = False
                self.dealerIndex += 1
                self.previousTrickWinner = (self.dealerIndex + 1) % 4
                self.currentPlayer = self.previousTrickWinner
                self.deal()
                self.contract = None
                self.betStarted = True
            

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
        
        # self.buttonBetOverTexture = pygame.image.load("betOver.png")
        # self.buttonBetOverTexture = pygame.transform.scale(self.buttonBetOverTexture, (self.cellSizex, self.cellSizey))
        
        # self.currentBetterTexture = None
        
        self.buttonBetOverTexture = my_font.render('Bet Over', False, (255, 255, 255))
        self.buttonBetOverTexture = pygame.transform.scale(self.buttonBetOverTexture, (self.cellSizex, self.cellSizey))
        
        self.buttonKittySeenTexture = my_font.render('Kitty Seen', False, (255, 255, 255))
        self.buttonKittySeenTexture = pygame.transform.scale(self.buttonKittySeenTexture, (self.cellSizex, self.cellSizey))
        
        self.buttonKittyOverTexture = my_font.render('Kitty Over', False, (255, 255, 255))
        self.buttonKittyOverTexture = pygame.transform.scale(self.buttonKittyOverTexture, (self.cellSizex, self.cellSizey))
        
        self.attackEarnedTexture = my_font.render('Attack Score: %s' %self.gameState.attackScore, False, (255, 255, 255))
        self.attackEarnedTexture = pygame.transform.scale(self.attackEarnedTexture, (3*self.cellSizex, self.cellSizey))
        
        self.defenseEarnedTexture = my_font.render('Defense Score: %s' %self.gameState.defenseScore, False, (255, 255, 255))
        self.defenseEarnedTexture = pygame.transform.scale(self.defenseEarnedTexture, (3*self.cellSizex, self.cellSizey))
        
        self.buttonRoundSummaryTexture = my_font.render('Round Summary', False, (255, 255, 255))
        self.buttonRoundSummaryTexture = pygame.transform.scale(self.buttonRoundSummaryTexture, (self.cellSizex, self.cellSizey))
        
        self.buttonRoundSeenTexture = my_font.render('Round Seen', False, (255, 255, 255))
        self.buttonRoundSeenTexture = pygame.transform.scale(self.buttonRoundSeenTexture, (self.cellSizex, self.cellSizey))
        
        self.buttonScoreSeenTexture = my_font.render('Score Seen', False, (255, 255, 255))
        self.buttonScoreSeenTexture = pygame.transform.scale(self.buttonScoreSeenTexture, (self.cellSizex, self.cellSizey))
        
        # Position of the card sprites within the sprite image
        self.positions = {'0E': (5, 6), '14H': (3, 4), '13H': (3, 5), '12H': (2, 1), '11H': (3, 2), '10H': (3, 3), '9H': (2, 2), '8H': (2, 3), '7H': (2, 4), '6H': (2, 5), '5H': (10, 6), '4H': (9, 6), '3H': (8, 6), '2H': (7, 6), '1H': (6, 6), '14C': (3, 7), '13C': (2, 7), '12C': (1, 7), '11C': (5, 7), '10C': (4, 7), '9C': (10, 8), '8C': (9, 8), '7C': (8, 8), '6C': (7, 8), '5C': (6, 8), '4C': (5, 8), '3C': (4, 8), '2C': (3, 8), '1C': (2, 8), '14D': (2, 6), '13D': (1, 1), '12D': (1, 2), '11D': (4, 6), '10D': (3, 6), '9D': (1, 3), '8D': (1, 4), '7D': (1, 5), '6D': (1, 6), '5D': (10, 7), '4D': (9, 7), '3D': (8, 7), '2D': (7, 7), '1D': (6, 7), '14S': (4, 1), '13S': (4, 2), '12S': (4, 3), '11S': (5, 3), '10S': (5, 4), '9S': (4, 4), '8S': (10, 5), '7S': (9, 5), '6S': (8, 5), '5S': (7, 5), '4S': (6, 5), '3S': (5, 5), '2S': (4, 5), '1S': (3, 1), '1A': (5, 2), '2A': (5, 1), '3A': (6, 4), '4A': (7, 4), '5A': (8, 4), '6A': (9, 4), '7A': (10, 4), '8A': (6, 3), '9A': (6, 2), '10A': (6, 1), '11A': (7, 3), '12A': (7, 2), '13A': (7, 1), '14A': (8, 3), '15A': (9, 3), '16A': (10, 3), '17A': (8, 2), '18A': (8, 1), '19A': (9, 2), '20A': (9, 1), '21A': (10, 2)}
        self.played_card_position = None
        
        # Window
        windowSize = self.gameState.worldSize.elementwise() * self.cellSize
        self.window = pygame.display.set_mode((int(windowSize.x),int(windowSize.y)))
        pygame.display.set_caption("Fench Tarot")
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
                if x >= position[0] and x < position[0]+self.cellSizex and y >= position[1] and y < position[1] + self.cellSizey:
                    self.gameState.update(card)
            else:
                pass

    def render(self):
        self.window.fill((0, 0, 0))
        self.sprites = {}
        
        # Render for the betting phase
        
        if self.gameState.betStarted:
            for k,player in enumerate(self.gameState.players):
                if k == 0:
                    for i, card in enumerate(player):
                        handSize = len(player)
                        x, y = self.positions[card]
                        y = 2*(8-y)
                        x = 2*(x-1)
                        textureRect = pygame.Rect(x*self.cellSizex, y*self.cellSizey, self.cellSizex, self.cellSizey)
                        spritePoint = Vector2(13-handSize//2+i,25).elementwise()*self.cellSize
                        self.sprites[card] = spritePoint
                        self.window.blit(self.cardsTexture, spritePoint, textureRect)
                elif k == 1:
                    for i, card in enumerate(player):
                        handSize = len(player)
                        x, y = self.positions[card]
                        y = 2*(8-y)
                        x = 2*(x-1)
                        textureRect = pygame.Rect(x*self.cellSizex, y*self.cellSizey, self.cellSizex, self.cellSizey)
                        spritePoint = Vector2(0,13-handSize//2+i).elementwise()*self.cellSize
                        self.sprites[card] = spritePoint
                        self.window.blit(self.cardsTexture, spritePoint, textureRect)
                elif k == 2:
                    for i, card in enumerate(player):
                        handSize = len(player)
                        x, y = self.positions[card]
                        y = 2*(8-y)
                        x = 2*(x-1)
                        textureRect = pygame.Rect(x*self.cellSizex, y*self.cellSizey, self.cellSizex, self.cellSizey)
                        spritePoint = Vector2(13-handSize//2+i,0).elementwise()*self.cellSize
                        self.sprites[card] = spritePoint
                        self.window.blit(self.cardsTexture, spritePoint, textureRect)
                elif k == 3:
                    for i, card in enumerate(player):
                        handSize = len(player)
                        x, y = self.positions[card]
                        y = 2*(8-y)
                        x = 2*(x-1)
                        textureRect = pygame.Rect(x*self.cellSizex, y*self.cellSizey, self.cellSizex, self.cellSizey)
                        spritePoint = Vector2(25,13-handSize//2+i).elementwise()*self.cellSize
                        self.sprites[card] = spritePoint
                        self.window.blit(self.cardsTexture, spritePoint, textureRect)
            
            self.currentBetterTexture = my_font.render('Current better: %s' %(self.gameState.indexPosition[self.gameState.currentPlayer]), False, (255, 255, 255))
            # self.currentBetterTexture = my_font.render('Current better:', False, (255, 255, 255))
            self.currentBetterTexture = pygame.transform.scale(self.currentBetterTexture, (4*self.cellSizex, self.cellSizey))
            textureRect = pygame.Rect(0, 0, 4*self.cellSizex, self.cellSizey)
            spritePoint = Vector2(11,18).elementwise()*self.cellSize
            self.window.blit(self.currentBetterTexture, spritePoint, textureRect)
            
            
            if self.gameState.contract == None:
                k = -1
            else:
                k = self.gameState.contracts.index(self.gameState.contract)
            for l in range(k + 1, len(self.gameState.contracts)):
                contract = self.gameState.contracts[l]
                textureRect = pygame.Rect(0, 0, self.cellSizex, self.cellSizey)
                spritePoint = Vector2(9+2*l,15).elementwise()*self.cellSize
                self.sprites[contract] = spritePoint
                self.window.blit(self.contractSprites[l], spritePoint, textureRect)
            
        if self.gameState.betOver == True:
            
            for k,player in enumerate(self.gameState.players):
                if k == 0:
                    for i, card in enumerate(player):
                        handSize = len(player)
                        x, y = self.positions[card]
                        y = 2*(8-y)
                        x = 2*(x-1)
                        textureRect = pygame.Rect(x*self.cellSizex, y*self.cellSizey, self.cellSizex, self.cellSizey)
                        spritePoint = Vector2(13-handSize//2+i,25).elementwise()*self.cellSize
                        self.sprites[card] = spritePoint
                        self.window.blit(self.cardsTexture, spritePoint, textureRect)
                elif k == 1:
                    for i, card in enumerate(player):
                        handSize = len(player)
                        x, y = self.positions[card]
                        y = 2*(8-y)
                        x = 2*(x-1)
                        textureRect = pygame.Rect(x*self.cellSizex, y*self.cellSizey, self.cellSizex, self.cellSizey)
                        spritePoint = Vector2(0,13-handSize//2+i).elementwise()*self.cellSize
                        self.sprites[card] = spritePoint
                        self.window.blit(self.cardsTexture, spritePoint, textureRect)
                elif k == 2:
                    for i, card in enumerate(player):
                        handSize = len(player)
                        x, y = self.positions[card]
                        y = 2*(8-y)
                        x = 2*(x-1)
                        textureRect = pygame.Rect(x*self.cellSizex, y*self.cellSizey, self.cellSizex, self.cellSizey)
                        spritePoint = Vector2(13-handSize//2+i,0).elementwise()*self.cellSize
                        self.sprites[card] = spritePoint
                        self.window.blit(self.cardsTexture, spritePoint, textureRect)
                elif k == 3:
                    for i, card in enumerate(player):
                        handSize = len(player)
                        x, y = self.positions[card]
                        y = 2*(8-y)
                        x = 2*(x-1)
                        textureRect = pygame.Rect(x*self.cellSizex, y*self.cellSizey, self.cellSizex, self.cellSizey)
                        spritePoint = Vector2(25,13-handSize//2+i).elementwise()*self.cellSize
                        self.sprites[card] = spritePoint
                        self.window.blit(self.cardsTexture, spritePoint, textureRect)
                        
            textureRect = pygame.Rect(0, 0, self.cellSizex, self.cellSizey)
            spritePoint = Vector2(13,17).elementwise()*self.cellSize
            self.sprites['betOver'] = spritePoint
            # self.window.blit(self.button_next_trick_texture, spritePoint, textureRect)
            self.window.blit(self.buttonBetOverTexture, spritePoint, textureRect)
        
        
        if self.gameState.kittyRevealed:
            for k,player in enumerate(self.gameState.players):
                if k == 0:
                    for i, card in enumerate(player):
                        handSize = len(player)
                        x, y = self.positions[card]
                        y = 2*(8-y)
                        x = 2*(x-1)
                        textureRect = pygame.Rect(x*self.cellSizex, y*self.cellSizey, self.cellSizex, self.cellSizey)
                        spritePoint = Vector2(13-handSize//2+i,25).elementwise()*self.cellSize
                        self.sprites[card] = spritePoint
                        self.window.blit(self.cardsTexture, spritePoint, textureRect)
                elif k == 1:
                    for i, card in enumerate(player):
                        handSize = len(player)
                        x, y = self.positions[card]
                        y = 2*(8-y)
                        x = 2*(x-1)
                        textureRect = pygame.Rect(x*self.cellSizex, y*self.cellSizey, self.cellSizex, self.cellSizey)
                        spritePoint = Vector2(0,13-handSize//2+i).elementwise()*self.cellSize
                        self.sprites[card] = spritePoint
                        self.window.blit(self.cardsTexture, spritePoint, textureRect)
                elif k == 2:
                    for i, card in enumerate(player):
                        handSize = len(player)
                        x, y = self.positions[card]
                        y = 2*(8-y)
                        x = 2*(x-1)
                        textureRect = pygame.Rect(x*self.cellSizex, y*self.cellSizey, self.cellSizex, self.cellSizey)
                        spritePoint = Vector2(13-handSize//2+i,0).elementwise()*self.cellSize
                        self.sprites[card] = spritePoint
                        self.window.blit(self.cardsTexture, spritePoint, textureRect)
                elif k == 3:
                    for i, card in enumerate(player):
                        handSize = len(player)
                        x, y = self.positions[card]
                        y = 2*(8-y)
                        x = 2*(x-1)
                        textureRect = pygame.Rect(x*self.cellSizex, y*self.cellSizey, self.cellSizex, self.cellSizey)
                        spritePoint = Vector2(25,13-handSize//2+i).elementwise()*self.cellSize
                        self.sprites[card] = spritePoint
                        self.window.blit(self.cardsTexture, spritePoint, textureRect)
            
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
            self.window.blit(self.buttonKittySeenTexture, spritePoint, textureRect)
        
        # Kitty building phase, the cards in the kitty are highlighted
        
        if self.gameState.kittyBuilding:
            for k,player in enumerate(self.gameState.players):
                if k == 0:
                    for i, card in enumerate(player):
                        handSize = len(player)
                        x, y = self.positions[card]
                        y = 2*(8-y)
                        x = 2*(x-1)
                        textureRect = pygame.Rect(x*self.cellSizex, y*self.cellSizey, self.cellSizex, self.cellSizey)
                        spritePoint = Vector2(13-handSize//2+i,25).elementwise()*self.cellSize
                        self.sprites[card] = spritePoint
                        self.window.blit(self.cardsTexture, spritePoint, textureRect)
                elif k == 1:
                    for i, card in enumerate(player):
                        handSize = len(player)
                        x, y = self.positions[card]
                        y = 2*(8-y)
                        x = 2*(x-1)
                        textureRect = pygame.Rect(x*self.cellSizex, y*self.cellSizey, self.cellSizex, self.cellSizey)
                        spritePoint = Vector2(0,13-handSize//2+i).elementwise()*self.cellSize
                        self.sprites[card] = spritePoint
                        self.window.blit(self.cardsTexture, spritePoint, textureRect)
                elif k == 2:
                    for i, card in enumerate(player):
                        handSize = len(player)
                        x, y = self.positions[card]
                        y = 2*(8-y)
                        x = 2*(x-1)
                        textureRect = pygame.Rect(x*self.cellSizex, y*self.cellSizey, self.cellSizex, self.cellSizey)
                        spritePoint = Vector2(13-handSize//2+i,0).elementwise()*self.cellSize
                        self.sprites[card] = spritePoint
                        self.window.blit(self.cardsTexture, spritePoint, textureRect)
                elif k == 3:
                    for i, card in enumerate(player):
                        handSize = len(player)
                        x, y = self.positions[card]
                        y = 2*(8-y)
                        x = 2*(x-1)
                        textureRect = pygame.Rect(x*self.cellSizex, y*self.cellSizey, self.cellSizex, self.cellSizey)
                        spritePoint = Vector2(25,13-handSize//2+i).elementwise()*self.cellSize
                        self.sprites[card] = spritePoint
                        self.window.blit(self.cardsTexture, spritePoint, textureRect)
                
                for k, card in enumerate(self.gameState.kitty):
                    x, y = self.positions[card]
                    y = 2*(8-y)
                    x = 2*(x-1)
                    textureRect = pygame.Rect(x*self.cellSizex, y*self.cellSizey, self.cellSizex, self.cellSizey)
                    spritePoint = Vector2(9+k, 13).elementwise()*self.cellSize
                    self.sprites[card] = spritePoint
                    self.window.blit(self.cardsTexture, spritePoint, textureRect)
        
            if self.gameState.kittyOver == True:
                textureRect = pygame.Rect(0, 0, self.cellSizex, self.cellSizey)
                spritePoint = Vector2(13,17).elementwise()*self.cellSize
                self.sprites['kittyOver'] = spritePoint
                self.window.blit(self.buttonKittyOverTexture, spritePoint, textureRect)
        
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
            self.window.blit(self.buttonRoundSummaryTexture, spritePoint, textureRect)
        
        
        
        if self.gameState.roundStarted:
            
            self.attackEarnedTexture = my_font.render('Attack Score: %s' %self.gameState.attackScore, False, (255, 255, 255))
            self.attackEarnedTexture = pygame.transform.scale(self.attackEarnedTexture, (3*self.cellSizex, self.cellSizey))
            
            self.defenseEarnedTexture = my_font.render('Defense Score: %s' %self.gameState.defenseScore, False, (255, 255, 255))
            self.defenseEarnedTexture = pygame.transform.scale(self.defenseEarnedTexture, (3*self.cellSizex, self.cellSizey))
            
            textureRect = pygame.Rect(0, 0, 3*self.cellSizex, self.cellSizey)
            spritePoint = Vector2(20,5).elementwise()*self.cellSize
            # self.window.blit(self.button_next_trick_texture, spritePoint, textureRect)
            self.window.blit(self.attackEarnedTexture, spritePoint, textureRect)
            
            textureRect = pygame.Rect(0, 0, 3*self.cellSizex, self.cellSizey)
            spritePoint = Vector2(20,6).elementwise()*self.cellSize
            # self.window.blit(self.button_next_trick_texture, spritePoint, textureRect)
            self.window.blit(self.defenseEarnedTexture, spritePoint, textureRect)
            
            for i,card in enumerate(self.gameState.playedCards):
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
                if k == 0 and self.gameState.currentPlayer != k:
                    for i, card in enumerate(player):
                        handSize = len(player)
                        x, y = self.positions[card]
                        y = 2*(8-y)
                        x = 2*(x-1)
                        textureRect = pygame.Rect(x*self.cellSizex, y*self.cellSizey, self.cellSizex, self.cellSizey)
                        spritePoint = Vector2(13-handSize//2+i,25).elementwise()*self.cellSize
                        self.sprites[card] = spritePoint
                        self.window.blit(self.cardsTexture, spritePoint, textureRect)
                elif k == 0 and self.gameState.currentPlayer == k:
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
                elif k == 1 and self.gameState.currentPlayer != k:
                    for i, card in enumerate(player):
                        handSize = len(player)
                        x, y = self.positions[card]
                        y = 2*(8-y)
                        x = 2*(x-1)
                        textureRect = pygame.Rect(x*self.cellSizex, y*self.cellSizey, self.cellSizex, self.cellSizey)
                        spritePoint = Vector2(0,13-handSize//2+i).elementwise()*self.cellSize
                        self.sprites[card] = spritePoint
                        self.window.blit(self.cardsTexture, spritePoint, textureRect)
                elif k == 1 and self.gameState.currentPlayer == k:
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
                elif k == 2 and self.gameState.currentPlayer != k:
                    for i, card in enumerate(player):
                        handSize = len(player)
                        x, y = self.positions[card]
                        y = 2*(8-y)
                        x = 2*(x-1)
                        textureRect = pygame.Rect(x*self.cellSizex, y*self.cellSizey, self.cellSizex, self.cellSizey)
                        spritePoint = Vector2(13-handSize//2+i,0).elementwise()*self.cellSize
                        self.sprites[card] = spritePoint
                        self.window.blit(self.cardsTexture, spritePoint, textureRect)
                elif k == 2 and self.gameState.currentPlayer == k:
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
                elif k == 3 and self.gameState.currentPlayer != k:
                    for i, card in enumerate(player):
                        handSize = len(player)
                        x, y = self.positions[card]
                        y = 2*(8-y)
                        x = 2*(x-1)
                        textureRect = pygame.Rect(x*self.cellSizex, y*self.cellSizey, self.cellSizex, self.cellSizey)
                        spritePoint = Vector2(25,13-handSize//2+i).elementwise()*self.cellSize
                        self.sprites[card] = spritePoint
                        self.window.blit(self.cardsTexture, spritePoint, textureRect)
                elif k == 3 and self.gameState.currentPlayer == k:
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
        
        
        if self.gameState.roundSummary:
            
            self.attackEarnedTexture = my_font.render('Attack Score: %s' %self.gameState.attackScore, False, (255, 255, 255))
            self.attackEarnedTexture = pygame.transform.scale(self.attackEarnedTexture, (3*self.cellSizex, self.cellSizey))
            
            self.defenseEarnedTexture = my_font.render('Defense Score: %s' %self.gameState.defenseScore, False, (255, 255, 255))
            self.defenseEarnedTexture = pygame.transform.scale(self.defenseEarnedTexture, (3*self.cellSizex, self.cellSizey))
            
            self.winnerTexture = my_font.render('The winner is: %s' %self.gameState.winner, False, (255, 255, 255))
            self.winnerTexture = pygame.transform.scale(self.winnerTexture, (3*self.cellSizex, 2*self.cellSizey))
            
            textureRect = pygame.Rect(0, 0, 3*self.cellSizex, self.cellSizey)
            spritePoint = Vector2(15,5).elementwise()*self.cellSize
            # self.window.blit(self.button_next_trick_texture, spritePoint, textureRect)
            self.window.blit(self.attackEarnedTexture, spritePoint, textureRect)
            
            textureRect = pygame.Rect(0, 0, 3*self.cellSizex, self.cellSizey)
            spritePoint = Vector2(15,7).elementwise()*self.cellSize
            # self.window.blit(self.button_next_trick_texture, spritePoint, textureRect)
            self.window.blit(self.defenseEarnedTexture, spritePoint, textureRect)
            
            textureRect = pygame.Rect(0, 0, 3*self.cellSizex, 2*self.cellSizey)
            spritePoint = Vector2(15,9).elementwise()*self.cellSize
            # self.window.blit(self.button_next_trick_texture, spritePoint, textureRect)
            self.window.blit(self.winnerTexture, spritePoint, textureRect)
            
            textureRect = pygame.Rect(0, 0, self.cellSizex, self.cellSizey)
            spritePoint = Vector2(13,13).elementwise()*self.cellSize
            self.sprites['roundSeen'] = spritePoint
            # self.window.blit(self.button_next_trick_texture, spritePoint, textureRect)
            self.window.blit(self.buttonRoundSeenTexture, spritePoint, textureRect)
        
        if self.gameState.scoreDisplayed:
            
            self.southScoreTexture = my_font.render('South Score: %s' %self.gameState.scores[0], False, (255, 255, 255))
            self.southScoreTexture = pygame.transform.scale(self.southScoreTexture, (3*self.cellSizex, self.cellSizey))
            
            self.westScoreTexture = my_font.render('West Score: %s' %self.gameState.scores[1], False, (255, 255, 255))
            self.westScoreTexture = pygame.transform.scale(self.westScoreTexture, (3*self.cellSizex, self.cellSizey))
            
            self.northScoreTexture = my_font.render('North Score: %s' %self.gameState.scores[2], False, (255, 255, 255))
            self.northScoreTexture = pygame.transform.scale(self.northScoreTexture, (3*self.cellSizex, self.cellSizey))
            
            self.eastScoreTexture = my_font.render('East Score: %s' %self.gameState.scores[3], False, (255, 255, 255))
            self.eastScoreTexture = pygame.transform.scale(self.eastScoreTexture, (3*self.cellSizex, self.cellSizey))
            
            textureRect = pygame.Rect(0, 0, 3*self.cellSizex, self.cellSizey)
            spritePoint = Vector2(15,5).elementwise()*self.cellSize
            # self.window.blit(self.button_next_trick_texture, spritePoint, textureRect)
            self.window.blit(self.southScoreTexture, spritePoint, textureRect)
            
            textureRect = pygame.Rect(0, 0, 3*self.cellSizex, self.cellSizey)
            spritePoint = Vector2(15,7).elementwise()*self.cellSize
            # self.window.blit(self.button_next_trick_texture, spritePoint, textureRect)
            self.window.blit(self.westScoreTexture, spritePoint, textureRect)
            
            textureRect = pygame.Rect(0, 0, 3*self.cellSizex, 2*self.cellSizey)
            spritePoint = Vector2(15,9).elementwise()*self.cellSize
            # self.window.blit(self.button_next_trick_texture, spritePoint, textureRect)
            self.window.blit(self.northScoreTexture, spritePoint, textureRect)
            
            textureRect = pygame.Rect(0, 0, 3*self.cellSizex, 2*self.cellSizey)
            spritePoint = Vector2(15,11).elementwise()*self.cellSize
            # self.window.blit(self.button_next_trick_texture, spritePoint, textureRect)
            self.window.blit(self.eastScoreTexture, spritePoint, textureRect)
            
            textureRect = pygame.Rect(0, 0, self.cellSizex, self.cellSizey)
            spritePoint = Vector2(13,13).elementwise()*self.cellSize
            self.sprites['scoreSeen'] = spritePoint
            # self.window.blit(self.button_next_trick_texture, spritePoint, textureRect)
            self.window.blit(self.buttonScoreSeenTexture, spritePoint, textureRect)

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