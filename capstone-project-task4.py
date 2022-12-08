import random

# Set values of global variables:
suits = ("Hearts", "Diamonds", "Spades", "Clubs")
ranks = (
    "Two",
    "Three",
    "Four",
    "Five",
    "Six",
    "Seven",
    "Eight",
    "Nine",
    "Ten",
    "Jack",
    "Queen",
    "King",
    "Ace",
)
values = {
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
    "Six": 6,
    "Seven": 7,
    "Eight": 8,
    "Nine": 9,
    "Ten": 10,
    "Jack": 10,
    "Queen": 10,
    "King": 10,
    "Ace": [],
}
# Initialize the number of players to 0:
num_player = 0
# Create a list to contain chips for all players:
chips = []
# Create a list to contain bets for all players:
bets = []
# Create a list to contain split bets for all players:
split_bets = []
# Define player cards on the table
player_table_cards = [[] for i in range(num_player)]
# Define player split cards on the table:
player_table_split_cards = [[] for i in range(num_player)]
# Define dealer cards on the table:
dealer_table_cards = []
# Create a list to store the total value of all cards for all players:
player_cards_val = []
# Create a list to store the total value of all split cards for all players:
player_split_cards_val = []
# Record busts for players:
bust = []
# Record split busts for players:
split_bust = []
# Define the game round number:
game_num = 0
# Define the game_on boolean variable:
game_on = True


class Card:
    """Define the card in the Blackjack game"""

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + " of " + self.suit

    def set_rank(self, rank):
        """Set card's rank to a new rank"""

        self.rank = rank
        self.value = values[rank]


class Deck:
    """Define the deck(a set of cards) in the Blackjack game"""

    def __init__(self):
        self.all_cards = []
        for suit in suits:
            for rank in ranks:
                # This assumes the Card class has already been defined!
                self.all_cards.append(Card(suit, rank))

    def shuffle(self):
        """Shuffle cards"""
        random.shuffle(self.all_cards)

    def deal_one(self):
        """Remove one card from the list of all_cards"""
        return self.all_cards.pop()


def check_ace(card, num, player=True):
    """
    Check ace either for players or the dealer and adjust its value according to the player(num+1)
    """

    # Check ace for players:
    if player:
        if card.rank == "Ace":
            while True:
                ace_val = int(
                    input(
                        f"\nFor player {num + 1}, what value do you want to consider for Ace (1/11)? :"
                    )
                )

                if ace_val == 1:
                    values["Ace"][num] = 1
                    break
                elif ace_val == 11:
                    values["Ace"][num] = 11
                    break
                else:
                    print("Choose a valid value between 1 or 11!")
                    continue

    # Check ace for the dealer:
    else:
        hidden = False
        # Check if the dealer's shown card is Ace:
        if card.rank == "Ace":
            print("The dealer's shown card is Ace!")
            # Check dealer's hidden card:
            if dealer_table_cards[1].rank in ("Ten", "Jack", "Queen", "King"):
                hidden = True

            # Create a list to record players' choice:
            choice = [0 for i in range(num_player)]
            # Ask for players' choices:
            for i in range(num_player):
                while True:
                    # Ask if the
                    insurance = input(
                        f"\nFor player {i + 1}, do you want to buy insurance? (y/n) :"
                    )

                    if insurance == "y":
                        # Check if player i+1 has enough chips to buy insurance:
                        if chips[i] >= 0.5 * bets[i]:
                            chips[i] -= 0.5 * bets[i]
                            chips[i] = int(chips[i])
                            choice[i] = 1
                            break
                        else:
                            print(
                                f"\nPlayer {i + 1} does not have enough chips to buy insurance!"
                            )
                            break
                    elif insurance == "n":
                        break
                    else:
                        print("Type y or n!")
                        continue

            # Check player's choices and show their remaining chips:
            for i in range(num_player):
                # If player i+1 chose to buy insurance:
                if choice[i] == 1:
                    # If the hidden card is ten/jack/queen/king:
                    if hidden:
                        chips[i] += bets[i]
                        print(f"\nPlayer {i + 1} wins the insurance bet!")
                        print(f"{chips[i]} chips left for player {i + 1}")
                    else:
                        print(
                            f"\nUnfortunately! Player {i + 1} lost the insurance bet!"
                        )
                        print(f"{chips[i]} chips left for player {i + 1}")

            if hidden:
                print(
                    f"\nGame round {game_num} is over because the dealer got blackjack from the first two cards!"
                )

        return hidden


