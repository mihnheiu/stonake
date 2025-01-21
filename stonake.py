import tkinter as tk
from tkinter import ttk
import time
import random

# Stopwatch class
class StopwatchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("stonake")
        self.root.geometry("900x600")
        self.root.configure(bg="#2E3B55")

        # Stopwatch setup
        self.running = False
        self.start_time = 0
        self.elapsed_time = 0
        self.lap_times = []

        self.stopwatch_frame = ttk.Frame(self.root, width=400, height=600, style="TFrame")
        self.stopwatch_frame.pack(side="left", fill="both", expand=True)

        # Stopwatch UI
        self.title_label = ttk.Label(self.stopwatch_frame, text="Stopwatch", font=("Arial", 24, "bold"), foreground="white", background="#2E3B55")
        self.title_label.pack(pady=20)

        self.time_label = ttk.Label(self.stopwatch_frame, text="00:00:00:00", font=("Arial", 40), foreground="white", background="#2E3B55")
        self.time_label.pack(pady=20)

        self.start_button = ttk.Button(self.stopwatch_frame, text="Start", command=self.start_stopwatch, width=12)
        self.start_button.pack(side="left", padx=20, pady=10)

        self.reset_button = ttk.Button(self.stopwatch_frame, text="Reset", command=self.reset_stopwatch, width=12)
        self.reset_button.pack(side="right", padx=20, pady=10)

        self.lap_button = ttk.Button(self.stopwatch_frame, text="Lap", command=self.record_lap, width=12)
        self.lap_button.pack(side="bottom", padx=20, pady=10)

        self.lap_frame = ttk.Frame(self.stopwatch_frame)
        self.lap_frame.pack(fill="both", expand=True)

        self.update_time()

        # Snake setup
        self.snake_game_frame = ttk.Frame(self.root, width=480, height=600, style="TFrame")
        self.snake_game_frame.pack(side="right", fill="both", expand=True)

        self.canvas = tk.Canvas(self.snake_game_frame, width=600, height=400, bg="white")
        self.canvas.pack()

        self.snake = [(20, 20), (15, 20), (10, 20)]
        self.food = None
        self.direction = 'Right'
        self.game_running = True
        self.snake_speed = 50  # Default speed value in range 1-10, 5 in the middle
        self.create_food()
        self.update_snake()

        self.root.bind("<KeyPress>", self.change_direction)
        self.run_game()

        # Play Again button
        self.play_again_button = ttk.Button(self.snake_game_frame, text="Play Again", command=self.play_again)
        self.play_again_button.pack(side="bottom", pady=10)
        self.play_again_button.place_forget()

        # Game Over Text
        self.game_over_text = self.canvas.create_text(290, 200, text="Game Over", font=("Arial", 24), fill="black")
        self.canvas.itemconfig(self.game_over_text, state="hidden")

        # Speed Control Buttons (Updated to 0 and 1)
        self.speed_up_button = ttk.Button(self.snake_game_frame, text="Speed Up", command=self.speed_up)
        self.speed_up_button.pack(side="left", padx=10, pady=10)

        self.speed_down_button = ttk.Button(self.snake_game_frame, text="Speed Down", command=self.speed_down)
        self.speed_down_button.pack(side="left", padx=10, pady=10)

        self.reset_speed_button = ttk.Button(self.snake_game_frame, text="Reset Speed", command=self.reset_speed)
        self.reset_speed_button.pack(side="left", padx=10, pady=10)

        self.speed_label = ttk.Label(self.snake_game_frame, text=f"Current Speed: {self.snake_speed // 10}", font=("Arial", 12), foreground="black", background="white")
        self.speed_label.pack(side="bottom", pady=10)

        # Instruction text for hotkeys
        self.instructions_label = ttk.Label(self.snake_game_frame, text="Hotkeys:\n0 Decrease Speed\n1 Increase Speed\nEnter Play Again\nSpace Start/Stop\nR Reset\nL Lap", font=("Arial", 12), foreground="black", background="white")
        self.instructions_label.pack(side="right", padx=10, pady=10)

        # Scrollbar for laps
        self.lap_canvas = tk.Canvas(self.stopwatch_frame)
        self.lap_scrollbar = ttk.Scrollbar(self.stopwatch_frame, orient="vertical", command=self.lap_canvas.yview)
        self.lap_canvas.config(yscrollcommand=self.lap_scrollbar.set)

        self.lap_frame_scrollable = ttk.Frame(self.lap_canvas)
        self.lap_canvas.create_window((0, 0), window=self.lap_frame_scrollable, anchor="nw")
        self.lap_scrollbar.pack(side="right", fill="y")
        self.lap_canvas.pack(side="left", fill="both", expand=True)

        self.lap_frame_scrollable.bind(
            "<Configure>",
            lambda e: self.lap_canvas.configure(scrollregion=self.lap_canvas.bbox("all"))
        )

    # Stopwatch functions
    def update_time(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
            minutes, seconds = divmod(int(self.elapsed_time), 60)
            hours, minutes = divmod(minutes, 60)
            milliseconds = int((self.elapsed_time - int(self.elapsed_time)) * 100)
            time_str = f"{hours:02}:{minutes:02}:{seconds:02}:{milliseconds:02}"
            self.time_label.config(text=time_str)
        
        self.root.after(10, self.update_time)

    def start_stopwatch(self):
        if self.running:
            self.running = False
            self.start_button.config(text="Start")
        else:
            self.running = True
            self.start_time = time.time() - self.elapsed_time
            self.start_button.config(text="Stop")

    def reset_stopwatch(self):
        self.running = False
        self.elapsed_time = 0
        self.lap_times = []
        self.time_label.config(text="00:00:00:00")
        self.start_button.config(text="Start")
        self.clear_laps()

    def record_lap(self):
        if self.running:
            lap_time = self.elapsed_time
            minutes, seconds = divmod(int(lap_time), 60)
            hours, minutes = divmod(minutes, 60)
            milliseconds = int((lap_time - int(lap_time)) * 100)
            lap_str = f"Lap {len(self.lap_times) + 1} - {hours:02}:{minutes:02}:{seconds:02}:{milliseconds:02}"
            self.lap_times.insert(0, {"time": lap_str})  # Insert lap at the top

            self.update_lap_display()

    def update_lap_display(self):
        self.clear_laps()
        for lap in self.lap_times:
            lap_text = f"{lap['time']}"
            lap_label = ttk.Label(self.lap_frame_scrollable, text=lap_text, font=("Arial", 12), foreground="white", background="#2E3B55")
            lap_label.pack(anchor="w")

    def clear_laps(self):
        for widget in self.lap_frame_scrollable.winfo_children():
            widget.destroy()

    # Snake game functions
    def run_game(self):
        if self.game_running:
            self.move_snake()
            self.check_collision()
            self.check_food_collision()
            self.canvas.after(self.snake_speed, self.run_game)

    def create_food(self):
        self.food = (random.randint(1, 59) * 10, random.randint(1, 39) * 10)
        self.canvas.create_rectangle(self.food[0], self.food[1], self.food[0] + 10, self.food[1] + 10, fill="red", outline="black", tags="food")

    def update_snake(self):
        self.canvas.delete("snake")
        for segment in self.snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + 10, segment[1] + 10, fill="green", outline="black", tags="snake")

    def move_snake(self):
        head_x, head_y = self.snake[0]
        if self.direction == "Up":
            head_y -= 10
        elif self.direction == "Down":
            head_y += 10
        elif self.direction == "Left":
            head_x -= 10
        elif self.direction == "Right":
            head_x += 10

        new_head = (head_x, head_y)
        self.snake = [new_head] + self.snake[:-1]
        self.update_snake()

    def change_direction(self, event):
        if event.keysym == 'Up' and self.direction != 'Down':
            self.direction = 'Up'
        elif event.keysym == 'Down' and self.direction != 'Up':
            self.direction = 'Down'
        elif event.keysym == 'Left' and self.direction != 'Right':
            self.direction = 'Left'
        elif event.keysym == 'Right' and self.direction != 'Left':
            self.direction = 'Right'
        elif event.keysym == '0':  # Speed down (0)
            self.speed_down()
        elif event.keysym == '1':  # Speed up (1)
            self.speed_up()
        elif event.keysym == 'Return':  # Enter key
            self.play_again()
        elif event.keysym == 'space':  # Space key to start/stop stopwatch
            self.start_stopwatch()
        elif event.keysym == 'r':  # Reset stopwatch
            self.reset_stopwatch()
        elif event.keysym == 'l':  # Lap key
            self.record_lap()

    def check_collision(self):
        head_x, head_y = self.snake[0]
        if (head_x, head_y) in self.snake[1:]:
            if self.game_running:
                self.game_over()

        if head_x < 0 or head_x >= 600 or head_y < 0 or head_y >= 400:
            if self.game_running:
                self.game_over()

    def check_food_collision(self):
        head_x, head_y = self.snake[0]
        if (head_x, head_y) == self.food:
            self.snake.append(self.snake[-1])
            self.canvas.delete("food")
            self.create_food()

    def game_over(self):
        self.game_running = False
        self.canvas.itemconfig(self.game_over_text, state="normal")
        self.play_again_button.place(relx=0.5, rely=0.9, anchor="center")

    def play_again(self):
        self.snake = [(20, 20), (15, 20), (10, 20)]
        self.food = None
        self.direction = 'Right'
        self.game_running = True
        self.snake_speed = 50  # Speed back to the default 5
        self.canvas.delete("food")
        self.create_food()
        self.update_snake()
        self.canvas.itemconfig(self.game_over_text, state="hidden")
        self.play_again_button.place_forget()
        self.run_game()

    def speed_up(self):
        if self.snake_speed > 10:
            self.snake_speed -= 10
            self.update_speed_label()

    def speed_down(self):
        if self.snake_speed < 100:
            self.snake_speed += 10
            self.update_speed_label()

    def reset_speed(self):
        self.snake_speed = 50
        self.update_speed_label()

    def update_speed_label(self):
        self.speed_label.config(text=f"Current Speed: {self.snake_speed // 10}")

# Khởi tạo giao diện
root = tk.Tk()
app = StopwatchApp(root)
root.mainloop()
