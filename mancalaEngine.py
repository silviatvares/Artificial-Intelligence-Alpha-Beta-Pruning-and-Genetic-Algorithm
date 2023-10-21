from copy import deepcopy
import numpy as np

print("\nWelcome to Mancala Project!\n")
while True:
    try:
        pit_num = int(input("Enter number of pits: "))
        break
    except ValueError:
        print("Invalid input. Please enter a valid number.")
while True:
    try:
        seed = int(input("Enter number of seeds: "))
        break
    except ValueError:
        print("Invalid input. Please enter a valid number.")

initial_board = np.array(([seed] * pit_num + [0]) * 2)
turn = np.random.choice([0, 1])


class PocketName:
    num_pockets = pit_num * 2 + 2
    seed = seed
    p0_mancala = pit_num
    p1_mancala = num_pockets - 1
    p0_pockets = list(range(pit_num))
    p1_pockets = list(range(pit_num * 2, pit_num, -1))


class GameState:
    def __init__(self, init_state=initial_board, player_turn=turn, stealing=True):
        self.state = init_state
        self.player_turn = player_turn
        self.stealing = stealing
        self.winner = None

    def show(self):
        print()
        print(f"Player {self.player_turn}'s turn:")
        self.head_1 = "  "
        self.head_2 = "  "
        self.digit_seed = len(str(seed))
        if len(str(seed)) <= 2:
            self.blankspace = pit_num
        else:
            self.blankspace = pit_num + len(str(seed)) + 1
        for i in range(pit_num - 1, -1, -1):
            if i == pit_num - 1:
                self.head_1 += "  " + str(i)
            else:
                if len(str(seed)) == 3:
                    self.head_1 += "   " + str(i)
                elif len(str(seed)) >= 4:
                    self.head_1 += "    " + str(i)
                else:
                    self.head_1 += "  " + str(i)
        print("\n" + self.head_1)

        if len(str(seed)) <= 2:
            print("+---" + "---" * pit_num + "--+")
        else:
            print("+-----" + "----" * pit_num + "--+")
        print("  ", end=" ")
        for i in range(pit_num * 2, pit_num - 1, -1):
            if PocketName.p0_mancala < i < PocketName.p1_mancala:
                print(str(self.state[i]).rjust(2), end=" ")
        print("\n", self.state[PocketName.p1_mancala], "   " * self.blankspace, self.state[PocketName.p0_mancala])
        print("  ", end=" ")
        for i in range(pit_num):
            if i < PocketName.p0_mancala:
                print(str(self.state[i]).rjust(2), end=" ")
        if len(str(seed)) <= 2:
            print("\n+---" + "---" * pit_num + "--+")
        else:
            print("\n+-----" + "----" * pit_num + "--+")
        for j in range(pit_num):
            if j == 0:
                self.head_2 += "  " + str(j)
            else:
                if len(str(seed)) == 3:
                    self.head_2 += "   " + str(j)
                elif len(str(seed)) >= 4:
                    self.head_2 += "    " + str(j)
                else:
                    self.head_2 += "  " + str(j)
        print(self.head_2)

    def show_winning_message(self):
        print(f"Player {self.winner} Won!")

    def is_terminal(self):
        if self.winner is not None:
            return True
        return False

    def children(self):
        for move in self.possible_moves():
            new_state = self.make_move(move)
            yield move, new_state

    def possible_moves(self):
        if self.player_turn == 0:
            for i in PocketName.p0_pockets:
                if self.state[i] != 0:
                    yield i
        else:
            for i in PocketName.p1_pockets:
                if self.state[i] != 0:
                    yield i

    def make_move(self, move):
        # assumes that the move is valid
        player0_turn = self.player_turn == 0
        self.capture = False

        new_state = deepcopy(self.state)
        hand = new_state[move]
        new_state[move] = 0

        while hand > 0:
            move = (move + 1) % PocketName.num_pockets
            if (player0_turn and move == PocketName.p1_mancala) or (not player0_turn and move == PocketName.p0_mancala):
                # skip opponent's side
                continue
            hand -= 1
            new_state[move] += 1

        if self.stealing:
            if (player0_turn and move in PocketName.p0_pockets) or (not player0_turn and move in PocketName.p1_pockets):
                if new_state[move] == 1:
                    # steal seeds from opponent
                    opposite_move = pit_num * 2 - move
                    hand = new_state[move] + new_state[opposite_move]
                    new_state[move], new_state[opposite_move] = 0, 0
                    self.capture = True

                    if player0_turn:
                        new_state[PocketName.p0_mancala] += hand
                    else:
                        new_state[PocketName.p1_mancala] += hand

        if (player0_turn and move == PocketName.p0_mancala) or (not player0_turn and move == PocketName.p1_mancala):
            # play again 
            next_player = self.player_turn
        else:
            next_player = 1 - self.player_turn

        # check for winner
        game_done = sum(new_state[:pit_num]) == 0 or sum(new_state[pit_num + 1:pit_num * 2 + 1]) == 0
        winner = None
        if game_done:
            if sum(new_state[:pit_num]) == 0:
                new_state[PocketName.p1_mancala] += sum(new_state[pit_num + 1:pit_num * 2 + 1])
                for i in PocketName.p1_pockets:
                    new_state[i] = 0
            elif sum(new_state[pit_num + 1:pit_num * 2 + 1]) == 0:
                new_state[PocketName.p0_mancala] += sum(new_state[:pit_num])
                for i in PocketName.p0_pockets:
                    new_state[i] = 0
            winner = 0 if new_state[PocketName.p0_mancala] > new_state[PocketName.p1_mancala] else 1

        new_game_state = GameState(new_state, next_player, self.stealing)
        new_game_state.winner = winner
        return new_game_state


if __name__ == "__main__":
    game_state = GameState()
    game_state.show()
