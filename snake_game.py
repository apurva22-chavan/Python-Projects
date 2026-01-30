import tkinter as tk
from tkinter import messagebox
import random
from collections import deque
from enum import Enum

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Professional Snake Game")
        self.root.configure(bg='black')
        self.root.resizable(False, False)
        
        # Game settings
        self.GRID_SIZE = 20
        self.WIDTH = 40
        self.HEIGHT = 30
        self.CANVAS_WIDTH = self.WIDTH * self.GRID_SIZE
        self.CANVAS_HEIGHT = self.HEIGHT * self.GRID_SIZE
        self.SPEED = 100
        
        # Create main frame
        self.main_frame = tk.Frame(root, bg='black')
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Info frame
        self.info_frame = tk.Frame(self.main_frame, bg='black')
        self.info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.score_label = tk.Label(self.info_frame, text="Score: 0", font=("Arial", 16, "bold"), fg="white", bg="black")
        self.score_label.pack(side=tk.LEFT, padx=10)
        
        self.high_score_label = tk.Label(self.info_frame, text="High Score: 0", font=("Arial", 16, "bold"), fg="yellow", bg="black")
        self.high_score_label.pack(side=tk.LEFT, padx=10)
        
        self.status_label = tk.Label(self.info_frame, text="Use Arrow Keys | Space: Pause | R: Restart | Q: Quit", 
                                     font=("Arial", 12), fg="cyan", bg="black")
        self.status_label.pack(side=tk.RIGHT, padx=10)
        
        # Canvas for game
        self.canvas = tk.Canvas(self.main_frame, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT,
                               bg='black', highlightthickness=2, highlightbackground='green')
        self.canvas.pack(padx=10, pady=10)
        
        # Instructions frame
        self.instruction_frame = tk.Frame(self.main_frame, bg='black')
        self.instruction_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.instruction_label = tk.Label(self.instruction_frame, 
                                         text="Eat red food to grow | Avoid walls and yourself | Each food = +10 points",
                                         font=("Arial", 11), fg="lime", bg="black")
        self.instruction_label.pack()
        
        # Game variables
        self.reset_game()
        self.high_score = 0
        self.paused = False
        self.game_over = False
        
        # Bind keys
        self.root.bind('<Up>', lambda e: self.change_direction(Direction.UP))
        self.root.bind('<Down>', lambda e: self.change_direction(Direction.DOWN))
        self.root.bind('<Left>', lambda e: self.change_direction(Direction.LEFT))
        self.root.bind('<Right>', lambda e: self.change_direction(Direction.RIGHT))
        self.root.bind('<space>', self.toggle_pause)
        self.root.bind('r', self.restart_game)
        self.root.bind('q', self.quit_game)
        self.root.bind('R', self.restart_game)
        self.root.bind('Q', self.quit_game)
        
        self.canvas.focus()
        self.draw_menu()
        
    def reset_game(self):
        """Reset game state"""
        start_x = self.WIDTH // 2
        start_y = self.HEIGHT // 2
        self.snake = deque([(start_x, start_y),
                           (start_x - 1, start_y),
                           (start_x - 2, start_y)])
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False
        self.paused = False
        self.game_started = False
        
    def spawn_food(self):
        """Spawn food at random position"""
        while True:
            x = random.randint(0, self.WIDTH - 1)
            y = random.randint(0, self.HEIGHT - 1)
            if (x, y) not in self.snake:
                return (x, y)
    
    def change_direction(self, new_direction):
        """Change snake direction"""
        if not self.game_started or self.paused or self.game_over:
            if not self.game_started and not self.game_over:
                self.game_started = True
                self.draw_game()
                self.game_loop()
            return
        
        # Prevent 180 degree turns
        if (new_direction == Direction.UP and self.direction != Direction.DOWN) or \
           (new_direction == Direction.DOWN and self.direction != Direction.UP) or \
           (new_direction == Direction.LEFT and self.direction != Direction.RIGHT) or \
           (new_direction == Direction.RIGHT and self.direction != Direction.LEFT):
            self.next_direction = new_direction
    
    def toggle_pause(self, event=None):
        """Toggle pause state"""
        if self.game_started and not self.game_over:
            self.paused = not self.paused
            if self.paused:
                self.status_label.config(text="⏸ PAUSED - Press Space to Resume", fg="red")
            else:
                self.status_label.config(text="Use Arrow Keys | Space: Pause | R: Restart | Q: Quit", fg="cyan")
                self.game_loop()
    
    def restart_game(self, event=None):
        """Restart the game"""
        self.reset_game()
        self.status_label.config(text="Use Arrow Keys | Space: Pause | R: Restart | Q: Quit", fg="cyan")
        self.draw_game()
    
    def quit_game(self, event=None):
        """Quit the game"""
        if messagebox.askokcancel("Quit", f"Final Score: {self.score}\nHigh Score: {self.high_score}\n\nQuit Snake Game?"):
            self.root.quit()
    
    def update_game(self):
        """Update game state"""
        self.direction = self.next_direction
        
        # Calculate new head
        head_x, head_y = self.snake[0]
        dx, dy = self.direction.value
        new_head = (head_x + dx, head_y + dy)
        
        # Wall collision
        if new_head[0] < 0 or new_head[0] >= self.WIDTH or \
           new_head[1] < 0 or new_head[1] >= self.HEIGHT:
            self.end_game("Hit the wall!")
            return
        
        # Self collision
        if new_head in self.snake:
            self.end_game("Hit yourself!")
            return
        
        # Add head
        self.snake.appendleft(new_head)
        
        # Food collision
        if new_head == self.food:
            self.score += 10
            self.food = self.spawn_food()
        else:
            self.snake.pop()
    
    def end_game(self, reason):
        """End the game"""
        self.game_over = True
        if self.score > self.high_score:
            self.high_score = self.score
        
        self.draw_game()
        messagebox.showinfo("Game Over!", 
                           f"Reason: {reason}\n\n"
                           f"Score: {self.score}\n"
                           f"High Score: {self.high_score}\n\n"
                           f"Press R to restart or Q to quit")
    
    def draw_menu(self):
        """Draw menu screen"""
        self.canvas.delete("all")
        
        # Draw menu text
        self.canvas.create_text(self.CANVAS_WIDTH // 2, 100,
                              text="SNAKE GAME", font=("Arial", 48, "bold"),
                              fill="lime", tags="menu")
        
        self.canvas.create_text(self.CANVAS_WIDTH // 2, 200,
                              text="Controls:", font=("Arial", 24, "bold"),
                              fill="cyan", tags="menu")
        
        instructions = [
            "↑ ↓ ← → : Move Snake",
            "SPACE : Pause/Resume",
            "R : Restart Game",
            "Q : Quit Game",
            "",
            "Press ANY ARROW KEY to Start!"
        ]
        
        y = 250
        for instruction in instructions:
            color = "yellow" if "Press" in instruction else "white"
            self.canvas.create_text(self.CANVAS_WIDTH // 2, y,
                                   text=instruction, font=("Arial", 16),
                                   fill=color, tags="menu")
            y += 40
    
    def draw_game(self):
        """Draw game screen"""
        self.canvas.delete("all")
        
        # Draw grid
        for x in range(0, self.CANVAS_WIDTH, self.GRID_SIZE):
            self.canvas.create_line(x, 0, x, self.CANVAS_HEIGHT, fill="darkgray", width=1)
        for y in range(0, self.CANVAS_HEIGHT, self.GRID_SIZE):
            self.canvas.create_line(0, y, self.CANVAS_WIDTH, y, fill="darkgray", width=1)
        
        # Draw snake
        for i, (x, y) in enumerate(self.snake):
            rect_x = x * self.GRID_SIZE
            rect_y = y * self.GRID_SIZE
            
            if i == 0:  # Head
                self.canvas.create_rectangle(rect_x + 1, rect_y + 1,
                                            rect_x + self.GRID_SIZE - 1,
                                            rect_y + self.GRID_SIZE - 1,
                                            fill="white", outline="yellow", width=2)
            else:  # Body
                self.canvas.create_rectangle(rect_x + 1, rect_y + 1,
                                            rect_x + self.GRID_SIZE - 1,
                                            rect_y + self.GRID_SIZE - 1,
                                            fill="lime", outline="green", width=1)
        
        # Draw food
        food_x, food_y = self.food
        rect_x = food_x * self.GRID_SIZE
        rect_y = food_y * self.GRID_SIZE
        self.canvas.create_rectangle(rect_x + 2, rect_y + 2,
                                    rect_x + self.GRID_SIZE - 2,
                                    rect_y + self.GRID_SIZE - 2,
                                    fill="red", outline="darkred", width=1)
        
        # Update score labels
        self.score_label.config(text=f"Score: {self.score}")
        self.high_score_label.config(text=f"High Score: {self.high_score}")
        
        if self.paused:
            self.canvas.create_text(self.CANVAS_WIDTH // 2, self.CANVAS_HEIGHT // 2,
                                   text="PAUSED", font=("Arial", 48, "bold"),
                                   fill="red")
    
    def game_loop(self):
        """Main game loop"""
        if not self.game_over and not self.paused:
            self.update_game()
            self.draw_game()
            self.root.after(self.SPEED, self.game_loop)
        elif not self.game_over:
            self.root.after(100, self.game_loop)

def main():
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()

