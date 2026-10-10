
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, date


DB_NAME = "business_sales.db"


class BusinessSalesSystem:

    def __init__(self, root):

        self.root = root
        self.root.title("Business Sales & Income System")
        self.root.geometry("1150x750")
        self.root.minsize(1000, 650)

        # Database
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()

        self.create_database()

        # Variables
        self.setup_variables()

        # Style
        self.setup_style()

        # GUI
        self.build_gui()

        # Load data
        self.load_products()
        self.load_today_sales()
        self.update_summary()


    # =========================================================
    # DATABASE
    # =========================================================

    def create_database(self):

        # Sales table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_date TEXT NOT NULL,
                sale_time TEXT NOT NULL,
                product TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                total REAL NOT NULL
            )
        """)

        # Products table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT UNIQUE NOT NULL,
                price REAL NOT NULL
            )
        """)

        # Default products
        default_products = [
            ("Feeds", 40.00),
            ("Tahop", 32.00),
            ("Sardinas", 26.00),
            ("Coke", 20.00)
        ]

        for product_name, price in default_products:

            self.cursor.execute("""
                INSERT OR IGNORE INTO products
                (product_name, price)
                VALUES (?, ?)
            """, (product_name, price))

        self.conn.commit()


    # =========================================================
    # VARIABLES
    # =========================================================

    def setup_variables(self):

        self.product_var = tk.StringVar()
        self.quantity_var = tk.StringVar(value="1")
        self.price_var = tk.StringVar()

        self.new_product_var = tk.StringVar()
        self.new_price_var = tk.StringVar()

        self.search_var = tk.StringVar()

        self.date_var = tk.StringVar(
            value=date.today().strftime("%B %d, %Y")
        )

        self.total_income_var = tk.StringVar(
            value="₱0.00"
        )

        self.transaction_var = tk.StringVar(
            value="0"
        )

        self.items_var = tk.StringVar(
            value="0"
        )

        self.selected_id = None


    # =========================================================
    # STYLE
    # =========================================================

    def setup_style(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Title.TLabel",
            font=("Segoe UI", 22, "bold")
        )

        style.configure(
            "Summary.TLabel",
            font=("Segoe UI", 15, "bold")
        )

        style.configure(
            "Treeview",
            rowheight=30,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold")
        )

        style.configure(
            "TButton",
            font=("Segoe UI", 10),
            padding=7
        )


    # =========================================================
    # BUILD GUI
    # =========================================================

    def build_gui(self):

        # =====================================================
        # HEADER
        # =====================================================

        header = ttk.Frame(
            self.root,
            padding=(15, 12)
        )

        header.pack(fill="x")

        ttk.Label(
            header,
            text="💰 BUSINESS SALES & INCOME SYSTEM",
            style="Title.TLabel"
        ).pack(side="left")

        ttk.Label(
            header,
            textvariable=self.date_var,
            font=("Segoe UI", 11)
        ).pack(side="right")


        # =====================================================
        # SUMMARY
        # =====================================================

        summary = ttk.Frame(
            self.root,
            padding=(15, 5)
        )

        summary.pack(fill="x")

        self.create_summary_card(
            summary,
            "TOTAL INCOME",
            self.total_income_var
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=5
        )

        self.create_summary_card(
            summary,
            "TRANSACTIONS",
            self.transaction_var
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=5
        )

        self.create_summary_card(
            summary,
            "ITEMS SOLD",
            self.items_var
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=5
        )


        # =====================================================
        # SALE FORM
        # =====================================================

        form = ttk.LabelFrame(
            self.root,
            text="  ADD / EDIT SALE  ",
            padding=12
        )

        form.pack(
            fill="x",
            padx=15,
            pady=10
        )


        # Product
        ttk.Label(
            form,
            text="Product:"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=5,
            pady=5
        )

        self.product_combo = ttk.Combobox(
            form,
            textvariable=self.product_var,
            width=27,
            state="normal"
        )

        self.product_combo.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        self.product_combo.bind(
            "<<ComboboxSelected>>",
            self.product_selected
        )

        self.product_combo.bind(
            "<KeyRelease>",
            self.product_typed
        )


        # Quantity
        ttk.Label(
            form,
            text="Quantity:"
        ).grid(
            row=0,
            column=2,
            sticky="w",
            padx=5,
            pady=5
        )

        ttk.Entry(
            form,
            textvariable=self.quantity_var,
            width=10
        ).grid(
            row=0,
            column=3,
            padx=5,
            pady=5
        )


        # Price
        ttk.Label(
            form,
            text="Price (₱):"
        ).grid(
            row=0,
            column=4,
            sticky="w",
            padx=5,
            pady=5
        )

        self.price_entry = ttk.Entry(
            form,
            textvariable=self.price_var,
            width=13
        )

        self.price_entry.grid(
            row=0,
            column=5,
            padx=5,
            pady=5
        )


        # Add Sale
        ttk.Button(
            form,
            text="➕ Add Sale",
            command=self.add_sale
        ).grid(
            row=0,
            column=6,
            padx=5
        )


        # Update
        ttk.Button(
            form,
            text="✏️ Update",
            command=self.update_sale
        ).grid(
            row=0,
            column=7,
            padx=5
        )


        # Clear
        ttk.Button(
            form,
            text="🧹 Clear",
            command=self.clear_form
        ).grid(
            row=0,
            column=8,
            padx=5
        )


        # =====================================================
        # PRODUCT MANAGEMENT
        # =====================================================

        product_frame = ttk.LabelFrame(
            self.root,
            text="  PRODUCT MANAGEMENT  ",
            padding=10
        )

        product_frame.pack(
            fill="x",
            padx=15,
            pady=5
        )


        ttk.Label(
            product_frame,
            text="Product:"
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=5
        )


        ttk.Entry(
            product_frame,
            textvariable=self.new_product_var,
            width=25
        ).grid(
            row=0,
            column=1,
            padx=5
        )


        ttk.Label(
            product_frame,
            text="Price (₱):"
        ).grid(
            row=0,
            column=2,
            padx=5
        )


        ttk.Entry(
            product_frame,
            textvariable=self.new_price_var,
            width=15
        ).grid(
            row=0,
            column=3,
            padx=5
        )


        ttk.Button(
            product_frame,
            text="➕ Add Product",
            command=self.add_product
        ).grid(
            row=0,
            column=4,
            padx=5
        )


        ttk.Button(
            product_frame,
            text="✏️ Update Product",
            command=self.update_product
        ).grid(
            row=0,
            column=5,
            padx=5
        )


        ttk.Button(
            product_frame,
            text="🗑️ Delete Product",
            command=self.delete_product
        ).grid(
            row=0,
            column=6,
            padx=5
        )


        # Product Table
        self.product_tree = ttk.Treeview(
            product_frame,
            columns=("id", "product", "price"),
            show="headings",
            height=4
        )

        self.product_tree.heading(
            "id",
            text="ID"
        )

        self.product_tree.heading(
            "product",
            text="Product"
        )

        self.product_tree.heading(
            "price",
            text="Price"
        )

        self.product_tree.column(
            "id",
            width=50,
            anchor="center"
        )

        self.product_tree.column(
            "product",
            width=250
        )

        self.product_tree.column(
            "price",
            width=120,
            anchor="center"
        )

        self.product_tree.grid(
            row=1,
            column=0,
            columnspan=7,
            sticky="ew",
            padx=5,
            pady=5
        )

        self.product_tree.bind(
            "<<TreeviewSelect>>",
            self.select_product
        )


        # =====================================================
        # SEARCH
        # =====================================================

        search_frame = ttk.Frame(
            self.root,
            padding=(15, 0)
        )

        search_frame.pack(
            fill="x",
            pady=5
        )


        ttk.Label(
            search_frame,
            text="🔎 Search Product:"
        ).pack(
            side="left",
            padx=(0, 5)
        )


        search_entry = ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=30
        )

        search_entry.pack(
            side="left",
            padx=5
        )

        search_entry.bind(
            "<KeyRelease>",
            lambda event: self.search_sales()
        )


        ttk.Button(
            search_frame,
            text="Today",
            command=self.load_today_sales
        ).pack(
            side="left",
            padx=5
        )


        ttk.Button(
            search_frame,
            text="All Records",
            command=self.load_all_sales
        ).pack(
            side="left",
            padx=5
        )


        ttk.Button(
            search_frame,
            text="🗑️ Delete Selected",
            command=self.delete_sale
        ).pack(
            side="right",
            padx=5
        )


        # =====================================================
        # SALES TABLE
        # =====================================================

        table_frame = ttk.Frame(
            self.root,
            padding=(15, 5)
        )

        table_frame.pack(
            fill="both",
            expand=True
        )


        columns = (
            "id",
            "date",
            "time",
            "product",
            "quantity",
            "price",
            "total"
        )


        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )


        headings = {
            "id": "ID",
            "date": "Date",
            "time": "Time",
            "product": "Product",
            "quantity": "Qty",
            "price": "Price",
            "total": "Total"
        }


        widths = {
            "id": 50,
            "date": 100,
            "time": 100,
            "product": 280,
            "quantity": 70,
            "price": 100,
            "total": 110
        }


        for col in columns:

            self.tree.heading(
                col,
                text=headings[col]
            )

            self.tree.column(
                col,
                width=widths[col],
                anchor="center"
            )


        self.tree.column(
            "product",
            anchor="w"
        )


        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )


        self.tree.configure(
            yscrollcommand=scrollbar.set
        )


        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )


        scrollbar.pack(
            side="right",
            fill="y"
        )


        self.tree.bind(
            "<<TreeviewSelect>>",
            self.select_sale
        )


        # =====================================================
        # BOTTOM BUTTONS
        # =====================================================

        bottom = ttk.Frame(
            self.root,
            padding=15
        )

        bottom.pack(
            fill="x"
        )


        ttk.Button(
            bottom,
            text="📊 Refresh Summary",
            command=self.refresh
        ).pack(
            side="left"
        )


        ttk.Button(
            bottom,
            text="❌ Exit",
            command=self.close_app
        ).pack(
            side="right"
        )


    # =========================================================
    # SUMMARY CARD
    # =========================================================

    def create_summary_card(
        self,
        parent,
        title,
        variable
    ):

        frame = ttk.LabelFrame(
            parent,
            text=title,
            padding=15
        )

        ttk.Label(
            frame,
            textvariable=variable,
            style="Summary.TLabel"
        ).pack()

        return frame


    # =========================================================
    # LOAD PRODUCTS
    # =========================================================

    def load_products(self):

        self.cursor.execute("""
            SELECT id, product_name, price
            FROM products
            ORDER BY id ASC
        """)

        products = self.cursor.fetchall()


        # Update dropdown
        product_names = [
            product[1]
            for product in products
        ]

        self.product_combo["values"] = product_names


        # Clear product table
        for item in self.product_tree.get_children():

            self.product_tree.delete(item)


        # Insert products
        for product_id, name, price in products:

            self.product_tree.insert(
                "",
                "end",
                values=(
                    product_id,
                    name,
                    f"{price:,.2f}"
                )
            )


    # =========================================================
    # AUTOMATIC PRICE
    # =========================================================

    def product_selected(self, event=None):

        product = self.product_var.get().strip()

        if not product:
            return

        self.cursor.execute("""
            SELECT price
            FROM products
            WHERE LOWER(product_name) = LOWER(?)
        """, (product,))

        result = self.cursor.fetchone()


        if result:

            self.price_var.set(
                f"{result[0]:.2f}"
            )


    def product_typed(self, event=None):

        product = self.product_var.get().strip()

        if not product:

            self.price_var.set("")
            return


        self.cursor.execute("""
            SELECT price
            FROM products
            WHERE LOWER(product_name) = LOWER(?)
        """, (product,))

        result = self.cursor.fetchone()


        if result:

            self.price_var.set(
                f"{result[0]:.2f}"
            )


    # =========================================================
    # ADD PRODUCT
    # =========================================================

    def add_product(self):

        name = self.new_product_var.get().strip()

        if not name:

            messagebox.showwarning(
                "Missing Product",
                "Please enter a product name."
            )

            return


        try:

            price = float(
                self.new_price_var.get().replace(",", "")
            )

            if price < 0:
                raise ValueError

        except ValueError:

            messagebox.showwarning(
                "Invalid Price",
                "Please enter a valid price."
            )

            return


        try:

            self.cursor.execute("""
                INSERT INTO products
                (product_name, price)
                VALUES (?, ?)
            """, (name, price))

            self.conn.commit()

        except sqlite3.IntegrityError:

            messagebox.showwarning(
                "Duplicate Product",
                "That product already exists."
            )

            return


        self.new_product_var.set("")
        self.new_price_var.set("")

        self.load_products()


        messagebox.showinfo(
            "Product Added",
            f"Product: {name}\n"
            f"Price: ₱{price:,.2f}"
        )


    # =========================================================
    # SELECT PRODUCT
    # =========================================================

    def select_product(self, event=None):

        selected = self.product_tree.selection()

        if not selected:
            return


        values = self.product_tree.item(
            selected[0],
            "values"
        )


        self.new_product_var.set(
            values[1]
        )

        self.new_price_var.set(
            values[2]
        )


    # =========================================================
    # UPDATE PRODUCT
    # =========================================================

    def update_product(self):

        selected = self.product_tree.selection()

        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select a product first."
            )

            return


        values = self.product_tree.item(
            selected[0],
            "values"
        )


        product_id = values[0]

        name = self.new_product_var.get().strip()


        if not name:

            messagebox.showwarning(
                "Missing Product",
                "Please enter a product name."
            )

            return


        try:

            price = float(
                self.new_price_var.get().replace(",", "")
            )

            if price < 0:
                raise ValueError

        except ValueError:

            messagebox.showwarning(
                "Invalid Price",
                "Please enter a valid price."
            )

            return


        try:

            self.cursor.execute("""
                UPDATE products
                SET product_name = ?, price = ?
                WHERE id = ?
            """, (
                name,
                price,
                product_id
            ))

            self.conn.commit()

        except sqlite3.IntegrityError:

            messagebox.showwarning(
                "Duplicate Product",
                "Another product already has that name."
            )

            return


        self.new_product_var.set("")
        self.new_price_var.set("")

        self.load_products()


        messagebox.showinfo(
            "Updated",
            "Product updated successfully."
        )


    # =========================================================
    # DELETE PRODUCT
    # =========================================================

    def delete_product(self):

        selected = self.product_tree.selection()

        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select a product first."
            )

            return


        values = self.product_tree.item(
            selected[0],
            "values"
        )


        product_id = values[0]
        product_name = values[1]


        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Delete '{product_name}'?"
        )


        if not confirm:
            return


        self.cursor.execute(
            "DELETE FROM products WHERE id = ?",
            (product_id,)
        )

        self.conn.commit()


        self.new_product_var.set("")
        self.new_price_var.set("")

        self.load_products()


        messagebox.showinfo(
            "Deleted",
            "Product deleted successfully."
        )


    # =========================================================
    # VALIDATE SALE
    # =========================================================

    def validate_inputs(self):

        product = self.product_var.get().strip()


        if not product:

            messagebox.showwarning(
                "Missing Product",
                "Please select a product."
            )

            return None


        try:

            quantity = int(
                self.quantity_var.get()
            )

            if quantity <= 0:
                raise ValueError

        except ValueError:

            messagebox.showwarning(
                "Invalid Quantity",
                "Quantity must be a whole number greater than 0."
            )

            return None


        try:

            price = float(
                self.price_var.get().replace(",", "")
            )

            if price < 0:
                raise ValueError

        except ValueError:

            messagebox.showwarning(
                "Invalid Price",
                "Please enter a valid price."
            )

            return None


        return product, quantity, price


    # =========================================================
    # ADD SALE
    # =========================================================

    def add_sale(self):

        data = self.validate_inputs()

        if not data:
            return


        product, quantity, price = data


        now = datetime.now()

        sale_date = now.strftime(
            "%Y-%m-%d"
        )

        sale_time = now.strftime(
            "%I:%M:%S %p"
        )


        total = quantity * price


        self.cursor.execute("""
            INSERT INTO sales
            (
                sale_date,
                sale_time,
                product,
                quantity,
                price,
                total
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            sale_date,
            sale_time,
            product,
            quantity,
            price,
            total
        ))


        self.conn.commit()


        self.clear_form()
        self.load_today_sales()
        self.update_summary()


        messagebox.showinfo(
            "Sale Added",
            f"Sale recorded successfully!\n\n"
            f"Product: {product}\n"
            f"Quantity: {quantity}\n"
            f"Price: ₱{price:,.2f}\n"
            f"Total: ₱{total:,.2f}"
        )


    # =========================================================
    # UPDATE SALE
    # =========================================================

    def update_sale(self):

        if self.selected_id is None:

            messagebox.showwarning(
                "No Selection",
                "Please select a sale first."
            )

            return


        data = self.validate_inputs()

        if not data:
            return


        product, quantity, price = data

        total = quantity * price


        self.cursor.execute("""
            UPDATE sales
            SET
                product = ?,
                quantity = ?,
                price = ?,
                total = ?
            WHERE id = ?
        """, (
            product,
            quantity,
            price,
            total,
            self.selected_id
        ))


        self.conn.commit()


        self.clear_form()
        self.load_today_sales()
        self.update_summary()


        messagebox.showinfo(
            "Updated",
            "Sale updated successfully."
        )


    # =========================================================
    # DELETE SALE
    # =========================================================

    def delete_sale(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select a sale."
            )

            return


        values = self.tree.item(
            selected[0],
            "values"
        )


        sale_id = values[0]


        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Delete sale #{sale_id}?\n\n"
            f"Product: {values[3]}\n"
            f"Total: ₱{float(values[6]):,.2f}"
        )


        if not confirm:
            return


        self.cursor.execute(
            "DELETE FROM sales WHERE id = ?",
            (sale_id,)
        )

        self.conn.commit()


        self.clear_form()
        self.load_today_sales()
        self.update_summary()


    # =========================================================
    # SELECT SALE
    # =========================================================

    def select_sale(self, event=None):

        selected = self.tree.selection()

        if not selected:
            return


        values = self.tree.item(
            selected[0],
            "values"
        )


        self.selected_id = int(
            values[0]
        )

        self.product_var.set(
            values[3]
        )

        self.quantity_var.set(
            values[4]
        )

        self.price_var.set(
            values[5]
        )


    # =========================================================
    # CLEAR FORM
    # =========================================================

    def clear_form(self):

        self.selected_id = None

        self.product_var.set("")
        self.quantity_var.set("1")
        self.price_var.set("")


        for item in self.tree.selection():

            self.tree.selection_remove(item)


        self.product_combo.focus()


    # =========================================================
    # LOAD TODAY'S SALES
    # =========================================================

    def load_today_sales(self):

        self.search_var.set("")

        today = date.today().isoformat()


        self.cursor.execute("""
            SELECT
                id,
                sale_date,
                sale_time,
                product,
                quantity,
                price,
                total
            FROM sales
            WHERE sale_date = ?
            ORDER BY id DESC
        """, (today,))


        rows = self.cursor.fetchall()

        self.display_rows(rows)


    # =========================================================
    # LOAD ALL SALES
    # =========================================================

    def load_all_sales(self):

        self.search_var.set("")


        self.cursor.execute("""
            SELECT
                id,
                sale_date,
                sale_time,
                product,
                quantity,
                price,
                total
            FROM sales
            ORDER BY id DESC
        """)


        rows = self.cursor.fetchall()

        self.display_rows(rows)


    # =========================================================
    # SEARCH SALES
    # =========================================================

    def search_sales(self):

        keyword = self.search_var.get().strip()


        if not keyword:

            self.load_today_sales()
            return


        self.cursor.execute("""
            SELECT
                id,
                sale_date,
                sale_time,
                product,
                quantity,
                price,
                total
            FROM sales
            WHERE product LIKE ?
            ORDER BY id DESC
        """, (
            f"%{keyword}%",
        ))


        rows = self.cursor.fetchall()

        self.display_rows(rows)


    # =========================================================
    # DISPLAY SALES
    # =========================================================

    def display_rows(self, rows):

        for item in self.tree.get_children():

            self.tree.delete(item)


        for row in rows:

            (
                sale_id,
                sale_date,
                sale_time,
                product,
                quantity,
                price,
                total
            ) = row


            self.tree.insert(
                "",
                "end",
                values=(
                    sale_id,
                    sale_date,
                    sale_time,
                    product,
                    quantity,
                    f"{price:,.2f}",
                    f"{total:,.2f}"
                )
            )


    # =========================================================
    # UPDATE SUMMARY
    # =========================================================

    def update_summary(self):

        today = date.today().isoformat()


        self.cursor.execute("""
            SELECT
                COALESCE(SUM(total), 0),
                COUNT(*),
                COALESCE(SUM(quantity), 0)
            FROM sales
            WHERE sale_date = ?
        """, (today,))


        total_income, transactions, items = (
            self.cursor.fetchone()
        )


        self.total_income_var.set(
            f"₱{total_income:,.2f}"
        )

        self.transaction_var.set(
            str(transactions)
        )

        self.items_var.set(
            str(items)
        )


    # =========================================================
    # REFRESH
    # =========================================================

    def refresh(self):

        self.load_products()
        self.load_today_sales()
        self.update_summary()


    # =========================================================
    # CLOSE
    # =========================================================

    def close_app(self):

        self.conn.close()
        self.root.destroy()


# =============================================================
# MAIN
# =============================================================

def main():

    root = tk.Tk()

    app = BusinessSalesSystem(root)

    root.protocol(
        "WM_DELETE_WINDOW",
        app.close_app
    )

    root.mainloop()


if __name__ == "__main__":
    main()
