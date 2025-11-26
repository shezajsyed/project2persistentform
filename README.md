# Movie Booking App

## Overview

This project is a Python-based movie ticket booking system built using **Tkinter** for the GUI and **SQLite** for the database. The application allows users to browse movies, select showtimes, proceed through payment, and then select their seats. The database is automatically created when the program runs, so no manual setup is required.

---

## Features

* **Movie Selection/Payment Screen**
* **Showtime Selection**
* **Seat Selection Screen** (runs after payment)
* **Automatic Database Creation** using SQLite
* **Data Analysis & Visualization** using Pandas and Matplotlib
* **Modular Code Structure** split into multiple Python files:

  * `movie_buttons.py` – main screen & navigation
  * `seat_selection.py` – seat selection UI

---

## How to Run the App

1. Clone the repository:

   ```bash
   git clone <your-repo-link>
   cd project2persistentform
   ```

2. Run the main application file:

   ```bash
   python3 movie_buttons.py
   ```

3. The **database file (`cinema.db`) will be created automatically** when the app runs.

> **You do NOT need to provide a database file manually.**

---

## Database Note

`cinema.db` is **generated automatically** by `seat_selection.py` when the app launches. It tracks seat availability and updates as users book seats.

---

## Data Analysis & Visualization
* **Pandas** – automatically loads seat data from SQLite and analyzes ticket sales/occupancy.
* **Matplotlib** – automatically visualizes booking trends after seats are confirmed.

---

Example snippet:

```python
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

conn = sqlite3.connect("cinema.db")
df = pd.read_sql_query("SELECT * FROM seats", conn)
conn.close()

df['status'].value_counts().plot(kind='bar', color=['green','red'])
plt.title("Seat Booking Status")
plt.xlabel("Seat Status (1=Available, 0=Booked)")
plt.ylabel("Number of Seats")
plt.show()
```

---

## Project Structure

```
project2persistentform/
│
├── movie_buttons.py        # Main screens & navigation
├── seat_selection.py       # Seat selection UI
├── README.md               # Project documentation
├── cinema.db               # Local database (ignored by GitHub)
└── ui/                     # Images, icons, and assets
```

---

## Requirements

* Python 3.10+
* Tkinter (usually included with Python)
* SQLite (included with Python)
* Pandas (optional, for analysis)
* Matplotlib (optional, for visualization)

---

## Contributors

* Sheza Syed
* Alia Hanafy
* Hamda Yousuf

---

## Notes

* If `cinema.db` already exists and you want a fresh database, delete it before running the program.
* All database and data analysis operations are handled automatically.
