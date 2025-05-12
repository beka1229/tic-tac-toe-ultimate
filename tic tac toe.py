import tkinter as tk
from tkinter import font, messagebox
import random

# Main Tic-Tac-Toe game class
class TicTacToe:
    def __init__(self, root):
        # Initialize main window
        self.root = root
        self.root.title("Tic-Tac-Toe Ultimate")
        self.root.geometry("450x600")
        self.root.configure(bg="#f0f0f0")
        
        # Game state variables
        self.board = [" " for _ in range(9)]
        self.current_player = "X"
        self.scores = {"X": 0, "O": 0, "Draws": 0}
        self.game_active = False
        self.ai_enabled = False
        self.ai_difficulty = "hard"
        
        # Fonts used in the game
        self.title_font = font.Font(family="Helvetica", size=24, weight="bold")
        self.button_font = font.Font(family="Helvetica", size=28, weight="bold")
        self.score_font = font.Font(family="Helvetica", size=14)
        self.difficulty_font = font.Font(family="Helvetica", size=12)
        
        self.show_main_menu()

    # Display the main menu options
    def show_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        tk.Label(
            self.root, text="Tic-Tac-Toe Ultimate", 
            font=self.title_font, bg="#f0f0f0", fg="#333"
        ).pack(pady=20)
        
        tk.Button(
            self.root, text="Player vs AI", font=self.score_font,
            bg="#3498db", fg="white", width=20, height=2,
            command=self.show_ai_difficulty_menu
        ).pack(pady=10)
        
        tk.Button(
            self.root, text="Player vs Player", font=self.score_font,
            bg="#2ecc71", fg="white", width=20, height=2,
            command=self.setup_pvp_game
        ).pack(pady=10)

    # Show difficulty options for AI
    def show_ai_difficulty_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        tk.Label(
            self.root, text="Select AI Difficulty", 
            font=self.title_font, bg="#f0f0f0", fg="#333"
        ).pack(pady=20)
        
        # Difficulty button options
        difficulties = [
            ("Easy", "🟢", "#4CAF50"),
            ("Medium", "🟡", "#FFC107"),
            ("Hard", "🔴", "#F44336")
        ]
        
        for text, emoji, color in difficulties:
            btn = tk.Button(
                self.root, text=f"{emoji} {text}", font=self.difficulty_font,
                bg=color, fg="white", width=15, height=2,
                command=lambda diff=text.lower(): self.setup_ai_game(diff)
            )
            btn.pack(pady=7, ipadx=10)
        
        tk.Button(
            self.root, text="← Back", font=self.score_font,
            bg="#95a5a6", fg="white", command=self.show_main_menu
        ).pack(pady=20)

    # Initialize AI mode with chosen difficulty
    def setup_ai_game(self, difficulty):
        self.ai_enabled = True
        self.ai_difficulty = difficulty
        self.initialize_game()

    # Initialize player vs player mode
    def setup_pvp_game(self):
        self.ai_enabled = False
        self.initialize_game()

    # Initialize or reset game UI and variables
    def initialize_game(self):
        self.board = [" " for _ in range(9)]
        self.game_active = True
        self.current_player = "X"
        
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Score display
        self.score_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.score_frame.pack(pady=10)
        
        tk.Label(
            self.score_frame, text=f"Player X: {self.scores['X']}",
            font=self.score_font, bg="#f0f0f0", fg="#e74c3c"
        ).pack(side=tk.LEFT, padx=15)
        
        tk.Label(
            self.score_frame, text=f"Draws: {self.scores['Draws']}",
            font=self.score_font, bg="#f0f0f0", fg="#333"
        ).pack(side=tk.LEFT, padx=15)
        
        tk.Label(
            self.score_frame, 
            text=f"{'AI O' if self.ai_enabled else 'Player O'}: {self.scores['O']}",
            font=self.score_font, bg="#f0f0f0", fg="#3498db"
        ).pack(side=tk.LEFT, padx=15)
        
        # Show current player's turn
        self.player_label = tk.Label(
            self.root, text=f"Current: {self.current_player}",
            font=self.score_font, bg="#f0f0f0",
            fg="#e74c3c" if self.current_player == "X" else "#3498db"
        )
        self.player_label.pack(pady=5)
        
        # AI difficulty label (if enabled)
        if self.ai_enabled:
            color = {
                "easy": "#4CAF50",
                "medium": "#FFC107",
                "hard": "#F44336"
            }[self.ai_difficulty]
            
            tk.Label(
                self.root, text=f"AI Difficulty: {self.ai_difficulty.capitalize()}",
                font=self.score_font, bg=color, fg="white", bd=2, relief="groove"
            ).pack(pady=5)
        
        # Game board buttons
        self.board_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.board_frame.pack(pady=15)
        
        self.buttons = []
        for i in range(9):
            btn = tk.Button(
                self.board_frame, text=" ", font=self.button_font,
                width=3, height=1, bg="#fff", fg="#333",
                relief="groove", bd=3,
                command=lambda idx=i: self.make_move(idx)
            )
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.buttons.append(btn)
        
        tk.Button(
            self.root, text="Main Menu", font=self.score_font,
            bg="#95a5a6", fg="white", command=self.show_main_menu
        ).pack(pady=20)
        
        # Let AI play if it’s AI’s turn
        if self.ai_enabled and self.current_player == "O":
            self.root.after(500, self.ai_move)

    # Handle a move when a button is clicked
    def make_move(self, position):
        if self.board[position] == " " and self.game_active:
            self.board[position] = self.current_player
            self.buttons[position].config(
                text=self.current_player,
                fg="#e74c3c" if self.current_player == "X" else "#3498db"
            )
            
            if self.check_winner():
                self.handle_win()
            elif " " not in self.board:
                self.handle_draw()
            else:
                self.switch_player()
                if self.ai_enabled and self.current_player == "O":
                    self.root.after(500, self.ai_move)

    # Handle AI move logic based on difficulty
    def ai_move(self):
        if not self.game_active:
            return
            
        if self.ai_difficulty == "easy":
            move = random.choice([i for i, spot in enumerate(self.board) if spot == " "])
        elif self.ai_difficulty == "medium":
            if random.random() < 0.7:
                move = self.find_best_move()
            else:
                move = random.choice([i for i, spot in enumerate(self.board) if spot == " "])
        else:
            move = self.find_best_move()
        
        self.make_move(move)

    # Find best move using minimax
    def find_best_move(self):
        best_score = -float("inf")
        best_move = None
        for i in range(9):
            if self.board[i] == " ":
                self.board[i] = "O"
                score = self.minimax(self.board, 0, False)
                self.board[i] = " "
                if score > best_score:
                    best_score = score
                    best_move = i
        return best_move

    # Minimax algorithm for AI decision-making
    def minimax(self, board, depth, is_maximizing):
        if self.check_winner(board):
            return 1 if is_maximizing else -1
        elif " " not in board:
            return 0

        if is_maximizing:
            best_score = -float("inf")
            for i in range(9):
                if board[i] == " ":
                    board[i] = "O"
                    score = self.minimax(board, depth+1, False)
                    board[i] = " "
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float("inf")
            for i in range(9):
                if board[i] == " ":
                    board[i] = "X"
                    score = self.minimax(board, depth+1, True)
                    board[i] = " "
                    best_score = min(score, best_score)
            return best_score

    # Check if someone won
    def check_winner(self, board=None):
        if board is None:
            board = self.board
        win_combinations = [
            (0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)
        ]
        for a,b,c in win_combinations:
            if board[a] == board[b] == board[c] != " ":
                return True
        return False

    # Handle game win
    def handle_win(self):
        self.scores[self.current_player] += 1
        self.game_active = False
        self.highlight_winning_cells()
        winner = "AI" if (self.current_player == "O" and self.ai_enabled) else f"Player {self.current_player}"
        messagebox.showinfo("Game Over", f"{winner} wins!")
        self.offer_rematch()

    # Handle game draw
    def handle_draw(self):
        self.scores["Draws"] += 1
        self.game_active = False
        messagebox.showinfo("Game Over", "It's a draw!")
        self.offer_rematch()

    # Highlight the winning combination
    def highlight_winning_cells(self):
        win_combinations = [
            (0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)
        ]
        for a,b,c in win_combinations:
            if self.board[a] == self.board[b] == self.board[c] != " ":
                for idx in (a,b,c):
                    self.buttons[idx].config(bg="#2ecc71", fg="white")

    # Switch to the other player
    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"
        self.player_label.config(
            text=f"Current: {self.current_player}",
            fg="#e74c3c" if self.current_player == "X" else "#3498db"
        )

    # Ask user if they want a rematch
    def offer_rematch(self):
        answer = messagebox.askyesno("Rematch", "Play again?")
        if answer:
            self.reset_game()
        else:
            self.show_main_menu()

    # Reset game state for a new round
    def reset_game(self):
        self.board = [" " for _ in range(9)]
        self.current_player = "X"
        self.game_active = True
        self.player_label.config(
            text=f"Current: {self.current_player}",
            fg="#e74c3c"
        )
        for button in self.buttons:
            button.config(text=" ", bg="#fff", fg="#333")
        
        if self.ai_enabled and self.current_player == "O":
            self.root.after(500, self.ai_move)

# Start the game
if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
