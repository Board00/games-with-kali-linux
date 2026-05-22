import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
BLUE = (50, 50, 255)
GREEN = (50, 255, 50)
YELLOW = (255, 255, 50)
PURPLE = (255, 50, 255)
CYAN = (50, 255, 255)
ORANGE = (255, 150, 50)
DARK_GRAY = (40, 40, 40)
GRAY = (100, 100, 100)

# Paddle settings
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 120
PADDLE_SPEED = 7

# Ball settings
BALL_SIZE = 15
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# AI Settings
AI_SPEED = 5.5  # Slightly slower than player for fair challenge

class Paddle:
    def __init__(self, x, y, color, is_player=True):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.color = color
        self.is_player = is_player
        self.score = 0
    
    def move(self, y_change):
        self.rect.y += y_change
        # Keep paddle on screen
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        # Add gradient effect (optional)
        pygame.draw.rect(screen, (min(self.color[0] + 50, 255),
                                  min(self.color[1] + 50, 255),
                                  min(self.color[2] + 50, 255)), 
                        self.rect, 3)
    
    def reset_position(self):
        self.rect.y = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2

class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BALL_SIZE, BALL_SIZE)
        self.speed_x = BALL_SPEED_X * random.choice([-1, 1])
        self.speed_y = BALL_SPEED_Y * random.choice([-1, 1])
        self.start_x = x
        self.start_y = y
    
    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
    
    def draw(self, screen):
        # Draw a glowing ball effect
        pygame.draw.ellipse(screen, WHITE, self.rect)
        pygame.draw.ellipse(screen, CYAN, self.rect.inflate(-4, -4))
    
    def reset(self):
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.speed_x = BALL_SPEED_X * random.choice([-1, 1])
        self.speed_y = BALL_SPEED_Y * random.choice([-1, 1])
        # Slight random angle variation
        if random.random() > 0.5:
            self.speed_y += random.uniform(-1, 1)
    
    def increase_speed(self, factor=1.05):
        self.speed_x *= factor
        self.speed_y *= factor
        # Cap maximum speed
        max_speed = 12
        if abs(self.speed_x) > max_speed:
            self.speed_x = max_speed if self.speed_x > 0 else -max_speed
        if abs(self.speed_y) > max_speed:
            self.speed_y = max_speed if self.speed_y > 0 else -max_speed

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.lifetime = 30
        self.size = random.randint(2, 5)
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
    
    def draw(self, screen):
        alpha = int(255 * (self.lifetime / 30))
        color = (255, 255, 100, alpha)
        pygame.draw.circle(screen, (255, 255, 100), (int(self.x), int(self.y)), self.size)

class PongGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🏓 PONG - Classic Arcade Game")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # Game objects
        self.left_paddle = Paddle(30, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, BLUE, True)
        self.right_paddle = Paddle(SCREEN_WIDTH - 30 - PADDLE_WIDTH, 
                                   SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, RED, False)
        self.ball = Ball(SCREEN_WIDTH // 2 - BALL_SIZE // 2, 
                        SCREEN_HEIGHT // 2 - BALL_SIZE // 2)
        
        # Game state
        self.running = True
        self.paused = False
        self.game_mode = "2player"  # "2player" or "ai"
        self.particles = []
        
        # Visual effects
        self.trail_positions = []
        self.screen_shake = 0
        
        # AI difficulty
        self.ai_difficulty = "medium"  # "easy", "medium", "hard"
        
        # Sounds (using pygame.mixer)
        try:
            self.bounce_sound = pygame.mixer.Sound(self.create_beep_sound(440, 0.1))
            self.score_sound = pygame.mixer.Sound(self.create_beep_sound(880, 0.3))
        except:
            self.bounce_sound = None
            self.score_sound = None
    
    def create_beep_sound(self, frequency, duration):
        """Create a simple beep sound programmatically"""
        sample_rate = 44100
        n_samples = int(sample_rate * duration)
        buf = pygame.sndarray.make_sound(
            (4096 * pygame.sndarray.array(
                [int(32767.0 * math.sin(2 * math.pi * frequency * t / sample_rate)) 
                 for t in range(n_samples)]
            )).astype('int16')
        )
        return buf
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        # Left paddle controls (W/S)
        if keys[pygame.K_w]:
            self.left_paddle.move(-PADDLE_SPEED)
        if keys[pygame.K_s]:
            self.left_paddle.move(PADDLE_SPEED)
        
        # Right paddle controls
        if self.game_mode == "2player":
            if keys[pygame.K_UP]:
                self.right_paddle.move(-PADDLE_SPEED)
            if keys[pygame.K_DOWN]:
                self.right_paddle.move(PADDLE_SPEED)
    
    def ai_move(self):
        """AI-controlled right paddle"""
        if self.game_mode == "ai":
            ball_center = self.ball.rect.centery
            paddle_center = self.right_paddle.rect.centery
            error_margin = 0
            
            # Difficulty-based error margin and speed
            if self.ai_difficulty == "easy":
                error_margin = 60
                speed = AI_SPEED * 0.7
            elif self.ai_difficulty == "medium":
                error_margin = 30
                speed = AI_SPEED
            else:  # hard
                error_margin = 10
                speed = AI_SPEED * 1.2
            
            # Predict where ball will be (simple prediction)
            if abs(self.ball.speed_x) > 0:
                time_to_reach = (self.right_paddle.rect.x - self.ball.rect.x) / abs(self.ball.speed_x)
                predicted_y = self.ball.rect.centery + self.ball.speed_y * time_to_reach
                
                # Add some randomness for difficulty
                if self.ai_difficulty == "easy":
                    predicted_y += random.uniform(-error_margin, error_margin)
                elif self.ai_difficulty == "medium":
                    predicted_y += random.uniform(-error_margin/2, error_margin/2)
                
                # Keep within bounds
                predicted_y = max(0, min(SCREEN_HEIGHT, predicted_y))
            else:
                predicted_y = ball_center
            
            # Move paddle toward predicted position
            if paddle_center < predicted_y - error_margin:
                self.right_paddle.move(speed)
            elif paddle_center > predicted_y + error_margin:
                self.right_paddle.move(-speed)
    
    def update_ball(self):
        self.ball.move()
        
        # Add trail effect
        self.trail_positions.append((self.ball.rect.centerx, self.ball.rect.centery))
        if len(self.trail_positions) > 10:
            self.trail_positions.pop(0)
        
        # Wall collision (top/bottom)
        if self.ball.rect.top <= 0 or self.ball.rect.bottom >= SCREEN_HEIGHT:
            self.ball.speed_y *= -1
            self.add_particles(self.ball.rect.centerx, self.ball.rect.centery)
            if self.bounce_sound:
                self.bounce_sound.play()
        
        # Paddle collisions
        if self.ball.rect.colliderect(self.left_paddle.rect):
            self.handle_paddle_collision(self.left_paddle)
        elif self.ball.rect.colliderect(self.right_paddle.rect):
            self.handle_paddle_collision(self.right_paddle)
        
        # Score detection
        if self.ball.rect.left <= 0:
            self.score_point("right")
        elif self.ball.rect.right >= SCREEN_WIDTH:
            self.score_point("left")
    
    def handle_paddle_collision(self, paddle):
        # Calculate where ball hit the paddle (offset from center)
        paddle_center = paddle.rect.centery
        ball_center = self.ball.rect.centery
        offset = (ball_center - paddle_center) / (PADDLE_HEIGHT / 2)
        
        # Change angle based on where it hit (-1 to 1)
        angle = offset * 0.8  # Max 45 degree angle change
        
        # Reverse X direction and adjust Y based on angle
        self.ball.speed_x *= -1
        self.ball.speed_y += angle * 4
        
        # Increase speed slightly on each hit
        self.ball.increase_speed(1.02)
        
        # Add particles
        self.add_particles(self.ball.rect.centerx, self.ball.rect.centery)
        
        # Small screen shake
        self.screen_shake = 3
        
        if self.bounce_sound:
            self.bounce_sound.play()
        
        # Ensure ball doesn't get stuck
        if abs(self.ball.speed_y) < 2:
            self.ball.speed_y = 2 if self.ball.speed_y > 0 else -2
    
    def score_point(self, scorer):
        if scorer == "left":
            self.left_paddle.score += 1
        else:
            self.right_paddle.score += 1
        
        if self.score_sound:
            self.score_sound.play()
        
        # Reset ball and paddles after scoring
        self.ball.reset()
        self.left_paddle.reset_position()
        self.right_paddle.reset_position()
        
        # Add celebration particles
        for _ in range(50):
            self.add_particles(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        
        # Check for win condition (first to 7)
        if self.left_paddle.score >= 7 or self.right_paddle.score >= 7:
            self.game_over()
    
    def game_over(self):
        winner = "Left Player (Blue)" if self.left_paddle.score >= 7 else "Right Player (Red)"
        if self.game_mode == "ai" and self.right_paddle.score >= 7:
            winner = "AI (Red)"
        
        # Create game over text
        text = self.font_large.render("GAME OVER", True, YELLOW)
        winner_text = self.font_medium.render(f"{winner} Wins!", True, WHITE)
        
        # Display final score
        self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 
                                SCREEN_HEIGHT // 2 - 60))
        self.screen.blit(winner_text, (SCREEN_WIDTH // 2 - winner_text.get_width() // 2, 
                                       SCREEN_HEIGHT // 2))
        
        # Show score
        score_text = self.font_medium.render(
            f"Final Score: {self.left_paddle.score} - {self.right_paddle.score}", 
            True, GREEN)
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 
                                     SCREEN_HEIGHT // 2 + 40))
        
        pygame.display.flip()
        pygame.time.wait(3000)
        
        # Reset game
        self.left_paddle.score = 0
        self.right_paddle.score = 0
        self.ball.reset()
        self.left_paddle.reset_position()
        self.right_paddle.reset_position()
    
    def add_particles(self, x, y):
        for _ in range(15):
            self.particles.append(Particle(x, y))
    
    def update_particles(self):
        self.particles = [p for p in self.particles if p.lifetime > 0]
        for particle in self.particles:
            particle.update()
    
    def draw_trail(self):
        for i, (x, y) in enumerate(self.trail_positions):
            alpha = i / len(self.trail_positions)
            size = int(5 * alpha)
            if size > 0:
                pygame.draw.circle(self.screen, (100, 100, 255), (int(x), int(y)), size)
    
    def draw_ui(self):
        # Draw scores
        left_score = self.font_large.render(str(self.left_paddle.score), True, BLUE)
        right_score = self.font_large.render(str(self.right_paddle.score), True, RED)
        
        self.screen.blit(left_score, (SCREEN_WIDTH // 4 - left_score.get_width() // 2, 20))
        self.screen.blit(right_score, (3 * SCREEN_WIDTH // 4 - right_score.get_width() // 2, 20))
        
        # Draw mode indicator
        if self.game_mode == "ai":
            mode_text = self.font_small.render(f"VS AI ({self.ai_difficulty.upper()})", True, YELLOW)
        else:
            mode_text = self.font_small.render("2-PLAYER MODE", True, YELLOW)
        self.screen.blit(mode_text, (SCREEN_WIDTH // 2 - mode_text.get_width() // 2, 80))
        
        # Draw center line
        for y in range(0, SCREEN_HEIGHT, 30):
            pygame.draw.rect(self.screen, GRAY, 
                           (SCREEN_WIDTH // 2 - 5, y, 10, 15))
        
        # Draw instructions
        if self.game_mode == "2player":
            left_inst = self.font_small.render("Left: W/S", True, BLUE)
            right_inst = self.font_small.render("Right: ↑/↓", True, RED)
            self.screen.blit(left_inst, (50, SCREEN_HEIGHT - 40))
            self.screen.blit(right_inst, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 40))
        else:
            left_inst = self.font_small.render("You: W/S", True, BLUE)
            ai_inst = self.font_small.render("AI: Computer", True, RED)
            self.screen.blit(left_inst, (50, SCREEN_HEIGHT - 40))
            self.screen.blit(ai_inst, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 40))
        
        # Pause indicator
        if self.paused:
            pause_text = self.font_medium.render("PAUSED - Press P to Resume", True, YELLOW)
            self.screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2,
                                         SCREEN_HEIGHT // 2))
    
    def draw(self):
        # Apply screen shake
        shake_x = random.randint(-self.screen_shake, self.screen_shake) if self.screen_shake > 0 else 0
        shake_y = random.randint(-self.screen_shake, self.screen_shake) if self.screen_shake > 0 else 0
        self.screen_shake = max(0, self.screen_shake - 1)
        
        # Clear screen with gradient effect
        self.screen.fill(BLACK)
        
        # Draw stars in background
        for _ in range(100):
            pygame.draw.circle(self.screen, DARK_GRAY, 
                             (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)), 1)
        
        # Draw game objects with offset for shake
        self.left_paddle.draw(self.screen)
        self.right_paddle.draw(self.screen)
        self.draw_trail()
        self.ball.draw(self.screen)
        
        # Draw particles
        for particle in self.particles:
            particle.draw(self.screen)
        
        self.draw_ui()
        
        # Apply shake by shifting the entire display
        if shake_x != 0 or shake_y != 0:
            temp_surface = self.screen.copy()
            self.screen.fill(BLACK)
            self.screen.blit(temp_surface, (shake_x, shake_y))
        
        pygame.display.flip()
    
    def run(self):
        # Game mode selection menu
        self.show_menu()
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_p:
                        self.paused = not self.paused
                    elif event.key == pygame.K_1:
                        self.game_mode = "2player"
                    elif event.key == pygame.K_2:
                        self.game_mode = "ai"
                    elif event.key == pygame.K_3:
                        self.ai_difficulty = "easy"
                    elif event.key == pygame.K_4:
                        self.ai_difficulty = "medium"
                    elif event.key == pygame.K_5:
                        self.ai_difficulty = "hard"
                    elif event.key == pygame.K_r:
                        self.left_paddle.score = 0
                        self.right_paddle.score = 0
                        self.ball.reset()
            
            if not self.paused:
                self.handle_input()
                self.ai_move()
                self.update_ball()
                self.update_particles()
                self.draw()
            
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()
    
    def show_menu(self):
        menu = True
        while menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.game_mode = "2player"
                        menu = False
                    elif event.key == pygame.K_2:
                        self.game_mode = "ai"
                        menu = False
                    elif event.key == pygame.K_3:
                        self.game_mode = "ai"
                        self.ai_difficulty = "easy"
                        menu = False
                    elif event.key == pygame.K_4:
                        self.game_mode = "ai"
                        self.ai_difficulty = "medium"
                        menu = False
                    elif event.key == pygame.K_5:
                        self.game_mode = "ai"
                        self.ai_difficulty = "hard"
                        menu = False
            
            self.screen.fill(BLACK)
            
            # Draw title
            title = self.font_large.render("PONG", True, YELLOW)
            self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
            
            # Draw options
            options = [
                "Press 1: 2-Player Mode",
                "Press 2: VS AI (Medium)",
                "Press 3: VS AI (Easy)",
                "Press 4: VS AI (Medium)",
                "Press 5: VS AI (Hard)"
            ]
            
            y = 250
            for option in options:
                text = self.font_medium.render(option, True, WHITE)
                self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y))
                y += 50
            
            # Draw controls preview
            controls_text = self.font_small.render("Controls: W/S (Left) | ↑/↓ (Right) | P (Pause) | ESC (Quit)", 
                                                   True, GRAY)
            self.screen.blit(controls_text, (SCREEN_WIDTH // 2 - controls_text.get_width() // 2, 
                                            SCREEN_HEIGHT - 50))
            
            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = PongGame()
    game.run()