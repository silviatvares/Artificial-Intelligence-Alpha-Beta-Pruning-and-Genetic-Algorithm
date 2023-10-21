import numpy as np
import random
from mancalaEngine import PocketName, GameState

pinf = np.inf
ninf = - np.inf


def static_eval(game_state):
    """
       Evaluate the given game state and return a numeric value representing the expected outcome of the game.

       The returned value is positive if the current player is expected to win, negative if they are expected to lose,
       and zero if the game is expected to end in a tie.

       Args:
           game_state: A `GameState` object representing the current state of the game.

       Returns:
           A numeric value representing the expected outcome of the game.

       """
    if game_state.is_terminal():
        if game_state.state[PocketName.p0_mancala] > game_state.state[PocketName.p1_mancala]:
            value = 100
        elif game_state.state[PocketName.p0_mancala] == game_state.state[PocketName.p1_mancala]:
            value = 0
        else:
            value = -100
    else:
        value = game_state.state[PocketName.p0_mancala] - game_state.state[PocketName.p1_mancala]
    return value


def simple_score(game_state):
    """
    Simple Score: An evaluation function that returns the difference between the current player's score
    and the opponent's score. This function encourages the current player to maximize their own score while
    minimizing their opponent's score.

    Args:
        game_state: A `GameState` object representing the current state of the game.

    Returns:
        The difference between the current player's score and the opponent's score, where the current
        player is determined by the `current_player_id` property of the `game_state` object. If the difference
        is positive, the current player is in the lead, and if it is negative, the current player is behind.
        If the difference is zero, the game is tied.
    """
    player_score = game_state.state[PocketName.p0_mancala]
    opponent_score = game_state.state[PocketName.p1_mancala]
    player = game_state.current_player_id
    if player == 1:
        player_score, opponent_score = opponent_score, player_score
    return player_score - opponent_score


def material_advantage(game_state):
    """
    Evaluate the material advantage of the given game state and return a numeric value representing the expected
    outcome of the game.
    The returned value is positive if the current player has a material advantage, negative if they have a
       disadvantage, and zero if both players have equal amount of materials.

       Args:
           game_state: A `GameState` object representing the current state of the game.

       Returns:
           A numeric value representing the material advantage of the game.
    """
    player_material = sum(game_state.state[PocketName.p0_pockets])
    opponent_material = sum(game_state.state[PocketName.p1_pockets])
    player = game_state.current_player_id
    if player == 1:
        player_material, opponent_material = opponent_material, player_material
    return player_material - opponent_material


def extra_turn(game_state):
    """
    Extra turn and capture heuristic. Choose the moove that gives an extra turn.

    Args:
    - board: list of integers representing the current board state

    Returns:
    - integer representing the number of seeds to add to the hoarded seeds value for the Right Side pit heuristic
    """
    pit = game_state.move
    player = game_state.current_player_id
    aux = PocketName.p0_mancala + 1

    # Check if the last seed was sown in an empty pit on the player's side
    if pit % aux == PocketName.p0_mancala or game_state[pit] > 1:
        return 0

    # Check if the last seed was sown in a pit with seeds on the player's side
    opposite_pit = PocketName.p0_mancala * 2 - pit
    if opposite_pit < player * aux or opposite_pit > player * aux + PocketName.p0_mancala - 1 \
            or game_state[opposite_pit] == 0:
        return 0

    # Calculate the number of seeds to add to the hoarded seeds value
    captured_seeds = game_state[opposite_pit]
    game_state[player * aux - 1] += captured_seeds + 1
    game_state[opposite_pit] = 0
    game_state[pit] = 0

    # Check if the player gets an extra turn
    if player == 0 and pit == PocketName.p0_mancala or player == 1 and pit == PocketName.p1_mancala:
        return captured_seeds + rightside_pit(game_state)

    return captured_seeds


def rightside_pit(game_state):
    """
    Hoard as many seeds as possible in the pit on the right side heuristic.

    Args:
    - board: list of integers representing the current board stat

    Returns:
    - integer representing the heuristic value of the board for the given player
    """
    player = game_state.current_player_id
    aux = PocketName.p0_mancala + 1
    # Find all pits that belong to the player
    player_pits = [i for i in range(player * aux, player * aux + PocketName.p0_mancala)]

    # Find the right-most pit with seeds
    hoarding_pit = max(player_pits, key=lambda x: game_state[x])

    # Check if the hoarding pit is empty or has only one seed
    if game_state[hoarding_pit] <= 1:
        return 0

    # Calculate the number of seeds that would be hoarded
    hoarded_seeds = game_state[hoarding_pit] - (PocketName.p0_mancala - hoarding_pit % aux)

    # Check if the hoarding pit leads to a capture or extra turn
    if (hoarding_pit + hoarded_seeds) % (PocketName.p1_mancala + 1) == player * aux + PocketName.p0_mancala:
        hoarded_seeds += extra_turn(game_state[:], hoarding_pit + hoarded_seeds, player)

    return hoarded_seeds


def keep_on_own_side(game_state):
    """
    Keep as many seeds as possible on the player's own side heuristic.

    Args:
    - board: list of integers representing the current board state

    Returns:
    - integer representing the number of seeds to add to the hoarded seeds value for the H1 heuristic
    """
    # Initialize variables 
    player_seeds = 0
    opponent_seeds = 0
    player = game_state.current_player_id

    # Count the number of seeds on the player's side and the opponent's side
    if player == 0:
        player_seeds = sum(game_state.state[PocketName.p0_pockets])
        opponent_seeds = sum(game_state.state[PocketName.p1_pockets])
    else:
        player_seeds = sum(game_state.state[PocketName.p1_pockets])
        opponent_seeds = sum(game_state.state[PocketName.p0_pockets])

    # Calculate the difference between the number of seeds on the player's side and the opponent's side
    seed_difference = player_seeds - opponent_seeds

    # If the difference is positive, return it as the number of seeds to add to the hoarded seeds value
    if seed_difference > 0:
        return seed_difference

    # If the difference is negative or 0, return 0 as the number of seeds to add to the hoarded seeds value
    else:
        return 0


