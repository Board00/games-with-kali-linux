import tkinter as tk
from tkinter import messagebox
import random
from math import inf

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Tic-Tac-Toe")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        self.root.configure(bg='#1a1a2e')
        
        # Game variables
        self.board = [''] * 9
        self.current_player = 'X'  # X goes first
        self.game_mode = "2player"  # "2player" or "ai"
        self.ai_difficulty = "medium"  # "easy", "medium", "hard"
        self.game_active = True
        
        # Colors
        self.bg_color = '#1a1a2e'
        self.board_color = '#16213e'
        self.cell_color = '#0f3460'
        self.x_color = '#e94560'
        self.o_color = '#00fff5'
        self.text_color = '#ffffff'
        
        self.setup_ui()
        
    def setup_ui(self):
        # Title
        title_frame = tk.Frame(self.root, bg=self.bg_color)
        title_frame.pack(pady=20)
        
        title_label = tk.Label(
            title_frame,
            text="TIC-TAC-TOE",
            font=('Arial', 28, 'bold'),
            bg=self.bg_color,
            fg=self.text_color
        )
        title_label.pack()
        
        # Mode Selection
        mode_frame = tk.Frame(self.root, bg=self.bg_color)
        mode_frame.pack(pady=10)
        
        tk.Label(
            mode_frame,
            text="Game Mode:",
            font=('Arial', 12),
            bg=self.bg_color,
            fg=self.text_color
        ).pack(side=tk.LEFT, padx=10)
        
        self.mode_var = tk.StringVar(value="2player")
        modes = [("👥 2-Player", "2player"), ("🤖 VS AI", "ai")]
        
        for text, value in modes:
            tk.Radiobutton(
                mode_frame,
                text=text,
                variable=self.mode_var,
                value=value,
                command=self.change_mode,
                bg=self.bg_color,
                fg=self.text_color,
                selectcolor=self.bg_color,
                activebackground=self.bg_color,
                font=('Arial', 10)
            ).pack(side=tk.LEFT, padx=15)
        
        # AI Difficulty (initially hidden)
        self.difficulty_frame = tk.Frame(self.root, bg=self.bg_color)
        
        tk.Label(
            self.difficulty_frame,
            text="AI Difficulty:",
            font=('Arial', 12),
            bg=self.bg_color,
            fg=self.text_color
        ).pack(side=tk.LEFT, padx=10)
        
        self.difficulty_var = tk.StringVar(value="medium")
        difficulties = [("Easy", "easy"), ("Medium", "medium"), ("Hard", "hard")]
        
        for text, value in difficulties:
            tk.Radiobutton(
                self.difficulty_frame,
                text=text,
                variable=self.difficulty_var,
                value=value,
                command=self.change_difficulty,
                bg=self.bg_color,
                fg=self.text_color,
                selectcolor=self.bg_color,
                activebackground=self.bg_color,
                font=('Arial', 10)
            ).pack(side=tk.LEFT, padx=10)
        
        # Status Display
        self.status_frame = tk.Frame(self.root, bg=self.bg_color)
        self.status_frame.pack(pady=15)
        
        self.status_label = tk.Label(
            self.status_frame,
            text="Player X's Turn",
            font=('Arial', 18, 'bold'),
            bg=self.bg_color,
            fg=self.x_color
        )
        self.status_label.pack()
        
        # Game Board
        self.board_frame = tk.Frame(self.root, bg=self.board_color)
        self.board_frame.pack(pady=20)
        
        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                btn = tk.Button(
                    self.board_frame,
                    text='',
                    font=('Arial', 40, 'bold'),
                    width=4,
                    height=2,
                    bg=self.cell_color,
                    fg=self.x_color,
                    activebackground=self.board_color,
                    command=lambda row=i, col=j: self.make_move(row, col)
                )
                btn.grid(row=i, column=j, padx=5, pady=5)
                row.append(btn)
            self.buttons.append(row)
        
        # Control Buttons
        control_frame = tk.Frame(self.root, bg=self.bg_color)
        control_frame.pack(pady=20)
        
        self.reset_button = tk.Button(
            control_frame,
            text="🔄 New Game",
            font=('Arial', 12, 'bold'),
            bg='#e94560',
            fg='white',
            padx=20,
            pady=10,
            command=self.reset_game,
            cursor='hand2'
        )
        self.reset_button.pack(side=tk.LEFT, padx=10)
        
        # Score Display
        self.score_frame = tk.Frame(self.root, bg=self.bg_color)
        self.score_frame.pack(pady=10)
        
        self.x_score = 0
        self.o_score = 0
        
        self.score_label = tk.Label(
            self.score_frame,
            text=f"X: {self.x_score}  |  O: {self.o_score}",
            font=('Arial', 14),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.score_label.pack()
        
        # Update UI based on mode
        self.change_mode()
    
    def change_mode(self):
        self.game_mode = self.mode_var.get()
        if self.game_mode == "ai":
            self.difficulty_frame.pack(pady=5)
            self.status_label.config(text=f"Player X's Turn (You vs AI)")
            self.current_player = 'X'
            self.update_board_display()
        else:
            self.difficulty_frame.pack_forget()
            self.status_label.config(text=f"Player X's Turn")
            self.current_player = 'X'
            self.update_board_display()
        self.reset_game()
    
    def change_difficulty(self):
        self.ai_difficulty = self.difficulty_var.get()
        self.reset_game()
    
    def make_move(self, row, col):
        index = row * 3 + col
        
        if not self.game_active:
            return
        
        if self.board[index] != '':
            return
        
        # Make the move
        self.board[index] = self.current_player
        self.buttons[row][col].config(
            text=self.current_player,
            fg=self.x_color if self.current_player == 'X' else self.o_color
        )
        
        # Check for win or tie
        if self.check_win():
            self.game_active = False
            winner = self.current_player
            self.update_score(winner)
            messagebox.showinfo("Game Over", f"Player {winner} wins! 🎉")
            self.status_label.config(text=f"Player {winner} Wins! 🎉")
            return
        elif self.check_tie():
            self.game_active = False
            messagebox.showinfo("Game Over", "It's a tie! 🤝")
            self.status_label.config(text="It's a Tie! 🤝")
            return
        
        # Switch player
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        self.update_status()
        
        # AI Move
        if self.game_mode == "ai" and self.game_active and self.current_player == 'O':
            self.root.after(500, self.ai_move)  # Delay for better UX
    
    def ai_move(self):
        if not self.game_active or self.current_player != 'O':
            return
        
        if self.ai_difficulty == "easy":
            move = self.get_random_move()
        elif self.ai_difficulty == "medium":
            move = self.get_medium_move()
        else:  # hard
            move = self.get_best_move()
        
        if move is not None:
            row, col = move
            self.make_move(row, col)
    
    def get_random_move(self):
        """Easy AI: Random move"""
        available = [i for i in range(9) if self.board[i] == '']
        if available:
            index = random.choice(available)
            return (index // 3, index % 3)
        return None
    
    def get_medium_move(self):
        """Medium AI: Block wins and try to win"""
        # Check if AI can win
        for i in range(9):
            if self.board[i] == '':
                self.board[i] = 'O'
                if self.check_win_on_board():
                    self.board[i] = ''
                    return (i // 3, i % 3)
                self.board[i] = ''
        
        # Check if player can win and block
        for i in range(9):
            if self.board[i] == '':
                self.board[i] = 'X'
                if self.check_win_on_board():
                    self.board[i] = ''
                    return (i // 3, i % 3)
                self.board[i] = ''
        
        # Otherwise random move
        return self.get_random_move()
    
    def get_best_move(self):
        """Hard AI: Minimax algorithm - unbeatable"""
        best_score = -inf
        best_move = None
        
        for i in range(9):
            if self.board[i] == '':
                self.board[i] = 'O'
                score = self.minimax(self.board, 0, False)
                self.board[i] = ''
                
                if score > best_score:
                    best_score = score
                    best_move = (i // 3, i % 3)
        
        return best_move
    
    def minimax(self, board, depth, is_maximizing):
        # Check terminal states
        winner = self.check_winner_on_board(board)
        if winner == 'O':
            return 10 - depth
        elif winner == 'X':
            return -10 + depth
        elif self.is_board_full(board):
            return 0
        
        if is_maximizing:
            best_score = -inf
            for i in range(9):
                if board[i] == '':
                    board[i] = 'O'
                    score = self.minimax(board, depth + 1, False)
                    board[i] = ''
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = inf
            for i in range(9):
                if board[i] == '':
                    board[i] = 'X'
                    score = self.minimax(board, depth + 1, True)
                    board[i] = ''
                    best_score = min(score, best_score)
            return best_score
    
    def check_win_on_board(self):
        """Check if current board state is a win (for current move test)"""
        win_combinations = [
            [0,1,2], [3,4,5], [6,7,8],  # Rows
            [0,3,6], [1,4,7], [2,5,8],  # Columns
            [0,4,8], [2,4,6]             # Diagonals
        ]
        
        for combo in win_combinations:
            if (self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ''):
                return True
        return False
    
    def check_winner_on_board(self, board):
        """Check winner for minimax"""
        win_combinations = [
            [0,1,2], [3,4,5], [6,7,8],
            [0,3,6], [1,4,7], [2,5,8],
            [0,4,8], [2,4,6]
        ]
        
        for combo in win_combinations:
            if (board[combo[0]] == board[combo[1]] == board[combo[2]] != ''):
                return board[combo[0]]
        return None
    
    def is_board_full(self, board):
        return all(cell != '' for cell in board)
    
    def check_win(self):
        win_combinations = [
            [0,1,2], [3,4,5], [6,7,8],  # Rows
            [0,3,6], [1,4,7], [2,5,8],  # Columns
            [0,4,8], [2,4,6]             # Diagonals
        ]
        
        for combo in win_combinations:
            if (self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ''):
                return True
        return False
    
    def check_tie(self):
        return all(cell != '' for cell in self.board) and not self.check_win()
    
    def update_score(self, winner):
        if winner == 'X':
            self.x_score += 1
        else:
            self.o_score += 1
        self.score_label.config(text=f"X: {self.x_score}  |  O: {self.o_score}")
    
    def update_status(self):
        if self.game_active:
            if self.current_player == 'X':
                self.status_label.config(text="Player X's Turn", fg=self.x_color)
            else:
                if self.game_mode == "ai":
                    self.status_label.config(text="AI's Turn (Thinking...)", fg=self.o_color)
                else:
                    self.status_label.config(text="Player O's Turn", fg=self.o_color)
    
    def update_board_display(self):
        for i in range(3):
            for j in range(3):
                index = i * 3 + j
                if self.board[index] == 'X':
                    self.buttons[i][j].config(text='X', fg=self.x_color)
                elif self.board[index] == 'O':
                    self.buttons[i][j].config(text='O', fg=self.o_color)
                else:
                    self.buttons[i][j].config(text='')
    
    def reset_game(self):
        self.board = [''] * 9
        self.current_player = 'X'
        self.game_active = True
        
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text='', bg=self.cell_color)
        
        self.update_status()
        
        # If AI starts (but X always starts in this version)
        # AI never starts first to keep it fair
    
def main():
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()

if __name__ == "__main__":
    main()