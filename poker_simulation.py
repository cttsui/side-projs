'''
Simulation of a poker hand. Given two pairs of hole cards, a random board is drawn and the winner is decided.
The winning percentage of one hand against another is estimated by Monte Carlo.
'''


import random
#Aces are both 1 and 14
#d=0, c=1, h=2, s=3
class Card:
    def __init__(self,value,suit):
        self.value = value
        self.suit = suit

    def __repr__(self):
        return '(%s, %s)' %(self.value,self.suit)


class Hand:
    def __init__(self,c1,c2,c3,c4,c5,c6,c7):
        self.cards = [c1,c2,c3,c4,c5,c6,c7]

    def get_values(self):
        value_dist = [0 for _ in range(14)]
        for card in self.cards:
            value_dist[card.value-1] += 1
        return value_dist

    def get_value_bool(self):
        value_bool = [0 for _ in range(14)]
        for card in self.cards:
            value_bool[card.value-1] = 1
            if card.value == 14:
                value_bool[0] = 1
        return value_bool

    def get_suits(self):
        suit_dist = [0 for _ in range(4)]
        for card in self.cards:
            suit_dist[card.suit] += 1
        return suit_dist

    def __repr__(self):
        return self.cards.__repr__()


class Hand_Result:
    def __init__(self,hand_type,c1,c2,c3,c4,c5):
        self.hand_type = hand_type
        self.card_values = [c1,c2,c3,c4,c5]

    def compare(self,other_hand):
        hand_order = {'straight flush': 1,'quads': 2, 'full house': 3, 'flush': 4,'straight': 5,'trips': 6, 'two pair': 7,
                      'pair': 8,'high card': 9}
        if hand_order[self.hand_type] < hand_order[other_hand.hand_type]:
            return 1
        if hand_order[self.hand_type] > hand_order[other_hand.hand_type]:
            return -1
        if self.card_values > other_hand.card_values:
            return 1
        if self.card_values < other_hand.card_values:
            return -1
        return 0

    def __repr__(self):
        return self.hand_type + ': ' + '(' + ' '.join(str(i) for i in self.card_values) + ')'


def create_hand(card_strings):
    return Hand(*[string_to_card(s) for s in card_strings])