def calculate_card(num, split=False, dealer=False):
    """Calculate the total of existing or split card values for player num+1 or the dealer"""
    if not dealer:
        # Calculate the total value of existing cards:
        if not split:
            sum_val = 0
            for player_card in player_table_cards[num]:
                if player_card.rank == "Ace":
                    sum_val += values["Ace"][num]
                else:
                    sum_val += player_card.value

            return sum_val

        # Calculate the total value of split cards:
        else:
            sum_split_val = 0
            for player_split_card in player_table_split_cards[num]:
                if player_split_card.rank == "Ace":
                    sum_split_val += values["Ace"][num]

                else:
                    sum_split_val += player_split_card.value

            return sum_split_val

    # Calculate the total value of cards for the dealer:
    else:
        dealer_cards_val = 0
        for card in dealer_table_cards:
            # Check if there is Ace in dealer's cards and set its value to 11 at first:
            if card.rank == "Ace":
                dealer_cards_val += 11
            else:
                dealer_cards_val += card.value

        return dealer_cards_val


def show_playercard(num, split=False):
    """Show existing or split cards for player num+1"""

    # Show existing cards for player num+1:
    if not split:
        print(f"\nPlayer {num + 1}'s hand:")
        [print(j) for j in player_table_cards[num]]

    # Show split cards for player num+1:
    else:
        print(f"\nPlayer {num + 1}'s second hand(split cards):")
        [print(j) for j in player_table_split_cards[num]]


def hit_or_stand(num, split=False):
    """Ask for player num+1's choice(hit or stand) including card value calculations"""

    i = num
    if not split:
        while True:
            show_playercard(i)
            hit_or_stand_choice = input(
                f"\nFor player {i + 1}, do you want to hit or stand? (hit/stand):"
            ).lower()

            # If the player i+1 chooses to hit:
            if hit_or_stand_choice == "hit":
                # Distribute a card to player i+1:
                player_table_cards[i].append(new_deck.deal_one())
                check_ace(player_table_cards[i][-1], i)

                # Show the hit card for player i+1:
                print(f"\nThe player {i + 1} hits card: {player_table_cards[i][-1]}")
                # Show existing cards for player i+1:
                show_playercard(i)

                # Calculate the total value of all cards for player i+1:
                player_cards_val[i] = calculate_card(i)

                # The player num+1 gets a blackjack if the total value of all cards = 21:
                if player_cards_val[i] == 21:
                    print(
                        f"\nThe total value of existing cards in player {i + 1}'s hand is {player_cards_val[i]}"
                    )
                    print(f"Player {i + 1} got a blackjack!")
                    break

                # Loop the options again if the total value of all cards < 21:
                elif player_cards_val[i] < 21:
                    print(
                        f"\nThe total value of existing cards in player {i + 1}'s hand is {player_cards_val[i]}"
                    )
                    continue

                # The player num+1 busts if the total value of all cards > 21:
                else:
                    print(
                        f"\nThe total value of existing cards in player {i + 1}'s hand is {player_cards_val[i]}"
                    )
                    print(f"PLAYER {i + 1} BUSTED!")

                    bust[i] = 1
                    break

            # If the player num+1 chooses to stand:
            elif hit_or_stand_choice == "stand":
                # Calculate the total value of all cards for player i+1:
                player_cards_val[i] = calculate_card(i)

                print(f"\nPlayer {i + 1} has decided to stand.")
                # Show existing cards for player i+1:
                show_playercard(i)
                print(
                    f"\nThe total value of existing cards in player {i + 1}'s hand is {player_cards_val[i]}"
                )

                if player_cards_val[i] == 21:
                    print(f"Player {i + 1} got a blackjack!")

                break

            else:
                print("Please enter a valid option(hit/stand)!\n")
                continue

    # Check if player i+1 decides to hit/stand split cards:
    else:
        while True:
            show_playercard(i, split=True)
            hit_or_stand_split_choice = input(
                f"\nFor player {i + 1}, do you want to hit or stand for your split cards? (hit/stand):"
            ).lower()

            # If the player i+1 chooses to hit:
            if hit_or_stand_split_choice == "hit":
                # Distribute a card to player i+1:
                player_table_split_cards[i].append(new_deck.deal_one())
                check_ace(player_table_split_cards[i][-1], i)

                # Show the hit card for player i+1:
                print(
                    f"\nThe player {i + 1} hits card: {player_table_split_cards[i][-1]}"
                )
                # Show existing cards for player i+1:
                show_playercard(i, split=True)

                # Calculate the total value of all cards for player i+1:
                player_split_cards_val[i] = calculate_card(i, split=True)

                # The player num+1 gets a blackjack if the total value of all cards = 21:
                if player_split_cards_val[i] == 21:
                    print(
                        f"\nThe total value of split cards in player {i + 1}'s hand is {player_split_cards_val[i]}"
                    )
                    print(f"Player {i + 1} got a blackjack!")
                    break

                # Loop the options again if the total value of all cards < 21:
                elif player_split_cards_val[i] < 21:
                    print(
                        f"\nThe total value of split cards in player {i + 1}'s hand is {player_split_cards_val[i]}"
                    )
                    continue

                # The player num+1 busts if the total value of all cards > 21:
                else:
                    print(
                        f"\nThe total value of split cards in player {i + 1}'s hand is {player_split_cards_val[i]}"
                    )
                    print(f"PLAYER {i + 1}'s split cards BUSTED!")

                    split_bust[i] = 1
                    break

            # If the player num+1 chooses to stand:
            elif hit_or_stand_split_choice == "stand":
                # Calculate the total value of all cards for player i+1:
                player_split_cards_val[i] = calculate_card(i, split=True)

                print(f"\nPlayer {i + 1} has decided to stand.")
                # Show split cards for player i+1:
                show_playercard(i, split=True)
                print(
                    f"\nThe total value of split cards in player {i + 1}'s hand is {player_split_cards_val[i]}"
                )

                if player_split_cards_val[i] == 21:
                    print(f"Player {i + 1} got a blackjack!")

                break

            else:
                print("Please enter a valid option(hit/stand)!\n")
                continue


