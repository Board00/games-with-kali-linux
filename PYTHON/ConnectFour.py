import tkinter as tk
from tkinter import messagebox
import random
import math
# import winsound  # For Windows sound effects (optional)
import sys

class ConnectFour:
    def __init__(self, root):
        self.root = root
        self.root.title("🔴 Connect Four 🟡")
        self.root.geometry("700x650")
        self.root.configure(bg='#1a1a2e')
        
        # Game constants
        self.ROWS = 6
        self.COLS = 7
        self.CELL_SIZE = 80
        self.RADIUS = 35
        
        # Game variables
        self.board = [[None for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.current_player = 'red'  # Red goes first
        self.game_mode = "2player"  # "2player" or "ai"
        self.ai_difficulty = "medium"  # "easy", "medium", "hard"
        self.game_over = False
        self.winner = None
        self.animation_running = False
        
        # Colors
        self.bg_color = '#1a1a2e'
        self.board_color = '#16213e'
        self.red_color = '#e74c3c'
        self.yellow_color = '#f1c40f'
        
        self.setup_ui()
        self.draw_board()
        
        # Bind click event
        self.canvas.bind("<Button-1>", self.on_click)
    
    def setup_ui(self):
        # Title
        title_frame = tk.Frame(self.root, bg='#1a1a2e')
        title_frame.pack(pady=10)
        
        title = tk.Label(title_frame, text="🔴 CONNECT FOUR 🟡",
                        font=('Arial', 28, 'bold'), bg='#1a1a2e', fg='#ffd700')
        title.pack()
        
        # Game mode selection
        mode_frame = tk.Frame(self.root, bg='#1a1a2e')
        mode_frame.pack(pady=5)
        
        tk.Label(mode_frame, text="Mode:", font=('Arial', 12),
                bg='#1a1a2e', fg='white').pack(side=tk.LEFT, padx=10)
        
        self.mode_var = tk.StringVar(value="2player")
        modes = [("👥 2-Player", "2player"), ("🤖 VS AI", "ai")]
        
        for text, value in modes:
            rb = tk.Radiobutton(mode_frame, text=text, variable=self.mode_var,
                               value=value, command=self.change_mode,
                               bg='#1a1a2e', fg='white', selectcolor='#1a1a2e')
            rb.pack(side=tk.LEFT, padx=10)
        
        # AI Difficulty (initially hidden)
        self.difficulty_frame = tk.Frame(self.root, bg='#1a1a2e')
        
        tk.Label(self.difficulty_frame, text="AI Difficulty:", font=('Arial', 12),
                bg='#1a1a2e', fg='white').pack(side=tk.LEFT, padx=10)
        
        self.difficulty_var = tk.StringVar(value="medium")
        difficulties = [("Easy", "easy"), ("Medium", "medium"), ("Hard", "hard")]
        
        for text, value in difficulties:
            rb = tk.Radiobutton(self.difficulty_frame, text=text, variable=self.difficulty_var,
                               value=value, command=self.change_difficulty,
                               bg='#1a1a2e', fg='white', selectcolor='#1a1a2e')
            rb.pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_label = tk.Label(self.root, text="Red's Turn", font=('Arial', 16, 'bold'),
                                     bg='#1a1a2e', fg=self.red_color)
        self.status_label.pack(pady=5)
        
        # Canvas for game board
        self.canvas = tk.Canvas(self.root, width=self.COLS * self.CELL_SIZE,
                               height=self.ROWS * self.CELL_SIZE, bg=self.board_color,
                               highlightthickness=0)
        self.canvas.pack(pady=10)
        
        # Control buttons
        control_frame = tk.Frame(self.root, bg='#1a1a2e')
        control_frame.pack(pady=10)
        
        self.reset_btn = tk.Button(control_frame, text="🔄 New Game", font=('Arial', 12, 'bold'),
                                   bg='#27ae60', fg='white', padx=20, pady=8,
                                   command=self.reset_game, cursor='hand2')
        self.reset_btn.pack(side=tk.LEFT, padx=10)
        
        self.reset_score_btn = tk.Button(control_frame, text="📊 Reset Scores", font=('Arial', 10),
                                         bg='#e74c3c', fg='white', padx=15, pady=5,
                                         command=self.reset_scores, cursor='hand2')
        self.reset_score_btn.pack(side=tk.LEFT, padx=10)
        
        # Score display
        score_frame = tk.Frame(self.root, bg='#16213e', relief=tk.RAISED, bd=3)
        score_frame.pack(pady=10, padx=20, fill='x')
        
        self.red_score = 0
        self.yellow_score = 0
        
        self.red_score_label = tk.Label(score_frame, text=f"🔴 Red: {self.red_score}",
                                        font=('Arial', 14, 'bold'), bg='#16213e', fg=self.red_color)
        self.red_score_label.pack(side=tk.LEFT, padx=40, pady=5)
        
        self.yellow_score_label = tk.Label(score_frame, text=f"🟡 Yellow: {self.yellow_score}",
                                           font=('Arial', 14, 'bold'), bg='#16213e', fg=self.yellow_color)
        self.yellow_score_label.pack(side=tk.LEFT, padx=40, pady=5)
    
    def change_mode(self):
        self.game_mode = self.mode_var.get()
        if self.game_mode == "ai":
            self.difficulty_frame.pack(pady=5)
            self.status_label.config(text="Red's Turn (You vs AI)")
        else:
            self.difficulty_frame.pack_forget()
            self.status_label.config(text="Red's Turn")
        self.reset_game()
    
    def change_difficulty(self):
        self.ai_difficulty = self.difficulty_var.get()
        self.reset_game()
    
    def draw_board(self):
        """Draw the game board"""
        self.canvas.delete("all")
        
        for row in range(self.ROWS):
            for col in range(self.COLS):
                x1 = col * self.CELL_SIZE
                y1 = row * self.CELL_SIZE
                x2 = x1 + self.CELL_SIZE
                y2 = y1 + self.CELL_SIZE
                
                # Draw cell background
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.board_color, outline='#2c3e50')
                
                # Draw circle for piece
                cx = x1 + self.CELL_SIZE // 2
                cy = y1 + self.CELL_SIZE // 2
                
                if self.board[row][col] == 'red':
                    self.canvas.create_oval(cx - self.RADIUS, cy - self.RADIUS,
                                           cx + self.RADIUS, cy + self.RADIUS,
                                           fill=self.red_color, outline='white', width=2)
                elif self.board[row][col] == 'yellow':
                    self.canvas.create_oval(cx - self.RADIUS, cy - self.RADIUS,
                                           cx + self.RADIUS, cy + self.RADIUS,
                                           fill=self.yellow_color, outline='white', width=2)
                else:
                    self.canvas.create_oval(cx - self.RADIUS, cy - self.RADIUS,
                                           cx + self.RADIUS, cy + self.RADIUS,
                                           fill='#2c3e50', outline='#34495e', width=2)
    
    def on_click(self, event):
        """Handle mouse click"""
        if self.game_over or self.animation_running:
            return
        
        col = event.x // self.CELL_SIZE
        
        if 0 <= col < self.COLS:
            if self.game_mode == "ai" and self.current_player == 'yellow' and self.ai_difficulty:
                return  # AI's turn
            self.drop_piece(col)
    
    def drop_piece(self, col):
        """Drop a piece in the selected column"""
        # Find the lowest empty row in the column
        for row in range(self.ROWS - 1, -1, -1):
            if self.board[row][col] is None:
                self.animate_drop(row, col, self.current_player)
                return False
        return False
    
    def animate_drop(self, target_row, col, player):
        """Animate the piece dropping"""
        self.animation_running = True
        
        # Disable clicks during animation
        self.canvas.unbind("<Button-1>")
        
        # Animation frames
        start_y = 0
        end_y = target_row * self.CELL_SIZE + self.CELL_SIZE // 2
        steps = 20
        
        def animate_step(step=0):
            if step <= steps:
                # Clear the area
                self.draw_board()
                
                # Draw dropping piece
                current_y = start_y + (end_y - start_y) * (step / steps)
                cx = col * self.CELL_SIZE + self.CELL_SIZE // 2
                
                color = self.red_color if player == 'red' else self.yellow_color
                self.canvas.create_oval(cx - self.RADIUS, current_y - self.RADIUS,
                                       cx + self.RADIUS, current_y + self.RADIUS,
                                       fill=color, outline='white', width=2)
                
                self.root.after(30, lambda: animate_step(step + 1))
            else:
                # Place piece on board
                self.board[target_row][col] = player
                self.draw_board()
                
                # Play sound
                self.play_sound('drop')
                
                # Check for win
                if self.check_win(target_row, col, player):
                    self.game_over = True
                    self.winner = player
                    self.update_score(player)
                    self.play_sound('win')
                    messagebox.showinfo("Game Over", f"{player.upper()} wins! 🎉")
                    self.status_label.config(text=f"{player.upper()} Wins! 🎉")
                    self.canvas.bind("<Button-1>", self.on_click)
                    self.animation_running = False
                    return
                
                # Check for tie
                if self.check_tie():
                    self.game_over = True
                    self.play_sound('tie')
                    messagebox.showinfo("Game Over", "It's a tie! 🤝")
                    self.status_label.config(text="It's a Tie! 🤝")
                    self.canvas.bind("<Button-1>", self.on_click)
                    self.animation_running = False
                    return
                
                # Switch player
                self.current_player = 'yellow' if self.current_player == 'red' else 'red'
                self.update_status()
                
                self.animation_running = False
                self.canvas.bind("<Button-1>", self.on_click)
                
                # AI move
                if self.game_mode == "ai" and not self.game_over and self.current_player == 'yellow':
                    self.root.after(500, self.ai_move)
        
        animate_step()
    
    def ai_move(self):
        """AI makes a move"""
        if self.game_over or self.current_player != 'yellow':
            return
        
        if self.ai_difficulty == "easy":
            col = self.get_random_move()
        elif self.ai_difficulty == "medium":
            col = self.get_medium_move()
        else:  # hard
            col = self.get_best_move()
        
        if col is not None:
            self.drop_piece(col)
    
    def get_random_move(self):
        """Easy AI: Random valid move"""
        valid_cols = [col for col in range(self.COLS) if self.board[0][col] is None]
        if valid_cols:
            return random.choice(valid_cols)
        return None
    
    def get_medium_move(self):
        """Medium AI: Try to win or block"""
        # Try to win
        for col in range(self.COLS):
            if self.is_valid_move(col):
                row = self.get_empty_row(col)
                if row is not None:
                    self.board[row][col] = 'yellow'
                    if self.check_win(row, col, 'yellow'):
                        self.board[row][col] = None
                        return col
                    self.board[row][col] = None
        
        # Try to block player
        for col in range(self.COLS):
            if self.is_valid_move(col):
                row = self.get_empty_row(col)
                if row is not None:
                    self.board[row][col] = 'red'
                    if self.check_win(row, col, 'red'):
                        self.board[row][col] = None
                        return col
                    self.board[row][col] = None
        
        # Otherwise random
        return self.get_random_move()
    
    def get_best_move(self):
        """Hard AI: Use minimax algorithm"""
        best_score = -math.inf
        best_col = None
        
        for col in range(self.COLS):
            if self.is_valid_move(col):
                row = self.get_empty_row(col)
                if row is not None:
                    self.board[row][col] = 'yellow'
                    score = self.minimax(self.board, 4, -math.inf, math.inf, False)
                    self.board[row][col] = None
                    
                    if score > best_score:
                        best_score = score
                        best_col = col
        
        return best_col if best_col is not None else self.get_random_move()
    
    def minimax(self, board, depth, alpha, beta, is_maximizing):
        """Minimax algorithm with alpha-beta pruning"""
        # Check terminal states
        if self.check_win_board(board, 'yellow'):
            return 1000000
        if self.check_win_board(board, 'red'):
            return -1000000
        if self.is_board_full(board) or depth == 0:
            return self.evaluate_board(board)
        
        if is_maximizing:
            max_score = -math.inf
            for col in range(self.COLS):
                row = self.get_empty_row_board(board, col)
                if row is not None:
                    board[row][col] = 'yellow'
                    score = self.minimax(board, depth - 1, alpha, beta, False)
                    board[row][col] = None
                    max_score = max(max_score, score)
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
            return max_score
        else:
            min_score = math.inf
            for col in range(self.COLS):
                row = self.get_empty_row_board(board, col)
                if row is not None:
                    board[row][col] = 'red'
                    score = self.minimax(board, depth - 1, alpha, beta, True)
                    board[row][col] = None
                    min_score = min(min_score, score)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
            return min_score
    
    def evaluate_board(self, board):
        """Evaluate the board position"""
        score = 0
        # Center column preference
        center_col = self.COLS // 2
        for row in range(self.ROWS):
            if board[row][center_col] == 'yellow':
                score += 3
            elif board[row][center_col] == 'red':
                score -= 3
        
        # Evaluate all possible windows of 4
        for row in range(self.ROWS):
            for col in range(self.COLS - 3):
                window = [board[row][col + i] for i in range(4)]
                score += self.evaluate_window(window)
        
        for col in range(self.COLS):
            for row in range(self.ROWS - 3):
                window = [board[row + i][col] for i in range(4)]
                score += self.evaluate_window(window)
        
        for row in range(self.ROWS - 3):
            for col in range(self.COLS - 3):
                window = [board[row + i][col + i] for i in range(4)]
                score += self.evaluate_window(window)
        
        for row in range(3, self.ROWS):
            for col in range(self.COLS - 3):
                window = [board[row - i][col + i] for i in range(4)]
                score += self.evaluate_window(window)
        
        return score
    
    def evaluate_window(self, window):
        """Evaluate a window of 4 pieces"""
        yellow_count = window.count('yellow')
        red_count = window.count('red')
        
        if yellow_count == 4:
            return 100
        elif yellow_count == 3 and window.count(None) == 1:
            return 5
        elif yellow_count == 2 and window.count(None) == 2:
            return 2
        
        if red_count == 4:
            return -100
        elif red_count == 3 and window.count(None) == 1:
            return -5
        elif red_count == 2 and window.count(None) == 2:
            return -2
        
        return 0
    
    def is_valid_move(self, col):
        """Check if move is valid"""
        return self.board[0][col] is None
    
    def get_empty_row(self, col):
        """Get the lowest empty row in column"""
        for row in range(self.ROWS - 1, -1, -1):
            if self.board[row][col] is None:
                return row
        return None
    
    def get_empty_row_board(self, board, col):
        """Get empty row for a given board state"""
        for row in range(self.ROWS - 1, -1, -1):
            if board[row][col] is None:
                return row
        return None
    
    def is_board_full(self, board):
        """Check if board is full"""
        return all(board[0][col] is not None for col in range(self.COLS))
    
    def check_win_board(self, board, player):
        """Check win for a given board state"""
        # Horizontal
        for row in range(self.ROWS):
            for col in range(self.COLS - 3):
                if all(board[row][col + i] == player for i in range(4)):
                    return True
        
        # Vertical
        for col in range(self.COLS):
            for row in range(self.ROWS - 3):
                if all(board[row + i][col] == player for i in range(4)):
                    return True
        
        # Diagonal (positive slope)
        for row in range(self.ROWS - 3):
            for col in range(self.COLS - 3):
                if all(board[row + i][col + i] == player for i in range(4)):
                    return True
        
        # Diagonal (negative slope)
        for row in range(3, self.ROWS):
            for col in range(self.COLS - 3):
                if all(board[row - i][col + i] == player for i in range(4)):
                    return True
        
        return False
    
    def check_win(self, row, col, player):
        """Check if the current move wins the game"""
        # Horizontal
        count = 1
        for c in range(col + 1, self.COLS):
            if self.board[row][c] == player:
                count += 1
            else:
                break
        for c in range(col - 1, -1, -1):
            if self.board[row][c] == player:
                count += 1
            else:
                break
        if count >= 4:
            return True
        
        # Vertical
        count = 1
        for r in range(row + 1, self.ROWS):
            if self.board[r][col] == player:
                count += 1
            else:
                break
        if count >= 4:
            return True
        
        # Diagonal (positive slope)
        count = 1
        r, c = row + 1, col + 1
        while r < self.ROWS and c < self.COLS:
            if self.board[r][c] == player:
                count += 1
                r += 1
                c += 1
            else:
                break
        r, c = row - 1, col - 1
        while r >= 0 and c >= 0:
            if self.board[r][c] == player:
                count += 1
                r -= 1
                c -= 1
            else:
                break
        if count >= 4:
            return True
        
        # Diagonal (negative slope)
        count = 1
        r, c = row + 1, col - 1
        while r < self.ROWS and c >= 0:
            if self.board[r][c] == player:
                count += 1
                r += 1
                c -= 1
            else:
                break
        r, c = row - 1, col + 1
        while r >= 0 and c < self.COLS:
            if self.board[r][c] == player:
                count += 1
                r -= 1
                c += 1
            else:
                break
        if count >= 4:
            return True
        
        return False
    
    def check_tie(self):
        """Check if the game is a tie"""
        return all(self.board[0][col] is not None for col in range(self.COLS))
    
    def update_score(self, player):
        """Update score for winner"""
        if player == 'red':
            self.red_score += 1
            self.red_score_label.config(text=f"🔴 Red: {self.red_score}")
        else:
            self.yellow_score += 1
            self.yellow_score_label.config(text=f"🟡 Yellow: {self.yellow_score}")
    
    def reset_scores(self):
        """Reset scores"""
        self.red_score = 0
        self.yellow_score = 0
        self.red_score_label.config(text=f"🔴 Red: {self.red_score}")
        self.yellow_score_label.config(text=f"🟡 Yellow: {self.yellow_score}")
    
    def update_status(self):
        """Update status label"""
        if self.current_player == 'red':
            self.status_label.config(text="Red's Turn", fg=self.red_color)
        else:
            if self.game_mode == "ai":
                self.status_label.config(text="AI's Turn (Thinking...)", fg=self.yellow_color)
            else:
                self.status_label.config(text="Yellow's Turn", fg=self.yellow_color)
    
    def play_sound(self, sound_type):
        """Play sound effects (Windows only, optional)"""
        try:
            if sys.platform == "win32":
                if sound_type == 'drop':
                    winsound.Beep(440, 100)
                elif sound_type == 'win':
                    winsound.Beep(880, 300)
                    winsound.Beep(440, 300)
                elif sound_type == 'tie':
                    winsound.Beep(330, 200)
                    winsound.Beep(330, 200)
        except:
            pass  # Skip sound if not available
    
    def reset_game(self):
        """Reset the game"""
        self.board = [[None for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.current_player = 'red'
        self.game_over = False
        self.winner = None
        self.draw_board()
        self.update_status()
        self.canvas.bind("<Button-1>", self.on_click)

if __name__ == "__main__":
    root = tk.Tk()
    game = ConnectFour(root)
    root.mainloop()