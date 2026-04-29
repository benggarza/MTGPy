from .types.card import Card

class Format:
    name = ""
    minimum_deck_size : int = 60
    maximum_deck_size : int = -1
    minimum_sideboard_size : int = 0
    maximum_sideboard_size : int = 15
    maximum_individual_card_count : int = 4
    starting_life_total : int = 20
    maximum_number_players : int = 2
    minimum_number_players : int = 2
    legal_cards : list[Card] = []
    banned_cards : list[Card] = [] # necessary? legal cards is enough I think
    # deckbuilding restrictions are functions that take a decklist and
    # return whether it is legal or notc x
    deckbuilding_restrictions : list[callable] = [(lambda _: True)]
    free_mulligan : bool = False

Pauper : Format = Format()
Pauper.legal_cards = []
Pauper.name = "Pauper"
