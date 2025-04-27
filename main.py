import random
import time
from copy import deepcopy

class TicTacToe:
    def __init__(self):
        # Initialize empty 3x3 board
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = random.choice(['X', 'O'])
        
    def print_board(self):
        """Display the current state of the board."""
        print("\n  0 1 2")
        for i in range(3):
            print(f"{i}", end=" ")
            for j in range(3):
                print(self.board[i][j], end=" ")
            print()
        print()
    
    def is_valid_move(self, row, col):
        """Check if a move is valid."""
        if 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == ' ':
            return True
        return False
    
    def make_move(self, row, col, player):
        """Place a player's mark on the board."""
        if self.is_valid_move(row, col):
            self.board[row][col] = player
            return True
        return False
    
    def get_available_moves(self):
        """Return a list of available moves as (row, col) tuples."""
        moves = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    moves.append((i, j))
        return moves
    
    def is_winner(self, player):
        """Check if the given player has won."""
        # Check rows
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)):
                return True
        
        # Check columns
        for j in range(3):
            if all(self.board[i][j] == player for i in range(3)):
                return True
        
        # Check diagonals
        if all(self.board[i][i] == player for i in range(3)):
            return True
        if all(self.board[i][2-i] == player for i in range(3)):
            return True
        
        return False
    
    def is_draw(self):
        """Check if the game is a draw."""
        return all(self.board[i][j] != ' ' for i in range(3) for j in range(3))
    
    def is_game_over(self):
        """Check if the game is over (win or draw)."""
        return self.is_winner('X') or self.is_winner('O') or self.is_draw()
    
    def switch_player(self):
        """Switch the current player."""
        self.current_player = 'O' if self.current_player == 'X' else 'X'
    
    def minimax(self, depth, is_maximizing, player, opponent):
        """Minimax algorithm for the AI."""
        if self.is_winner(player):
            return 10 - depth
        if self.is_winner(opponent):
            return depth - 10
        if self.is_draw():
            return 0
        
        available_moves = self.get_available_moves()
        if not available_moves:
            return 0
        
        if is_maximizing:
            best_score = float('-inf')
            for move in available_moves:
                row, col = move
                self.board[row][col] = player
                score = self.minimax(depth + 1, False, player, opponent)
                self.board[row][col] = ' '
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for move in available_moves:
                row, col = move
                self.board[row][col] = opponent
                score = self.minimax(depth + 1, True, player, opponent)
                self.board[row][col] = ' '
                best_score = min(score, best_score)
            return best_score
    
    def minimax_alpha_beta(self, depth, alpha, beta, is_maximizing, player, opponent):
        """Minimax algorithm with alpha-beta pruning for the AI."""
        if self.is_winner(player):
            return 10 - depth
        if self.is_winner(opponent):
            return depth - 10
        if self.is_draw():
            return 0
        
        available_moves = self.get_available_moves()
        if not available_moves:
            return 0
        
        if is_maximizing:
            best_score = float('-inf')
            for move in available_moves:
                row, col = move
                self.board[row][col] = player
                score = self.minimax_alpha_beta(depth + 1, alpha, beta, False, player, opponent)
                self.board[row][col] = ' '
                best_score = max(score, best_score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            return best_score
        else:
            best_score = float('inf')
            for move in available_moves:
                row, col = move
                self.board[row][col] = opponent
                score = self.minimax_alpha_beta(depth + 1, alpha, beta, True, player, opponent)
                self.board[row][col] = ' '
                best_score = min(score, best_score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            return best_score
    
    def get_best_move_minimax(self, player):
        """Get the best move using minimax algorithm."""
        opponent = 'O' if player == 'X' else 'X'
        best_score = float('-inf')
        best_move = None
        
        for move in self.get_available_moves():
            row, col = move
            self.board[row][col] = player
            score = self.minimax(0, False, player, opponent)
            self.board[row][col] = ' '
            
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move
    
    def get_best_move_alpha_beta(self, player):
        """Get the best move using minimax with alpha-beta pruning."""
        opponent = 'O' if player == 'X' else 'X'
        best_score = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')
        
        for move in self.get_available_moves():
            row, col = move
            self.board[row][col] = player
            score = self.minimax_alpha_beta(0, alpha, beta, False, player, opponent)
            self.board[row][col] = ' '
            
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move
    
    def human_turn(self):
        """Handle human player's turn."""
        while True:
            try:
                print(f"Your turn (you are {self.current_player})")
                row = int(input("Enter row (0-2): "))
                col = int(input("Enter column (0-2): "))
                
                if self.make_move(row, col, self.current_player):
                    break
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Please enter valid numbers (0-2).")
    
    def bot_turn_minimax(self):
        """Handle minimax bot's turn."""
        print(f"Minimax Bot's turn (playing as {self.current_player})...")
        time.sleep(1)  # Add a small delay to make it more user-friendly
        
        move = self.get_best_move_minimax(self.current_player)
        if move:
            row, col = move
            self.make_move(row, col, self.current_player)
            print(f"Minimax Bot placed {self.current_player} at position ({row}, {col})")
    
    def bot_turn_alpha_beta(self):
        """Handle alpha-beta pruning bot's turn."""
        print(f"Alpha-Beta Bot's turn (playing as {self.current_player})...")
        time.sleep(1)  # Add a small delay to make it more user-friendly
        
        move = self.get_best_move_alpha_beta(self.current_player)
        if move:
            row, col = move
            self.make_move(row, col, self.current_player)
            print(f"Alpha-Beta Bot placed {self.current_player} at position ({row}, {col})")
    
    def play_human_vs_minimax(self):
        """Human vs Minimax Bot game mode."""
        human_player = random.choice(['X', 'O'])
        bot_player = 'O' if human_player == 'X' else 'X'
        
        print(f"You are playing as {human_player}")
        print(f"Minimax Bot is playing as {bot_player}")
        print(f"{'You' if self.current_player == human_player else 'Minimax Bot'} will go first")
        
        while not self.is_game_over():
            self.print_board()
            
            if self.current_player == human_player:
                self.human_turn()
            else:
                self.bot_turn_minimax()
            
            if self.is_game_over():
                break
                
            self.switch_player()
        
        self.print_board()
        if self.is_winner(human_player):
            print("Congratulations! You won!")
        elif self.is_winner(bot_player):
            print("Minimax Bot wins!")
        else:
            print("It's a draw!")
    
    def play_human_vs_alpha_beta(self):
        """Human vs Alpha-Beta Bot game mode."""
        human_player = random.choice(['X', 'O'])
        bot_player = 'O' if human_player == 'X' else 'X'
        
        print(f"You are playing as {human_player}")
        print(f"Alpha-Beta Bot is playing as {bot_player}")
        print(f"{'You' if self.current_player == human_player else 'Alpha-Beta Bot'} will go first")
        
        while not self.is_game_over():
            self.print_board()
            
            if self.current_player == human_player:
                self.human_turn()
            else:
                self.bot_turn_alpha_beta()
            
            if self.is_game_over():
                break
                
            self.switch_player()
        
        self.print_board()
        if self.is_winner(human_player):
            print("Congratulations! You won!")
        elif self.is_winner(bot_player):
            print("Alpha-Beta Bot wins!")
        else:
            print("It's a draw!")
    
    def play_bot_vs_bot(self):
        """Minimax Bot vs Alpha-Beta Bot game mode."""
        minimax_player = 'X' if random.choice([True, False]) else 'O'
        alpha_beta_player = 'O' if minimax_player == 'X' else 'X'
        
        print(f"Minimax Bot is playing as {minimax_player}")
        print(f"Alpha-Beta Bot is playing as {alpha_beta_player}")
        print(f"{'Minimax Bot' if self.current_player == minimax_player else 'Alpha-Beta Bot'} will go first")
        
        while not self.is_game_over():
            self.print_board()
            
            if self.current_player == minimax_player:
                self.bot_turn_minimax()
            else:
                self.bot_turn_alpha_beta()
            
            if self.is_game_over():
                break
                
            self.switch_player()
            time.sleep(1)  # Pause between moves to make it easier to follow
        
        self.print_board()
        if self.is_winner(minimax_player):
            print("Minimax Bot wins!")
        elif self.is_winner(alpha_beta_player):
            print("Alpha-Beta Bot wins!")
        else:
            print("It's a draw!")

def main():
    print("Welcome to Tic Tac Toe!")
    print("1. Play against Minimax Bot")
    print("2. Play against Alpha-Beta Pruning Bot")
    print("3. Watch Bots play against each other")
    
    while True:
        try:
            choice = int(input("Enter your choice (1-3): "))
            if 1 <= choice <= 3:
                break
            else:
                print("Please enter a number between 1 and 3.")
        except ValueError:
            print("Please enter a valid number.")
    
    game = TicTacToe()
    
    if choice == 1:
        game.play_human_vs_minimax()
    elif choice == 2:
        game.play_human_vs_alpha_beta()
    else:
        game.play_bot_vs_bot()
    
    print("Thanks for playing!")

if __name__ == "__main__":
    main()