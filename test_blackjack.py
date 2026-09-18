# Tests til blackjack.py
# Åbn denne fil i Thonny og tryk F5 for at køre testene.

import unittest

import blackjack


def card(rank, suit="spar"):
    """Lille hjælpefunktion så testene bliver kortere at skrive."""
    return {"rank": rank, "suit": suit}


class TestDeck(unittest.TestCase):

    def test_ny_bunke_har_52_kort(self):
        deck = blackjack.new_deck()
        self.assertEqual(len(deck), 52)

    def test_ny_bunke_har_52_forskellige_kort(self):
        deck = blackjack.new_deck()
        par = []
        for kort in deck:
            par.append(kort["rank"] + kort["suit"])
        self.assertEqual(len(set(par)), 52)

    def test_fire_kort_af_hver_rank(self):
        deck = blackjack.new_deck()
        for rank in blackjack.RANKS:
            antal = 0
            for kort in deck:
                if kort["rank"] == rank:
                    antal = antal + 1
            self.assertEqual(antal, 4)

    def test_deal_card_tager_det_forreste_kort(self):
        deck = [card("2", "klør"), card("3", "ruder"), card("4", "hjerter")]
        hand = []
        blackjack.deal_card(deck, hand)
        self.assertEqual(hand, [card("2", "klør")])
        self.assertEqual(len(deck), 2)
        self.assertEqual(deck[0], card("3", "ruder"))


class TestKortvaerdier(unittest.TestCase):

    def test_talkort_har_deres_egen_vaerdi(self):
        for rank in ["2", "3", "4", "5", "6", "7", "8", "9", "10"]:
            self.assertEqual(blackjack.card_value(card(rank)), int(rank))

    def test_billedkort_er_10(self):
        for rank in ["J", "Q", "K"]:
            self.assertEqual(blackjack.card_value(card(rank)), 10)

    def test_es_er_11(self):
        self.assertEqual(blackjack.card_value(card("A")), 11)


class TestHandTotal(unittest.TestCase):

    def test_tom_haand(self):
        self.assertEqual(blackjack.hand_total([]), 0)
        self.assertFalse(blackjack.is_bust([]))
        self.assertFalse(blackjack.is_blackjack([]))

    def test_haand_uden_es(self):
        self.assertEqual(blackjack.hand_total([card("10"), card("7", "ruder")]), 17)

    def test_es_taeller_11_naar_der_er_plads(self):
        self.assertEqual(blackjack.hand_total([card("A"), card("6", "ruder")]), 17)

    def test_es_taeller_1_naar_vi_ellers_ville_gaa_over(self):
        hand = [card("A"), card("6", "ruder"), card("K", "hjerter")]
        self.assertEqual(blackjack.hand_total(hand), 17)

    def test_es_og_es_og_9(self):
        hand = [card("A"), card("A", "ruder"), card("9", "hjerter")]
        self.assertEqual(blackjack.hand_total(hand), 21)


class TestBust(unittest.TestCase):

    def test_over_21_er_bust(self):
        hand = [card("K"), card("Q", "ruder"), card("2", "hjerter")]
        self.assertTrue(blackjack.is_bust(hand))

    def test_21_er_ikke_bust(self):
        hand = [card("K"), card("Q", "ruder"), card("A", "hjerter")]
        self.assertFalse(blackjack.is_bust(hand))


class TestBlackjack(unittest.TestCase):

    def test_es_og_billedkort_er_blackjack(self):
        self.assertTrue(blackjack.is_blackjack([card("A"), card("K", "ruder")]))

    def test_es_og_ti_er_blackjack(self):
        self.assertTrue(blackjack.is_blackjack([card("A"), card("10", "ruder")]))


class TestUdfald(unittest.TestCase):

    def test_hoejeste_total_vinder(self):
        spiller = [card("10"), card("10", "ruder")]
        dealer = [card("10", "hjerter"), card("8", "klør")]
        self.assertEqual(blackjack.find_outcome(spiller, dealer), "PLAYER_WIN")

    def test_dealeren_vinder_med_hoejeste_total(self):
        spiller = [card("10"), card("8", "ruder")]
        dealer = [card("10", "hjerter"), card("10", "klør")]
        self.assertEqual(blackjack.find_outcome(spiller, dealer), "DEALER_WIN")

    def test_lige_totaler_giver_push(self):
        spiller = [card("10"), card("8", "ruder")]
        dealer = [card("10", "hjerter"), card("8", "klør")]
        self.assertEqual(blackjack.find_outcome(spiller, dealer), "PUSH")

    def test_teksterne_til_udfaldene(self):
        self.assertEqual(
            blackjack.outcome_text("PLAYER_BLACKJACK"), "Spilleren vinder med blackjack."
        )
        self.assertEqual(blackjack.outcome_text("PLAYER_WIN"), "Spilleren vinder.")
        self.assertEqual(blackjack.outcome_text("DEALER_WIN"), "Dealeren vinder.")
        self.assertEqual(blackjack.outcome_text("PUSH"), "Uafgjort.")


if __name__ == "__main__":
    unittest.main()
