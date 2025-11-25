import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Payment Window
class PaymentDetailsWindow(tk.Toplevel):
    def __init__(self, movie, showtime, tickets):
        super().__init__()
        self.title("Payment Details")
        self.geometry("450x450")
        self.configure(bg="#FFC0CB")  # Light pink background

        tk.Label(self, text="Payment Details", font=("Helvetica", 20, "bold"), bg="#FFC0CB", fg="#DD77AA").pack(pady=15)
        tk.Label(self, text=f"Movie: {movie}", font=("Comic Sans MS", 12, "bold"), bg="#FFC0CB").pack()
        tk.Label(self, text=f"Showtime: {showtime}", font=("Comic Sans MS", 12, "bold"), bg="#FFC0CB").pack()
        tk.Label(self, text=f"Tickets: {tickets}", font=("Comic Sans MS", 12, "bold"), bg="#FFC0CB").pack(pady=10)

        # Name on Card
        tk.Label(self, text="Name on Card", font=("Comic Sans MS", 12, "bold"), bg="#FFC0CB").pack(anchor="w", padx=20)
        self.name_entry = tk.Entry(self, font=("Helvetica", 12))
        self.name_entry.pack(fill="x", padx=20, pady=5)

        # Card Number
        tk.Label(self, text="Card Number", font=("Comic Sans MS", 12, "bold"), bg="#FFC0CB").pack(anchor="w", padx=20)
        self.card_entry = tk.Entry(self, font=("Helvetica", 12))
        self.card_entry.pack(fill="x", padx=20, pady=5)

        # Expiry & CVV
        tk.Label(self, text="Expiry (MM/YY)", font=("Comic Sans MS", 12, "bold"), bg="#FFC0CB").pack(anchor="w", padx=20)
        self.expiry_entry = tk.Entry(self, font=("Helvetica", 12))
        self.expiry_entry.pack(fill="x", padx=20, pady=5)

        tk.Label(self, text="CVV", font=("Comic Sans MS", 12, "bold"), bg="#FFC0CB").pack(anchor="w", padx=20)
        self.cvv_entry = tk.Entry(self, font=("Helvetica", 12), show="*")
        self.cvv_entry.pack(fill="x", padx=20, pady=5)

        tk.Button(self, text="Pay Now", font=("Helvetica", 14, "bold"), bg="#FF69B4", fg="#DD77AA",
                  command=self.process_payment).pack(pady=20)

    def process_payment(self):
        name = self.name_entry.get()
        card = self.card_entry.get()
        expiry = self.expiry_entry.get()
        cvv = self.cvv_entry.get()

        if not all([name, card, expiry, cvv]):
            messagebox.showerror("Error", "Please fill in all fields!")
            return
        if len(card) != 16 or not card.isdigit():
            messagebox.showerror("Error", "Card number must be 16 digits")
            return
        if len(cvv) != 3 or not cvv.isdigit():
            messagebox.showerror("Error", "CVV must be 3 digits")
            return

        messagebox.showinfo("Success", "Payment Successful!")
        self.destroy()

# ---------------- Ticket Selection ----------------
class TicketSelectionWindow(tk.Toplevel):
    def __init__(self, movie):
        super().__init__()
        self.title(f"{movie} - Tickets")
        self.geometry("400x300")
        self.movie = movie

        self.configure(bg="#FFC0CB")

        tk.Label(self, text=f"Movie: {movie}", font=("Helvetica", 16, "bold"), bg="#FFC0CB", fg="#DD77AA").pack(pady=10)
        tk.Label(self, text="Select Showtime", font=("Helvetica", 14, "bold"), bg="#FFC0CB").pack(pady=5)

        # Showtimes
        self.showtime_var = tk.StringVar(value="12:00 PM")
        showtimes = ["12:00 PM", "3:00 PM", "6:00 PM", "9:00 PM"]
        self.showtime_menu = tk.OptionMenu(self, self.showtime_var, *showtimes)
        self.showtime_menu.pack(pady=10)

        tk.Label(self, text="Number of Tickets", font=("Helvetica", 14, "bold"), bg="#FFC0CB").pack(pady=5)
        self.ticket_var = tk.IntVar(value=1)
        tk.Spinbox(self, from_=1, to=10, textvariable=self.ticket_var, width=5, font=("Helvetica", 12)).pack(pady=10)

        tk.Button(self, text="Proceed to Payment", font=("Helvetica", 12, "bold"),
                  bg="#FF69B4", fg="#DD77AA",
                  command=self.proceed_payment).pack(pady=20)

    def proceed_payment(self):
        showtime = self.showtime_var.get()
        tickets = self.ticket_var.get()
        self.withdraw()
        PaymentDetailsWindow(self.movie, showtime, tickets)

# ---------------- Main Page with Poster Buttons ----------------
class MainPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Movie Kiosk")
        self.geometry("800x700")
        self.configure(bg="#FFC0CB")

        tk.Label(self, text="Select a Movie", font=("Helvetica", 24, "bold"), bg="#FFC0CB", fg="#DD77AA").pack(pady=20)

        self.movies = [
            {"title": "How to Lose a Guy in 10 Days", "image": "ui/movie_posters/howtoloseaguyin10days.png"},
            {"title": "The Princess Bride", "image": "ui/movie_posters/theprincessbride.png"},
            {"title": "La La Land", "image": "ui/movie_posters/lalaland.png"},
            {"title": "27 Dresses", "image": "ui/movie_posters/27dresses.png"},
            {"title": "The Notebook", "image": "ui/movie_posters/thenotebook.png"}
        ]

        self.poster_frame = tk.Frame(self, bg="#DD77AA")
        self.poster_frame.pack(pady=10)
        self.load_posters()

    def load_posters(self):
        self.poster_images = []

        for idx, movie in enumerate(self.movies):
            frame = tk.Frame(self.poster_frame, bg="#DD77AA")
            frame.grid(row=idx // 4, column=idx % 4, padx=20, pady=20, sticky="n")

            img = Image.open(movie["image"])
            img = img.resize((150, 220), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.poster_images.append(photo)

            # Button with image
            btn = tk.Button(frame, image=photo, cursor="hand2",
                            command=lambda m=movie["title"]: self.open_ticket_window(m),
                            bd=0, highlightthickness=0)
            btn.pack(pady=(0, 5))

            tk.Label(frame, text=movie["title"], font=("Helvetica", 12, "bold"),
                     bg="#DD77AA").pack()

    def open_ticket_window(self, movie):
        self.withdraw()
        TicketSelectionWindow(movie)

# ---------------- Launch App ----------------
if __name__ == "__main__":
    app = MainPage()
    app.mainloop()