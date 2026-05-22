import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CELL_SIZE = 20
SNAKE_SPEED = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        
        self.reset_game()
    
    def reset_game(self):
        self.snake = [(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)]
        self.direction = (CELL_SIZE, 0)
        self.next_direction = (CELL_SIZE, 0)
        self.score = 0
        self.high_score = self.load_high_score()
        self.game_over = False
        self.paused = False
        
        # Generate initial food
        self.food = self.generate_food()
    
    def load_high_score(self):
        try:
            with open("snake_highscore.txt", "r") as f:
                return int(f.read())
        except:
            return 0
    
    def save_high_score(self):
        with open("snake_highscore.txt", "w") as f:
            f.write(str(self.high_score))
    
    def generate_food(self):
        while True:
            x = random.randint(0, (WINDOW_WIDTH // CELL_SIZE) - 1) * CELL_SIZE
            y = random.randint(0, (WINDOW_HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
            if (x, y) not in self.snake:
                return (x, y)
    
    def draw_snake(self):
        for i, segment in enumerate(self.snake):
            color = DARK_GREEN if i == 0 else GREEN
            pygame.draw.rect(self.screen, color, (segment[0], segment[1], CELL_SIZE - 2, CELL_SIZE - 2))
            pygame.draw.rect(self.screen, (0, 100, 0), (segment[0], segment[1], CELL_SIZE - 2, CELL_SIZE - 2), 1)
    
    def draw_food(self):
        pygame.draw.rect(self.screen, RED, (self.food[0], self.food[1], CELL_SIZE - 2, CELL_SIZE - 2))
        # Draw inner glow
        pygame.draw.rect(self.screen, (255, 100, 100), (self.food[0] + 4, self.food[1] + 4, 12, 12))
    
    def draw_grid(self):
        for x in range(0, WINDOW_WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, (40, 40, 40), (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, (40, 40, 40), (0, y), (WINDOW_WIDTH, y))
    
    def draw_score(self):
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, YELLOW)
        self.screen.blit(high_score_text, (10, 50))
        
        if self.paused:
            pause_text = self.big_font.render("PAUSED", True, YELLOW)
            text_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(pause_text, text_rect)
    
    def move_snake(self):
        self.direction = self.next_direction
        new_head = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])
        
        # Check collision with walls
        if (new_head[0] < 0 or new_head[0] >= WINDOW_WIDTH or
            new_head[1] < 0 or new_head[1] >= WINDOW_HEIGHT):
            self.game_over = True
            return
        
        # Check collision with self
        if new_head in self.snake[:-1]:
            self.game_over = True
            return
        
        self.snake.insert(0, new_head)
        
        # Check collision with food
        if new_head == self.food:
            self.score += 10
            if self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score()
            self.food = self.generate_food()
        else:
            self.snake.pop()
    
    def show_game_over(self):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.big_font.render("GAME OVER", True, RED)
        text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        self.screen.blit(game_over_text, text_rect)
        
        score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
        self.screen.blit(score_text, score_rect)
        
        restart_text = self.font.render("Press SPACE to play again or ESC to quit", True, YELLOW)
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80))
        self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                        return True
                    elif event.key == pygame.K_ESCAPE:
                        return False
        return False
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if not self.game_over:
                        if event.key == pygame.K_UP and self.direction != (0, CELL_SIZE):
                            self.next_direction = (0, -CELL_SIZE)
                        elif event.key == pygame.K_DOWN and self.direction != (0, -CELL_SIZE):
                            self.next_direction = (0, CELL_SIZE)
                        elif event.key == pygame.K_LEFT and self.direction != (CELL_SIZE, 0):
                            self.next_direction = (-CELL_SIZE, 0)
                        elif event.key == pygame.K_RIGHT and self.direction != (-CELL_SIZE, 0):
                            self.next_direction = (CELL_SIZE, 0)
                        elif event.key == pygame.K_p:
                            self.paused = not self.paused
                    elif event.key == pygame.K_SPACE:
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        running = False
            
            if not self.game_over and not self.paused:
                self.move_snake()
            
            # Draw everything
            self.screen.fill(BLACK)
            self.draw_grid()
            self.draw_food()
            self.draw_snake()
            self.draw_score()
            
            if self.game_over:
                if not self.show_game_over():
                    running = False
            
            pygame.display.flip()
            self.clock.tick(SNAKE_SPEED)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()