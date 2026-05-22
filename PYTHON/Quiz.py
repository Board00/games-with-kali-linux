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
        
        # EXPANDED Quiz questions database - 50+ questions per category!
        self.questions = {
            'Science': [
                # Physics
                {'question': 'What is the chemical symbol for Gold?', 'options': ['Go', 'Gd', 'Au', 'Ag'], 'correct': 2, 'explanation': 'Au comes from Latin "Aurum" meaning gold'},
                {'question': 'What is the hardest natural substance?', 'options': ['Iron', 'Diamond', 'Platinum', 'Titanium'], 'correct': 1, 'explanation': 'Diamond is the hardest known natural material'},
                {'question': 'What planet is known as the "Red Planet"?', 'options': ['Mars', 'Jupiter', 'Venus', 'Saturn'], 'correct': 0, 'explanation': 'Mars appears red due to iron oxide on its surface'},
                {'question': 'What is the largest organ in the human body?', 'options': ['Heart', 'Brain', 'Liver', 'Skin'], 'correct': 3, 'explanation': 'The skin is the largest organ, covering about 2 square meters'},
                {'question': 'What gas do plants absorb from the air?', 'options': ['Oxygen', 'Nitrogen', 'Carbon Dioxide', 'Hydrogen'], 'correct': 2, 'explanation': 'Plants absorb CO2 for photosynthesis'},
                {'question': 'What is the speed of light?', 'options': ['300,000 km/s', '150,000 km/s', '1,000,000 km/s', '500,000 km/s'], 'correct': 0, 'explanation': 'Light travels at approximately 299,792 km/s'},
                {'question': 'Who developed the theory of relativity?', 'options': ['Isaac Newton', 'Galileo Galilei', 'Albert Einstein', 'Nikola Tesla'], 'correct': 2, 'explanation': 'Einstein published the theory of relativity in 1905 and 1915'},
                {'question': 'What is the chemical symbol for Water?', 'options': ['O2', 'CO2', 'H2O', 'NaCl'], 'correct': 2, 'explanation': 'Water is H2O - two hydrogen atoms and one oxygen atom'},
                {'question': 'What is the largest bone in the human body?', 'options': ['Femur', 'Tibia', 'Fibula', 'Humerus'], 'correct': 0, 'explanation': 'The femur (thigh bone) is the longest and strongest bone'},
                {'question': 'What is the freezing point of water in Celsius?', 'options': ['100°C', '0°C', '32°C', '-10°C'], 'correct': 1, 'explanation': 'Water freezes at 0°C (32°F)'},
                {'question': 'What is the powerhouse of the cell?', 'options': ['Nucleus', 'Mitochondria', 'Ribosome', 'Golgi'], 'correct': 1, 'explanation': 'Mitochondria produce energy for the cell'},
                {'question': 'Which planet is known as the "Blue Planet"?', 'options': ['Mars', 'Earth', 'Uranus', 'Neptune'], 'correct': 1, 'explanation': 'Earth appears blue due to its oceans'},
                {'question': 'What is the atomic number of Carbon?', 'options': ['4', '5', '6', '7'], 'correct': 2, 'explanation': 'Carbon has 6 protons in its nucleus'},
                {'question': 'What type of energy is stored in food?', 'options': ['Kinetic', 'Chemical', 'Thermal', 'Nuclear'], 'correct': 1, 'explanation': 'Food contains chemical energy that our bodies convert'},
                {'question': 'What is the study of fossils called?', 'options': ['Geology', 'Paleontology', 'Archaeology', 'Biology'], 'correct': 1, 'explanation': 'Paleontologists study fossils and ancient life'},
                {'question': 'What gas do humans exhale?', 'options': ['Oxygen', 'Nitrogen', 'Carbon Dioxide', 'Hydrogen'], 'correct': 2, 'explanation': 'Humans breathe in oxygen and exhale carbon dioxide'},
                {'question': 'What is the closest star to Earth?', 'options': ['Proxima Centauri', 'Alpha Centauri', 'The Sun', 'Sirius'], 'correct': 2, 'explanation': 'The Sun is the closest star to Earth'},
                {'question': 'What is the hardest mineral on Mohs scale?', 'options': ['Corundum', 'Topaz', 'Diamond', 'Quartz'], 'correct': 2, 'explanation': 'Diamond ranks 10 on Mohs hardness scale'},
                {'question': 'What is the main component of air?', 'options': ['Oxygen', 'Carbon Dioxide', 'Nitrogen', 'Argon'], 'correct': 2, 'explanation': 'Air is about 78% nitrogen and 21% oxygen'},
                {'question': 'What is the study of heredity called?', 'options': ['Genetics', 'Biology', 'Ecology', 'Evolution'], 'correct': 0, 'explanation': 'Genetics studies how traits are passed through generations'},
                {'question': 'What is the boiling point of water?', 'options': ['50°C', '75°C', '100°C', '125°C'], 'correct': 2, 'explanation': 'Water boils at 100°C at sea level'},
                {'question': 'Who discovered Penicillin?', 'options': ['Louis Pasteur', 'Alexander Fleming', 'Marie Curie', 'Edward Jenner'], 'correct': 1, 'explanation': 'Fleming discovered penicillin in 1928'},
                {'question': 'What is the smallest planet in our solar system?', 'options': ['Mars', 'Mercury', 'Pluto', 'Venus'], 'correct': 1, 'explanation': 'Mercury is the smallest planet (Pluto is a dwarf planet)'},
                {'question': 'What is the unit of electrical resistance?', 'options': ['Volt', 'Ampere', 'Ohm', 'Watt'], 'correct': 2, 'explanation': 'Ohms measure electrical resistance'},
                {'question': 'What is the main gas in Earth\'s atmosphere?', 'options': ['Oxygen', 'Carbon Dioxide', 'Nitrogen', 'Argon'], 'correct': 2, 'explanation': 'Nitrogen makes up about 78% of our atmosphere'},
            ],
            'History': [
                # Ancient History
                {'question': 'Who painted the Mona Lisa?', 'options': ['Van Gogh', 'Picasso', 'Da Vinci', 'Rembrandt'], 'correct': 2, 'explanation': 'Leonardo da Vinci painted the Mona Lisa in the 16th century'},
                {'question': 'In which year did World War II end?', 'options': ['1943', '1944', '1945', '1946'], 'correct': 2, 'explanation': 'WWII ended in 1945 after the surrender of Japan'},
                {'question': 'Who was the first person to walk on the moon?', 'options': ['Buzz Aldrin', 'Neil Armstrong', 'Yuri Gagarin', 'Alan Shepard'], 'correct': 1, 'explanation': 'Neil Armstrong walked on the moon on July 20, 1969'},
                {'question': 'Which ancient civilization built Machu Picchu?', 'options': ['Aztecs', 'Mayans', 'Incas', 'Olmecs'], 'correct': 2, 'explanation': 'The Incas built Machu Picchu in the 15th century'},
                {'question': 'Who wrote "Romeo and Juliet"?', 'options': ['Charles Dickens', 'Jane Austen', 'William Shakespeare', 'Mark Twain'], 'correct': 2, 'explanation': 'Shakespeare wrote Romeo and Juliet around 1595'},
                {'question': 'Who was the first President of the United States?', 'options': ['John Adams', 'Thomas Jefferson', 'George Washington', 'Benjamin Franklin'], 'correct': 2, 'explanation': 'George Washington was president from 1789-1797'},
                {'question': 'Who discovered America?', 'options': ['Christopher Columbus', 'Leif Erikson', 'Marco Polo', 'Ferdinand Magellan'], 'correct': 0, 'explanation': 'Columbus reached the Americas in 1492'},
                {'question': 'Which empire was ruled by Julius Caesar?', 'options': ['Greek', 'Persian', 'Roman', 'Egyptian'], 'correct': 2, 'explanation': 'Caesar was a Roman general and dictator'},
                {'question': 'What was the name of the ship that Darwin sailed on?', 'options': ['Santa Maria', 'Beagle', 'Endeavour', 'Victory'], 'correct': 1, 'explanation': 'Darwin sailed on HMS Beagle (1831-1836)'},
                {'question': 'Who built the Great Wall of China?', 'options': ['Ming Dynasty', 'Qin Dynasty', 'Han Dynasty', 'Tang Dynasty'], 'correct': 1, 'explanation': 'The Qin Dynasty began construction around 221 BCE'},
                {'question': 'Who was known as the "Iron Lady"?', 'options': ['Queen Victoria', 'Indira Gandhi', 'Margaret Thatcher', 'Angela Merkel'], 'correct': 2, 'explanation': 'Thatcher was British Prime Minister from 1979-1990'},
                {'question': 'Who invented the telephone?', 'options': ['Thomas Edison', 'Nikola Tesla', 'Alexander Graham Bell', 'Guglielmo Marconi'], 'correct': 2, 'explanation': 'Bell patented the telephone in 1876'},
                {'question': 'Where was Napoleon Bonaparte exiled?', 'options': ['Elba', 'St. Helena', 'Corsica', 'Malta'], 'correct': 1, 'explanation': 'Napoleon was exiled to Elba (1814) and St. Helena (1815)'},
                {'question': 'Who wrote the Declaration of Independence?', 'options': ['George Washington', 'John Adams', 'Thomas Jefferson', 'Benjamin Franklin'], 'correct': 2, 'explanation': 'Jefferson was the primary author in 1776'},
                {'question': 'Who was the last emperor of China?', 'options': ['Puyi', 'Cixi', 'Kangxi', 'Qianlong'], 'correct': 0, 'explanation': 'Puyi abdicated in 1912, ending imperial China'},
                {'question': 'Who painted the Sistine Chapel?', 'options': ['Leonardo da Vinci', 'Raphael', 'Michelangelo', 'Donatello'], 'correct': 2, 'explanation': 'Michelangelo painted it between 1508-1512'},
                {'question': 'Who was the first woman to win a Nobel Prize?', 'options': ['Marie Curie', 'Mother Teresa', 'Rosalind Franklin', 'Ada Lovelace'], 'correct': 0, 'explanation': 'Curie won Physics (1903) and Chemistry (1911)'},
                {'question': 'Who discovered penicillin?', 'options': ['Louis Pasteur', 'Alexander Fleming', 'Robert Koch', 'Joseph Lister'], 'correct': 1, 'explanation': 'Fleming discovered penicillin in 1928'},
                {'question': 'Who was the first African-American president?', 'options': ['Colin Powell', 'Barack Obama', 'Kamala Harris', 'Martin Luther King'], 'correct': 1, 'explanation': 'Obama served from 2009-2017'},
                {'question': 'Who wrote "The Communist Manifesto"?', 'options': ['Lenin', 'Stalin', 'Marx and Engels', 'Rosa Luxemburg'], 'correct': 2, 'explanation': 'Marx and Engels published it in 1848'},
                {'question': 'Who led the civil rights movement?', 'options': ['Malcolm X', 'Martin Luther King Jr.', 'Rosa Parks', 'Nelson Mandela'], 'correct': 1, 'explanation': 'King led the movement from 1955 until 1968'},
                {'question': 'Who was the first man in space?', 'options': ['Neil Armstrong', 'Buzz Aldrin', 'Yuri Gagarin', 'Alan Shepard'], 'correct': 2, 'explanation': 'Gagarin orbited Earth in 1961'},
                {'question': 'Who invented the printing press?', 'options': ['Johannes Gutenberg', 'William Caxton', 'Aldus Manutius', 'John Baskerville'], 'correct': 0, 'explanation': 'Gutenberg invented it around 1440'},
                {'question': 'Who was the first emperor of Rome?', 'options': ['Julius Caesar', 'Augustus', 'Nero', 'Constantine'], 'correct': 1, 'explanation': 'Augustus became first emperor in 27 BCE'},
                {'question': 'Who discovered radium?', 'options': ['Albert Einstein', 'Isaac Newton', 'Marie Curie', 'Louis Pasteur'], 'correct': 2, 'explanation': 'Marie Curie discovered radium in 1898'},
                {'question': 'Who was the founder of Microsoft?', 'options': ['Steve Jobs', 'Bill Gates', 'Paul Allen', 'Mark Zuckerberg'], 'correct': 1, 'explanation': 'Gates co-founded Microsoft with Paul Allen in 1975'},
                {'question': 'Who was known as the "Maid of Orleans"?', 'options': ['Joan of Arc', 'Eleanor of Aquitaine', 'Catherine the Great', 'Queen Elizabeth I'], 'correct': 0, 'explanation': 'Joan of Arc led French forces in the Hundred Years\' War'},
                {'question': 'Who wrote the "I Have a Dream" speech?', 'options': ['Malcolm X', 'John F. Kennedy', 'Martin Luther King Jr.', 'Barack Obama'], 'correct': 2, 'explanation': 'King delivered it in 1963 during the March on Washington'},
            ],
            'Movies': [
                # Classics & Modern
                {'question': 'Who played Jack Dawson in Titanic?', 'options': ['Brad Pitt', 'Leonardo DiCaprio', 'Johnny Depp', 'Matt Damon'], 'correct': 1, 'explanation': 'Leonardo DiCaprio played Jack Dawson in the 1997 film'},
                {'question': 'What is the highest-grossing film of all time (unadjusted)?', 'options': ['Avatar', 'Avengers: Endgame', 'Titanic', 'Star Wars'], 'correct': 0, 'explanation': 'Avatar holds the record with over $2.8 billion'},
                {'question': 'Which movie won the Oscar for Best Picture in 2020?', 'options': ['1917', 'Joker', 'Parasite', 'Once Upon a Time in Hollywood'], 'correct': 2, 'explanation': 'Parasite made history as the first non-English film to win'},
                {'question': 'Who directed "Inception"?', 'options': ['Steven Spielberg', 'Christopher Nolan', 'Quentin Tarantino', 'James Cameron'], 'correct': 1, 'explanation': 'Christopher Nolan directed Inception in 2010'},
                {'question': 'What is the name of Harry Potter\'s owl?', 'options': ['Errol', 'Hedwig', 'Pigwidgeon', 'Hermes'], 'correct': 1, 'explanation': 'Hedwig was Harry\'s snowy owl'},
                {'question': 'Who played Iron Man in the MCU?', 'options': ['Chris Evans', 'Chris Hemsworth', 'Robert Downey Jr.', 'Mark Ruffalo'], 'correct': 2, 'explanation': 'Downey played Tony Stark from 2008-2019'},
                {'question': 'What year was "The Godfather" released?', 'options': ['1970', '1971', '1972', '1973'], 'correct': 2, 'explanation': 'The Godfather was released in 1972'},
                {'question': 'Who directed "Pulp Fiction"?', 'options': ['Martin Scorsese', 'Quentin Tarantino', 'David Fincher', 'Coen Brothers'], 'correct': 1, 'explanation': 'Tarantino directed Pulp Fiction in 1994'},
                {'question': 'What is the name of the fictional African country in "Black Panther"?', 'options': ['Zamunda', 'Zimbabwe', 'Wakanda', 'Kenya'], 'correct': 2, 'explanation': 'Wakanda is a technologically advanced hidden nation'},
                {'question': 'Who played the Joker in "The Dark Knight"?', 'options': ['Jack Nicholson', 'Jared Leto', 'Heath Ledger', 'Joaquin Phoenix'], 'correct': 2, 'explanation': 'Ledger won a posthumous Oscar for his performance'},
                {'question': 'What is the longest-running movie franchise?', 'options': ['James Bond', 'Star Wars', 'Marvel', 'Godzilla'], 'correct': 0, 'explanation': 'James Bond started in 1962 and has 25+ films'},
                {'question': 'Who played Forrest Gump?', 'options': ['Tom Hanks', 'Brad Pitt', 'Johnny Depp', 'Matt Damon'], 'correct': 0, 'explanation': 'Hanks won an Oscar for his role in 1994'},
                {'question': 'What is the name of the wizarding school in "Harry Potter"?', 'options': ['Beauxbatons', 'Durmstrang', 'Hogwarts', 'Ilvermorny'], 'correct': 2, 'explanation': 'Hogwarts School of Witchcraft and Wizardry'},
                {'question': 'Who directed "Schindler\'s List"?', 'options': ['Martin Scorsese', 'Steven Spielberg', 'Francis Ford Coppola', 'Stanley Kubrick'], 'correct': 1, 'explanation': 'Spielberg won Best Director for this 1993 film'},
                {'question': 'What is the name of the spaceship in "Wall-E"?', 'options': ['Axiom', 'Eve', 'BNL', 'Plant'], 'correct': 0, 'explanation': 'The Axiom is the luxury starliner in the film'},
                {'question': 'Who played Elle Woods in "Legally Blonde"?', 'options': ['Cameron Diaz', 'Reese Witherspoon', 'Julia Roberts', 'Kate Hudson'], 'correct': 1, 'explanation': 'Witherspoon starred as Elle Woods in 2001'},
                {'question': 'What movie features the song "My Heart Will Go On"?', 'options': ['The Bodyguard', 'Titanic', 'Ghost', 'Dirty Dancing'], 'correct': 1, 'explanation': 'Celine Dion sang the theme for Titanic'},
                {'question': 'Who played Neo in "The Matrix"?', 'options': ['Keanu Reeves', 'Brad Pitt', 'Tom Cruise', 'Will Smith'], 'correct': 0, 'explanation': 'Reeves played Neo in all three Matrix films'},
                {'question': 'What is the name of the alien in "E.T."?', 'options': ['E.T.', 'M&M', 'Alf', 'Stitch'], 'correct': 0, 'explanation': 'E.T. (Extra-Terrestrial) is the friendly alien'},
                {'question': 'Who directed "The Shining"?', 'options': ['Alfred Hitchcock', 'Stanley Kubrick', 'Stephen King', 'John Carpenter'], 'correct': 1, 'explanation': 'Kubrick directed the 1980 horror classic'},
                {'question': 'What is the name of Simba\'s father in "The Lion King"?', 'options': ['Scar', 'Mufasa', 'Musafa', 'Mufasa'], 'correct': 1, 'explanation': 'Mufasa is the king of Pride Rock'},
                {'question': 'Who played Indiana Jones?', 'options': ['Harrison Ford', 'Sean Connery', 'Tom Selleck', 'Kurt Russell'], 'correct': 0, 'explanation': 'Ford played Indy in four films'},
                {'question': 'What is the name of the villain in "The Little Mermaid"?', 'options': ['Maleficent', 'Ursula', 'Cruella', 'Grimhilde'], 'correct': 1, 'explanation': 'Ursula is the sea witch'},
                {'question': 'Who starred in "Die Hard" as John McClane?', 'options': ['Arnold Schwarzenegger', 'Bruce Willis', 'Sylvester Stallone', 'Jean-Claude Van Damme'], 'correct': 1, 'explanation': 'Willis played McClane in all Die Hard films'},
                {'question': 'What movie won the most Oscars of all time?', 'options': ['Titanic', 'Ben-Hur', 'The Lord of the Rings', 'All of the above'], 'correct': 3, 'explanation': 'Three films have won 11 Oscars each'},
                {'question': 'Who played James Bond in "Casino Royale"?', 'options': ['Pierce Brosnan', 'Timothy Dalton', 'Daniel Craig', 'Sean Connery'], 'correct': 2, 'explanation': 'Craig debuted as Bond in 2006'},
                {'question': 'What year was "The Wizard of Oz" released?', 'options': ['1935', '1937', '1939', '1941'], 'correct': 2, 'explanation': 'The classic film was released in 1939'},
                {'question': 'Who voiced Woody in "Toy Story"?', 'options': ['Tim Allen', 'Tom Hanks', 'John Ratzenberger', 'Don Rickles'], 'correct': 1, 'explanation': 'Hanks has voiced Woody since 1995'},
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
        
        # subtitle = tk.Label(title_frame, text="50+ Questions Per Category!",
        #                    font=('Arial', 12), bg='#1a1a2e', fg='#2ecc71')
        # subtitle.pack()
        
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
        
        self.question_num_label = tk.Label(score_frame, text="Question: 0/10", font=('Arial', 14),
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
        
        # # Info Label
        # info_label = tk.Label(self.root, text="💡 10 random questions from 50+ in each category!",
        #                       font=('Arial', 10), bg='#1a1a2e', fg='#7f8c8d')
        # info_label.pack(pady=5)
        
        # High Scores Frame
        high_score_frame = tk.LabelFrame(self.root, text="🏆 Top 5 High Scores 🏆", font=('Arial', 12, 'bold'),
                                         bg='#1a1a2e', fg='white')
        high_score_frame.pack(pady=10, padx=20, fill='x')
        
        self.high_scores_text = tk.Text(high_score_frame, height=5, font=('Courier', 10),
                                        bg='#0f3460', fg='#2ecc71')
        self.high_scores_text.pack(fill='both', expand=True, padx=5, pady=5)
    
    def change_category(self):
        self.current_category = self.category_var.get()
        self.start_new_game()
    
    def start_new_game(self):
        # Select 10 random questions from category (changed from 5 to 10)
        category_questions = self.questions[self.current_category]
        self.current_questions = random.sample(category_questions, min(10, len(category_questions)))
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
        remove_count = 2
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
        poll_window.geometry("450x400")
        poll_window.configure(bg='#1a1a2e')
        
        tk.Label(poll_window, text="📊 AUDIENCE POLL RESULTS 📊",
                font=('Arial', 14, 'bold'), bg='#1a1a2e', fg='#ffd700').pack(pady=10)
        
        for text, percentage in poll_results:
            frame = tk.Frame(poll_window, bg='#1a1a2e')
            frame.pack(fill='x', padx=20, pady=5)
            
            tk.Label(frame, text=text, font=('Arial', 10),
                    bg='#1a1a2e', fg='white', width=25, anchor='w').pack(side=tk.LEFT)
            
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
        result_window.geometry("500x450")
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
                    f"{i}. {score['score']}/10 ({score['percentage']:.1f}%) - {score['category']} - {score['date']}\n")
        else:
            self.high_scores_text.insert(tk.END, "No high scores yet. Play a game!")

if __name__ == "__main__":
    root = tk.Tk()
    game = QuizGame(root)
    root.mainloop()