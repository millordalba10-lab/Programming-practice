import tkinter as tk
from tkinter import messagebox
import random

# =========================
# MAIN WINDOW
# =========================
window = tk.Tk()
window.title("Sales Calculator")
window.geometry("450x600")
window.resizable(False, False)
window.configure(bg="#1e1e1e")


# =========================
# EMOJI BACKGROUND
# =========================
emojis = ["💰", "🛒", "🧾", "💵", "🛍️", "⭐", "💳", "📦"]

for i in range(25):
    emoji = random.choice(emojis)

    x = random.randint(10, 420)
    y = random.randint(10, 570)

    label = tk.Label(
        window,
        text=emoji,
        font=("Arial", random.randint(15, 25)),
        bg="#1e1e1e",
        fg="white"
    )

    label.place(x=x, y=y)


# =========================
# FUNCTIONS
# =========================
def calculate():
    try:
        price = float(price_entry.get())
        quantity = int(quantity_entry.get())

        if price < 0 or quantity <= 0:
            messagebox.showerror(
                "Invalid Input",
                "Please enter valid price and quantity."
            )
            return

        total = price * quantity

        result.config(
            text=f"₱{total:,.2f}"
        )

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter numbers only."
        )


def clear():
    price_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    result.config(text="₱0.00")


# =========================
# HEADER
# =========================
header = tk.Frame(
    window,
    bg="#252525"
)
header.pack(fill="x", pady=(0, 20))

tk.Label(
    header,
    text="💰 SALES CALCULATOR 💰",
    font=("Arial", 24, "bold"),
    fg="white",
    bg="#252525"
).pack(pady=(20, 5))

tk.Label(
    header,
    text="🛒 Calculate your sales easily 🧾",
    font=("Arial", 11),
    fg="#cccccc",
    bg="#252525"
).pack(pady=(0, 15))


# =========================
# INPUT AREA
# =========================
tk.Label(
    window,
    text="💵 PRODUCT PRICE",
    font=("Arial", 12, "bold"),
    fg="white",
    bg="#1e1e1e"
).pack()

price_entry = tk.Entry(
    window,
    font=("Arial", 18),
    justify="center",
    bg="#333333",
    fg="white",
    insertbackground="white",
    relief="flat"
)
price_entry.pack(
    padx=50,
    pady=10,
    ipady=8,
    fill="x"
)


tk.Label(
    window,
    text="📦 QUANTITY SOLD",
    font=("Arial", 12, "bold"),
    fg="white",
    bg="#1e1e1e"
).pack()

quantity_entry = tk.Entry(
    window,
    font=("Arial", 18),
    justify="center",
    bg="#333333",
    fg="white",
    insertbackground="white",
    relief="flat"
)
quantity_entry.pack(
    padx=50,
    pady=10,
    ipady=8,
    fill="x"
)


# =========================
# BUTTONS
# =========================
button_frame = tk.Frame(
    window,
    bg="#1e1e1e"
)
button_frame.pack(pady=20)

tk.Button(
    button_frame,
    text="🧮 CALCULATE",
    font=("Arial", 13, "bold"),
    bg="#4CAF50",
    fg="white",
    relief="flat",
    command=calculate,
    padx=20,
    pady=10
).pack(side="left", padx=5)

tk.Button(
    button_frame,
    text="🗑️ CLEAR",
    font=("Arial", 13, "bold"),
    bg="#555555",
    fg="white",
    relief="flat",
    command=clear,
    padx=20,
    pady=10
).pack(side="left", padx=5)


# =========================
# RESULT
# =========================
result_frame = tk.Frame(
    window,
    bg="#252525"
)
result_frame.pack(
    padx=40,
    pady=15,
    fill="x"
)

tk.Label(
    result_frame,
    text="🧾 TOTAL SALES",
    font=("Arial", 13, "bold"),
    fg="#cccccc",
    bg="#252525"
).pack(pady=(20, 5))

result = tk.Label(
    result_frame,
    text="₱0.00",
    font=("Arial", 32, "bold"),
    fg="#4CAF50",
    bg="#252525"
)
result.pack(pady=(5, 20))


# =========================
# FOOTER
# =========================
tk.Label(
    window,
    text="⭐ Simple • Fast • Easy ⭐",
    font=("Arial", 10),
    fg="#888888",
    bg="#1e1e1e"
).pack(pady=10)


window.mainloop()