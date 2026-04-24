# CR100.2. To play, each player needs their own deck of traditional Magic cards...
class Deck:
    # CR100.5. If a deck must contain at least a certain number of cards,
    # that number is referred to as a minimum deck size.
    # There is no maximum deck size for non-Commander decks.
    minimum_deck_size : int = 0
    maximum_deck_size : int = -1