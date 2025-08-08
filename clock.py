import tkinter as tk
import math
import time

class StopwatchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stopwatch with Rotating Hands")

        # Initialize time variables
        self.running = False
        self.start_time = None
        self.elapsed_time = 0

        # Create canvas for clock
        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()

        # Create the clock face
        self.canvas.create_oval(50, 50, 350, 350)

        # Add numbers to the clock
        self.add_numbers()

        # Create clock hands
        self.second_hand = self.canvas.create_line(200, 200, 200, 100, width=2, fill="red")
        self.minute_hand = self.canvas.create_line(200, 200, 200, 60, width=4, fill="blue")
        self.hour_hand = self.canvas.create_line(200, 200, 200, 40, width=6, fill="green")

        # Create the timer label
        self.timer_label = tk.Label(self.root, text="00:00", font=("Arial", 20))
        self.timer_label.pack(pady=20)

        # Create buttons
        self.start_button = tk.Button(self.root, text="Start", command=self.start)
        self.start_button.pack(side=tk.LEFT, padx=20)

        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop)
        self.stop_button.pack(side=tk.LEFT, padx=20)

        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset)
        self.reset_button.pack(side=tk.LEFT, padx=20)

        # Update the clock hands initially
        self.update_clock()

    def rotate_point(self, x, y, cx, cy, angle):
        """Rotate a point (x, y) around (cx, cy) by the given angle in radians."""
        new_x = cx + (x - cx) * math.cos(angle) - (y - cy) * math.sin(angle)
        new_y = cy + (x - cx) * math.sin(angle) + (y - cy) * math.cos(angle)
        return new_x, new_y

    def flip_x(self, x, cx):
        """Flip a point along the Y-axis by negating its x-coordinate."""
        return 2 * cx - x

    def add_numbers(self):
        # Add numbers (1-12) to the clock face with correct orientation (12 at the bottom)
        for i in range(1, 13):
            angle = math.radians(i * 30)  # 30 degrees between each hour
            x = 200 + 120 * math.cos(angle)
            y = 200 - 120 * math.sin(angle)
            # Rotate the number by 90 degrees anticlockwise
            x, y = self.rotate_point(x, y, 200, 200, math.radians(-90))  # Apply -90 degree anticlockwise rotation
            # Flip the number along the Y-axis
            x = self.flip_x(x, 200)  # Flip by the center of the clock (200, 200)
            self.canvas.create_text(x, y, text=str(i), font=("Arial", 14, "bold"))

    def start(self):
        if not self.running:
            self.running = True
            self.start_time = time.time() - self.elapsed_time
            self.update_clock()
        
    def stop(self):
        if self.running:
            self.running = False
            self.elapsed_time = time.time() - self.start_time
        
    def reset(self):
        self.running = False
        self.elapsed_time = 0
        self.start_time = None
        self.update_clock()

    def update_clock(self):
        if self.running:
            elapsed = time.time() - self.start_time
        else:
            elapsed = self.elapsed_time
        
        # Convert time into hours, minutes, seconds
        hours = (elapsed // 3600) % 12
        minutes = (elapsed // 60) % 60
        seconds = elapsed % 60

        # Update the timer label
        formatted_time = f"{int(minutes):02}:{int(seconds):02}"
        self.timer_label.config(text=formatted_time)

        # Rotate the second hand (clockwise rotation)
        self.rotate_hand(self.second_hand, seconds, 360)
        
        # Rotate the minute hand (clockwise rotation)
        self.rotate_hand(self.minute_hand, minutes + seconds / 60, 360 / 60)
        
        # Rotate the hour hand (clockwise rotation)
        self.rotate_hand(self.hour_hand, hours + minutes / 60, 360 / 12)

        # Update every 100ms
        self.root.after(100, self.update_clock)

    def rotate_hand(self, hand, time_unit, max_rotation):
        # Calculate the rotation angle (clockwise)
        angle = (time_unit / 60) * max_rotation
        radians = math.radians(angle)  # Use positive angle for clockwise rotation

        # Update the hand position using trigonometry
        x_end = 200 + 100 * math.cos(radians)
        y_end = 200 - 100 * math.sin(radians)

        # Rotate the hand by 90 degrees anticlockwise
        x_end, y_end = self.rotate_point(x_end, y_end, 200, 200, math.radians(-90))  # Apply -90 degree anticlockwise rotation

        # Flip the hand along the Y-axis
        x_end = self.flip_x(x_end, 200)  # Flip by the center of the clock (200, 200)
        
        self.canvas.coords(hand, 200, 200, x_end, y_end)


if __name__ == "__main__":
    root = tk.Tk()
    app = StopwatchApp(root)
    root.mainloop()
