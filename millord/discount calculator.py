import tkinter as tk
from tkinter import messagebox

window = tk.Tk()
window.title("Discount Calculator")
window.geometry("400x500")
window.resizable(False, False)

tk.Label(.py
    window,
    text="DISCOUNT CALCULATOR",
    font=("Arial", 24, "bold")
).pack(pady=25)

tk.Label(
    window,
    text="Original Price (₱)",
    font=("Arial", 14)
).pack()

price_entry = tk.Entry(
    window,
    font=("Arial", 18),
    justify="center"
)
price_entry.pack(pady=10)

tk.Label(
    window,
    text="Discount (%)",
    font=("Arial", 14)
).pack()

discount_entry = tk.Entry(
    window,
    font=("Arial", 18),
    justify="center"
)
discount_entry.pack(pady=10)


def calculate():
    try:
        price = float(price_entry.get())
        discount = float(discount_entry.get())

        if price < 0 or discount < 0 or discount > 100:
            messagebox.showerror(
                "Error",
                "Please enter valid values."
            )
            return

        discount_amount = price * discount / 100
        final_price = price - discount_amount

        discount_result.config(
            text=f"Discount: ₱{discount_amount:,.2f}"
        )

        final_result.config(
            text=f"Final Price: ₱{final_price:,.2f}"
        )

    except ValueError:
        messagebox.showerror(
            "Error",
            "Please enter numbers only."
        )


def clear():
    price_entry.delete(0, tk.END)
    discount_entry.delete(0, tk.END)
    discount_result.config(text="Discount: ₱0.00")
    final_result.config(text="Final Price: ₱0.00")


tk.Button(
    window,
    text="CALCULATE",
    font=("Arial", 15, "bold"),
    command=calculate,
    width=15
).pack(pady=20)

tk.Button(
    window,
    text="CLEAR",
    font=("Arial", 15),
    command=clear,
    width=15
).pack()

discount_result = tk.Label(
    window,
    text="Discount: ₱0.00",
    font=("Arial", 16)
)
discount_result.pack(pady=25)

final_result = tk.Label(
    window,
    text="Final Price: ₱0.00",
    font=("Arial", 20, "bold")
)
final_result.pack()

window.mainloop()