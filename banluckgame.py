from random import shuffle

class BanluckGame(object):
    def __init__(self, bankroll=100, multiplier=None):
        if multiplier == None:
            self.multiplier = {
                'ban_ban': 3,
                'ban_luck': 2,
                'five_dragon': 2,
                'failed_five_dragon': -2,
                'normal': 1
            }

        self.default_bankroll = bankroll
        self.bankroll = self.default_bankroll
        self.records = []

    def shuffle(self):
        #creates and shuffle a pack of cards
        SUITS = 'DCHS'
        NUMBER = '23456789TJQKA'
        self.deck = [''.join((n, s)) for s in SUITS for n in NUMBER]
        shuffle(self.deck)

        self.dealer = []
        self.player = []

        #all points are in ascending order and will only contain valid combinations (<= 21 points)
        #thus if self.points['player'][-1] == 21, this is extremely good
        self.points = {
            'dealer': [],
            'player': []
        }

        self.status = {
            'dealer': 'normal',
            'player': 'normal'        
        }

    def start_simulation(self, bet=1, iterations=500):
        for _ in range(iterations):
            self.start_game()

        print('Mean: {}'.format(sum(self.records) / len(self.records)))
        print('Detailed breakdown: ({} iterations)'.format(iterations))
        print(self.records)

    def start_game(self, bet=1):
        round = 1
        self.bankroll = self.default_bankroll

        while round <= 1000 and self.bankroll > 0:
            self.start_round(bet)
            round += 1
        self.records.append(self.bankroll)

    def start_round(self, bet=1):
        self.shuffle()
        #deals initial cards
        self.deal('dealer', 2)
        self.deal('player', 2)

        player_status = self.status['player']
        dealer_status = self.status['dealer']

        #draw -> both have ban ban or both have ban luck
        if player_status == dealer_status and (player_status == 'ban_ban' or player_status == 'ban_luck'):
            # print('Draw')
            # self.display()
            return
            
        elif player_status == 'ban_ban' or dealer_status == 'ban_ban':
            self.bankroll += bet * self.multiplier['ban_ban'] * (1 if player_status == 'ban_ban' else -1)
            # print('{} wins with ban ban!'.format('Player' if player_status == 'ban_ban' else 'Dealer'))
            # self.display()
            return

        elif player_status == 'ban_luck' or dealer_status == 'ban_luck':
            self.bankroll += bet * self.multiplier['ban_luck'] * (1 if player_status == 'ban_luck' else -1)
            # self.display()
            # print('{} wins with ban luck!'.format('Player' if player_status == 'ban_luck' else 'Dealer'))
            return

        self.player_strategy()
        if self.status['player'] == 'failed_five_dragon':
            self.bankroll += bet * self.multiplier['failed_five_dragon']
            # print('Player failed its Five Dragon!')
        else:
            self.dealer_strategy()
            self.evaluate(bet)

        # self.display()

    def player_strategy(self):
        while len(self.points['player']) > 0:
            #stop at 20 or 21 points
            if self.points['player'][-1] > 19:
                break
            #if have less than 17 points, take one more card
            elif self.points['player'][-1] < 17:
                self.deal('player')
            #if we have between 17 and 19 points but one of our combinations is less than 14 (with ace), try for 5 dragons
            elif len(self.player) == 4 and self.points['player'][0] < 14:
                self.deal('player')
            else:
                break

            
    def dealer_strategy(self):
        while len(self.points['dealer']) > 0 and self.points['dealer'][-1] < 17:
            self.deal('dealer')

    def evaluate(self, bet):
        player_status = self.status['player']
        dealer_status = self.status['dealer']

        #draw -> both have 5 dragon
        if player_status == dealer_status and (player_status == 'five_dragon'):
            # print('Draw')
            pass
            
        elif player_status == 'five_dragon' or dealer_status == 'five_dragon':
            self.bankroll += bet * self.multiplier['five_dragon'] * (1 if player_status == 'five_dragon' else -1)
            # print('{} wins with Five Dragon!'.format('Player' if player_status == 'five_dragon' else 'Dealer'))

        elif dealer_status == 'failed_five_dragon':
            self.bankroll += bet * self.multiplier['failed_five_dragon'] * -1
            # print('Player wins as Dealer failed its Five Dragon!')

        elif self.status['player'] == 'failed' and self.status['dealer'] == 'failed':
            # print('Draw.')
            pass
        elif self.status['player'] == 'normal' and self.status['dealer'] == 'failed':
            self.bankroll += bet * self.multiplier['normal']
            # print('Player wins!')
        elif self.status['dealer'] == 'normal' and self.status['player'] == 'failed':
            self.bankroll += bet * self.multiplier['normal'] * -1
            # print('Dealer wins!')
        #both player and deal have valid hands
        else:
            player_points = self.points['player'][-1]
            dealer_points = self.points['dealer'][-1]

            if player_points == dealer_points:
                # print('Draw')
                pass
            else:
                self.bankroll += bet * self.multiplier['normal'] * (1 if player_points > dealer_points else -1)
                # print('{} wins!'.format('Player' if player_points > dealer_points else 'Dealer'))

    def display(self):
        print('Player has ${}'.format(self.bankroll))

    def deal(self, target, number_cards=1):
        target_ = self.dealer if target == 'dealer' else self.player
        for _ in range(number_cards):
            if len(self.deck) <= 0:
                raise
            target_.append(self.deck.pop(0))
        self.count(target)

    #returns a dictionary containing the status as well as different points combinations
    #when cards do not contain an ace, there will only be one points combination
    def count(self, target):
        target_ = self.dealer if target == 'dealer' else self.player

        #resets the count
        self.points[target] = [0]

        #cards have not been dealt yet
        if len(target_) < 2:
            raise

        #checking for ban ban or ban luck
        elif len(target_) == 2:
            #ban ban
            if target_[0][0] == 'A' and target_[1][0] == 'A':
                self.points[target] = [21]
                self.status[target] = 'ban_ban'
                return
            
            #ban luck
            if (target_[0][0] == 'A' and target_[1][0] in 'TJQK') or target_[1][0] == 'A' and target_[0][0] in 'TJQK':
                self.points[target] = [21]
                self.status[target] = 'ban_luck'
                return

        for c in target_:
            num = c[0]
            if num in '23456789':
                self.points[target] = [x + int(num) for x in self.points[target]]

            #ace is worth 11 points with 2 cards and 10 points with >2 cards
            elif num == 'A':
                initial_len = len(self.points[target])
                self.points[target].extend(self.points[target])

                for i, _ in enumerate(self.points[target]):
                    if i < initial_len:
                        self.points[target][i] += 1
                    else:
                        self.points[target][i] += (11 if len(target_) == 2 else 10)

                #removes duplicates in a list (this is for when there are 2 aces) and sort it in ascending order
                self.points[target] = sorted(list(set(self.points[target])))
            #TJQK
            else:
                self.points[target] = [x + 10 for x in self.points[target]]
        
        #removes combinations that are over 21 as they are invalid
        # print(target, self.points[target])
        self.points[target] = [x for x in self.points[target] if x <= 21]
        
        if len(target_) == 5:
            if len(self.points[target]) > 0:
                self.status[target] = 'five_dragon'
            else:
                self.status[target] = 'failed_five_dragon'

        elif len(self.points[target]) == 0:
            self.status[target] = 'failed'