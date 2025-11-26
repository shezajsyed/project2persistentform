import tkinter as tk
from tkinter import messagebox
import sqlite3

def init_db():
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

class SeatSelectionWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Seat Selection")
        self.master.configure(bg="#F8E8EE")
        self.text_color = "#7A5C61"
        self.selected_seats = set()
        self.load_seats()
        self.build_ui()

    def load_seats(self):
        conn = sqlite3.connect("cinema.db")
        c = conn.cursor()
        c.execute("SELECT seat_id, status FROM seats ORDER BY seat_id")
        self.seat_data = c.fetchall()
        conn.close()

    def build_ui(self):
        title = tk.Label(
            self.master,
            text="Select Your Seats",
            font=("Arial", 18, "bold"),
            bg="#F8E8EE",
            fg=self.text_color
        )
        title.pack(pady=15)

        grid_frame = tk.Frame(self.master, bg="#F8E8EE")
        grid_frame.pack()

        self.colors = {
            "available": "#7A5C61",
            "selected": "#F9D5E5",
            "taken": "#7A5C61"
        }

        self.buttons = {}
        row = 0
        col = 0

        for seat_id, status in self.seat_data:
            if status == 1:
                bg = self.colors["available"]
                state = "normal"
            else:
                bg = self.colors["taken"]
                state = "disabled"

            btn = tk.Button(
                grid_frame,
                text=str(seat_id),
                width=5,
                height=2,
                bg=bg,
                fg=self.text_color,
                font=("Arial", 10, "bold"),
                activebackground="#FCE1F3",
                relief="flat",
                bd=0,
                state=state,
                command=lambda s=seat_id: self.toggle_seat(s)
            )

            btn.grid(row=row, column=col, padx=7, pady=7)
            self.buttons[seat_id] = btn

            col += 1
            if col == 6:
                col = 0
                row += 1

        confirm_btn = tk.Button(
            self.master,
            text="Confirm Selection",
            font=("Arial", 12),
            bg="#FFD1DC",
            fg=self.text_color,
            activebackground="#F7C5CC",
            relief="flat",
            bd=0,
            command=self.confirm_selection
        )
        confirm_btn.pack(pady=20)

    def toggle_seat(self, seat_id):
        btn = self.buttons[seat_id]

        if seat_id in self.selected_seats:
            self.selected_seats.remove(seat_id)
            btn.config(bg=self.colors["available"], fg=self.text_color)
        else:
            self.selected_seats.add(seat_id)
            btn.config(bg=self.colors["selected"], fg=self.text_color)
    def confirm_selection(self):
        if not self.selected_seats:
            messagebox.showwarning("No seats selected", "Please select at least one seat.")
            return

        conn = sqlite3.connect("cinema.db")
        c = conn.cursor()

        for seat_id in self.selected_seats:
            c.execute("UPDATE seats SET status = 0 WHERE seat_id = ?", (seat_id,))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"Seats {list(self.selected_seats)} booked!")
        
        # -- Data analysis (pandas) --
        import pandas as pd
        import matplotlib.pyplot as plt

        conn = sqlite3.connect("cinema.db")
        df = pd.read_sql_query("SELECT * FROM seats", conn)
        conn.close()

        df['status'].value_counts().plot(kind='bar', color=['green', 'red'])
        plt.title("Seat Booking Status")
        plt.xlabel("Seat Status (1=Available, 0=Booked)")
        plt.ylabel("Number of Seats")
        plt.show()

        self.master.destroy()

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = SeatSelectionWindow(root)
    root.mainloop()
