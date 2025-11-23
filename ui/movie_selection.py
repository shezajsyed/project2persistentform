import tkinter as tk
from tkinter import ttk
from showtime_selection import ShowtimeSelectionWindow

class MovieSelectionWindow(tk.Tk):
    def __init__(self, screenName = None, baseName = None, className = "Tk", useTk = True, sync = False, use = None):
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.title("Select Your Movie")
        self.geometry("400x300")

        label = tk.Label(self, text="Select Your Movie: ", font=("Arial", 16))
        label.pack(pady=20)

        # MOVIE LIST (placeholder titles for now)
        self.movies = ["Movie A", "Movie B", "Movie C", "Movie D", "Movie E"]

        self.movie_var = tk.StringVar()
        self.dropdown = ttk.Combobox(self, textvariable=self.movie_var, values=self.movies)
        self.dropdown.pack(pady=10)

        next_btn = tk.Button(self, text="Next", command=self.go_next)
        next_btn.pack(pady=20)
    
    def go_next(self):
        selected_movie = self.movie_var.get()
        if selected_movie:
            showtime_window = ShowtimeSelectionWindow(selected_movie)
            print("Your Current Movie Selection: ", self.movie_var.get())
        else:
            print("Please select a movie first!")

if __name__ == "__main__":
    app = MovieSelectionWindow()
    app.mainloop()