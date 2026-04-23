import mtgpy

def main():
    # Start up an interface with the user, and start a basic game
    # Player vs computer as default to start
    # decks are placed in deck0.csv, deck1.csv
    human_player = mtgpy.HumanPlayer()
    comp_player = mtgpy.CompPlayer()
    deck0 = mtgpy.Deck()
    deck1 = mtgpy.Deck()
    human_player.set_deck(deck0)
    comp_player.set_deck(deck1)
    with mtgpy.InterfaceEngine.get_interface() as interface:
        game = mtgpy.Game([human_player, comp_player], interface=interface)
        result = game.play()

    if result == 1:
        print("Congrats! You won.")
    elif result == -1:
        print("The computer won.")
    else:
        print("It's a draw")
    


if __name__=="__main__":
    main()