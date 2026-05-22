import tkinter as tk
from tkinter import messagebox
import random

class NumberGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🔢 Number Guessing Game")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        self.root.configure(bg='#2c3e50')
        
        # Game variables
        self.secret_number = None
        self.attempts = 0
        self.max_attempts = 10
        self.difficulty = "medium"
        self.min_range = 1
        self.max_range = 100
        
        # Colors
        self.bg_color = '#2c3e50'
        self.fg_color = '#ecf0f1'
        self.button_color = '#3498db'
        self.button_hover = '#2980b9'
        
        self.setup_ui()
        self.new_game()
    
    def setup_ui(self):
        # Title Frame
        title_frame = tk.Frame(self.root, bg=self.bg_color)
        title_frame.pack(pady=20)
        
        title_label = tk.Label(
            title_frame,
            text="🎯 NUMBER GUESSING GAME BY KONI",
            font=('Arial', 18, 'bold'),
            bg=self.bg_color,
            fg=self.fg_color
        )
        title_label.pack()
        
        # Difficulty Frame
        diff_frame = tk.Frame(self.root, bg=self.bg_color)
        diff_frame.pack(pady=10)
        
        tk.Label(
            diff_frame,
            text="Difficulty:",
            font=('Arial', 12),
            bg=self.bg_color,
            fg=self.fg_color
        ).pack(side=tk.LEFT, padx=5)
        
        self.difficulty_var = tk.StringVar(value="medium")
        difficulties = [("Easy", "easy"), ("Medium", "medium"), ("Hard", "hard")]
        
        for text, value in difficulties:
            tk.Radiobutton(
                diff_frame,
                text=text,
                variable=self.difficulty_var,
                value=value,
                command=self.change_difficulty,
                bg=self.bg_color,
                fg=self.fg_color,
                selectcolor=self.bg_color,
                activebackground=self.bg_color
            ).pack(side=tk.LEFT, padx=10)
        
        # Range Display
        self.range_frame = tk.Frame(self.root, bg=self.bg_color)
        self.range_frame.pack(pady=10)
        
        self.range_label = tk.Label(
            self.range_frame,
            text="Range: 1 - 100",
            font=('Arial', 14),
            bg=self.bg_color,
            fg='#e74c3c'
        )
        self.range_label.pack()
        
        # Guess Entry Frame
        guess_frame = tk.Frame(self.root, bg=self.bg_color)
        guess_frame.pack(pady=20)
        
        self.guess_entry = tk.Entry(
            guess_frame,
            font=('Arial', 18),
            width=15,
            justify='center',
            bd=3
        )
        self.guess_entry.pack(pady=10)
        self.guess_entry.bind('<Return>', lambda event: self.check_guess())
        
        # Buttons Frame
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(pady=10)
        
        self.guess_button = tk.Button(
            button_frame,
            text="🔍 CHECK GUESS",
            font=('Arial', 12, 'bold'),
            bg=self.button_color,
            fg='white',
            padx=20,
            pady=10,
            command=self.check_guess,
            cursor='hand2'
        )
        self.guess_button.pack(pady=5)
        
        # Hover effect
        self.guess_button.bind('<Enter>', lambda e: self.guess_button.configure(bg=self.button_hover))
        self.guess_button.bind('<Leave>', lambda e: self.guess_button.configure(bg=self.button_color))
        
        self.new_button = tk.Button(
            button_frame,
            text="🔄 NEW GAME",
            font=('Arial', 12, 'bold'),
            bg='#e67e22',
            fg='white',
            padx=20,
            pady=10,
            command=self.new_game,
            cursor='hand2'
        )
        self.new_button.pack(pady=5)
        
        # Hint Display
        self.hint_frame = tk.Frame(self.root, bg=self.bg_color)
        self.hint_frame.pack(pady=20)
        
        self.hint_label = tk.Label(
            self.hint_frame,
            text="💡 Enter your guess and click CHECK!",
            font=('Arial', 12, 'italic'),
            bg=self.bg_color,
            fg='#f39c12',
            wraplength=400
        )
        self.hint_label.pack()
        
        # Attempts Display
        self.attempts_frame = tk.Frame(self.root, bg=self.bg_color)
        self.attempts_frame.pack(pady=10)
        
        self.attempts_label = tk.Label(
            self.attempts_frame,
            text=f"Attempts: 0/{self.max_attempts}",
            font=('Arial', 14),
            bg=self.bg_color,
            fg=self.fg_color
        )
        self.attempts_label.pack()
        
        # Previous Guesses
        self.history_frame = tk.Frame(self.root, bg=self.bg_color)
        self.history_frame.pack(pady=20)
        
        tk.Label(
            self.history_frame,
            text="📝 Previous Guesses:",
            font=('Arial', 12, 'bold'),
            bg=self.bg_color,
            fg=self.fg_color
        ).pack()
        
        self.history_text = tk.Text(
            self.history_frame,
            height=6,
            width=30,
            font=('Courier', 10),
            bg='#34495e',
            fg=self.fg_color,
            bd=0
        )
        self.history_text.pack(pady=5)
        
        # Stats Display
        self.stats_frame = tk.Frame(self.root, bg=self.bg_color)
        self.stats_frame.pack(pady=10)
        
        self.stats_label = tk.Label(
            self.stats_frame,
            text="",
            font=('Arial', 10),
            bg=self.bg_color,
            fg='#95a5a6'
        )
        self.stats_label.pack()
        
        # Focus on entry
        self.guess_entry.focus()
    
    def change_difficulty(self):
        self.difficulty = self.difficulty_var.get()
        if self.difficulty == "easy":
            self.max_attempts = 15
            self.min_range = 1
            self.max_range = 50
            self.range_label.config(text="Range: 1 - 50")
        elif self.difficulty == "medium":
            self.max_attempts = 10
            self.min_range = 1
            self.max_range = 100
            self.range_label.config(text="Range: 1 - 100")
        else:  # hard
            self.max_attempts = 7
            self.min_range = 1
            self.max_range = 200
            self.range_label.config(text="Range: 1 - 200")
        
        self.new_game()
    
    def new_game(self):
        self.secret_number = random.randint(self.min_range, self.max_range)
        self.attempts = 0
        self.attempts_label.config(text=f"Attempts: 0/{self.max_attempts}")
        self.hint_label.config(text="🎲 New game started! Enter your first guess!")
        self.guess_entry.delete(0, tk.END)
        self.guess_entry.config(state='normal')
        self.guess_button.config(state='normal')
        self.history_text.delete(1.0, tk.END)
        self.stats_label.config(text="")
        self.range_label.config(fg='#e74c3c')
        self.guess_entry.focus()
        
        # Debug (remove in production)
        # print(f"Secret number: {self.secret_number}")
    
    def check_guess(self):
        try:
            guess = int(self.guess_entry.get())
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter a valid number!")
            self.guess_entry.delete(0, tk.END)
            return
        
        # Check range
        if guess < self.min_range or guess > self.max_range:
            messagebox.showwarning(
                "Out of Range",
                f"Please enter a number between {self.min_range} and {self.max_range}!"
            )
            self.guess_entry.delete(0, tk.END)
            return
        
        self.attempts += 1
        remaining = self.max_attempts - self.attempts
        
        # Add to history
        self.history_text.insert(1.0, f"Attempt {self.attempts}: {guess}\n")
        
        # Check guess
        if guess == self.secret_number:
            messagebox.showinfo(
                "🎉 VICTORY! 🎉",
                f"Congratulations!\nYou guessed the number {self.secret_number} in {self.attempts} attempts!"
            )
            self.game_over(win=True)
        elif guess < self.secret_number:
            self.hint_label.config(text=f"📈 Too LOW! {remaining} attempts left")
            self.range_label.config(text=f"Range: {guess} - {self.max_range}", fg='#3498db')
            self.min_range = max(self.min_range, guess + 1)
        else:
            self.hint_label.config(text=f"📉 Too HIGH! {remaining} attempts left")
            self.range_label.config(text=f"Range: {self.min_range} - {guess}", fg='#3498db')
            self.max_range = min(self.max_range, guess - 1)
        
        self.attempts_label.config(text=f"Attempts: {self.attempts}/{self.max_attempts}")
        
        # Check for game over
        if self.attempts >= self.max_attempts and guess != self.secret_number:
            messagebox.showinfo(
                "💀 GAME OVER 💀",
                f"You ran out of attempts!\nThe secret number was {self.secret_number}."
            )
            self.game_over(win=False)
        
        self.guess_entry.delete(0, tk.END)
        self.guess_entry.focus()
    
    def game_over(self, win=False):
        self.guess_entry.config(state='disabled')
        self.guess_button.config(state='disabled')
        
        # Update stats
        if win:
            accuracy = "Excellent!"
            if self.attempts <= self.max_attempts * 0.3:
                accuracy = "🎯 Amazing! 🎯"
            elif self.attempts <= self.max_attempts * 0.6:
                accuracy = "👍 Good job! 👍"
            else:
                accuracy = "💪 You made it! 💪"
            
            self.stats_label.config(
                text=f"{accuracy} You guessed in {self.attempts} attempts!",
                fg='#2ecc71'
            )
        else:
            self.stats_label.config(
                text=f"Game Over! The number was {self.secret_number}. Click NEW GAME!",
                fg='#e74c3c'
            )

def main():
    root = tk.Tk()
    game = NumberGuessingGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()