import tkinter as tk
from tkinter import messagebox
import random

class Game2048:
    def __init__(self, root):
        self.root = root
        self.root.title("2048 Game")
        self.root.geometry("500x600")
        self.root.configure(bg='#faf8ef')
        
        self.grid_size = 4
        self.grid = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.score = 0
        self.best_score = self.load_best_score()
        
        self.setup_ui()
        self.new_game()
    
    def load_best_score(self):
        try:
            with open("2048_bestscore.txt", "r") as f:
                return int(f.read())
        except:
            return 0
    
    def save_best_score(self):
        with open("2048_bestscore.txt", "w") as f:
            f.write(str(self.best_score))
    
    def setup_ui(self):
        # Title
        title_frame = tk.Frame(self.root, bg='#faf8ef')
        title_frame.pack(pady=20)
        
        title = tk.Label(title_frame, text="2048", font=('Arial', 48, 'bold'),
                        bg='#faf8ef', fg='#776e65')
        title.pack(side=tk.LEFT, padx=20)
        
        # Score Frame
        score_frame = tk.Frame(title_frame, bg='#bbada0', padx=20, pady=10, relief=tk.RAISED)
        score_frame.pack(side=tk.LEFT, padx=20)
        
        self.score_label = tk.Label(score_frame, text=f"Score: {self.score}",
                                    font=('Arial', 14, 'bold'), bg='#bbada0', fg='white')
        self.score_label.pack()
        
        self.best_label = tk.Label(score_frame, text=f"Best: {self.best_score}",
                                   font=('Arial', 12), bg='#bbada0', fg='#f9f6f2')
        self.best_label.pack()
        
        # Game Grid Frame
        self.grid_frame = tk.Frame(self.root, bg='#bbada0', padx=10, pady=10)
        self.grid_frame.pack(pady=20)
        
        self.cells = []
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                cell = tk.Label(self.grid_frame, text="", width=6, height=3,
                               font=('Arial', 24, 'bold'), bg='#cdc1b4', relief=tk.RAISED)
                cell.grid(row=i, column=j, padx=5, pady=5)
                row.append(cell)
            self.cells.append(row)
        
        # Control Buttons
        control_frame = tk.Frame(self.root, bg='#faf8ef')
        control_frame.pack(pady=(20))
        
        new_game_btn = tk.Button(control_frame, text="New Game", font=('Arial', 12, 'bold'),
                                bg='#8f7a66', fg='white', padx=20, pady=10,
                                command=self.new_game, cursor='hand2')
        new_game_btn.pack(side=tk.LEFT, padx=10)
        
        # Instructions
        instr_frame = tk.Frame(self.root, bg='#faf8ef')
        instr_frame.pack(pady=(20))
        
        instructions = tk.Label(instr_frame, text="Use Arrow Keys to Move Tiles",
                               font=('Arial', 10), bg='#faf8ef', fg='#776e65')
        instructions.pack()
        
        # Bind arrow keys
        self.root.bind('<Up>', lambda e: self.move('up'))
        self.root.bind('<Down>', lambda e: self.move('down'))
        self.root.bind('<Left>', lambda e: self.move('left'))
        self.root.bind('<Right>', lambda e: self.move('right'))
    
    def get_cell_color(self, value):
        colors = {
            0: '#cdc1b4',
            2: '#eee4da',
            4: '#ede0c8',
            8: '#f2b179',
            16: '#f59563',
            32: '#f67c5f',
            64: '#f65e3b',
            128: '#edcf72',
            256: '#edcc61',
            512: '#edc850',
            1024: '#edc53f',
            2048: '#edc22e'
        }
        return colors.get(value, '#3c3a32')
    
    def get_text_color(self, value):
        if value in [2, 4]:
            return '#776e65'
        return '#f9f6f2'
    
    def update_display(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                value = self.grid[i][j]
                self.cells[i][j].config(text=str(value) if value != 0 else "",
                                       bg=self.get_cell_color(value),
                                       fg=self.get_text_color(value))
        
        self.score_label.config(text=f"Score: {self.score}")
        if self.score > self.best_score:
            self.best_score = self.score
            self.best_label.config(text=f"Best: {self.best_score}")
            self.save_best_score()
    
    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(self.grid_size) for j in range(self.grid_size) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4
    
    def compress(self, row):
        new_row = [x for x in row if x != 0]
        new_row += [0] * (self.grid_size - len(new_row))
        return new_row
    
    def merge(self, row):
        for i in range(self.grid_size - 1):
            if row[i] == row[i + 1] and row[i] != 0:
                row[i] *= 2
                self.score += row[i]
                row[i + 1] = 0
        return row
    
    def move_left(self):
        moved = False
        for i in range(self.grid_size):
            original = self.grid[i][:]
            compressed = self.compress(original)
            merged = self.merge(compressed)
            final = self.compress(merged)
            self.grid[i] = final
            if original != final:
                moved = True
        return moved
    
    def move_right(self):
        moved = False
        for i in range(self.grid_size):
            original = self.grid[i][:]
            reversed_row = original[::-1]
            compressed = self.compress(reversed_row)
            merged = self.merge(compressed)
            final = self.compress(merged)[::-1]
            self.grid[i] = final
            if original != final:
                moved = True
        return moved
    
    def move_up(self):
        moved = False
        for j in range(self.grid_size):
            original = [self.grid[i][j] for i in range(self.grid_size)]
            compressed = self.compress(original)
            merged = self.merge(compressed)
            final = self.compress(merged)
            for i in range(self.grid_size):
                if self.grid[i][j] != final[i]:
                    moved = True
                self.grid[i][j] = final[i]
        return moved
    
    def move_down(self):
        moved = False
        for j in range(self.grid_size):
            original = [self.grid[i][j] for i in range(self.grid_size)]
            reversed_col = original[::-1]
            compressed = self.compress(reversed_col)
            merged = self.merge(compressed)
            final = self.compress(merged)[::-1]
            for i in range(self.grid_size):
                if self.grid[i][j] != final[i]:
                    moved = True
                self.grid[i][j] = final[i]
        return moved
    
    def is_game_over(self):
        # Check for empty cells
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i][j] == 0:
                    return False
        
        # Check for possible merges
        for i in range(self.grid_size):
            for j in range(self.grid_size - 1):
                if self.grid[i][j] == self.grid[i][j + 1]:
                    return False
        
        for i in range(self.grid_size - 1):
            for j in range(self.grid_size):
                if self.grid[i][j] == self.grid[i + 1][j]:
                    return False
        
        return True
    
    def move(self, direction):
        if self.game_over:
            return
        
        moved = False
        if direction == 'left':
            moved = self.move_left()
        elif direction == 'right':
            moved = self.move_right()
        elif direction == 'up':
            moved = self.move_up()
        elif direction == 'down':
            moved = self.move_down()
        
        if moved:
            self.add_new_tile()
            self.update_display()
            
            if self.is_game_over():
                self.game_over = True
                messagebox.showinfo("Game Over", f"Game Over!\nYour score: {self.score}")
    
    def new_game(self):
        self.grid = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.score = 0
        self.game_over = False
        
        # Add two initial tiles
        self.add_new_tile()
        self.add_new_tile()
        
        self.update_display()

if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()