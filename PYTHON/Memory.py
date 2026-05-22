import tkinter as tk
from tkinter import messagebox
import random
from itertools import product

class MemoryCardGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🧠 Memory Card Match")
        self.root.geometry("800x700")
        self.root.resizable(False, False)
        self.root.configure(bg='#2d1810')
        
        # Game variables
        self.grid_size = 4  # 4x4 grid (8 pairs)
        self.cards = []
        self.card_buttons = []
        self.first_card = None
        self.first_index = None
        self.second_card = None
        self.second_index = None
        self.locked = False
        self.moves = 0
        self.matches = 0
        self.total_pairs = 8
        self.theme = "emojis"  # "emojis", "colors", "numbers"
        
        # Themes
        self.themes = {
            "emojis": ["🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼"],
            "animals": ["🦁", "🐧", "🐘", "🦒", "🐪", "🐬", "🦋", "🐞"],
            "fruits": ["🍎", "🍐", "🍊", "🍋", "🍌", "🍉", "🍒", "🍓"],
            "sports": ["⚽", "🏀", "🏈", "⚾", "🎾", "🏐", "🏓", "🥊"],
            "space": ["🌍", "🌙", "⭐", "☄️", "🪐", "🌞", "🚀", "👽"]
        }
        
        self.current_theme_icons = self.themes["emojis"]
        
        self.setup_ui()
        self.start_new_game()
    
    def setup_ui(self):
        # Title Frame
        title_frame = tk.Frame(self.root, bg='#2d1810')
        title_frame.pack(pady=15)
        
        title_label = tk.Label(
            title_frame,
            text="🧠 MEMORY CARD MATCH BY KONI 🧠",
            font=('Arial', 18, 'bold'),
            bg='#2d1810',
            fg='#ffd700'
        )
        title_label.pack()
        
        # Stats Frame
        stats_frame = tk.Frame(self.root, bg='#2d1810')
        stats_frame.pack(pady=10)
        
        # Moves counter
        self.moves_label = tk.Label(
            stats_frame,
            text="Moves: 0",
            font=('Arial', 16, 'bold'),
            bg='#2d1810',
            fg='#ffffff'
        )
        self.moves_label.pack(side=tk.LEFT, padx=20)
        
        # Matches counter
        self.matches_label = tk.Label(
            stats_frame,
            text=f"Matches: 0/{self.total_pairs}",
            font=('Arial', 16, 'bold'),
            bg='#2d1810',
            fg='#ffffff'
        )
        self.matches_label.pack(side=tk.LEFT, padx=20)
        
        # Timer
        self.time_elapsed = 0
        self.timer_running = False
        self.timer_label = tk.Label(
            stats_frame,
            text="Time: 0s",
            font=('Arial', 16, 'bold'),
            bg='#2d1810',
            fg='#ffd700'
        )
        self.timer_label.pack(side=tk.LEFT, padx=20)
        
        # Theme Selection Frame
        theme_frame = tk.Frame(self.root, bg='#2d1810')
        theme_frame.pack(pady=10)
        
        tk.Label(
            theme_frame,
            text="Theme:",
            font=('Arial', 12),
            bg='#2d1810',
            fg='#ffffff'
        ).pack(side=tk.LEFT, padx=10)
        
        self.theme_var = tk.StringVar(value="emojis")
        themes_list = [("😊 Emojis", "emojis"), ("🦁 Animals", "animals"), 
                       ("🍎 Fruits", "fruits"), ("⚽ Sports", "sports"),
                       ("🚀 Space", "space")]
        
        for text, value in themes_list:
            tk.Radiobutton(
                theme_frame,
                text=text,
                variable=self.theme_var,
                value=value,
                command=self.change_theme,
                bg='#2d1810',
                fg='#ffffff',
                selectcolor='#2d1810',
                activebackground='#2d1810'
            ).pack(side=tk.LEFT, padx=5)
        
        # Game Board Frame
        self.board_frame = tk.Frame(self.root, bg='#3d2317', relief=tk.RAISED, bd=5)
        self.board_frame.pack(pady=20, padx=20)
        
        # Control Buttons
        control_frame = tk.Frame(self.root, bg='#2d1810')
        control_frame.pack(pady=15)
        
        self.new_game_btn = tk.Button(
            control_frame,
            text="🔄 New Game",
            font=('Arial', 12, 'bold'),
            bg='#4a6fa5',
            fg='white',
            padx=20,
            pady=10,
            command=self.start_new_game,
            cursor='hand2'
        )
        self.new_game_btn.pack(side=tk.LEFT, padx=10)
        
        self.shuffle_btn = tk.Button(
            control_frame,
            text="🎲 Shuffle",
            font=('Arial', 12, 'bold'),
            bg='#6b4c3a',
            fg='white',
            padx=20,
            pady=10,
            command=self.shuffle_board,
            cursor='hand2'
        )
        self.shuffle_btn.pack(side=tk.LEFT, padx=10)
        
        # Status Label
        self.status_label = tk.Label(
            self.root,
            text="Click on cards to find matching pairs!",
            font=('Arial', 12, 'italic'),
            bg='#2d1810',
            fg='#ffd700'
        )
        self.status_label.pack(pady=10)
    
    def change_theme(self):
        self.theme = self.theme_var.get()
        self.current_theme_icons = self.themes[self.theme]
        self.start_new_game()
    
    def start_new_game(self):
        # Reset game state
        self.moves = 0
        self.matches = 0
        self.first_card = None
        self.second_card = None
        self.locked = False
        self.time_elapsed = 0
        self.timer_running = False
        
        # Update displays
        self.moves_label.config(text="Moves: 0")
        self.matches_label.config(text=f"Matches: 0/{self.total_pairs}")
        self.timer_label.config(text="Time: 0s")
        self.status_label.config(text="New game! Find matching pairs!", fg='#ffd700')
        
        # Create card pairs
        pairs = self.current_theme_icons[:self.total_pairs]
        self.cards = pairs * 2
        random.shuffle(self.cards)
        
        # Create board
        self.create_board()
        
        # Start timer after first move
        self.start_timer()
    
    def create_board(self):
        # Clear existing board
        for widget in self.board_frame.winfo_children():
            widget.destroy()
        
        self.card_buttons = []
        
        # Calculate button size based on grid
        btn_width = 8
        btn_height = 3
        
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                index = i * self.grid_size + j
                btn = tk.Button(
                    self.board_frame,
                    text="?",
                    font=('Arial', 24, 'bold'),
                    width=btn_width,
                    height=btn_height,
                    bg='#4a3729',
                    fg='#ffd700',
                    activebackground='#5c4535',
                    relief=tk.RAISED,
                    bd=3,
                    command=lambda idx=index: self.card_click(idx)
                )
                btn.grid(row=i, column=j, padx=5, pady=5)
                row.append(btn)
            self.card_buttons.append(row)
    
    def shuffle_board(self):
        if not self.locked:
            random.shuffle(self.cards)
            self.reset_board_display()
            self.status_label.config(text="Board shuffled! Keep playing!", fg='#ffd700')
    
    def reset_board_display(self):
        # Reset all cards to face-down
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.card_buttons[i][j].config(text="?", bg='#4a3729', state=tk.NORMAL)
        
        self.first_card = None
        self.second_card = None
        self.locked = False
    
    def card_click(self, index):
        if self.locked:
            return
        
        if not self.timer_running:
            self.start_timer()
        
        row = index // self.grid_size
        col = index % self.grid_size
        
        # Check if card is already matched or already flipped
        if self.card_buttons[row][col].cget('text') != "?":
            return
        
        # If this is the first card
        if self.first_card is None:
            self.first_card = self.cards[index]
            self.first_index = index
            self.show_card(row, col, self.first_card)
        
        # If this is the second card and it's not the same as first
        elif self.second_card is None and index != self.first_index:
            self.second_card = self.cards[index]
            self.second_index = index
            self.show_card(row, col, self.second_card)
            
            # Check for match
            self.moves += 1
            self.moves_label.config(text=f"Moves: {self.moves}")
            
            if self.first_card == self.second_card:
                # Match found
                self.matches += 1
                self.matches_label.config(text=f"Matches: {self.matches}/{self.total_pairs}")
                self.status_label.config(text="🎉 Match found! 🎉", fg='#00ff00')
                
                # Keep cards face-up (disable them)
                self.disable_card(self.first_index)
                self.disable_card(self.second_index)
                
                # Reset temporary variables
                self.first_card = None
                self.second_card = None
                
                # Check win condition
                if self.matches == self.total_pairs:
                    self.game_won()
            else:
                # No match - flip cards back after delay
                self.locked = True
                self.status_label.config(text="❌ No match! Try again! ❌", fg='#ff4444')
                self.root.after(800, self.reset_cards)
    
    def show_card(self, row, col, value):
        self.card_buttons[row][col].config(text=value, bg='#6b4c3a')
    
    def disable_card(self, index):
        row = index // self.grid_size
        col = index % self.grid_size
        self.card_buttons[row][col].config(state=tk.DISABLED, bg='#2d5a27')
    
    def reset_cards(self):
        # Flip back the two unmatched cards
        row1 = self.first_index // self.grid_size
        col1 = self.first_index % self.grid_size
        row2 = self.second_index // self.grid_size
        col2 = self.second_index % self.grid_size
        
        self.card_buttons[row1][col1].config(text="?", bg='#4a3729')
        self.card_buttons[row2][col2].config(text="?", bg='#4a3729')
        
        # Reset temporary variables
        self.first_card = None
        self.second_card = None
        self.locked = False
        self.status_label.config(text="Keep going! Find the matches!", fg='#ffd700')
    
    def start_timer(self):
        if not self.timer_running and self.matches < self.total_pairs:
            self.timer_running = True
            self.update_timer()
    
    def update_timer(self):
        if self.timer_running and self.matches < self.total_pairs:
            self.time_elapsed += 1
            self.timer_label.config(text=f"Time: {self.time_elapsed}s")
            self.root.after(1000, self.update_timer)
    
    def stop_timer(self):
        self.timer_running = False
    
    def game_won(self):
        self.stop_timer()
        
        # Calculate score
        score = max(1000 - (self.moves * 5) - (self.time_elapsed * 2), 0)
        
        result = messagebox.askyesno(
            "🏆 YOU WIN! 🏆",
            f"Congratulations!\n\n"
            f"📊 Stats:\n"
            f"• Moves: {self.moves}\n"
            f"• Time: {self.time_elapsed} seconds\n"
            f"• Score: {score} points\n\n"
            f"Play again?",
            icon='info'
        )
        
        if result:
            self.start_new_game()
        else:
            self.status_label.config(text="Thanks for playing! Click New Game to play again.", fg='#ffd700')
            self.locked = True  # Prevent further moves until new game

class MemoryCardGame6x6(MemoryCardGame):
    """Advanced 6x6 version with 18 pairs"""
    def __init__(self, root):
        self.grid_size = 6
        self.total_pairs = 18
        super().__init__(root)
    
    def setup_ui(self):
        super().setup_ui()
        # Adjust window size for 6x6
        self.root.geometry("900x850")

def main():
    root = tk.Tk()
    
    # Ask for grid size
    choice = messagebox.askquestion(
        "Select Difficulty",
        "Would you like to play the CLASSIC 4x4 game?\n\n"
        "Yes = 4x4 (8 pairs, easier)\n"
        "No = 6x6 (18 pairs, harder)"
    )
    
    if choice == 'yes':
        game = MemoryCardGame(root)
    else:
        game = MemoryCardGame6x6(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()