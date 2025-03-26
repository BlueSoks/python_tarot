import random as rd


class Tarot():
    
    def __init__(self, number_of_rounds):
        self.number_of_rounds = number_of_rounds
        self.deck = ['0E', 'RH', 'DH', 'CH', 'VH', '10H', '9H', '8H', '7H', '6H', '5H', '4H', '3H', '2H', '1H', 'RC', 'DC', 'CC', 'VC', '10C', '9C', '8C', '7C', '6C', '5C', '4C', '3C', '2C', '1C', 'RD', 'DD', 'CD', 'VD', '10D', '9D', '8D', '7D', '6D', '5D', '4D', '3D', '2D', '1D', 'RS', 'DS', 'CS', 'VS', '10S', '9S', '8S', '7S', '6S', '5S', '4S', '3S', '2S', '1S']
        for j in range(1, 22):
            self.deck += ['%sA' %j]
        rd.shuffle(self.deck)
        self.values = {}
        self.values['R'] = 14
        self.values['D'] = 13
        self.values['C'] = 12
        self.values['V'] = 11
        self.values['21'] = 21
        self.values['20'] = 20
        self.values['19'] = 19
        self.values['18'] = 18
        self.values['17'] = 17
        self.values['16'] = 16
        self.values['15'] = 15
        self.values['14'] = 14
        self.values['13'] = 13
        self.values['12'] = 12
        self.values['11'] = 11
        self.values['10'] = 10
        self.values['9'] = 9
        self.values['8'] = 8
        self.values['7'] = 7
        self.values['6'] = 6
        self.values['5'] = 5
        self.values['4'] = 4
        self.values['3'] = 3
        self.values['2'] = 2
        self.values['1'] = 1
        self.south = []
        self.north_east = []
        self.north_west = []
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
        self.index_position = {0: 'South', 1: 'West', 2: 'North-west', 3: 'North-east', 4: 'East'}
        self.players = [self.south, self.west, self.north_west, self.north_east, self.east]
        self.players_earned = [self.south_earned, self.west_earned, self.north_west_earned, self.north_east_earned, self.east_earned]
        self.caller_index = None
        self.deal()
        self.previous_trick_winner = (self.dealer_index + 1) % 5
        self.total_scores = 5*[0]
        self.play_game()
    
    def play_game(self):
        print('Game in %s rounds, deck shuffled, game starting.' %self.number_of_rounds)
        for k in range(self.number_of_rounds):
            print('Round number: %s'%(k+1))
            self.play_round()
    
    def cut_deck(self, no_contract):
        cutter = self.index_position[self.dealer_index - 1]
        if no_contract:
            for item in self.players:
                self.deck += item
            print('%s cuts the deck.')
            cut_value = int(input('Enter where you would like to cut the deck (number between 2 and 76): '))
            while cut_value < 2 or cut_value > 76:
                print('Number not in range.')
                cut_value = int(input('Enter where you would like to cut the deck (number between 2 and 76): '))
            self.deck = self.deck[cut_value:] + self.deck[:cut_value]
        else:
            for item in self.players_earned:
                self.deck += item
            print('%s cuts the deck.')
            cut_value = int(input('Enter where you would like to cut the deck (number between 2 and 76): '))
            while cut_value < 2 or cut_value > 76:
                print('Number not in range.')
                cut_value = int(input('Enter where you would like to cut the deck (number between 2 and 76): '))
            self.deck = self.deck[cut_value:] + self.deck[:cut_value]
    
    def play_round(self):
        self.caller_index = None
        self.remaining_contracts = ['Small', 'Guard', 'Guard without', 'Guard against', 'None']
        self.contract = None
        print('Round starting, dealer is %s'%self.index_position[self.dealer_index])
        self.deal()
        for j in range(1,6):
            player_index = (self.dealer_index + j) % 5
            print('%s, you can call %s' %(self.index_position[player_index], self.remaining_contracts))
            print('Current cards in hand: %s' %self.players[player_index])
            contract = input('What do you call?')
            while contract not in self.remaining_contracts:
                print('Contract not available.')
                contract = input('What do you call?')
            if contract != 'None':
                self.caller_index = player_index
                self.remaining_contracts = self.remaining_contracts[self.remaining_contracts.index(contract)+1:]
        if self.caller_index == None:
            self.dealer_index += 1
            self.cut_deck(True)
            self.deal()
        else:
            for j in range(15):
                self.play_trick()
            self.cut_deck(False)
    
    
    def deal(self):
        counter = 0
        current_player_index = (self.dealer_index + 1) % 5
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
                current_player_index = (current_player_index + 1) % 5
                counter += 1
        self.previous_trick_winner = self.dealer_index + 1
        for k in range(len(self.players)):
            self.players[k] = [item for item in self.players[k] if item[-1] == 'C'] + [item for item in self.players[k] if item[-1] == 'S'] + [item for item in self.players[k] if item[-1] == 'D'] + [item for item in self.players[k] if item[-1] == 'H'] + [item for item in self.players[k] if item[-1] == 'A'] + [item for item in self.players[k] if item[-1] == 'E']
    
    def play_trick(self):
        trick = []
        player_index = self.previous_trick_winner
        # print('First player: %s' %self.index_position[player_index])
        # print('Current cards in hand: %s' %self.players[player_index])
        print('First player: %s' %self.index_position[player_index])
        print('Current cards in hand: %s' %self.players[player_index])
        played, valid = self.play_card(None, trick, player_index)
        while not(valid):
            print('Suit of the played card wrong or card not in hand.')
            played, valid = self.play_card(None, trick, player_index)
        trick += [played]
        suit_trick = played[-1]
        self.players[player_index].remove(played)
        for j in range(1, 5):
            player_index = (self.previous_trick_winner + j) % 5
            print('Current player: %s' %self.index_position[player_index])
            print('Current cards in hand: %s' %self.players[player_index])
            print('Cards played in the current trick: %s' %trick)
            played, valid = self.play_card(suit_trick, trick, player_index)
            while not(valid):
                print('Not allowed to play this card.')
                played, valid = self.play_card(suit_trick, trick, player_index)
            trick += [played]
            self.players[player_index].remove(played)
        print('Trick complete: %s' %trick)
        scores = []
        for card in trick:
            if card[-1] == 'A':
                scores += [100 + self.values[card[:-1]]]
            elif card[-1] == suit_trick:
                scores += [self.values[card[:-1]]]
            else:
                scores += [0]
        winner_index = (self.previous_trick_winner + scores.index(max(scores))) % 5
        winner = self.index_position[winner_index]
        self.previous_trick_winner = winner_index
        self.players_earned[winner_index] += trick
        print('Trick winner: %s' %winner)
            
            
        
            
    def play_card(self, suit_trick, trick, player_index):
        hand = self.players[player_index]
        played = input('Enter the card you wish to play: ')
        if played not in hand:
            return(None, False)
        if suit_trick == None or suit_trick == 'E':
            return(played, True)
        else:
            if suit_trick == played[-1] or played == '0E':
                return(played, True)
            else:
                if len([item for item in hand if item[-1] == suit_trick]) > 0:
                    return(played, False)
                if played[-1] == 'A':
                    trick_trump = max([int(item[:-1]) for item in trick if item[-1] == 'A'])
                    if int(played[:-1]) > trick_trump:
                        return(played, True)
                    else:
                         for k in range(trick_trump + 1, 22):
                             if (str(k) + 'A') in hand:
                                 return(played, False)
                         else:
                             return(played, True)
                if len([item for item in hand if item[-1] == 'A']) == 0:
                    return(played, True)
                else:
                    return(played, False)
    

number_of_rounds = 2

tarot = Tarot(number_of_rounds)
        
