# Blackjack - en spiller mod dealeren
# Kravene står i docs/kravspecifikation.md
# Åbn denne fil i Thonny og tryk F5 for at spille.

import random


SUITS = ["klør", "ruder", "hjerter", "spar"]
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

ACTION_PROMPT = "Vælg handling: h = hit, s = stand."
REPLAY_PROMPT = "Ny runde? j = ja, n = nej."
INVALID_INPUT = "Ugyldigt input."


def new_deck():
    """Laver en bunke med alle 52 kort."""
    deck = []
    for suit in SUITS:
        for rank in RANKS:
            deck.append({"rank": rank, "suit": suit})
    return deck


def shuffle_deck(deck):
    """Blander bunken."""
    random.shuffle(deck)


def card_value(card):
    """Værdien af et kort. Es er 11 her, det bliver rettet i hand_total."""
    rank = card["rank"]
    if rank == "A":
        return 11
    if rank == "J" or rank == "Q" or rank == "K":
        return 10
    return int(rank)


def hand_total(hand):
    """Lægger kortene sammen. Hvis vi er over 21 og har et es,
    tæller esset som 1 i stedet for 11, og vi trækker 10 fra."""
    total = 0
    aces = 0
    for card in hand:
        total = total + card_value(card)
        if card["rank"] == "A":
            aces = aces + 1
    if total > 21 and aces > 0:
        total = total - 10
    return total


def is_bust(hand):
    """Hånden er bust hvis totalen er over 21."""
    return hand_total(hand) > 21


def is_blackjack(hand):
    """Blackjack er 21."""
    if hand_total(hand) == 21:
        return True
    return False


def deal_card(deck, hand):
    """Tager det forreste kort fra bunken og lægger det i hånden."""
    card = deck.pop(0)
    hand.append(card)


def card_text(card):
    """Skriver et kort som fx 'K spar'."""
    return card["rank"] + " " + card["suit"]


def hand_text(hand):
    """Skriver hele hånden som fx '[K spar | 4 ruder]'."""
    texts = []
    for card in hand:
        texts.append(card_text(card))
    return "[" + " | ".join(texts) + "]"


def show_player(player):
    """Viser spillerens kort og total."""
    print("Spiller: " + hand_text(player) + " - total: " + str(hand_total(player)))


def show_dealer_hidden(dealer):
    """Viser kun dealerens første kort, det andet er skjult."""
    print("Dealer: [" + card_text(dealer[0]) + "] [skjult]")


def show_dealer(dealer):
    """Viser alle dealerens kort og totalen."""
    print("Dealer: " + hand_text(dealer) + " - total: " + str(hand_total(dealer)))


def outcome_text(outcome):
    """Teksten der hører til udfaldet."""
    if outcome == "PLAYER_BLACKJACK":
        return "Spilleren vinder med blackjack."
    if outcome == "PLAYER_WIN":
        return "Spilleren vinder."
    if outcome == "DEALER_WIN":
        return "Dealeren vinder."
    return "Uafgjort."


def find_outcome(player, dealer):
    """Finder ud af hvem der vinder runden."""
    if is_blackjack(player) and is_blackjack(dealer):
        return "PUSH"
    if is_blackjack(player):
        return "PLAYER_BLACKJACK"
    if is_blackjack(dealer):
        return "DEALER_WIN"
    if is_bust(player):
        return "DEALER_WIN"
    if is_bust(dealer):
        return "PLAYER_WIN"
    if hand_total(player) > hand_total(dealer):
        return "PLAYER_WIN"
    if hand_total(player) < hand_total(dealer):
        return "DEALER_WIN"
    return "PUSH"


def player_turn(deck, player, dealer):
    """Spilleren vælger h eller s indtil han står eller buster."""
    while True:
        show_player(player)
        show_dealer_hidden(dealer)
        print(ACTION_PROMPT)
        # Rydder op i det spilleren skriver, så store bogstaver
        # og mellemrum også virker.
        command = input().strip().lower()
        if command == "h":
            deal_card(deck, player)
            if is_bust(player):
                return
        elif command == "s":
            return
        else:
            print(INVALID_INPUT)


def dealer_turn(deck, dealer):
    """Dealeren trækker kort indtil 17 og står så."""
    while hand_total(dealer) <= 17:
        deal_card(deck, dealer)
        show_dealer(dealer)


def show_result(player, dealer):
    """Viser begge hænder og hvem der vandt."""
    print("")
    print("Resultat")
    show_player(player)
    show_dealer(dealer)
    print(outcome_text(find_outcome(player, dealer)))


def play_round(deck):
    """Spiller en hel runde med den bunke der bliver givet."""
    player = []
    dealer = []
    deal_card(deck, player)
    deal_card(deck, dealer)
    deal_card(deck, player)
    deal_card(deck, dealer)

    if is_blackjack(player) or is_blackjack(dealer):
        show_result(player, dealer)
        return

    player_turn(deck, player, dealer)

    print("")
    print("Dealeren viser sit skjulte kort.")
    show_dealer(dealer)
    dealer_turn(deck, dealer)

    show_result(player, dealer)


def main():
    """Starter spillet og spørger om ny runde bagefter."""
    print("BLACKJACK")
    print("Én spiller mod dealeren. 52 kort, ingen indsatser.")
    print("Kom tættest på 21 uden at gå over. Es er 11 eller 1.")
    print("Dealeren står på 17. Brug de små bogstaver som vist.")

    deck = new_deck()
    shuffle_deck(deck)

    playing = True
    round_number = 0
    while playing:
        round_number = round_number + 1
        print("")
        print("--- Runde " + str(round_number) + " ---")
        play_round(deck)

        while True:
            print(REPLAY_PROMPT)
            answer = input()
            if answer == "j":
                break
            if answer == "n":
                playing = False
                break
            print(INVALID_INPUT)

    print("Tak for spillet.")


if __name__ == "__main__":
    main()
