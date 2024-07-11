from typing import List

# Types de données
class Player:
    X = "X"
    O = "O"
    Empty = "_"

# Type d'état du jeu
State = List[List[Player]]

# Fonction pour vérifier si une case est vide
def is_empty(board: State, row: int, col: int) -> bool:
    try:
        row_index = int(row)
        col_index = int(col)
        return board[row_index][col_index] == Player.Empty
    except (ValueError, IndexError):
        return False


# Fonction pour afficher le plateau de jeu
def display_board(board: State) -> None:
    for row in board:
        print(" ".join(cell for cell in row))
    print()

# Évaluation de l'état du jeu
def evaluate_state(board: State) -> int:
    # Check if X or O wins
    for player in [Player.X, Player.O]:
        for i in range(3):
            # Check rows and columns for winning moves
            if board[i] == [player] * 3 or [board[row][i] for row in range(3)] == [player] * 3:
                return 10 if player == Player.X else -10

        # Check diagonals for winning moves
        if board[0][0] == board[1][1] == board[2][2] == player or \
           board[0][2] == board[1][1] == board[2][0] == player:
            return 10 if player == Player.X else -10

    # Check for draw
    if all(Player.Empty not in row for row in board):
        return 0

    # No winner yet
    return None


# Algorithme Alpha-Beta
def alphabeta(board: State, depth: int, alpha: int, beta: int, is_maximizing: bool) -> int:
    evaluate_score = evaluate_state(board)

    if evaluate_score is not None:
        return evaluate_score

    if depth == 0:
        return 0  # Return 0 if reached maximum depth

    if is_maximizing:
        best_score = float('-inf')
        for i in range(3):
            for j in range(3):
                if is_empty(board, i, j):
                    new_board = [row[:] for row in board]
                    new_board[i][j] = Player.X
                    score = alphabeta(new_board, depth - 1, alpha, beta, False)
                    best_score = max(best_score, score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if is_empty(board, i, j):
                    new_board = [row[:] for row in board]
                    new_board[i][j] = Player.O
                    score = alphabeta(new_board, depth - 1, alpha, beta, True)
                    best_score = min(best_score, score)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break
        return best_score


# Boucle de jeu
def game_loop(board: State, player_turn: Player) -> None:
    display_board(board)
    evaluate_score = evaluate_state(board)
    if evaluate_score == 10:
        print("X wins!")
        return
    elif evaluate_score == -10:
        print("O wins!")
        return
    elif evaluate_score == 0:
        print("It's a draw!")
        return

    if player_turn == Player.X:
        print("Player X's turn")
        row = int(input("Enter the row number (0, 1, or 2): "))
        col = int(input("Enter the column number (0, 1, or 2): "))
        if is_empty(board, row, col):
            board[row][col] = Player.X
            game_loop(board, Player.O)
        else:
            print("That cell is already occupied. Try again.")
            game_loop(board, player_turn)
    else:
        print("AI's turn (Player O)")
        best_score = float('-inf')
        best_move = None
        for i in range(3):
            for j in range(3):
                if is_empty(board, i, j):
                    new_board = [row[:] for row in board]
                    new_board[i][j] = Player.O
                    score = alphabeta(new_board, 9, float('-inf'), float('inf'), True)
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        if best_move:
            row, col = best_move
            board[row][col] = Player.O
            game_loop(board, Player.X)
        else:
            print("AI couldn't find a valid move. Something went wrong.")
            return

def start_game() -> None:
    print("Welcome to Tic Tac Toe!")
    initial_board = [[Player.Empty for _ in range(3)] for _ in range(3)]
    game_loop(initial_board, Player.X)

# Démarrer le jeu
if __name__ == "__main__":
    start_game()
