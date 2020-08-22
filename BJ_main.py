import random
from typing import Dict, Any, Union

from BJ_methods import *

######################
class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + " of " + self.suit


#######################
class Deck:

    def __init__(self):
        self.deck = []
        self.counter = 0
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))
                self.counter += 1

    def __str__(self):
        deck_content = ""
        for card in self.deck:
            deck_content += "\n" + card.__str__()
        return "Deck contains:" + deck_content

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        self.counter -= 1
        return self.deck.pop()

#####################
class Dealer:
    def __init__(self):
        self.hand = []
        self.point = 0
        self.ace_tracker = 0
        self.bust = 0

    def get_card(self, card):
        self.hand.append(card)
        self.point += values[card.rank]

        if card.rank == "Ace":
            self.ace_tracker += 1

    def adjust_ace(self):
        if (self.point > 21) and (self.ace_tracker > 0):
            self.point -= 10
            self.ace_tracker -= 1

    def check_bust(self):
        if self.point > 21:
            self.bust = 1
        return self.bust

    def __str__(self):
        return f"Dealer's points: {self.point}\nDealer's Hand: {self.hand}'"


######################
class Player(Dealer):

    def __init__(self):
        Dealer.__init__(self)
        self.balance = 100
        self.bet = 0
        self.lost = 0

    def get_bet(self, bet):
            self.bet = bet

    def win_bet(self):
        self.balance += self.bet

    def lose_bet(self):
        self.balance -= self.bet

    def __str__(self):
        return f"Player's balance: {self.balance}\nPlayer's points: {self.point}\nPlayner's Hand: {self.hand}'"


##################
# main starts here
if __name__ == "__main__":

    suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
    ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
    values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
             'Queen':10, 'King':10, 'Ace':11}
    #values: Dict[Union[str, Any], Union[int, Any]] = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
    #         'Queen':10, 'King':10, 'Ace':11}

    play_again = True # used at the end to ask if the player wants to start over and reshuffle
    continue_play = True

    while play_again:

        # Set up the game
        play = True  # used after each game session to ask if the player wants to continue
        num_of_players = 1
        dealer = Dealer()
        player = []
        for num in range(0,num_of_players):
            player.append(Player())
        for i in range(0, num_of_players):
            player[i].lost = 0
        loser = 0
        deck = Deck()
        deck.shuffle()

        while play:

            dealer.point = 0
            dealer.hand = []
            dealer.bust = 0
            dealer.ace_tracker = 0
            for i in range(0, num_of_players):
                player[i].point = 0
                player[i].bet = 0
                player[i].hand = []
                player[i].ace_tracker = 0
                player[i].bust = 0
                print("Player {}'s balance:{}".format(i + 1, player[i].balance))
                # check if zero balance
                if player[i].balance == 0:
                    print("Player {} has zero balance. Out of game.".format(i + 1))
                    player[i].lost = 1
                    loser += 1


            # take bet
            for i in range(0, num_of_players):
                while True and player[i].lost != 1:  # looping until a valid bet entered
                    try:
                        bet = int(input("\nHow much do you want to bet? Please enter:"))
                    except ValueError:
                        print("Invalid input. Please chose a number which is smaller than your current balance.")
                        continue
                    else:
                        if bet <= player[i].balance:
                            player[i].bet = bet
                            break
                        else:
                            print("Too much for bet. Not enough money in pocket!\nPlease enter a smaller number.")
                            continue


            # deal out the cards
            for i in range(0,2):
                dealer.get_card(deck.deal())
                for j in range(0,num_of_players):
                    if player[j].lost != 1:
                        player[j].get_card(deck.deal())

            # show hands
            #print(f"Dealer has a {dealer.hand[1]}")
            print(f"Dealer has a {dealer.hand[0]} and a {dealer.hand[1]}")
            for i in range(0, num_of_players):
                if player[i].lost != 1:
                    print("Player {} has a {} and a {}".format(i+1, player[i].hand[0], player[i].hand[1]))

            # Player take a hit?
            (deck, player) = player_take_hit(num_of_players,deck,player)

            # check if players are all busted
            sum = 0
            for i in range(0, num_of_players):
                if player[i].bust != 0  and player[i].lost != 1:
                    player[i].lose_bet()
                    player[i].bet = 0
                    sum += 1
                    print("Player {} bust!\nNew balance: {}".format(i + 1, player[i].balance))
            if sum == (num_of_players - loser):
                print("All player(s) lost.")
                del sum
                play = check_play_next()
                continue

            # dealer take a hit?
            while True:
                dealer.get_card(deck.deal())
                dealer.adjust_ace()
                dealer.bust = dealer.check_bust()
                print("Dealer hits.\nDealer gets {}".format(dealer.hand[-1]))
                if dealer.bust:
                    print("Dealer blow up his hand!")
                    break
                elif dealer.point < 17:
                    continue
                else:
                    break

            # Win check
            #win_check(num_of_players)
            if dealer.bust:
                for i in range(0, num_of_players):
                    if player[i].bust == 0 and player[i].lost != 1:
                        player[i].win_bet()
                        print("Player {} win!\nYour new balance:{}".format(i + 1, player[i].balance))
            else:
                for i in range(0, num_of_players):
                    if player[i].bust == 0 and player[i].lost != 1:
                        if player[i].point > dealer.point:
                            player[i].win_bet()
                            print("Player {} win!\nYour new balance:{}".format(i + 1, player[i].balance))
                            print("Dealer has point: {}".format(dealer.point))
                        elif player[i].point < dealer.point:
                            player[i].lose_bet()
                            print("Dealer has point: {}".format(dealer.point))
                            print("Player {} lost!\nYour new balance:{}".format(i + 1, player[i].balance))
                        elif player[i].point == dealer.point:
                            player[i].lose_bet()
                            print("Dealer also has point: {}".format(dealer.point))
                            print("Push for play {}.\nYour balance stays the same:{}".format(i + 1, player[i].balance))

            # ask if want to play the next game
            play = check_play_next()

        # check if player want to start over from the beginning
        play_again = start_over()