def double_down(num, split=False):
    """Ask for player num+1's choice(double down) including card value calculations"""

    i = num
    double_down_choice = False
    while True:
        show_playercard(i)
        # Ask for player i+1's double down choice:
        double_down = input(
            f"\nFor player {i + 1}, do you want to double down? (y/n) :"
        )

        # If player i+1 decides to double down:
        if double_down == "y":
            # Check if player i+1 has enough chips to double down:
            if chips[i] >= bets[i]:
                chips[i] -= bets[i]
                bets[i] += bets[i]
                # Distribute only one card to player i+1:
                player_table_cards[i].append(new_deck.deal_one())
                check_ace(player_table_cards[i][-1], i)
                # Show the hit card for player i+1:
                print(f"\nThe player {i + 1} hits card : {player_table_cards[i][-1]}")
                # Show existing cards for player i+1:
                show_playercard(i)
                # Calculate the total value of 3 cards for player i+1:
                player_cards_val[i] = calculate_card(i)

                if player_cards_val[i] > 21:
                    print(
                        f"\nThe total value of existing cards in player {i + 1}'s hand is {player_cards_val[i]}"
                    )
                    print(f"PLAYER {i + 1} BUSTED!")
                    bust[i] = 1

                elif player_cards_val[i] == 21:
                    print(
                        f"\nThe total value of existing cards in player {i + 1}'s hand is {player_cards_val[i]}"
                    )
                    print("You got a blackjack!")

                else:
                    print(
                        f"\nThe total value of existing cards in player {i + 1}'s hand is {player_cards_val[i]}"
                    )

                double_down_choice = True

            # Player i+1 does not have enough money to double down:
            else:
                print(f"Player {i + 1} does not have enough chips to double down!")

            break

        elif double_down == "n":
            break

        else:
            print("Please enter a valid option(y/n).\n")
            continue

    # If the player i+1 decides to split the card:
    double_down_split_choice = False
    if split:
        while True:
            show_playercard(i, split=True)
            # Ask for player i+1's double down choice:
            split_double_down = input(
                f"\nFor player {i + 1}, do you want to double down your split cards? (y/n) :"
            )

            # If player i+1 decides to double down:
            if split_double_down == "y":
                # Check if player i+1 has enough chips to double down:
                if chips[i] >= bets[i]:
                    chips[i] -= bets[i]
                    split_bets[i] += bets[i]
                    # Distribute only one card to player i+1:
                    player_table_split_cards[i].append(new_deck.deal_one())
                    check_ace(player_table_split_cards[i][-1], i)
                    # Show the hit card for player i+1:
                    print(
                        f"\nThe player {i + 1} hits card : {player_table_cards[i][-1]}"
                    )
                    # Show split cards for player i+1:
                    show_playercard(i, split=True)
                    # Calculate the total value of 3 cards for player i+1:
                    player_split_cards_val[i] = calculate_card(i, split=True)

                    if player_split_cards_val[i] > 21:
                        print(
                            f"\nThe total value of split cards in player {i + 1}'s hand is {player_split_cards_val[i]}"
                        )
                        print(f"PLAYER {i + 1} BUSTED!")
                        split_bust[i] = 1

                    elif player_split_cards_val[i] == 21:
                        print(
                            f"\nThe total value of split cards in player {i + 1}'s hand is {player_split_cards_val[i]}"
                        )
                        print("You got a blackjack!")

                    else:
                        print(
                            f"\nThe total value of split cards in player {i + 1}'s hand is {player_split_cards_val[i]}"
                        )

                    double_down_split_choice = True

                # Player i+1 does not have enough money to double down:
                else:
                    print(
                        f"Player {i + 1} does not have enough chips to double down split cards!"
                    )

                break

            elif split_double_down == "n":
                break

            else:
                print("Please enter a valid option(y/n).\n")
                continue

    return double_down_choice, double_down_split_choice


