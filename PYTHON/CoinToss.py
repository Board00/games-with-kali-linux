import tkinter as tk
from tkinter import messagebox
import random
import json
import os
from datetime import datetime

class CoinTossGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🪙 Coin Toss Game")
        self.root.geometry("700x600")
        self.root.configure(bg='#2c1810')
        # Compute UI scale based on screen size so large elements shrink on small screens
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.scale = min(sw / 900.0, sh / 800.0, 1.0)
        # Apply additional shrink to make UI smaller by default
        self.scale = self.scale * 0.8
        # Minimum scale floor to avoid too tiny fonts
        if self.scale < 0.35:
            self.scale = 0.35
        
        # Game variables
        self.balance = 1000  # Starting balance
        self.current_bet = 0
        self.current_choice = None
        self.wins = 0
        self.losses = 0
        self.current_streak = 0
        self.best_streak = 0
        self.toss_history = []
        self.animation_running = False
        
        self.load_stats()
        self.setup_ui()
        self.update_display()
    
    def load_stats(self):
        if os.path.exists('cointoss_stats.json'):
            with open('cointoss_stats.json', 'r') as f:
                data = json.load(f)
                self.wins = data.get('wins', 0)
                self.losses = data.get('losses', 0)
                self.best_streak = data.get('best_streak', 0)
                self.balance = data.get('balance', 1000)
    
    def save_stats(self):
        data = {
            'wins': self.wins,
            'losses': self.losses,
            'best_streak': self.best_streak,
            'balance': self.balance
        }
        with open('cointoss_stats.json', 'w') as f:
            json.dump(data, f)
    
    def setup_ui(self):
        # Scaled font sizes
        title_size = max(12, int(32 * self.scale))
        subtitle_size = max(9, int(14 * self.scale))
        label_size = max(10, int(14 * self.scale))
        small_size = max(8, int(10 * self.scale))
        entry_font_size = max(10, int(16 * self.scale))
        coin_font_size = max(40, int(180 * self.scale))
        btn_font_size = max(10, int(12 * self.scale))

        # Title
        title_frame = tk.Frame(self.root, bg='#2c1810')
        title_frame.pack(pady=int(16 * self.scale))

        title = tk.Label(title_frame, text="🪙 COIN TOSS GAME 🪙",
                        font=('Arial', title_size, 'bold'), bg='#2c1810', fg='#ffd700')
        title.pack()

        subtitle = tk.Label(title_frame, text="Bet on Heads or Tails!",
                           font=('Arial', subtitle_size), bg='#2c1810', fg='#ecf0f1')
        subtitle.pack()
        
        # Balance Display
        balance_frame = tk.Frame(self.root, bg='#3d2b1a', relief=tk.RAISED, bd=3)
        balance_frame.pack(pady=(int(8 * self.scale)), padx=20, fill='x')

        self.balance_label = tk.Label(balance_frame, text=f"💰 Balance: ${self.balance}",
                          font=('Arial', max(10, int(18 * self.scale)), 'bold'), bg='#3d2b1a', fg='#ffd700')
        self.balance_label.pack(pady=(int(8 * self.scale)))
        
        # Stats Frame
        stats_frame = tk.Frame(self.root, bg='#2c1810')
        stats_frame.pack(pady=(10))
        
        self.wins_label = tk.Label(stats_frame, text=f"🏆 Wins: {self.wins}",
                       font=('Arial', max(9, int(12 * self.scale)), 'bold'), bg='#2c1810', fg='#2ecc71')
        self.wins_label.pack(side=tk.LEFT, padx=20)
        
        self.losses_label = tk.Label(stats_frame, text=f"💀 Losses: {self.losses}",
                         font=('Arial', max(9, int(12 * self.scale)), 'bold'), bg='#2c1810', fg='#e74c3c')
        self.losses_label.pack(side=tk.LEFT, padx=20)
        
        self.streak_label = tk.Label(stats_frame, text=f"🔥 Streak: {self.current_streak}",
                         font=('Arial', max(9, int(12 * self.scale)), 'bold'), bg='#2c1810', fg='#f39c12')
        self.streak_label.pack(side=tk.LEFT, padx=20)
        
        # Coin Display Frame
        coin_frame = tk.Frame(self.root, bg='#3d2b1a', relief=tk.RAISED, bd=5)
        coin_frame.pack(pady=(int(12 * self.scale)), padx=20, ipadx=int(10 * self.scale), ipady=int(10 * self.scale), fill='x')

        self.coin_label = tk.Label(coin_frame, text="🪙", font=('Arial', coin_font_size),
                       bg='#3d2b1a', fg='#ffd700')
        self.coin_label.pack()
        
        # Result Label
        self.result_label = tk.Label(self.root, text="Place your bet and choose Heads or Tails!",
                         font=('Arial', label_size, 'bold'), bg='#2c1810', fg='#3498db')
        self.result_label.pack(pady=(int(8 * self.scale)))
        
        # Bet Controls
        bet_frame = tk.LabelFrame(self.root, text="Bet Amount", font=('Arial', max(9, int(12 * self.scale)), 'bold'),
                      bg='#2c1810', fg='white', padx=int(12 * self.scale), pady=int(8 * self.scale))
        bet_frame.pack(pady=(int(8 * self.scale)), padx=20, fill='x')
        
        bet_control_frame = tk.Frame(bet_frame, bg='#2c1810')
        bet_control_frame.pack()
        
        # Bet amount entry
        self.bet_entry = tk.Entry(bet_control_frame, font=('Arial', entry_font_size), width=10,
                      justify='center', bg='#0f3460', fg='white')
        self.bet_entry.pack(side=tk.LEFT, padx=int(6 * self.scale))
        self.bet_entry.insert(0, "100")
        
        # Quick bet buttons
        for amount in [10, 50, 100, 250, 500]:
            btn = tk.Button(bet_control_frame, text=f"${amount}",
                           font=('Arial', max(8, int(10 * self.scale))), bg='#34495e', fg='white',
                           command=lambda a=amount: self.set_bet(a), cursor='hand2')
            btn.pack(side=tk.LEFT, padx=int(4 * self.scale))
        
        # All-in button
        allin_btn = tk.Button(bet_control_frame, text="ALL IN", font=('Arial', max(8, int(10 * self.scale)), 'bold'),
                     bg='#e74c3c', fg='white', command=self.all_in, cursor='hand2')
        allin_btn.pack(side=tk.LEFT, padx=int(6 * self.scale))
        
        # Choice Buttons
        choice_frame = tk.Frame(self.root, bg='#2c1810')
        choice_frame.pack(pady=(int(12 * self.scale)))

        self.heads_btn = tk.Button(choice_frame, text="🪙 HEADS", font=('Arial', max(10, int(16 * self.scale)), 'bold'),
                       bg='#3498db', fg='white', padx=int(18 * self.scale), pady=int(10 * self.scale),
                       command=lambda: self.make_bet('Heads'), cursor='hand2')
        self.heads_btn.pack(side=tk.LEFT, padx=int(8 * self.scale))

        self.tails_btn = tk.Button(choice_frame, text="🪙 TAILS", font=('Arial', max(10, int(16 * self.scale)), 'bold'),
                       bg='#e74c3c', fg='white', padx=int(18 * self.scale), pady=int(10 * self.scale),
                       command=lambda: self.make_bet('Tails'), cursor='hand2')
        self.tails_btn.pack(side=tk.LEFT, padx=int(8 * self.scale))
        
        # Choice buttons are active — clicking HEADS/TAILS will read the bet and flip
        
        # Reset Game Button
        reset_btn = tk.Button(self.root, text="Reset Game", font=('Arial', max(8, int(10 * self.scale))),
                     bg='#95a5a6', fg='white', padx=int(12 * self.scale), pady=int(6 * self.scale),
                     command=self.reset_game, cursor='hand2')
        reset_btn.pack(pady=(int(6 * self.scale)))
        
        # History Frame
        history_frame = tk.LabelFrame(self.root, text="Toss History", font=('Arial', 12, 'bold'),
                                      bg='#2c1810', fg='white', padx=10, pady=10)
        history_frame.pack(pady=(10), padx=20, fill='both', expand=True)
        
        history_scroll = tk.Scrollbar(history_frame)
        history_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_text = tk.Text(history_frame, height=6, font=('Courier', 10),
                                    bg='#0f3460', fg='#2ecc71', yscrollcommand=history_scroll.set)
        self.history_text.pack(fill='both', expand=True)
        history_scroll.config(command=self.history_text.yview)
    
    def set_bet(self, amount):
        if amount <= self.balance:
            self.bet_entry.delete(0, tk.END)
            self.bet_entry.insert(0, str(amount))
            self.result_label.config(text=f"Bet amount set to ${amount}", fg='#2ecc71')
        else:
            messagebox.showwarning("Insufficient Funds", f"You only have ${self.balance}!")
    
    def all_in(self):
        self.bet_entry.delete(0, tk.END)
        self.bet_entry.insert(0, str(self.balance))
        self.result_label.config(text=f"ALL IN! Betting ${self.balance}", fg='#e74c3c')
    
    
    
    def animate_coin_toss(self, result):
        """Animate coin flipping"""
        self.animation_running = True
        self.heads_btn.config(state=tk.DISABLED)
        self.tails_btn.config(state=tk.DISABLED)
        
        # Animation frames
        frames = []
        for i in range(20):
            frames.append(random.choice(['🪙', '💰', '💎', '⭐']))
        
        def animate_frame(index=0):
            if index < len(frames):
                self.coin_label.config(text=frames[index])
                self.root.after(50, lambda: animate_frame(index + 1))
            else:
                # Show final result
                if result == 'Heads':
                    self.coin_label.config(text="🪙 HEADS 🪙", fg='#3498db')
                else:
                    self.coin_label.config(text="🪙 TAILS 🪙", fg='#e74c3c')
                
                self.root.after(500, lambda: self.show_result(result))
        
        animate_frame()
    
    def show_result(self, result):
        """Show the game result"""
        win = (result == self.current_choice)
        
        if win:
            # Win
            winnings = self.current_bet
            self.balance += winnings
            self.wins += 1
            self.current_streak += 1
            if self.current_streak > self.best_streak:
                self.best_streak = self.current_streak
            
            result_text = f"🎉 YOU WIN! 🎉\n{result}! You won ${winnings}!"
            result_color = '#2ecc71'
            
            # Celebration effect
            self.coin_label.config(fg='#ffd700')
            self.root.after(200, lambda: self.coin_label.config(fg='#2ecc71'))
            self.root.after(400, lambda: self.coin_label.config(fg='#ffd700'))
            
        else:
            # Loss
            self.balance -= self.current_bet
            self.losses += 1
            self.current_streak = 0
            
            result_text = f"💀 YOU LOSE! 💀\n{result}! You lost ${self.current_bet}!"
            result_color = '#e74c3c'
            
            # Sad effect
            self.coin_label.config(fg='#7f8c8d')
        
        # Update display
        self.result_label.config(text=result_text, fg=result_color)
        self.update_display()
        
        # Add to history
        timestamp = datetime.now().strftime("%H:%M:%S")
        history_entry = f"[{timestamp}] Bet: ${self.current_bet} on {self.current_choice} → {result} → {'WIN' if win else 'LOSS'}\n"
        self.history_text.insert(1.0, history_entry)
        
        # Keep only last 20 entries
        if len(self.history_text.get(1.0, tk.END).split('\n')) > 21:
            self.history_text.delete(tk.END + "-2l", tk.END)
        
        # Check for game over
        if self.balance <= 0:
            self.result_label.config(text="💀 GAME OVER! You're broke! Click Reset to play again! 💀", fg='#e74c3c')
            self.heads_btn.config(state=tk.DISABLED)
            self.tails_btn.config(state=tk.DISABLED)
        else:
            # Reset for next round: allow placing a new bet by clicking HEADS/TAILS
            self.current_bet = 0
            self.current_choice = None
            self.heads_btn.config(state=tk.NORMAL)
            self.tails_btn.config(state=tk.NORMAL)
            self.bet_entry.delete(0, tk.END)
            self.bet_entry.insert(0, "100")
        
        self.save_stats()
        self.animation_running = False
    
    def make_bet(self, choice):
        if self.animation_running:
            return

        # Read and validate bet amount immediately when user clicks Heads/Tails
        try:
            bet = int(self.bet_entry.get())
            if bet <= 0:
                messagebox.showwarning("Invalid Bet", "Bet amount must be positive!")
                return
            if bet > self.balance:
                messagebox.showwarning("Insufficient Funds", f"You only have ${self.balance}!")
                return
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter a valid number!")
            return

        self.current_bet = bet
        self.current_choice = choice
        self.result_label.config(text=f"You bet ${bet} on {choice}! Tossing coin...", fg='#f39c12')

        # Simulate coin toss
        result = random.choice(['Heads', 'Tails'])

        # Animate
        self.animate_coin_toss(result)
    
    def update_display(self):
        self.balance_label.config(text=f"💰 Balance: ${self.balance}")
        self.wins_label.config(text=f"🏆 Wins: {self.wins}")
        self.losses_label.config(text=f"💀 Losses: {self.losses}")
        self.streak_label.config(text=f"🔥 Streak: {self.current_streak} (Best: {self.best_streak})")
        
        # Change color based on balance
        if self.balance < 100:
            self.balance_label.config(fg='#e74c3c')
        elif self.balance < 500:
            self.balance_label.config(fg='#f39c12')
        else:
            self.balance_label.config(fg='#2ecc71')
    
    def reset_game(self):
        if messagebox.askyesno("Reset Game", "Are you sure you want to reset the game? All progress will be lost!"):
            self.balance = 1000
            self.wins = 0
            self.losses = 0
            self.current_streak = 0
            self.best_streak = 0
            self.current_bet = 0
            self.current_choice = None
            self.toss_history = []
            
            self.history_text.delete(1.0, tk.END)
            self.coin_label.config(text="🪙", fg='#ffd700')
            self.result_label.config(text="Game reset! Place your bets!", fg='#3498db')
            self.update_display()
            
            # Allow direct betting after reset
            self.heads_btn.config(state=tk.NORMAL)
            self.tails_btn.config(state=tk.NORMAL)
            self.bet_entry.delete(0, tk.END)
            self.bet_entry.insert(0, "100")
            
            self.save_stats()

if __name__ == "__main__":
    root = tk.Tk()
    game = CoinTossGame(root)
    root.mainloop()