def many_moves(game_state):
    """
    Have as many moves as possible from which to choose heuristic.

    Args:
    - board: list of integers representing the current board state

    Returns:
    - integer representing the number of seeds to add to the hoarded seeds value for the H1 heuristic
    """
    # Initialize variables 
    pit = game_state.move
    valid_moves = 0
    aux = PocketName.p0_mancala + 1
    player = game_state.current_player_id
    pit = game_state.move

    # Iterate over the indices of the pits on the player's side
    for i in range(player * aux, (player + 1) * aux):
        # Check if the pit contains seeds
        if game_state[i] > 0:
            # Check if sowing from this pit would result in a capture
            if GameState.capture:
                valid_moves += 1
            # Otherwise, check if sowing from this pit would result in an extra turn
            elif player == 0 and pit == PocketName.p0_mancala or player == 1 and pit == PocketName.p1_mancala:
                valid_moves += 1
            # If neither condition is met, sowing from this pit would not result in a capture or an extra turn,
            # so it is a valid move but does not add to the number of valid moves
            else:
                valid_moves += 1

    # Return the number of valid moves as the number of seeds to add to the hoarded seeds value
    return valid_moves


def closest_to_opponent(game_state):
    """
    Choose a move based in the pit closest to the opponent's side.

    Args:
    - board: list of integers representing the current board state

    Returns:
    - integer representing the index of the pit to sow from
    """
    aux = PocketName.p0_mancala + 1
    player = game_state.current_player_id

    # Determine the range of pits to consider based on the current player
    if player == 0:
        pits = range(PocketName.p0_mancala, 0, -1)
    else:
        pits = range(aux, PocketName.p1_mancala)

    # Check each pit in the range
    for pit_index in pits:
        # Check if the pit has seeds
        if game_state[pit_index] > 0:
            # Return the pit index
            return pit_index

    # If no pits in the range have seeds, choose a random pit
    return random.choice([pit_index for pit_index in range(player * aux - PocketName.p0_mancala, player * aux) if
                          game_state[pit_index] > 0])


def random_move(state):
    """
    Returns a random move from the current state of the game.
    """
    possible_moves = list(state.possible_moves())
    if len(possible_moves) == 0:
        return None
    move = random.choice(possible_moves)
    return move


def minimax(state, depth, evaluation_func=static_eval):
    """
        The minimax algorithm is a recursive algorithm used to find the optimal move in a two-player, zero-sum game.
        It explores the game tree by alternating between maximizing and minimizing the value of each node until it
        reaches a leaf node or a specified depth.

        Args:
        state: A `GameState` object representing the current state of the game.
        depth: An integer representing the maximum depth to explore the game tree.
        evaluation_func: A function that takes a `GameState` object and returns a numeric value representing the
        expected outcome of the game. the evaluation function used to evaluate game states, defaults to static_eval.

        Returns:
            A tuple containing the best move and its corresponding value for the current player. If the current player
            is the maximizer, the best move is the move that leads to the maximum value, and if the current player is
            the minimizer, the best move is the move that leads to the minimum value. The value of the best move is
            returned as the second element of the tuple. If the game has ended or the maximum depth has been reached,
            the function returns None as the best move and the static evaluation of the current state as the value.
        """
    if depth <= 0 or state.is_terminal():
        return None, evaluation_func(state)

    if state.player_turn == 1:  # maximizer
        value = ninf
        best_move = None

        for move, child in state.children():
            _, child_value = minimax(child, depth - 1)
            if child_value > value:
                value = child_value
                best_move = move
        return best_move, value

    else:  # player 2: minimizer
        value = pinf
        best_move = None

        for move, child in state.children():
            _, child_value = minimax(child, depth - 1)
            if child_value < value:
                value = child_value
                best_move = move
        return best_move, value


def minimax_alpha_beta(state, depth, alpha=ninf, beta=pinf, eval_func=static_eval):
    """
    Perform minimax search with alpha-beta pruning to find the optimal move for the current player at a given state.
    Args:
    - state: the current game state
    - depth: the maximum search depth
    - alpha: the alpha value used for alpha-beta pruning, defaults to negative infinity
    - beta: the beta value used for alpha-beta pruning, defaults to positive infinity
    - eval_func: the evaluation function used to evaluate game states, defaults to static_eval

    Returns:
    - best_move: the optimal move for the current player
    - value: the value of the best move found by the search algorithm
    """

    if depth == 0 or state.is_terminal():
        return None, eval_func(state)

    if state.player_turn == 1:  # maximizer
        value = ninf
        best_move = None

        for move, child in state.children():
            _, child_value = minimax_alpha_beta(child, depth - 1, alpha, beta)
            if child_value > value:
                value = child_value
                best_move = move
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_move, value

    else:  # player 2: minimizer
        value = pinf
        best_move = None

        for move, child in state.children():
            _, child_value = minimax_alpha_beta(child, depth - 1, alpha, beta)
            if child_value < value:
                value = child_value
                best_move = move
            beta = min(beta, value)
            if beta <= alpha:
                break
        return best_move, value
