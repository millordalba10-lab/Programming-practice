import tkinter as tk
from tkinter import messagebox


products = []


def add_product():
    try:
        name = name_entry.get().strip()
        price = float(price_entry.get())
        quantity = int(quantity_entry.get())

        if name == "":
            messagebox.showerror("Error", "Please enter product name.")
            return

        if price < 0 or quantity <= 0:
            messagebox.showerror("Error", "Please enter valid price and quantity.")
            return

        total = price * quantity

        products.append({
            "name": name,
            "price": price,
            "quantity": quantity,
            "total": total
        })

        update_output()

        name_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)
        quantity_entry.delete(0, tk.END)

    except ValueError:
        messagebox.showerror(
            "Error",
            "Price and quantity must be numbers."
        )


def update_output():
    output.delete("1.0", tk.END)

    total_sales = 0

    output.insert(tk.END, "PRODUCT SALES\n")
    output.insert(tk.END, "------------------------------\n")

    for i, product in enumerate(products, 1):
        output.insert(
            tk.END,
            f"{i}. {product['name']}\n"
            f"   ₱{product['price']:,.2f} × {product['quantity']} "
            f"= ₱{product['total']:,.2f}\n\n"
        )

        total_sales += product["total"]

    output.insert(tk.END, "------------------------------\n")
    output.insert(
        tk.END,
        f"TOTAL SALES: ₱{total_sales:,.2f}"
    )


def clear_all():
    products.clear()

    name_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)

    output.delete("1.0", tk.END)

    output.insert(
        tk.END,
        "No products added yet."
    )


# =========================
# WINDOW
# =========================

window = tk.Tk()
window.title("Multiple Product Sales Calculator")
window.geometry("500x650")
window.resizable(False, False)
window.configure(bg="#1e1e1e")


# TITLE

tk.Label(
    window,
    text="SALES CALCULATOR",
    font=("Arial", 25, "bold"),
    fg="white",
    bg="#1e1e1e"
).pack(pady=20)


# PRODUCT NAME

tk.Label(
    window,
    text="Product Name",
    font=("Arial", 13),
    fg="white",
    bg="#1e1e1e"
).pack()

name_entry = tk.Entry(
    window,
    font=("Arial", 16),
    justify="center"
)
name_entry.pack(pady=8, padx=50, fill="x")


# PRICE

tk.Label(
    window,
    text="Product Price (₱)",
    font=("Arial", 13),
    fg="white",
    bg="#1e1e1e"
).pack()

price_entry = tk.Entry(
    window,
    font=("Arial", 16),
    justify="center"
)
price_entry.pack(pady=8, padx=50, fill="x")


# QUANTITY

tk.Label(
    window,
    text="Quantity",
    font=("Arial", 13),
    fg="white",
    bg="#1e1e1e"
).pack()

quantity_entry = tk.Entry(
    window,
    font=("Arial", 16),
    justify="center"
)
quantity_entry.pack(pady=8, padx=50, fill="x")


# BUTTONS

button_frame = tk.Frame(
    window,
    bg="#1e1e1e"
)
button_frame.pack(pady=15)

tk.Button(
    button_frame,
    text="ADD PRODUCT",
    font=("Arial", 12, "bold"),
    bg="#4CAF50",
    fg="white",
    command=add_product,
    width=15
).pack(side="left", padx=5)

tk.Button(
    button_frame,
    text="CLEAR ALL",
    font=("Arial", 12, "bold"),
    bg="#d9534f",
    fg="white",
    command=clear_all,
    width=15
).pack(side="left", padx=5)


# OUTPUT

tk.Label(
    window,
    text="SALES OUTPUT",
    font=("Arial", 16, "bold"),
    fg="white",
    bg="#1e1e1e"
).pack(pady=5)

output = tk.Text(
    window,
    height=14,
    font=("Arial", 12),
    bg="#2b2b2b",
    fg="white",
    relief="flat",
    padx=15,
    pady=15
)
output.pack(
    padx=30,
    pady=10,
    fill="both"
)

output.insert(
    tk.END,
    "No products added yet."
)


window.mainloop()