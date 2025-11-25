import tkinter as tk
from tkinter import ttk
from movie_selection import MovieSelectionWindow
from showtime_selection import ShowtimeSelectionWindow

#Movie Selection 
class MovieSelectionWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Select Your Movie")
        self.geometry("400x300")

        tk.Label(self, text="Select Your Movie", font=("Helvetica", 16, "bold")).pack(pady=20)
        self.configure(bg="#FFC0CB")  # Light pink background

        self.movies = ["How To Lose A Guy in 10 Days", "The Notebook", "27 Dresses", "The Princess Bride"]
        self.movie_var = tk.StringVar()

        self.dropdown = ttk.Combobox(self, textvariable=self.movie_var, values=self.movies, state="readonly")
        self.dropdown.pack(pady=10)
        self.dropdown.current(0)

        tk.Button(self, text="Next", command=self.go_next).pack(pady=20)

    def go_next(self):
        movie = self.movie_var.get()
        if movie:
            self.withdraw()  # Hide current window
            ShowtimeSelectionWindow(movie, self)
        else:
            messagebox.showwarning("No Selection", "Please select a movie first!")


# Showtime Choice
class ShowtimeSelectionWindow(tk.Toplevel):
    def __init__(self, movie, parent):
        super().__init__(parent)
        self.title("Select Showtime")
        self.geometry("400x300")
        self.movie = movie
        self.parent = parent

        tk.Label(self, text=f"Movie: {self.movie}", font=("Helvetica", 14)).pack(pady=10)
        tk.Label(self, text="Select Showtime", font=("Helvetica", 16, "bold")).pack(pady=10)

        self.showtimes = ["12:00 PM", "3:00 PM", "6:00 PM", "9:00 PM"]
        self.showtime_var = tk.StringVar()

        self.dropdown = ttk.Combobox(self, textvariable=self.showtime_var, values=self.showtimes, state="readonly")
        self.dropdown.pack(pady=10)
        self.dropdown.current(0)

        tk.Button(self, text="Next", command=self.go_next).pack(pady=20)

    def go_next(self):
        showtime = self.showtime_var.get()
        if showtime:
            self.withdraw()
            TicketSelectionWindow(self.movie, showtime, self.parent)
        else:
            messagebox.showwarning("No Selection", "Please select a showtime!")


# Ticket choice
class TicketSelectionWindow(tk.Toplevel):
    def __init__(self, movie, showtime, root):
        super().__init__(root)
        self.title("Select Number of Tickets")
        self.geometry("400x300")
        self.movie = movie
        self.showtime = showtime
        self.root = root

        tk.Label(self, text=f"Movie: {self.movie}", font=("Helvetica", 14)).pack(pady=5)
        tk.Label(self, text=f"Showtime: {self.showtime}", font=("Helvetica", 14)).pack(pady=5)
        tk.Label(self, text="Select Number of Tickets", font=("Helvetica", 16, "bold")).pack(pady=10)

        self.ticket_var = tk.IntVar(value=1)
        tk.Spinbox(self, from_=1, to=10, textvariable=self.ticket_var, width=5, font=("Helvetica", 12)).pack(pady=10)

        tk.Button(self, text="Next", command=self.go_next).pack(pady=20)

    def go_next(self):
        tickets = self.ticket_var.get()
        if tickets > 0:
            self.withdraw()
            PaymentDetailsWindow(self.movie, self.showtime, tickets, self.root)
        else:
            messagebox.showwarning("Invalid Number", "Please select at least 1 ticket!")


# Payment details
class PaymentDetailsWindow(tk.Toplevel):
    def __init__(self, selected_movie, selected_showtime, ticket_count, root):
        super().__init__(root)
        self.title("Payment Details")
        self.geometry("450x450")
        self.configure(bg="#FFC0CB")  # Light pink

        self.selected_movie = selected_movie
        self.selected_showtime = selected_showtime
        self.ticket_count = ticket_count

        header_font = ("Helvetica", 20, "bold")
        label_font = ("Comic Sans MS", 12, "bold")
        entry_font = ("Helvetica", 12)

        tk.Label(self, text="Payment Details", font=header_font, bg="#FFC0CB").pack(pady=15)

        tk.Label(self, text=f"Movie: {self.selected_movie}", font=label_font, bg="#FFC0CB").pack()
        tk.Label(self, text=f"Showtime: {self.selected_showtime}", font=label_font, bg="#FFC0CB").pack()
        tk.Label(self, text=f"Tickets: {self.ticket_count}", font=label_font, bg="#FFC0CB").pack(pady=10)

        tk.Label(self, text="Name on Card", font=label_font, bg="#FFC0CB").pack(anchor="w", padx=20)
        self.name_entry = tk.Entry(self, font=entry_font)
        self.name_entry.pack(fill="x", padx=20, pady=5)

        tk.Label(self, text="Card Number", font=label_font, bg="#FFC0CB").pack(anchor="w", padx=20)
        self.card_entry = tk.Entry(self, font=entry_font)
        self.card_entry.pack(fill="x", padx=20, pady=5)

        tk.Label(self, text="Expiry Date (MM/YY)", font=label_font, bg="#FFC0CB").pack(anchor="w", padx=20)
        self.expiry_entry = tk.Entry(self, font=entry_font)
        self.expiry_entry.pack(fill="x", padx=20, pady=5)

        tk.Label(self, text="CVV", font=label_font, bg="#FFC0CB").pack(anchor="w", padx=20)
        self.cvv_entry = tk.Entry(self, show="*", font=entry_font)
        self.cvv_entry.pack(fill="x", padx=20, pady=5)

        tk.Label(self, text="Billing ZIP Code", font=label_font, bg="#FFC0CB").pack(anchor="w", padx=20)
        self.zip_entry = tk.Entry(self, font=entry_font)
        self.zip_entry.pack(fill="x", padx=20, pady=5)

        tk.Button(self, text="Pay Now", font=("Helvetica", 14, "bold"), command=self.process_payment,
                  bg="#FF69B4", fg="white", activebackground="#FF1493").pack(pady=20)

    def process_payment(self):
        name = self.name_entry.get()
        card = self.card_entry.get()
        expiry = self.expiry_entry.get()
        cvv = self.cvv_entry.get()
        zip_code = self.zip_entry.get()

        if not (name and card and expiry and cvv and zip_code):
            messagebox.showerror("ERROR", "Please fill in all required fields!")
            return
        if len(card) != 16 or not card.isdigit():
            messagebox.showerror("ERROR", "Card number must be 16 digits.")
            return
        if len(cvv) != 3 or not cvv.isdigit():
            messagebox.showerror("ERROR", "CVV must be 3 digits.")
            return

        messagebox.showinfo("Payment Successful", f"Payment processed for {self.ticket_count} tickets!")
        self.destroy()
        self.root.destroy()  # Close the main window


# Launch App 
if __name__ == "__main__":
    app = MovieSelectionWindow()
    app.mainloop()

