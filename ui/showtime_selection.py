import tkinter as tk
from tkinter import ttk

class ShowtimeSelectionWindow(tk.Toplevel):
    def __init__(self, movie_name):
        super().__init__()
        self.title("Select Your Showtime")
        self.geometry("400x300")

        label = tk.Label(self, text=f"Select a Showtime for {movie_name}:", font=("Arial", 16))
        label.pack(pady=20)

        # LIST OF AVAILABLE SHOWTIMES (placeholder titles for now)
        self.showtimes = ["12:00 PM", "3:00 PM", "6:00 PM", "9:00 PM"]

        self.showtime_var = tk.StringVar()
        self.dropdown = ttk.Combobox(self, textvariable=self.showtime_var, values=self.showtimes)
        self.dropdown.pack(pady=10)

        next_btn = tk.Button(self, text="Next", command=self.go_next)
        next_btn.pack(pady=20)
    
    def go_next(self):
        print(f"You have now selected the {self.showtime_var.get()} for {self.movie_name}")

if __name__ == "__main__":
    app = ShowtimeSelectionWindow("Movie A")
    app.mainloop()