def string_to_card(s):
    values = {'2':2, '3':3, '4':4, '5':5, '6': 6, '7': 7, '8': 8,'9':9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    suits = {'d': 0, 'c': 1, 'h': 2, 's': 3}
    return Card(values[s[0]],suits[s[1]])


def is_quads(hand):
    values = hand.get_values()
    quad_index = None
    high_card_index = None
    for i in range(13,-1,-1):
        if values[i] == 4:
            quad_index = i
            break
    for j in range(13,-1,-1):
        if values[j] != 0 and j != quad_index:
            high_card_index = j
            break
    if quad_index is None:
        return is_full_house(hand)
    card_values = [quad_index+1,high_card_index+1,0,0,0]
    return Hand_Result('quads',*card_values)


def is_full_house(hand):
    values = hand.get_values()
    triple_index = None
    pair_index = None
    for i in range(14):
        if values[i] >= 3:
            triple_index = i
    for j in range(14):
        if (values[j] >= 2) and (j != triple_index):
            pair_index = j
    if triple_index is None or pair_index is None:
        return is_flush(hand)
    card_values = [triple_index+1,pair_index+1,0,0,0]
    return Hand_Result('full house',*card_values)


def is_flush(hand):
    suits = hand.get_suits()
    flush_suit = None
    for i in range(4):
        if suits[i] >= 5:
            flush_suit = i
    if flush_suit is None:
        return is_straight(hand)
    card_values = sorted([card.value for card in hand.cards if card.suit == flush_suit],reverse=True)
    while len(card_values) < 7:
        card_values.append(card_values[-1]) #placeholder cards
    card_list = [Card(v,flush_suit) for v in card_values]
    if is_straight(Hand(*card_list)).hand_type == 'straight':
        straight_flush_hand = is_straight(Hand(*card_list))
        straight_flush_hand.hand_type = 'straight flush'
        return straight_flush_hand
    return Hand_Result('flush',*card_values[:5])


def is_straight(hand):
    values = hand.get_value_bool()
    sums = [0 for _ in range(10)]
    index = None
    for i in range(10):
        sums[i] = sum(values[i:i+5])
        if sums[i] == 5:
            index = i
    if index is None:
        return is_trips(hand)
    i = index
    card_values = [i+5, i+4, i+3, i+2, i+1]
    return Hand_Result('straight',*card_values)


def is_trips(hand):
    values = hand.get_values()
    trips_index = None
    for i in range(13,-1,-1):
        if values[i] == 3:
            trips_index = i
            break
    if trips_index is None:
        return is_two_pair(hand)
    card_values = [trips_index+1]
    for j in range(13,-1,-1):
        if values[j] != 0 and j != trips_index:
            card_values.append(j+1)
            if len(card_values) == 3:
                break
    for _ in range(2):
        card_values.append(0)
    return Hand_Result('trips',*card_values)


def is_two_pair(hand):
    values = hand.get_values()
    pair_1_index = None
    pair_2_index = None
    for i in range(13,-1,-1):
        if values[i] == 2:
            if pair_1_index is None:
                pair_1_index = i
            else:
                pair_2_index = i
                break
    if pair_2_index is None:
        return is_pair(hand)
    card_values = [pair_1_index+1,pair_2_index+1]
    for j in range(13,-1,-1):
        if (values[j] != 0) and (j != pair_1_index) and (j != pair_2_index):
            card_values.append(j+1)
            break
    for _ in range(2):
        card_values.append(0)
    return Hand_Result('two pair',*card_values)


def is_pair(hand):
    values = hand.get_values()
    pair_index = None
    for i in range(13,-1,-1):
        if values[i] == 2:
            pair_index = i
            break
    if pair_index is None:
        return high_card(hand)
    card_list = [pair_index+1]
    for j in range(13,-1,-1):
        if (values[j] != 0) and (j != pair_index):
            card_list.append(j+1)
            if len(card_list) == 4:
                break
    card_list.append(0)
    return Hand_Result('pair',*card_list)


def high_card(hand):
    values = hand.get_values()
    card_values = []
    for i in range(13,-1,-1):
        if values[i] != 0:
            card_values.append(i)
            if len(card_values) == 5:
                break
    return Hand_Result('high card',*card_values)


def card_to_int(card):
    v = card.value
    s = card.suit
    return 4*(v-2)+s


def int_to_card(idx):
    s = int(idx % 4)
    v = int(((idx - s)/4)+2)
    return Card(v,s)


def generate_random_board(c1,c2,c3,c4):
    '''
    Given hole cards, generates a random board of 5 cards.
    Inputs: Cards c1 through c4
    Output: List of Cards
    '''
    random_cards = []
    hole_cards = [card_to_int(c1),card_to_int(c2),card_to_int(c3),card_to_int(c4)]
    while len(random_cards) < 5:
        n = random.randint(0,51)
        if (n not in hole_cards) and (n not in random_cards):
            random_cards.append(n)
    return [int_to_card(idx) for idx in random_cards]


def evaluate_hand(hand):
    '''
    Returns a Hand_Result with the strength of the hand.
    '''
    return is_quads(hand)


def simulate(c1,c2,c3,c4):
    '''
    Simulates a hand between two pairs of hole cards (c1,c2) and (c3,c4).
    Returns 1 if (c1,c2) wins, -1 if (c3,c4) wins and 0 if they tie.
    '''
    board = generate_random_board(c1,c2,c3,c4)
    hand1 = Hand(c1,c2,*board)
    hand2 = Hand(c3,c4,*board)
    result1 = evaluate_hand(hand1)
    result2 = evaluate_hand(hand2)
    return result1.compare(result2)


def monte_carlo(t,c1,c2,c3,c4):
    '''
    Simulates t hands and tallies the number of times each hand wins (or ties).
    '''
    hand1_win = 0
    tie = 0
    hand2_win = 0
    for _ in range(t):
        result = simulate(c1,c2,c3,c4)
        if result == 1:
            hand1_win += 1
        elif result == -1:
            hand2_win += 1
        else:
            tie += 1
    print('Hand 1 wins: {:0.1f}%, Hand 2 wins: {:0.1f}%, Tie: {:0.1f}%'.format(hand1_win*100/t,hand2_win*100/t,tie*100/t))
    return hand1_win, tie, hand2_win


if __name__ == '__main__':
    print('Poker Simulator')
    print('Format: For each prompt, input value followed by first letter of suit.')
    print('Values are (2,3,4,5,6,7,8,9,T,J,Q,K,A).')
    print('E.g. Ten of clubs is "Tc"')
    print('-----')
    c1 = string_to_card(input('Enter first card in first pair: '))
    c2 = string_to_card(input('Enter second card in first pair: '))
    c3 = string_to_card(input('Enter first card in second pair: '))
    c4 = string_to_card(input('Enter second card in second pair: '))
    t = int(input('Number of simulations'))
    monte_carlo(t,c1,c2,c3,c4)


