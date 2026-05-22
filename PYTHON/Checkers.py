import tkinter as tk
from tkinter import messagebox
import random

class Checkers:
    def __init__(self, root):
        self.root = root
        self.root.title("👑 Checkers Game")
        self.root.geometry("750x800")
        self.root.configure(bg='#1a1a2e')
        
        # Game constants
        self.BOARD_SIZE = 8
        self.CELL_SIZE = 70
        self.PIECE_RADIUS = 28
        
        # Game variables
        self.board = [[None for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        self.current_player = 'red'
        self.game_mode = "2player"
        self.ai_difficulty = "medium"
        self.game_over = False
        self.selected_piece = None
        self.valid_moves = []
        self.winner = None
        
        # Colors
        self.light_square = '#f0d9b5'
        self.dark_square = '#b58863'
        self.red_piece = '#e74c3c'
        self.black_piece = '#2c3e50'
        self.highlight_color = '#f1c40f'
        self.move_highlight = '#90EE90'
        
        self.setup_ui()
        self.init_board()
        self.draw_board()
        self.canvas.bind("<Button-1>", self.on_click)
    
    def setup_ui(self):
        # Title
        title_frame = tk.Frame(self.root, bg='#1a1a2e')
        title_frame.pack(pady=10)
        
        title = tk.Label(title_frame, text="👑 CHECKERS 👑",
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
        
        # AI Difficulty
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
                                     bg='#1a1a2e', fg=self.red_piece)
        self.status_label.pack(pady=5)
        
        # Canvas for game board
        self.canvas = tk.Canvas(self.root, width=self.BOARD_SIZE * self.CELL_SIZE,
                               height=self.BOARD_SIZE * self.CELL_SIZE, 
                               bg=self.light_square, highlightthickness=0)
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
        self.black_score = 0
        
        self.red_score_label = tk.Label(score_frame, text=f"🔴 Red: {self.red_score}",
                                        font=('Arial', 14, 'bold'), bg='#16213e', fg=self.red_piece)
        self.red_score_label.pack(side=tk.LEFT, padx=40, pady=5)
        
        self.black_score_label = tk.Label(score_frame, text=f"⚫ Black: {self.black_score}",
                                          font=('Arial', 14, 'bold'), bg='#16213e', fg=self.black_piece)
        self.black_score_label.pack(side=tk.LEFT, padx=40, pady=5)
    
    def change_mode(self):
        self.game_mode = self.mode_var.get()
        if self.game_mode == "ai":
            self.difficulty_frame.pack(pady=5)
            self.status_label.config(text="Red's Turn (You)", fg=self.red_piece)
        else:
            self.difficulty_frame.pack_forget()
            self.status_label.config(text="Red's Turn", fg=self.red_piece)
        self.reset_game()
    
    def change_difficulty(self):
        self.ai_difficulty = self.difficulty_var.get()
        self.reset_game()
    
    def init_board(self):
        """Initialize the board with pieces"""
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                if (row + col) % 2 == 1:
                    if row < 3:
                        self.board[row][col] = {'color': 'black', 'king': False}
                    elif row > 4:
                        self.board[row][col] = {'color': 'red', 'king': False}
                    else:
                        self.board[row][col] = None
                else:
                    self.board[row][col] = None
    
    def draw_board(self):
        """Draw the game board"""
        self.canvas.delete("all")
        
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                x1 = col * self.CELL_SIZE
                y1 = row * self.CELL_SIZE
                x2 = x1 + self.CELL_SIZE
                y2 = y1 + self.CELL_SIZE
                
                color = self.light_square if (row + col) % 2 == 0 else self.dark_square
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='black', width=1)
                
                # Highlight selected piece
                if self.selected_piece and (row, col) == self.selected_piece:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.highlight_color, outline='orange', width=3)
                
                # Highlight valid moves
                for move in self.valid_moves:
                    if len(move) == 2 and (row, col) == move:
                        cx = x1 + self.CELL_SIZE // 2
                        cy = y1 + self.CELL_SIZE // 2
                        self.canvas.create_oval(cx - self.PIECE_RADIUS//2, cy - self.PIECE_RADIUS//2,
                                               cx + self.PIECE_RADIUS//2, cy + self.PIECE_RADIUS//2,
                                               fill=self.move_highlight, outline='green', width=2)
                    elif len(move) == 4 and (row, col) == (move[0], move[1]):
                        cx = x1 + self.CELL_SIZE // 2
                        cy = y1 + self.CELL_SIZE // 2
                        self.canvas.create_oval(cx - self.PIECE_RADIUS//2, cy - self.PIECE_RADIUS//2,
                                               cx + self.PIECE_RADIUS//2, cy + self.PIECE_RADIUS//2,
                                               fill='#ff6666', outline='red', width=2)
                
                # Draw piece
                piece = self.board[row][col]
                if piece:
                    cx = x1 + self.CELL_SIZE // 2
                    cy = y1 + self.CELL_SIZE // 2
                    color = self.red_piece if piece['color'] == 'red' else self.black_piece
                    outline_color = '#ffd700' if piece['king'] else 'white'
                    
                    self.canvas.create_oval(cx - self.PIECE_RADIUS, cy - self.PIECE_RADIUS,
                                           cx + self.PIECE_RADIUS, cy + self.PIECE_RADIUS,
                                           fill=color, outline=outline_color, width=3)
                    
                    if piece['king']:
                        self.canvas.create_text(cx, cy, text="👑", font=('Arial', 24), fill='#ffd700')
    
    def get_valid_moves(self, row, col):
        """Get all valid moves for a piece"""
        piece = self.board[row][col]
        if not piece:
            return []
        
        moves = []
        jumps = []
        directions = []
        
        if piece['king']:
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        else:
            if piece['color'] == 'red':
                directions = [(-1, -1), (-1, 1)]
            else:
                directions = [(1, -1), (1, 1)]
        
        # Check for jumps
        for dr, dc in directions:
            jump_row, jump_col = row + dr * 2, col + dc * 2
            mid_row, mid_col = row + dr, col + dc
            
            if 0 <= jump_row < self.BOARD_SIZE and 0 <= jump_col < self.BOARD_SIZE:
                mid_piece = self.board[mid_row][mid_col]
                if mid_piece and mid_piece['color'] != self.current_player:
                    if self.board[jump_row][jump_col] is None:
                        jumps.append((jump_row, jump_col, mid_row, mid_col))
        
        if jumps:
            return jumps
        
        # Check for regular moves
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < self.BOARD_SIZE and 0 <= new_col < self.BOARD_SIZE:
                if self.board[new_row][new_col] is None:
                    moves.append((new_row, new_col))
        
        return moves
    
    def get_all_moves(self, player):
        """Get all possible moves for a player"""
        all_moves = []
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                piece = self.board[row][col]
                if piece and piece['color'] == player:
                    moves = self.get_valid_moves(row, col)
                    for move in moves:
                        all_moves.append((row, col, move))
        return all_moves
    
    def make_move(self, from_row, from_col, to_row, to_col, jumped=None):
        """Execute a move"""
        piece = self.board[from_row][from_col].copy()
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = None
        
        if jumped:
            self.board[jumped[0]][jumped[1]] = None
            
            # Check for additional jumps
            additional_jumps = self.get_valid_moves(to_row, to_col)
            if additional_jumps and len(additional_jumps[0]) == 4:
                self.selected_piece = (to_row, to_col)
                self.valid_moves = additional_jumps
                self.draw_board()
                return True
        
        # King promotion
        if piece['color'] == 'red' and to_row == 0:
            self.board[to_row][to_col]['king'] = True
        elif piece['color'] == 'black' and to_row == self.BOARD_SIZE - 1:
            self.board[to_row][to_col]['king'] = True
        
        # Switch player
        self.current_player = 'black' if self.current_player == 'red' else 'red'
        self.selected_piece = None
        self.valid_moves = []
        self.draw_board()
        self.update_status()
        
        # Check for winner AFTER switching
        self.check_game_over()
        
        # AI move
        if self.game_mode == "ai" and not self.game_over and self.current_player == 'black':
            self.root.after(500, self.ai_move)
        
        return False
    
    def check_game_over(self):
        """Check if the game is over - FIXED VERSION"""
        # Count pieces
        red_count = 0
        black_count = 0
        
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                piece = self.board[row][col]
                if piece:
                    if piece['color'] == 'red':
                        red_count += 1
                    else:
                        black_count += 1
        
        # Check if players have any moves
        red_moves = self.get_all_moves('red')
        black_moves = self.get_all_moves('black')
        
        # Determine winner based on current player's turn
        if red_count == 0 or (len(red_moves) == 0 and red_count > 0):
            self.game_over = True
            self.winner = 'black'
            self.black_score += 1
            self.black_score_label.config(text=f"⚫ Black: {self.black_score}")
            messagebox.showinfo("Game Over", "Black wins! 🎉")
            self.status_label.config(text="Black Wins! 🎉", fg=self.black_piece)
        elif black_count == 0 or (len(black_moves) == 0 and black_count > 0):
            self.game_over = True
            self.winner = 'red'
            self.red_score += 1
            self.red_score_label.config(text=f"🔴 Red: {self.red_score}")
            messagebox.showinfo("Game Over", "Red wins! 🎉")
            self.status_label.config(text="Red Wins! 🎉", fg=self.red_piece)
    
    def on_click(self, event):
        """Handle mouse click"""
        if self.game_over:
            return
        
        if self.game_mode == "ai" and self.current_player == 'black':
            return
        
        col = event.x // self.CELL_SIZE
        row = event.y // self.CELL_SIZE
        
        if not (0 <= row < self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE):
            return
        
        if (row + col) % 2 == 0:
            if self.selected_piece:
                self.selected_piece = None
                self.valid_moves = []
                self.draw_board()
            return
        
        if self.selected_piece is None:
            piece = self.board[row][col]
            if piece and piece['color'] == self.current_player:
                self.selected_piece = (row, col)
                self.valid_moves = self.get_valid_moves(row, col)
                self.draw_board()
        else:
            from_row, from_col = self.selected_piece
            
            move_found = None
            for move in self.valid_moves:
                if len(move) == 2 and (row, col) == move:
                    move_found = move
                    break
                elif len(move) == 4 and (row, col) == (move[0], move[1]):
                    move_found = move
                    break
            
            if move_found:
                if len(move_found) == 2:
                    self.make_move(from_row, from_col, move_found[0], move_found[1])
                else:
                    self.make_move(from_row, from_col, move_found[0], move_found[1],
                                  jumped=(move_found[2], move_found[3]))
            else:
                self.selected_piece = None
                self.valid_moves = []
                self.draw_board()
    
    def ai_move(self):
        """AI makes a move"""
        if self.game_over or self.current_player != 'black':
            return
        
        all_moves = self.get_all_moves('black')
        
        if not all_moves:
            self.check_game_over()
            return
        
        if self.ai_difficulty == "easy":
            move_data = random.choice(all_moves)
        elif self.ai_difficulty == "medium":
            jumps = [m for m in all_moves if len(m[2]) == 4]
            if jumps:
                move_data = random.choice(jumps)
            else:
                move_data = random.choice(all_moves)
        else:  # hard
            jumps = [m for m in all_moves if len(m[2]) == 4]
            if jumps:
                move_data = random.choice(jumps)
            else:
                move_data = random.choice(all_moves)
        
        from_row, from_col, move = move_data
        if len(move) == 2:
            self.make_move(from_row, from_col, move[0], move[1])
        else:
            self.make_move(from_row, from_col, move[0], move[1], jumped=(move[2], move[3]))
    
    def update_status(self):
        """Update status label"""
        if not self.game_over:
            if self.current_player == 'red':
                self.status_label.config(text="Red's Turn", fg=self.red_piece)
            else:
                if self.game_mode == "ai":
                    self.status_label.config(text="AI's Turn...", fg=self.black_piece)
                else:
                    self.status_label.config(text="Black's Turn", fg=self.black_piece)
    
    def reset_scores(self):
        self.red_score = 0
        self.black_score = 0
        self.red_score_label.config(text=f"🔴 Red: {self.red_score}")
        self.black_score_label.config(text=f"⚫ Black: {self.black_score}")
    
    def reset_game(self):
        self.board = [[None for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        self.init_board()
        self.current_player = 'red'
        self.selected_piece = None
        self.valid_moves = []
        self.game_over = False
        self.winner = None
        self.draw_board()
        self.update_status()

if __name__ == "__main__":
    root = tk.Tk()
    game = Checkers(root)
    root.mainloop()