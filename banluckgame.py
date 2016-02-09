from random import shuffle

class BanluckGame(object):
    def __init__(self):
        #creates and shuffle a pack of cards
        SUITS = 'DCHS'
        NUMBER = '23456789TJQKA'
        self.deck = [''.join((n, s)) for s in SUITS for n in NUMBER]
        shuffle(self.deck)

        self.dealer = []
        self.player = []

        #deals initial cards
        self.deal('dealer', 4)
        self.deal('player', 2)

        r = self.count('dealer')
        while len(r['points']) < 3:
            self.deck = [''.join((n, s)) for s in SUITS for n in NUMBER]
            shuffle(self.deck)            
            self.dealer = []
            self.deal('dealer', 4)
            r = self.count('dealer')                        


        print(self.dealer)
        print(self.count('dealer'))

    def deal(self, target, number_cards):
        target_ = self.dealer if target == 'dealer' else self.player
        for _ in range(number_cards):
            if len(self.deck) <= 0:
                raise
            target_.append(self.deck.pop(0))

    #returns a list [total, multiplier]
    def count(self, target):
        target_ = self.dealer if target == 'dealer' else self.player
        result = {
            'points': [0],
            'multiplier': 1
        }
        points = 0
        alt_points = 0

        if len(target_) == 2:
            #ban ban
            if target_[0][0] == 'A' and target_[1][0] == 'A':
                result['points'] = [21]
                result['multiplier'] = 3
                return result
            
            #ban luck
            if (target_[0][0] == 'A' and target_[1][0] in 'TJQK') or target_[1][0] == 'A' and target_[0][0] in 'TJQK':
                result['points'] = [21]
                result['multiplier'] = 2
                return result

        for c in target_:
            num = c[0]
            if num in '23456789':
                result['points'] = [x + int(num) for x in result['points']]

            #ace is worth 11 points with 2 cards and 10 points with >2 cards
            elif num == 'A':
                initial_len = len(result['points'])
                result['points'].extend(result['points'])

                for i, _ in enumerate(result['points']):
                    if i < initial_len:
                        result['points'][i] += 1
                    else:
                        result['points'][i] += (11 if len(target_) == 2 else 10)

                #removes duplicates in a list (this is for when there are 2 aces)
                result['points'] = sorted(list(set(result['points'])))
            #TJQK
            else:
                result['points'] = [x + 10 for x in result['points']]
        return result

        