def check_split(num):
    """Check split option for player num+1"""

    if player_table_cards[num][0].rank == player_table_cards[num][1].rank:
        return True

    else:
        return False


def split(num):
    """Ask for player num+1's choice(split)"""

    i = num
    split_option = False
    while True:
        # Ask for player i+1's split choice:
        split_choice = input(
            f"\nFor player {i + 1}, you have two cards with the same rank {player_table_cards[i][0].rank}.\nDo you want to split your cards? (y/n) :"
        )

        # If player i+1
        if split_choice == "y":
            # Check if player i+1 has enough chips to split:
            if chips[i] >= bets[i]:
                # Add chips to split bets:
                split_bets[i] = bets[i]
                chips[i] -= bets[i]
                # Split the card:
                split_card = player_table_cards[i].pop(-1)
                player_table_split_cards[i].append(split_card)
                # Distribute an additional card to both:
                player_table_cards[i].append(new_deck.deal_one())
                player_table_split_cards[i].append(new_deck.deal_one())
                # Show player i+1's cards and split cards:
                show_playercard(i)
                show_playercard(i, split=True)
                check_ace(player_table_cards[i][-1], i)
                check_ace(player_table_split_cards[i][-1], i)
                split_option = True
                break

            else:
                print(f"Player {i + 1} does not have enough chips to split!")
                break

        elif split_choice == "n":
            break

        else:
            print("Please enter a valid option(y/n).\n")

    return split_option


