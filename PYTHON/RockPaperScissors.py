import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk  # pip install pillow

class RockPaperScissors:
    def __init__(self, root):
        self.root = root
        self.root.title("✊ Rock Paper Scissors")
        self.root.geometry("800x600")
        self.root.configure(bg='#1a1a2e')
        
        # Scores
        self.player_score = 0
        self.computer_score = 0
        
        # Moves
        self.moves = {
            'rock': {'emoji': '✊', 'name': 'Rock', 'beats': 'scissors'},
            'paper': {'emoji': '✋', 'name': 'Paper', 'beats': 'rock'},
            'scissors': {'emoji': '✌️', 'name': 'Scissors', 'beats': 'paper'}
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        # Title
        title = tk.Label(self.root, text="✊ ROCK PAPER SCISSORS ✋", 
                        font=('Arial', 28, 'bold'), bg='#1a1a2e', fg='#ffd700')
        title.pack(pady=20)
        
        # Score Frame
        score_frame = tk.Frame(self.root, bg='#1a1a2e')
        score_frame.pack(pady=20)
        
        self.player_score_label = tk.Label(score_frame, text=f"You: {self.player_score}",
                                           font=('Arial', 20), bg='#1a1a2e', fg='#00ff00')
        self.player_score_label.pack(side=tk.LEFT, padx=40)
        
        self.computer_score_label = tk.Label(score_frame, text=f"Computer: {self.computer_score}",
                                             font=('Arial', 20), bg='#1a1a2e', fg='#ff4444')
        self.computer_score_label.pack(side=tk.LEFT, padx=40)
        
        # Game Display Frame
        self.game_frame = tk.Frame(self.root, bg='#16213e', relief=tk.RAISED, bd=5)
        self.game_frame.pack(pady=30, padx=50, fill='both', expand=True)
        
        # Player and Computer choices display
        display_frame = tk.Frame(self.game_frame, bg='#16213e')
        display_frame.pack(pady=40)
        
        self.player_display = tk.Label(display_frame, text="❓", font=('Arial', 80),
                                       bg='#16213e', fg='white', width=5)
        self.player_display.pack(side=tk.LEFT, padx=50)
        
        self.vs_label = tk.Label(display_frame, text="VS", font=('Arial', 40, 'bold'),
                                 bg='#16213e', fg='#ffd700')
        self.vs_label.pack(side=tk.LEFT, padx=50)
        
        self.computer_display = tk.Label(display_frame, text="❓", font=('Arial', 80),
                                         bg='#16213e', fg='white', width=5)
        self.computer_display.pack(side=tk.LEFT, padx=50)
        
        # Result Label
        self.result_label = tk.Label(self.game_frame, text="Click a button to start!",
                                     font=('Arial', 18, 'bold'), bg='#16213e', fg='#ffd700')
        self.result_label.pack(pady=20)
        
        # Move Buttons
        button_frame = tk.Frame(self.root, bg='#1a1a2e')
        button_frame.pack(pady=30)
        
        rock_btn = tk.Button(button_frame, text="✊ Rock", font=('Arial', 16, 'bold'),
                            bg='#e74c3c', fg='white', padx=30, pady=15,
                            command=lambda: self.play('rock'), cursor='hand2')
        rock_btn.pack(side=tk.LEFT, padx=10)
        
        paper_btn = tk.Button(button_frame, text="✋ Paper", font=('Arial', 16, 'bold'),
                             bg='#3498db', fg='white', padx=30, pady=15,
                             command=lambda: self.play('paper'), cursor='hand2')
        paper_btn.pack(side=tk.LEFT, padx=10)
        
        scissors_btn = tk.Button(button_frame, text="✌️ Scissors", font=('Arial', 16, 'bold'),
                                bg='#2ecc71', fg='white', padx=30, pady=15,
                                command=lambda: self.play('scissors'), cursor='hand2')
        scissors_btn.pack(side=tk.LEFT, padx=10)
        
        # Reset Button
        reset_btn = tk.Button(self.root, text="Reset Scores", font=('Arial', 12),
                             bg='#95a5a6', fg='white', padx=20, pady=10,
                             command=self.reset_scores, cursor='hand2')
        reset_btn.pack(pady=10)
    
    def play(self, player_move):
        computer_move = random.choice(['rock', 'paper', 'scissors'])
        
        # Update displays
        self.player_display.config(text=self.moves[player_move]['emoji'])
        self.computer_display.config(text=self.moves[computer_move]['emoji'])
        
        # Determine winner
        if player_move == computer_move:
            result = "It's a Tie! 🤝"
            result_color = '#ffd700'
        elif self.moves[player_move]['beats'] == computer_move:
            result = "You Win! 🎉"
            result_color = '#00ff00'
            self.player_score += 1
        else:
            result = "Computer Wins! 💀"
            result_color = '#ff4444'
            self.computer_score += 1
        
        self.result_label.config(text=result, fg=result_color)
        self.update_scores()
        
        # Check for game winner
        if self.player_score >= 5:
            messagebox.showinfo("Game Over!", "Congratulations! You won the game! 🏆")
            self.reset_scores()
        elif self.computer_score >= 5:
            messagebox.showinfo("Game Over!", "Computer wins the game! Better luck next time! 💀")
            self.reset_scores()
    
    def update_scores(self):
        self.player_score_label.config(text=f"You: {self.player_score}")
        self.computer_score_label.config(text=f"Computer: {self.computer_score}")
    
    def reset_scores(self):
        self.player_score = 0
        self.computer_score = 0
        self.update_scores()
        self.player_display.config(text="❓")
        self.computer_display.config(text="❓")
        self.result_label.config(text="Scores reset! Click a button to start!", fg='#ffd700')

if __name__ == "__main__":
    root = tk.Tk()
    game = RockPaperScissors(root)
    root.mainloop()