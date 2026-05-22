import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import json
import os
from datetime import datetime

class TypingSpeedTest:
    def __init__(self, root):
        self.root = root
        self.root.title("⌨️ Typing Speed Test")
        self.root.geometry("900x700")
        self.root.configure(bg='#1a1a2e')
        
        # Word lists by difficulty
        self.word_lists = {
            'Easy': ['cat', 'dog', 'run', 'fast', 'blue', 'red', 'car', 'house', 'tree', 'sun', 
                    'moon', 'star', 'fish', 'bird', 'happy', 'sad', 'big', 'small', 'hot', 'cold'],
            'Medium': ['python', 'programming', 'keyboard', 'developer', 'algorithm', 'function',
                      'variable', 'dictionary', 'iteration', 'conditional', 'exception', 'syntax',
                      'debugging', 'framework', 'database', 'network', 'security', 'performance'],
            'Hard': ['comprehensive', 'sophisticated', 'revolutionary', 'authentication', 'infrastructure',
                    'implementation', 'optimization', 'visualization', 'documentation', 'configuration',
                    'troubleshooting', 'scalability', 'maintainability', 'interoperability']
        }
        
        self.current_difficulty = 'Medium'
        self.current_words = []
        self.user_input = []
        self.start_time = None
        self.test_active = False
        self.high_scores = self.load_high_scores()
        
        self.setup_ui()
        self.new_test()
    
    def load_high_scores(self):
        if os.path.exists('typing_highscores.json'):
            with open('typing_highscores.json', 'r') as f:
                return json.load(f)
        return {'Easy': [], 'Medium': [], 'Hard': []}
    
    def save_high_scores(self):
        with open('typing_highscores.json', 'w') as f:
            json.dump(self.high_scores, f)
    
    def setup_ui(self):
        # Title
        title_frame = tk.Frame(self.root, bg='#1a1a2e')
        title_frame.pack(pady=20)
        
        title = tk.Label(title_frame, text="⌨️ TYPING SPEED TEST ⌨️",
                        font=('Arial', 28, 'bold'), bg='#1a1a2e', fg='#ffd700')
        title.pack()
        
        subtitle = tk.Label(title_frame, text="Test your typing speed and accuracy!",
                           font=('Arial', 12), bg='#1a1a2e', fg='#ecf0f1')
        subtitle.pack()
        
        # Stats Frame
        stats_frame = tk.Frame(self.root, bg='#16213e', relief=tk.RAISED, bd=3)
        stats_frame.pack(pady=10, padx=20, fill='x')
        
        # WPM Display
        self.wpm_label = tk.Label(stats_frame, text="WPM: 0", font=('Arial', 16, 'bold'),
                                  bg='#16213e', fg='#2ecc71')
        self.wpm_label.pack(side=tk.LEFT, padx=30, pady=10)
        
        # Accuracy Display
        self.accuracy_label = tk.Label(stats_frame, text="Accuracy: 0%", font=('Arial', 16, 'bold'),
                                       bg='#16213e', fg='#3498db')
        self.accuracy_label.pack(side=tk.LEFT, padx=30, pady=10)
        
        # Timer Display
        self.timer_label = tk.Label(stats_frame, text="Time: 0.0s", font=('Arial', 16, 'bold'),
                                    bg='#16213e', fg='#e74c3c')
        self.timer_label.pack(side=tk.LEFT, padx=30, pady=10)
        
        # Progress Display
        self.progress_label = tk.Label(stats_frame, text="Progress: 0/10", font=('Arial', 14),
                                       bg='#16213e', fg='#f39c12')
        self.progress_label.pack(side=tk.LEFT, padx=30, pady=10)
        
        # Difficulty Selection
        diff_frame = tk.Frame(self.root, bg='#1a1a2e')
        diff_frame.pack(pady=10)
        
        tk.Label(diff_frame, text="Difficulty:", font=('Arial', 12),
                bg='#1a1a2e', fg='white').pack(side=tk.LEFT, padx=10)
        
        self.difficulty_var = tk.StringVar(value='Medium')
        for diff in ['Easy', 'Medium', 'Hard']:
            rb = tk.Radiobutton(diff_frame, text=diff, variable=self.difficulty_var,
                               value=diff, command=self.change_difficulty,
                               bg='#1a1a2e', fg='white', selectcolor='#1a1a2e')
            rb.pack(side=tk.LEFT, padx=10)
        
        # Word Display Frame
        word_frame = tk.Frame(self.root, bg='#0f3460', relief=tk.RAISED, bd=5)
        word_frame.pack(pady=20, padx=20, fill='x')
        
        self.word_display = tk.Text(word_frame, height=4, font=('Courier', 18),
                                    bg='#0f3460', fg='#ffd700', wrap=tk.WORD,
                                    state=tk.DISABLED, padx=20, pady=20)
        self.word_display.pack(fill='x', padx=10, pady=10)
        
        # Current Word Display
        current_word_frame = tk.Frame(self.root, bg='#2c1810', relief=tk.RAISED, bd=3)
        current_word_frame.pack(pady=10, padx=20, fill='x')
        
        tk.Label(current_word_frame, text="Type this word:", font=('Arial', 12),
                bg='#2c1810', fg='white').pack()
        
        self.current_word_label = tk.Label(current_word_frame, text="", font=('Arial', 32, 'bold'),
                                           bg='#2c1810', fg='#2ecc71')
        self.current_word_label.pack(pady=10)
        
        # Input Entry
        input_frame = tk.Frame(self.root, bg='#1a1a2e')
        input_frame.pack(pady=10, padx=20, fill='x')
        
        self.input_entry = tk.Entry(input_frame, font=('Arial', 16), width=30,
                                    justify='center', bg='#ecf0f1', fg='#2c3e50')
        self.input_entry.pack(pady=10)
        self.input_entry.bind('<Return>', self.check_word)
        
        # Control Buttons
        control_frame = tk.Frame(self.root, bg='#1a1a2e')
        control_frame.pack(pady=10)
        
        self.start_btn = tk.Button(control_frame, text="🚀 START TEST", font=('Arial', 14, 'bold'),
                                   bg='#27ae60', fg='white', padx=30, pady=10,
                                   command=self.start_test, cursor='hand2')
        self.start_btn.pack(side=tk.LEFT, padx=10)
        
        self.reset_btn = tk.Button(control_frame, text="🔄 RESET", font=('Arial', 12),
                                   bg='#e74c3c', fg='white', padx=20, pady=8,
                                   command=self.reset_test, cursor='hand2')
        self.reset_btn.pack(side=tk.LEFT, padx=10)
        
        # Results Frame
        results_frame = tk.LabelFrame(self.root, text="Results", font=('Arial', 12, 'bold'),
                                      bg='#1a1a2e', fg='white', padx=10, pady=10)
        results_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        self.results_text = tk.Text(results_frame, height=8, font=('Courier', 10),
                                    bg='#0f3460', fg='#2ecc71', wrap=tk.WORD)
        self.results_text.pack(fill='both', expand=True)
        
        # High Scores
        self.update_high_scores_display()
    
    def change_difficulty(self):
        self.current_difficulty = self.difficulty_var.get()
        self.reset_test()
    
    def new_test(self):
        word_count = 10  # 10 words per test
        word_list = self.word_lists[self.current_difficulty]
        self.current_words = random.sample(word_list, min(word_count, len(word_list)))
        self.user_input = []
        self.current_word_index = 0
        self.update_word_display()
        self.update_current_word()
        self.progress_label.config(text=f"Progress: 0/{len(self.current_words)}")
        
        # Clear results
        self.results_text.delete(1.0, tk.END)
        
        # Disable input until start
        self.input_entry.config(state=tk.DISABLED)
    
    def update_word_display(self):
        self.word_display.config(state=tk.NORMAL)
        self.word_display.delete(1.0, tk.END)
        
        # Show all words with colored completed ones
        for i, word in enumerate(self.current_words):
            if i < self.current_word_index:
                self.word_display.insert(tk.END, f"✓ {word}  ", 'completed')
            elif i == self.current_word_index:
                self.word_display.insert(tk.END, f"▶ {word}  ", 'current')
            else:
                self.word_display.insert(tk.END, f"  {word}  ", 'pending')
        
        self.word_display.tag_config('completed', foreground='#2ecc71')
        self.word_display.tag_config('current', foreground='#ffd700', font=('Courier', 18, 'bold'))
        self.word_display.tag_config('pending', foreground='#7f8c8d')
        
        self.word_display.config(state=tk.DISABLED)
    
    def update_current_word(self):
        if self.current_word_index < len(self.current_words):
            self.current_word_label.config(text=self.current_words[self.current_word_index])
        else:
            self.current_word_label.config(text="Complete!")
    
    def start_test(self):
        self.new_test()
        self.test_active = True
        self.start_time = time.time()
        self.input_entry.config(state=tk.NORMAL)
        self.input_entry.focus()
        self.start_btn.config(state=tk.DISABLED)
        self.update_timer()
    
    def check_word(self, event):
        if not self.test_active:
            return
        
        typed_word = self.input_entry.get().strip()
        correct_word = self.current_words[self.current_word_index]
        
        # Check accuracy
        is_correct = (typed_word.lower() == correct_word.lower())
        self.user_input.append({'typed': typed_word, 'correct': correct_word, 'is_correct': is_correct})
        
        # Display result
        if is_correct:
            self.results_text.insert(tk.END, f"✓ {correct_word} - Correct!\n", 'correct')
            self.results_text.tag_config('correct', foreground='#2ecc71')
        else:
            self.results_text.insert(tk.END, f"✗ '{typed_word}' - Should be '{correct_word}'\n", 'incorrect')
            self.results_text.tag_config('incorrect', foreground='#e74c3c')
        
        self.results_text.see(tk.END)
        
        # Move to next word
        self.current_word_index += 1
        self.input_entry.delete(0, tk.END)
        
        if self.current_word_index >= len(self.current_words):
            # Test complete
            self.end_test()
        else:
            self.update_word_display()
            self.update_current_word()
            self.progress_label.config(text=f"Progress: {self.current_word_index}/{len(self.current_words)}")
    
    def update_timer(self):
        if self.test_active and self.start_time:
            elapsed = time.time() - self.start_time
            self.timer_label.config(text=f"Time: {elapsed:.1f}s")
            self.root.after(100, self.update_timer)
    
    def calculate_wpm(self, elapsed_time, correct_words):
        # WPM = (correct words / time in minutes)
        minutes = elapsed_time / 60
        if minutes > 0:
            wpm = int(correct_words / minutes)
        else:
            wpm = 0
        return wpm
    
    def calculate_accuracy(self, total_words, correct_words):
        if total_words > 0:
            return (correct_words / total_words) * 100
        return 0
    
    def end_test(self):
        self.test_active = False
        elapsed_time = time.time() - self.start_time
        
        # Calculate stats
        correct_words = sum(1 for item in self.user_input if item['is_correct'])
        total_words = len(self.user_input)
        accuracy = self.calculate_accuracy(total_words, correct_words)
        wpm = self.calculate_wpm(elapsed_time, correct_words)
        
        # Update displays
        self.wpm_label.config(text=f"WPM: {wpm}")
        self.accuracy_label.config(text=f"Accuracy: {accuracy:.1f}%")
        
        # Save high score
        self.save_high_score(wpm, accuracy)
        
        # Show final results
        self.show_final_results(wpm, accuracy, elapsed_time, correct_words, total_words)
        
        # Re-enable start button
        self.start_btn.config(state=tk.NORMAL)
        self.input_entry.config(state=tk.DISABLED)
    
    def save_high_score(self, wpm, accuracy):
        score_data = {
            'wpm': wpm,
            'accuracy': accuracy,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.high_scores[self.current_difficulty].append(score_data)
        # Keep only top 5 scores
        self.high_scores[self.current_difficulty].sort(key=lambda x: x['wpm'], reverse=True)
        self.high_scores[self.current_difficulty] = self.high_scores[self.current_difficulty][:5]
        self.save_high_scores()
        self.update_high_scores_display()
    
    def show_final_results(self, wpm, accuracy, elapsed_time, correct_words, total_words):
        result_window = tk.Toplevel(self.root)
        result_window.title("Test Results")
        result_window.geometry("500x400")
        result_window.configure(bg='#1a1a2e')
        
        # Center the window
        result_window.transient(self.root)
        result_window.grab_set()
        
        tk.Label(result_window, text="🎉 TEST COMPLETE! 🎉",
                font=('Arial', 20, 'bold'), bg='#1a1a2e', fg='#ffd700').pack(pady=20)
        
        stats_frame = tk.Frame(result_window, bg='#16213e', relief=tk.RAISED, bd=3)
        stats_frame.pack(pady=20, padx=20, fill='x')
        
        stats = [
            (f"📊 WPM: {wpm}", '#2ecc71'),
            (f"📈 Accuracy: {accuracy:.1f}%", '#3498db'),
            (f"⏱️ Time: {elapsed_time:.1f} seconds", '#e74c3c'),
            (f"✅ Correct Words: {correct_words}/{total_words}", '#f39c12'),
            (f"📝 Difficulty: {self.current_difficulty}", '#9b59b6')
        ]
        
        for text, color in stats:
            tk.Label(stats_frame, text=text, font=('Arial', 14),
                    bg='#16213e', fg=color).pack(pady=5)
        
        # Check if high score
        top_scores = self.high_scores[self.current_difficulty]
        if top_scores and wpm == top_scores[0]['wpm']:
            tk.Label(result_window, text="🏆 NEW HIGH SCORE! 🏆",
                    font=('Arial', 16, 'bold'), bg='#1a1a2e', fg='#ffd700').pack(pady=10)
        
        tk.Button(result_window, text="Close", command=result_window.destroy,
                 font=('Arial', 12), bg='#3498db', fg='white', padx=20, pady=10).pack(pady=20)
    
    def update_high_scores_display(self):
        # Update high scores in main window
        high_score_frame = tk.LabelFrame(self.root, text="High Scores", font=('Arial', 10, 'bold'),
                                         bg='#1a1a2e', fg='white')
        high_score_frame.pack(pady=10, padx=20, fill='x')
        
        # Clear existing widgets
        for widget in high_score_frame.winfo_children():
            widget.destroy()
        
        for difficulty in ['Easy', 'Medium', 'Hard']:
            diff_frame = tk.Frame(high_score_frame, bg='#1a1a2e')
            diff_frame.pack(side=tk.LEFT, expand=True, fill='both', padx=5)
            
            tk.Label(diff_frame, text=difficulty, font=('Arial', 10, 'bold'),
                    bg='#1a1a2e', fg='#ffd700').pack()
            
            scores = self.high_scores[difficulty][:3]
            if scores:
                for i, score in enumerate(scores, 1):
                    tk.Label(diff_frame, text=f"{i}. {score['wpm']} WPM",
                            font=('Arial', 9), bg='#1a1a2e', fg='#2ecc71').pack()
            else:
                tk.Label(diff_frame, text="No scores yet",
                        font=('Arial', 9), bg='#1a1a2e', fg='#7f8c8d').pack()
    
    def reset_test(self):
        self.test_active = False
        self.start_btn.config(state=tk.NORMAL)
        self.input_entry.config(state=tk.DISABLED)
        self.input_entry.delete(0, tk.END)
        self.wpm_label.config(text="WPM: 0")
        self.accuracy_label.config(text="Accuracy: 0%")
        self.timer_label.config(text="Time: 0.0s")
        self.new_test()

if __name__ == "__main__":
    root = tk.Tk()
    game = TypingSpeedTest(root)
    root.mainloop()