def game_continue():
    """Ask for user's choice to continue the game"""

    game_continue_choice = False
    global num_player

    while True:
        # Ask if players want to continue the game:
        cont = input("\nDo you want to continue? (y/n) :")
        if cont == "y":
            # Check chips for all players and report unqualified players:
            for i in range(num_player):
                if chips[i] == 0:
                    print(
                        f"\nPlayer {i + 1} are out of chips! Game over for player{i + 1}!"
                    )

            # Update the number of players for the next round:
            num_player -= chips.count(0)

            # Remove the corresponding player in chips:
            while 0 in chips:
                chips.remove(0)

            # Check the number of players:
            if num_player == 0:
                break

            game_continue_choice = True
            break

        elif cont == "n":

            break

        else:
            print("Please enter a valid option(y/n).\n")
            continue

    # If players want to continue the game:
    if game_continue_choice:
        print("\n" * 10)

        print(
            """
    ██████╗░██╗░░░░░░█████╗░░█████╗░██╗░░██╗░░░░░██╗░█████╗░░█████╗░██╗░░██╗
    ██╔══██╗██║░░░░░██╔══██╗██╔══██╗██║░██╔╝░░░░░██║██╔══██╗██╔══██╗██║░██╔╝
    ██████╦╝██║░░░░░███████║██║░░╚═╝█████═╝░░░░░░██║███████║██║░░╚═╝█████═╝░
    ██╔══██╗██║░░░░░██╔══██║██║░░██╗██╔═██╗░██╗░░██║██╔══██║██║░░██╗██╔═██╗░
    ██████╦╝███████╗██║░░██║╚█████╔╝██║░╚██╗╚█████╔╝██║░░██║╚█████╔╝██║░╚██╗
    ╚═════╝░╚══════╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝"""
        )

        # If players want to stop the game:
    else:
        print("\nGame over!")
        for i in range(num_player):
            print(f"\nTotal amount of chips left with the player {i + 1} = {chips[i]}")

        print(input("\nPress Enter to exit the game..."))

    return game_continue_choice


# clears up the terminal for a cleaner look
# print("\n" * 100)

print(
    """
██████╗░██╗░░░░░░█████╗░░█████╗░██╗░░██╗░░░░░██╗░█████╗░░█████╗░██╗░░██╗
██╔══██╗██║░░░░░██╔══██╗██╔══██╗██║░██╔╝░░░░░██║██╔══██╗██╔══██╗██║░██╔╝
██████╦╝██║░░░░░███████║██║░░╚═╝█████═╝░░░░░░██║███████║██║░░╚═╝█████═╝░
██╔══██╗██║░░░░░██╔══██║██║░░██╗██╔═██╗░██╗░░██║██╔══██║██║░░██╗██╔═██╗░
██████╦╝███████╗██║░░██║╚█████╔╝██║░╚██╗╚█████╔╝██║░░██║╚█████╔╝██║░╚██╗
╚═════╝░╚══════╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝"""
)

print(
    """
BlackJack is very popular card game mainly played in casinos around the world.
Let's imagine this program as a virtual casino with computer as the Dealer.
The purpose of this game is to beat the Dealer, which can be done in various ways.

---------------------------------------------------------------------------------------------------------------
Both the player and the dealer are given 2 cards at the beginning , but one of the dealer's card is kept hidden.

Each card holds a certain value. 
Numbered cards contain value identical to their number.
All face cards hold a value of 10
Ace can either hold a value of 1 or 11 depending on the situation.

BlackJack means 21. Whoever gets a total value of 21 with their cards immediately wins!
(winning through blackjack results in 3x the money)
If the value of cards goes over 21, its called a BUST, which results in immediate loss...
If both the players get the same value of cards , it's a TIE and the bet money is returned.

If none of the above cases are met ,the person with closer value to 21 wins.
(winning like this returns 2x the bet money)
---------------------------------------------------------------------------------------------------------------

Let the game begin!"""
)

