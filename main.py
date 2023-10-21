from game import play_game
from aiEngine import static_eval, simple_score, material_advantage, extra_turn, rightside_pit, many_moves, \
    keep_on_own_side, closest_to_opponent
from players import Human, Machine


def choose_player(player_type):
    if player_type == 'h':
        return Human
    elif player_type == 'm':
        return Machine


def choose_eval(level):
    if level == 2:
        return None
    else:
        print(
            "Choose an evaluation function:\n1) Game and evaluation \n2) Game Position\n3) Number of seeds\n4) Extra "
            "Turn\n5) Rightside Pit\n6) Many Moves\n7) Keep on Own Side\n8) Closest to Opponent")
        while True:
            try:
                eval_choice = int(input("Enter a number between 1 and 8: "))
                if eval_choice == 1:
                    return static_eval
                if eval_choice == 2:
                    return simple_score
                elif eval_choice == 3:
                    return material_advantage
                elif eval_choice == 4:
                    return extra_turn
                elif eval_choice == 5:
                    return rightside_pit
                elif eval_choice == 6:
                    return many_moves
                elif eval_choice == 7:
                    return keep_on_own_side
                elif eval_choice == 8:
                    return closest_to_opponent
                else:
                    print("Invalid input.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")


def main():
    print("\nWhich player do you want: Human(h) or Machine(m)")

    playerOne = input("Player 1: ").strip().lower()
    while playerOne != 'm' and playerOne != 'h':
        print("Invalid input.\n")
        playerOne = input("Player 1: ").strip().lower()

    if playerOne == 'm':
        while True:
            try:
                levelOne = int(input("Machine level (2 for easy, 4 for medium, 6 for hard, and 8 for expert): "))
                if levelOne in [2, 4, 6, 8]:
                    break
                else:
                    print("Error: Invalid input.Please enter a valid level.")
            except ValueError:
                print("Error: Invalid input. Please enter a valid level.")

    playerTwo = input("Player 2: ").strip().lower()
    while playerTwo != 'm' and playerTwo != 'h':
        print("Invalid input.\n")
        playerTwo = input("Player 1: ").strip().lower()

    if playerTwo == 'm':
        while True:
            try:
                levelTwo = int(input("Machine level (2 for easy, 4 for medium, 6 for hard, and 8 for expert): "))
                if levelTwo in [2, 4, 6, 8]:
                    break
                else:
                    print("Error: Invalid input.Please enter a valid level.")
            except ValueError:
                print("Error: Invalid input. Please enter a valid level.")

    stealing_mode = input("Turn on STEALING mode? (y/n) ").strip().lower()
    while stealing_mode.strip().lower() != 'y' and stealing_mode.strip().lower() != 'n':
        stealing_mode = input("Turn on STEALING mode? (y/n) ").strip().lower()

    p_one = "Human" if playerOne != 'm' else "Machine"
    p_two = "Human" if playerTwo != 'm' else "Machine"

    players_one = choose_player(playerOne)(1) if playerOne != 'm' else Machine(1, levelOne, choose_eval(levelOne))
    players_two = choose_player(playerTwo)(2) if playerTwo != 'm' else Machine(0, levelTwo, choose_eval(levelTwo))

    print("\nReady, Players!\n")
    print(f"{p_one} vs {p_two}")
    play_game(players_one, players_two, stealing_mode)


if __name__ == "__main__":
    main()
