# Blackjack game written in python
# v1.0
# Author: Redriel
#
# This is a simple blackjack game
# This class handle the game using objects from the blackjack_lib module
# It is an inline game with the goal to win 1000$, starting from 100, playing against a simple dealer-script.

from blackjack_lib import actor, cards
print('\n'*50)
print("♣ ♠ ♥ ♦ ♣ ♠ ♥ ♦ ♣")
print("B L A C K J A C K")
print("♠ ♦ ♥ ♣ ♠ ♦ ♣ ♥ ♠\n")

print("You start with 100$.Your goal is to get to 1000$.Good luck!")

# Main variables
player = actor.Actor()
dealer = actor.Actor()
deck = cards.Deck()
still_in_play = True
dealer_hand_value = 0
player_hand_value = 0
bet = 0

# Function to check the y/n input of the user
def response(message):
    answer = input(message + ' (y/n) \n')
    if answer == "y":
        return True
    elif answer == "n":
        return False
    else:
        print("ERROR: invalid answer.")
        response(message)

# Function to evaluate the hand of a player.
# It can automatically set an ace as 1 or 11 points, whatever is the best.
def evaluate_hand(hand):
    hand_value = 0
    for card in hand:
        if card.rank == "Ace" and hand_value <= 10:
            hand_value += 11
        else:
            hand_value += card.get_value()
    for card in hand:
        if hand_value <= 10 and card.rank == "Ace":
            hand_value += 10
        elif hand_value > 21 and card.rank == "Ace":
            hand_value -= 10
    return hand_value

# Main cycle of the game.
# Game ends whether the player wins or loses.
while player.get_money() > 0 and player.get_money() < 1000:

    # At the start of every new hand, previous hands are resetted
    player.discard()
    dealer.discard()
    dealer_hand_value = 0
    player_hand_value = 0

    # The still_in_play flag checks if the player hit "hard" (gone above 21 points)
    still_in_play = True

    # Storing the bet amount insered by the player
    bet = input("Bet amount: ")
    while not bet.isdigit() or int(bet) <= 0 or int(bet) > player.get_money():
        print("ERROR: invalid bet.")
        bet = input("Bet amount: ")
    bet = int(bet)

    # The dealer takes the bet, then the deck is shuffled and the player is given two starting cards
    player.deduct_money(bet)
    deck.shuffle()
    player.add_card(deck.deal_one())
    player.add_card(deck.deal_one())

    # Cycle that manages additional cards the player may request
    while True:
        print('\n'*50)
        player.hand_str("Your hand")
        while response("Do you want another card?") == True:
            player.add_card(deck.deal_one())
            print('\n'*50)
            player.hand_str("Your hand")
            player_hand_value = evaluate_hand(player.get_hand())
            if player_hand_value > 21:
                print(f"Woops! Above 21, You lost {bet}$")
                still_in_play = False
                break
        break

    print('\n'*50)

    # If the player is still in play, his/her hand is evalueted
    # Scoring a blackjack (21 points) is an automatic win
    if still_in_play:
        player_hand_value = evaluate_hand(player.get_hand())
        if player_hand_value == 21:
            print(f"Wow, 21! You won {bet}$")
            player.add_money(2*bet)
            break
        else:
            print(f'Your hand is worth {player_hand_value} points.')

        print("Now it's the dealer turn.")

        # Dealer cycle. The dealer calls additional cards until he hit "hard" or beats the player.
        while dealer_hand_value < player_hand_value:
            dealer.add_card(deck.deal_one())
            dealer_hand_value = evaluate_hand(dealer.get_hand())
        dealer.hand_str("Dealer hand")
        if dealer_hand_value > 21:
            print(f"Yay! The dealer went above 21.")
        else:
            print(f'Dealer hand is worth {dealer_hand_value} points.')

        # Player receive or loses money accordingly to the result of the hand
        if dealer_hand_value >= player_hand_value and dealer_hand_value <= 21:
            print("The dealer wins!")
        else:
            print("You won!")
            player.add_money(2*bet)

    print(f"You now have {player.get_money()}$")

    # If the player has 1000$, the game ends
    if player.get_money() >= 1000:
        print("Congrats, genius, you WON!")
        break

    # If the player loses all his money, the game ends as well
    if player.get_money() <= 0:
        print("You ran out of money. Game over!")
        break

    # At the end of every hand, the player can choose if he/she wants to play another hand
    if response("Do you want to go for another round?") == False:
        break

    print('\n'*50)