while game_on:

    try:
        # A new deck will be created and shuffled each round:
        new_deck = Deck()
        new_deck.shuffle()

        # Increase the game round number:
        game_num += 1
        print(f"\nGame Round number : {game_num}")

        # Enter the number of players if the game round is 1:
        if game_num == 1:
            while True:
                num_player = int(input("\nEnter the number of players:"))

                if num_player > 0:
                    # Add default 100 chips to each player:
                    for i in range(num_player):
                        chips.append(100)
                    break
                else:
                    print("The number of players must be greater than 0!")
                    continue

        # Initialize the bet for all players:
        bets = [0 for i in range(num_player)]
        # Initialize the split bet for all players:
        split_bets = [0 for i in range(num_player)]

        for i in range(num_player):
            # Use the loop to ask for user's input for the amount of chips bet for each player
            while True:
                # Enter the amount of chips for bet:
                print(f"\nChips remaining = {chips[i]} for player {i + 1}")
                bet = int(
                    input(f"Enter the integer amount of chips bet for player {i + 1}:")
                )
                if bet <= 0:
                    print("Less than 0 chip is not allowed for bet!")
                    print(f"Enter a valid integer between 0 and {chips[i]} \n")

                elif bet > chips[i]:
                    print("You don't have enough chips.")
                    print(f"Enter a valid integer between 0 and {chips[i]} \n")
                else:
                    bets[i] = bet
                    chips[i] -= bet
                    print(f"{chips[i]} chips left for player {i + 1}")
                    break

        # Define player cards on the table:
        player_table_cards = [[] for i in range(num_player)]
        # Define player split cards on the table:
        player_table_split_cards = [[] for i in range(num_player)]

        # Distribute 2 cards to each player:
        for i in range(num_player):
            for a in range(2):
                player_table_cards[i].append(new_deck.deal_one())

        # Test split function:
        player_table_cards[0][1].set_rank(player_table_cards[0][0].rank)

        # Distribute 2 cards to the dealer:
        [dealer_table_cards.append(new_deck.deal_one()) for i in range(2)]

        # Test buying insurance function:
        # dealer_table_cards[0].set_rank("Ace")
        # Test the dealer gets blackjack from the first two cards (game over):
        # dealer_table_cards[1].set_rank("Ten")

        # Show distributed cards for all players and the dealer:
        print()
        for i in range(num_player):
            print(
                f"Player {i + 1}'s cards are {player_table_cards[i][0]} and {player_table_cards[i][1]}"
            )
        print(f"Dealer's cards are {dealer_table_cards[0]} and Hidden.")

        # Check if the dealer's shown card is Ace and the dealer has blackjack:
        bj_dealer = check_ace(card=dealer_table_cards[0], num=0, player=False)
        # If the dealer gets blackjack from the first two cards:
        if bj_dealer:
            if game_continue():
                continue
            else:
                break

        # If the dealer does not get blackjack from the first two cards:
        else:
            # Initialize ace based on the number of players:
            for i in range(num_player):
                values["Ace"].append(0)
            # Check both cards given to each player for being ace:
            for i in range(num_player):
                for card in player_table_cards[i]:
                    check_ace(card, i)

            # Create a list to initialize the total value of all cards for all players:
            player_cards_val = [0 for i in range(num_player)]
            # Create a list to initialize the total value of all split cards for all players:
            player_split_cards_val = [0 for i in range(num_player)]
            # Record busts for all players:
            bust = [0 for i in range(num_player)]
            # Record split busts for all players:
            split_bust = [0 for i in range(num_player)]

            # Ask for each player's decision(split, double down and hit/stand):
            for i in range(num_player):
                split_player = False
                # Check split for player i+1:
                if check_split(i):
                    split_player = split(i)

                double_down_choice, double_down_split_choice = double_down(
                    i, split_player
                )

                # Check if player i+1 decides to double down:
                if not double_down_choice:
                    hit_or_stand(i)

                # Check if player i+1 decides to double down split cards:
                if split_player:
                    if not double_down_split_choice:
                        hit_or_stand(i, split=True)

            # Create a variable that stores how many times dealer hits before its cards value is more than or equal to 17:
            no_of_hits = 0

            while True:

                dealer_cards_val = 0

                # Update the value of dealer's cards:
                for card in dealer_table_cards:
                    # Check if there is Ace in dealer's cards and set its value to 11 at first:
                    if card.rank == "Ace":
                        dealer_cards_val += 11
                    else:
                        dealer_cards_val += card.value

                # Check if the ace(11) is appropriate(not bust):
                for card in dealer_table_cards:
                    # Check if there is Ace in dealer's cards:
                    if card.rank == "Ace" and dealer_cards_val >= 21:
                        dealer_cards_val -= 10

                # If the total value of dealer's cards < 17, hit one card:
                if dealer_cards_val < 17:
                    no_of_hits += 1
                    dealer_table_cards.append(new_deck.deal_one())
                    continue

                # If 21 > the total value of dealer's cards >= 17:
                elif 17 <= dealer_cards_val < 21:
                    print(f"\nThe Dealer has hit {no_of_hits} times.")
                    print("\nDealer's hand :")
                    [print(i) for i in dealer_table_cards]
                    break

                # If the total value of dealer's cards = 21:
                elif dealer_cards_val == 21:
                    print(f"\nThe Dealer has hit {no_of_hits} times.")
                    print("The Dealer got a blackjack!")
                    print("\nDealer's hand :")
                    [print(i) for i in dealer_table_cards]
                    break

                # If the total value of dealer's cards > 21:
                elif dealer_cards_val > 21:

                    print(f"\nThe Dealer has hit {no_of_hits} times.")
                    print(
                        f"The Dealer busted with a total value of {dealer_cards_val}!"
                    )
                    print("\nDealer's hand :")
                    [print(i) for i in dealer_table_cards]
                    break

            # Summarize the game result for this round:
            print(f"\nGame result of round {game_num} is summarized as below:")

            # Check busts for the dealer first:
            if dealer_cards_val > 21:
                for i in range(num_player):
                    if bust[i] == 1:
                        print(
                            f"\nSince both the dealer and player {i + 1} busted, player {i + 1} lost the money for bet."
                        )
                        # Check split_bust:
                        if split_bust[i] == 1:
                            print(f"Player {i + 1}'s split cards busted as well!")
                        else:
                            chips[i] += split_bets[i] * 2

                    else:
                        # Player i+1 won twice the money for bet:
                        chips[i] += bets[i] * 2

            # Dealer's card values < 21 (= is checked before):
            else:
                for i in range(num_player):
                    if player_cards_val[i] > 21:
                        print(
                            f"\nPlayer {i + 1} busted with {player_cards_val[i]} and lost the bet money!"
                        )
                    # Check player's blackjack then:
                    elif player_cards_val[i] == 21:
                        print(
                            f"\nPlayer {i + 1} won with a blackjack and got thrice the bet money!"
                        )
                        chips[i] += bets[i] * 3

                    elif 21 - player_cards_val[i] > 21 - dealer_cards_val:
                        print(
                            f"\nDealer won the player {i + 1} with {dealer_cards_val}:{player_cards_val[i]}! Player {i + 1} lost the bet money!"
                        )

                    elif 21 - player_cards_val[i] < 21 - dealer_cards_val:
                        print(
                            f"\nPlayer {i + 1} won the dealer with {player_cards_val[i]}:{dealer_cards_val}! Player {i + 1} got twice the bet money!"
                        )
                        chips[i] += bets[i] * 2

                    # The last situation can only be a tie:
                    else:
                        print(
                            f"\nIt's a tie with {dealer_cards_val}! Bet money was returned to player {i + 1}."
                        )
                        chips[i] += bets[i]

                # Show split card results:
                if split_bets[i] != 0:
                    if player_split_cards_val[i] > 21:
                        print(
                            f"\nPlayer {i + 1} busted with {player_split_cards_val[i]} for split cards and lost the bet money!"
                        )
                    # Check player's blackjack then:
                    elif player_split_cards_val[i] == 21:
                        print(
                            f"\nPlayer {i + 1} won with a blackjack and got thrice the bet money!"
                        )
                        chips[i] += split_bets[i] * 3

                    elif 21 - player_split_cards_val[i] > 21 - dealer_cards_val:
                        print(
                            f"\nDealer won the player {i + 1} (split cards) with {dealer_cards_val}:{player_split_cards_val[i]}! Player {i + 1} lost the bet money!"
                        )

                    elif 21 - player_split_cards_val[i] < 21 - dealer_cards_val:
                        print(
                            f"\nPlayer {i + 1} (split cards) won the dealer with {player_split_cards_val[i]}:{dealer_cards_val}! Player {i + 1} got twice the bet money!"
                        )
                        chips[i] += split_bets[i] * 2

                    # The last situation can only be a tie:
                    else:
                        print(
                            f"\nIt's a tie (split cards) with {dealer_cards_val}! Bet money was returned to player {i + 1}."
                        )
                        chips[i] += split_bets[i]

            # Show the chips for all players after this round:
            print(
                f"\nAfter round {game_num}, the number of chips for all players are shown below:"
            )
            for i in range(num_player):
                print(
                    f"\nTotal amount of chips left with the player {i + 1} = {chips[i]}"
                )

            # If players want to continue the game:
            if game_continue():
                continue

                # If players want to stop the game:
            else:
                break

    except Exception as error:

        print(f"Following error occurred : {error} \nPlease try again.")
        game_num -= 1  # round with error won't be counted
        continue
