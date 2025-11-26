import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import os


def init_seat_db():
    """Initialize seats database for seat selection"""
    conn = sqlite3.connect("cinema.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS seats (
            seat_id INTEGER PRIMARY KEY,
            status INTEGER DEFAULT 1
        )
    """)
    c.execute("SELECT COUNT(*) FROM seats")
    if c.fetchone()[0] == 0:
        for i in range(1, 31):
            c.execute("INSERT INTO seats (seat_id, status) VALUES (?, 1)", (i,))
    conn.commit()
    conn.close()

class MainPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Movie Kiosk")
        self.geometry("800x600")
        self.configure(bg="#f0f0f0")

        tk.Label(self, text="Select a Movie", font=("Helvetica", 24, "bold"), bg="#f0f0f0").pack(pady=20)

        self.movies = [
            {"La La Land": "Movie A", "image": "png/LLL_1.png"},
            {"Twenty Seven Dresses": "Movie B", "image": "png/TSD_2.png"},
            {"The Notebook": "Movie C", "image": "png/TN_3.png"},
            {"The Princess Bride": "Movie D", "image": "png/TPB_5.png"},
            {"How To Lose a Guy In 10 Days": "Movie E", "image": "png/HTLAGITD_4.png"}
        ]

        self.poster_frame = tk.Frame(self, bg="#f0f0f0")
        self.poster_frame.pack(pady=10)
        self.load_posters()

    def load_posters(self):
        self.poster_images = []
        for idx, movie in enumerate(self.movies):
            img = Image.open(movie["image"])
            img = img.resize((150, 220), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(img)
            self.poster_images.append(photo)

            # Button with image
            btn = tk.Button(self.poster_frame, image=photo, cursor="hand2",
                            command=lambda m=movie["title"]: self.open_ticket_window(m))
            btn.grid(row=idx // 4, column=idx % 4, padx=10, pady=10)

            tk.Label(self.poster_frame, text=movie["title"], font=("Helvetica", 12, "bold"),
                     bg="#f0f0f0").grid(row=(idx // 4)+1, column=idx % 4)

    def open_ticket_window(self, movie):
        self.withdraw()
        TicketSelectionWindow(movie)

# Payment
class PaymentDetailsWindow(tk.Toplevel):
    def __init__(self, movie, showtime, tickets):
        super().__init__()
        self.title("Payment Details")
        self.geometry("450x450")
        self.configure(bg="#FFC0CB")  # Light pink background

        tk.Label(self, text="Payment Details", font=("Helvetica", 20, "bold"), bg="#FFC0CB").pack(pady=15)
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

        tk.Button(self, text="Pay Now", font=("Helvetica", 14, "bold"), bg="#FF69B4", fg="white",
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

# Ticket Selection Window
class TicketSelectionWindow(tk.Toplevel):
    def __init__(self, movie):
        super().__init__()
        self.title(f"{movie} - Tickets")
        self.geometry("400x300")
        self.movie = movie

        tk.Label(self, text=f"Movie: {movie}", font=("Helvetica", 16, "bold")).pack(pady=10)
        tk.Label(self, text="Select Showtime", font=("Helvetica", 14)).pack(pady=5)

        # Showtimes
        self.showtime_var = tk.StringVar(value="12:00 PM")
        showtimes = ["12:00 PM", "3:00 PM", "6:00 PM", "9:00 PM"]
        self.showtime_menu = tk.OptionMenu(self, self.showtime_var, *showtimes)
        self.showtime_menu.pack(pady=10)

        tk.Label(self, text="Number of Tickets", font=("Helvetica", 14)).pack(pady=5)
        self.ticket_var = tk.IntVar(value=1)
        tk.Spinbo

