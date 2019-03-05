from BJ_main import *

def check_play_next():
    play = True
    while True:
        try:
            continue_play = input("Do you want to continue and start another game? (Y/N)")
        except ValueError:
            print("Invalid input. Please re-enter.")
            continue
        else:
            if continue_play == "n" or continue_play == "N":
                play = False
                break
            else:
                play = True
                break
    return play

def start_over():
    restart = True
    while True:
        try:
            continue_play = input("Do you want to re-start the entire game? (Y/N)")
        except ValueError:
            print("Invalid input. Please re-enter.")
            continue
        else:
            if continue_play == "n" or continue_play == "N":
                restart = False
                print("Thanks for playing!")
                break
            else:
                restart = True
                break
    return restart

def take_bet(num_of_players):
    global player

    for i in range(0, num_of_players):
        while True and player[i].lost != 1:  # looping until a valid bet entered
            try:
                bet = int(input("How much do you want to bet? Please enter:"))
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

def player_take_hit(num_of_players,deck,player):
    # this function is to deal a card to the players when player wants to take a card
    new_card = ["", ""]
    for i in range(0, num_of_players):          # iterate through all player
        while True and player[i].lost != 1:     # variable player.lost sets to 1 when this play has zero balance
            hit = input("Do you want to take a hit? (Y/N)")
            if hit == "Y" or hit == "y":
                new_card = deck.deal()
                player[i].get_card(new_card)    # use get_card method to append a new car to player's hand
                player[i].adjust_ace()          # change ace's value to 1 if needed
                if player[i].check_bust():      # use check_bust method to identify if player gets more than 21
                    print(new_card)
                    print(player[i].point)      # print player' total point to proof this player has busted
                    print("Bust! You lost!")
                    break
                else:
                    print(new_card)
            else:
                break
    return (deck, player)