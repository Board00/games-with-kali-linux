import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime

class QuizGame:
    def __init__(self, root):
        self.root = root
        self.root.title("📚 Quiz Game")
        self.root.geometry("900x700")
        self.root.configure(bg='#1a1a2e')
        
        # Quiz questions database
        self.questions = {
            'Science': [
                {
                    'question': 'What is the chemical symbol for Gold?',
                    'options': ['Go', 'Gd', 'Au', 'Ag'],
                    'correct': 2,
                    'explanation': 'Au comes from Latin "Aurum" meaning gold'
                },
                {
                    'question': 'What is the hardest natural substance?',
                    'options': ['Iron', 'Diamond', 'Platinum', 'Titanium'],
                    'correct': 1,
                    'explanation': 'Diamond is the hardest known natural material'
                },
                {
                    'question': 'What planet is known as the "Red Planet"?',
                    'options': ['Mars', 'Jupiter', 'Venus', 'Saturn'],
                    'correct': 0,
                    'explanation': 'Mars appears red due to iron oxide on its surface'
                },
                {
                    'question': 'What is the largest organ in the human body?',
                    'options': ['Heart', 'Brain', 'Liver', 'Skin'],
                    'correct': 3,
                    'explanation': 'The skin is the largest organ, covering about 2 square meters'
                },
                {
                    'question': 'What gas do plants absorb from the air?',
                    'options': ['Oxygen', 'Nitrogen', 'Carbon Dioxide', 'Hydrogen'],
                    'correct': 2,
                    'explanation': 'Plants absorb CO2 for photosynthesis'
                }
            ],
            'History': [
                {
                    'question': 'Who painted the Mona Lisa?',
                    'options': ['Van Gogh', 'Picasso', 'Da Vinci', 'Rembrandt'],
                    'correct': 2,
                    'explanation': 'Leonardo da Vinci painted the Mona Lisa in the 16th century'
                },
                {
                    'question': 'In which year did World War II end?',
                    'options': ['1943', '1944', '1945', '1946'],
                    'correct': 2,
                    'explanation': 'WWII ended in 1945 after the surrender of Japan'
                },
                {
                    'question': 'Who was the first person to walk on the moon?',
                    'options': ['Buzz Aldrin', 'Neil Armstrong', 'Yuri Gagarin', 'Alan Shepard'],
                    'correct': 1,
                    'explanation': 'Neil Armstrong walked on the moon on July 20, 1969'
                },
                {
                    'question': 'Which ancient civilization built Machu Picchu?',
                    'options': ['Aztecs', 'Mayans', 'Incas', 'Olmecs'],
                    'correct': 2,
                    'explanation': 'The Incas built Machu Picchu in the 15th century'
                },
                {
                    'question': 'Who wrote "Romeo and Juliet"?',
                    'options': ['Charles Dickens', 'Jane Austen', 'William Shakespeare', 'Mark Twain'],
                    'correct': 2,
                    'explanation': 'Shakespeare wrote Romeo and Juliet around 1595'
                }
            ],
            'Movies': [
                {
                    'question': 'Who played Jack Dawson in Titanic?',
                    'options': ['Brad Pitt', 'Leonardo DiCaprio', 'Johnny Depp', 'Matt Damon'],
                    'correct': 1,
                    'explanation': 'Leonardo DiCaprio played Jack Dawson in the 1997 film'
                },
                {
                    'question': 'What is the highest-grossing film of all time (unadjusted)?',
                    'options': ['Avatar', 'Avengers: Endgame', 'Titanic', 'Star Wars'],
                    'correct': 0,
                    'explanation': 'Avatar holds the record with over $2.8 billion'
                },
                {
                    'question': 'Which movie won the Oscar for Best Picture in 2020?',
                    'options': ['1917', 'Joker', 'Parasite', 'Once Upon a Time in Hollywood'],
                    'correct': 2,
                    'explanation': 'Parasite made history as the first non-English film to win'
                },
                {
                    'question': 'Who directed "Inception"?',
                    'options': ['Steven Spielberg', 'Christopher Nolan', 'Quentin Tarantino', 'James Cameron'],
                    'correct': 1,
                    'explanation': 'Christopher Nolan directed Inception in 2010'
                },
                {
                    'question': 'What is the name of Harry Potter\'s owl?',
                    'options': ['Errol', 'Hedwig', 'Pigwidgeon', 'Hermes'],
                    'correct': 1,
                    'explanation': 'Hedwig was Harry\'s snowy owl'
                }
            ]
        }
        
        self.current_category = 'Science'
        self.current_questions = []
        self.current_index = 0
        self.score = 0
        self.lifelines_used = {'fifty_fifty': False, 'audience': False}
        self.timer_running = False
        self.time_left = 15
        self.high_scores = self.load_high_scores()
        
        self.setup_ui()
        self.start_new_game()
    
    def load_high_scores(self):
        if os.path.exists('quiz_highscores.json'):
            with open('quiz_highscores.json', 'r') as f:
                return json.load(f)
        return []
    
    def save_high_score(self, score, percentage):
        high_score = {
            'score': score,
            'percentage': percentage,
            'category': self.current_category,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.high_scores.append(high_score)
        self.high_scores.sort(key=lambda x: x['score'], reverse=True)
        self.high_scores = self.high_scores[:5]
        
        with open('quiz_highscores.json', 'w') as f:
            json.dump(self.high_scores, f)
        
        self.update_high_scores_display()
    
    def setup_ui(self):
        # Title
        title_frame = tk.Frame(self.root, bg='#1a1a2e')
        title_frame.pack(pady=20)
        
        title = tk.Label(title_frame, text="📚 QUIZ GAME 📚",
                        font=('Arial', 28, 'bold'), bg='#1a1a2e', fg='#ffd700')
        title.pack()
        
        # Category Selection
        cat_frame = tk.Frame(self.root, bg='#1a1a2e')
        cat_frame.pack(pady=10)
        
        tk.Label(cat_frame, text="Category:", font=('Arial', 12),
                bg='#1a1a2e', fg='white').pack(side=tk.LEFT, padx=10)
        
        self.category_var = tk.StringVar(value='Science')
        for category in ['Science', 'History', 'Movies']:
            rb = tk.Radiobutton(cat_frame, text=category, variable=self.category_var,
                               value=category, command=self.change_category,
                               bg='#1a1a2e', fg='white', selectcolor='#1a1a2e')
            rb.pack(side=tk.LEFT, padx=10)
        
        # Score Display
        score_frame = tk.Frame(self.root, bg='#16213e', relief=tk.RAISED, bd=3)
        score_frame.pack(pady=10, padx=20, fill='x')
        
        self.score_label = tk.Label(score_frame, text="Score: 0", font=('Arial', 16, 'bold'),
                                    bg='#16213e', fg='#2ecc71')
        self.score_label.pack(side=tk.LEFT, padx=30, pady=10)
        
        self.question_num_label = tk.Label(score_frame, text="Question: 0/5", font=('Arial', 14),
                                           bg='#16213e', fg='#3498db')
        self.question_num_label.pack(side=tk.LEFT, padx=30, pady=10)
        
        # Timer Display
        self.timer_label = tk.Label(score_frame, text="Time: 15s", font=('Arial', 16, 'bold'),
                                    bg='#16213e', fg='#e74c3c')
        self.timer_label.pack(side=tk.LEFT, padx=30, pady=10)
        
        # Question Frame
        question_frame = tk.Frame(self.root, bg='#0f3460', relief=tk.RAISED, bd=5)
        question_frame.pack(pady=20, padx=20, fill='x')
        
        self.question_label = tk.Label(question_frame, text="", font=('Arial', 16, 'bold'),
                                       bg='#0f3460', fg='#ffd700', wraplength=700, justify='center')
        self.question_label.pack(pady=30, padx=20)
        
        # Options Frame
        self.options_frame = tk.Frame(self.root, bg='#1a1a2e')
        self.options_frame.pack(pady=20, padx=20)
        
        self.option_buttons = []
        for i in range(4):
            btn = tk.Button(self.options_frame, text="", font=('Arial', 14),
                           bg='#34495e', fg='white', padx=20, pady=10,
                           command=lambda idx=i: self.check_answer(idx), cursor='hand2')
            btn.pack(fill='x', pady=5)
            self.option_buttons.append(btn)
        
        # Lifelines Frame
        lifeline_frame = tk.Frame(self.root, bg='#1a1a2e')
        lifeline_frame.pack(pady=10)
        
        self.fifty_btn = tk.Button(lifeline_frame, text="50:50", font=('Arial', 12, 'bold'),
                                   bg='#9b59b6', fg='white', padx=20, pady=8,
                                   command=self.fifty_fifty, cursor='hand2')
        self.fifty_btn.pack(side=tk.LEFT, padx=10)
        
        self.audience_btn = tk.Button(lifeline_frame, text="Ask Audience", font=('Arial', 12, 'bold'),
                                      bg='#e67e22', fg='white', padx=20, pady=8,
                                      command=self.audience_poll, cursor='hand2')
        self.audience_btn.pack(side=tk.LEFT, padx=10)
        
        # Next Button
        self.next_btn = tk.Button(self.root, text="Next Question →", font=('Arial', 12, 'bold'),
                                  bg='#27ae60', fg='white', padx=30, pady=10,
                                  command=self.next_question, cursor='hand2', state=tk.DISABLED)
        self.next_btn.pack(pady=10)
        
        # High Scores Frame
        high_score_frame = tk.LabelFrame(self.root, text="🏆 High Scores 🏆", font=('Arial', 12, 'bold'),
                                         bg='#1a1a2e', fg='white')
        high_score_frame.pack(pady=10, padx=20, fill='x')
        
        self.high_scores_text = tk.Text(high_score_frame, height=5, font=('Courier', 10),
                                        bg='#0f3460', fg='#2ecc71')
        self.high_scores_text.pack(fill='both', expand=True, padx=5, pady=5)
    
    def change_category(self):
        self.current_category = self.category_var.get()
        self.start_new_game()
    
    def start_new_game(self):
        # Select 5 random questions from category
        category_questions = self.questions[self.current_category]
        self.current_questions = random.sample(category_questions, min(5, len(category_questions)))
        self.current_index = 0
        self.score = 0
        self.lifelines_used = {'fifty_fifty': False, 'audience': False}
        self.update_lifeline_buttons()
        self.update_score()
        self.load_question()
    
    def load_question(self):
        if self.current_index < len(self.current_questions):
            question_data = self.current_questions[self.current_index]
            self.question_label.config(text=question_data['question'])
            
            # Shuffle options
            options_with_indices = list(enumerate(question_data['options']))
            random.shuffle(options_with_indices)
            self.current_options_order = options_with_indices
            
            for i, (orig_idx, text) in enumerate(options_with_indices):
                self.option_buttons[i].config(text=text, bg='#34495e', state=tk.NORMAL)
            
            self.question_num_label.config(text=f"Question: {self.current_index + 1}/{len(self.current_questions)}")
            self.next_btn.config(state=tk.DISABLED)
            self.start_timer()
        else:
            self.end_quiz()
    
    def start_timer(self):
        if self.timer_running:
            self.root.after_cancel(self.timer_running)
        self.time_left = 15
        self.update_timer_display()
        self.timer_running = True
        self.update_timer()
    
    def update_timer(self):
        if self.timer_running and self.time_left > 0:
            self.timer_label.config(text=f"Time: {self.time_left}s")
            self.time_left -= 1
            self.timer_running = self.root.after(1000, self.update_timer)
        elif self.time_left <= 0:
            self.timer_running = False
            self.timeout()
    
    def update_timer_display(self):
        self.timer_label.config(text=f"Time: {self.time_left}s")
    
    def timeout(self):
        messagebox.showwarning("Time's Up!", "You ran out of time!")
        self.disable_options()
        self.next_btn.config(state=tk.NORMAL)
    
    def check_answer(self, selected_idx):
        if self.timer_running:
            self.root.after_cancel(self.timer_running)
            self.timer_running = False
        
        orig_idx, _ = self.current_options_order[selected_idx]
        question_data = self.current_questions[self.current_index]
        is_correct = (orig_idx == question_data['correct'])
        
        # Highlight correct/incorrect answers
        for i, (orig_idx_option, text) in enumerate(self.current_options_order):
            if orig_idx_option == question_data['correct']:
                self.option_buttons[i].config(bg='#2ecc71')  # Green for correct
            elif i == selected_idx and not is_correct:
                self.option_buttons[i].config(bg='#e74c3c')  # Red for wrong
        
        if is_correct:
            self.score += 1
            self.update_score()
            messagebox.showinfo("Correct!", f"✓ Correct!\n\n{question_data['explanation']}")
        else:
            correct_answer = question_data['options'][question_data['correct']]
            messagebox.showinfo("Incorrect!", f"✗ Wrong!\n\nThe correct answer is: {correct_answer}\n\n{question_data['explanation']}")
        
        self.disable_options()
        self.next_btn.config(state=tk.NORMAL)
    
    def disable_options(self):
        for btn in self.option_buttons:
            btn.config(state=tk.DISABLED)
    
    def fifty_fifty(self):
        if self.lifelines_used['fifty_fifty']:
            messagebox.showinfo("Lifeline Used", "You've already used the 50:50 lifeline!")
            return
        
        question_data = self.current_questions[self.current_index]
        correct_idx = question_data['correct']
        
        # Get wrong options
        wrong_options = [i for i in range(4) if i != correct_idx]
        remove_count = 2  # Remove 2 wrong options
        to_remove = random.sample(wrong_options, remove_count)
        
        # Disable the buttons to remove
        for i, (orig_idx, text) in enumerate(self.current_options_order):
            if orig_idx in to_remove:
                self.option_buttons[i].config(text="❌", state=tk.DISABLED, bg='#7f8c8d')
        
        self.lifelines_used['fifty_fifty'] = True
        self.fifty_btn.config(state=tk.DISABLED, bg='#7f8c8d')
        messagebox.showinfo("50:50 Lifeline", "Two wrong answers have been removed!")
    
    def audience_poll(self):
        if self.lifelines_used['audience']:
            messagebox.showinfo("Lifeline Used", "You've already used the Audience Poll lifeline!")
            return
        
        question_data = self.current_questions[self.current_index]
        
        # Create audience poll percentages
        correct_percentage = random.randint(60, 85)
        remaining = 100 - correct_percentage
        wrong_percentages = []
        for i in range(3):
            if i == question_data['correct']:
                wrong_percentages.append(0)
            else:
                perc = random.randint(5, remaining - (3 - i) * 5)
                wrong_percentages.append(perc)
                remaining -= perc
        
        # Shuffle to match current order
        poll_results = []
        for i, (orig_idx, text) in enumerate(self.current_options_order):
            if orig_idx == question_data['correct']:
                poll_results.append((text, correct_percentage))
            else:
                poll_results.append((text, wrong_percentages.pop(0)))
        
        # Create poll window
        poll_window = tk.Toplevel(self.root)
        poll_window.title("Audience Poll Results")
        poll_window.geometry("400x300")
        poll_window.configure(bg='#1a1a2e')
        
        tk.Label(poll_window, text="📊 AUDIENCE POLL RESULTS 📊",
                font=('Arial', 14, 'bold'), bg='#1a1a2e', fg='#ffd700').pack(pady=10)
        
        for text, percentage in poll_results:
            frame = tk.Frame(poll_window, bg='#1a1a2e')
            frame.pack(fill='x', padx=20, pady=5)
            
            tk.Label(frame, text=text, font=('Arial', 10),
                    bg='#1a1a2e', fg='white', width=30, anchor='w').pack(side=tk.LEFT)
            
            tk.Label(frame, text=f"{percentage}%", font=('Arial', 10, 'bold'),
                    bg='#1a1a2e', fg='#2ecc71').pack(side=tk.LEFT, padx=10)
            
            # Progress bar
            canvas = tk.Canvas(frame, width=percentage*2, height=15, bg='#34495e', highlightthickness=0)
            canvas.pack(side=tk.LEFT, padx=5)
            canvas.create_rectangle(0, 0, percentage*2, 15, fill='#2ecc71')
        
        tk.Button(poll_window, text="Close", command=poll_window.destroy,
                 font=('Arial', 10), bg='#3498db', fg='white', padx=20).pack(pady=10)
        
        self.lifelines_used['audience'] = True
        self.audience_btn.config(state=tk.DISABLED, bg='#7f8c8d')
    
    def update_lifeline_buttons(self):
        self.fifty_btn.config(state=tk.NORMAL if not self.lifelines_used['fifty_fifty'] else tk.DISABLED,
                             bg='#9b59b6' if not self.lifelines_used['fifty_fifty'] else '#7f8c8d')
        self.audience_btn.config(state=tk.NORMAL if not self.lifelines_used['audience'] else tk.DISABLED,
                                bg='#e67e22' if not self.lifelines_used['audience'] else '#7f8c8d')
    
    def update_score(self):
        self.score_label.config(text=f"Score: {self.score}")
    
    def next_question(self):
        self.current_index += 1
        if self.current_index < len(self.current_questions):
            self.load_question()
        else:
            self.end_quiz()
    
    def end_quiz(self):
        percentage = (self.score / len(self.current_questions)) * 100
        self.save_high_score(self.score, percentage)
        
        result_window = tk.Toplevel(self.root)
        result_window.title("Quiz Results")
        result_window.geometry("500x400")
        result_window.configure(bg='#1a1a2e')
        result_window.transient(self.root)
        result_window.grab_set()
        
        tk.Label(result_window, text="📊 QUIZ COMPLETE! 📊",
                font=('Arial', 20, 'bold'), bg='#1a1a2e', fg='#ffd700').pack(pady=20)
        
        stats = [
            (f"📝 Category: {self.current_category}", '#3498db'),
            (f"✅ Score: {self.score}/{len(self.current_questions)}", '#2ecc71'),
            (f"📈 Percentage: {percentage:.1f}%", '#f39c12'),
            (f"🏆 Final Grade: {self.get_grade(percentage)}", '#e74c3c')
        ]
        
        for text, color in stats:
            tk.Label(result_window, text=text, font=('Arial', 14),
                    bg='#1a1a2e', fg=color).pack(pady=10)
        
        # Show if high score
        if len(self.high_scores) > 0 and self.score >= self.high_scores[0]['score']:
            tk.Label(result_window, text="🏆 NEW HIGH SCORE! 🏆",
                    font=('Arial', 16, 'bold'), bg='#1a1a2e', fg='#ffd700').pack(pady=10)
        
        btn_frame = tk.Frame(result_window, bg='#1a1a2e')
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Play Again", command=lambda: [result_window.destroy(), self.start_new_game()],
                 font=('Arial', 12), bg='#27ae60', fg='white', padx=20).pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="Close", command=result_window.destroy,
                 font=('Arial', 12), bg='#3498db', fg='white', padx=20).pack(side=tk.LEFT, padx=10)
    
    def get_grade(self, percentage):
        if percentage >= 90:
            return "A+ (Excellent!)"
        elif percentage >= 80:
            return "A (Very Good!)"
        elif percentage >= 70:
            return "B (Good!)"
        elif percentage >= 60:
            return "C (Fair)"
        else:
            return "D (Keep Practicing!)"
    
    def update_high_scores_display(self):
        self.high_scores_text.delete(1.0, tk.END)
        
        if self.high_scores:
            for i, score in enumerate(self.high_scores[:5], 1):
                self.high_scores_text.insert(tk.END, 
                    f"{i}. {score['score']}/5 ({score['percentage']:.1f}%) - {score['category']} - {score['date']}\n")
        else:
            self.high_scores_text.insert(tk.END, "No high scores yet. Play a game!")

if __name__ == "__main__":
    root = tk.Tk()
    game = QuizGame(root)
    root.mainloop()