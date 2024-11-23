import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import sqlite3
from datetime import datetime

class ExpenseManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Manager")
        self.root.geometry("800x900")
        self.root.resizable(False, False)

        self.frame1 = tk.Frame(self.root)
        self.frame2 = tk.Frame(self.root)

        self.setup_database()
        self.set_background_image()

        self.create_screen1_widgets()
        self.create_screen2_widgets()

        self.frame1.pack(fill="both", expand=True)

    def setup_database(self):
        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                expense TEXT,
                due_date TEXT,
                price REAL,
                category TEXT,
                receipt TEXT
            )
        """)
        conn.commit()
        conn.close()

    def set_background_image(self):
        bg_image = Image.open("bg.jpg")
        bg_image = bg_image.resize((800, 700), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(bg_image)

        self.bg_label1 = tk.Label(self.frame1, image=self.bg_image)
        self.bg_label1.place(relwidth=1, relheight=1)

        self.bg_label2 = tk.Label(self.frame2, image=self.bg_image)
        self.bg_label2.place(relwidth=1, relheight=1)

    def create_screen1_widgets(self):
        label_font = ("Arial", 12, "bold")

        self.expense_label = tk.Label(self.frame1, text="Expense Description:", font=label_font, bg="gray", anchor="w")
        self.expense_label.place(x=20, y=60, width=200, height=30)
        self.expense_entry = tk.Entry(self.frame1, font=("Arial", 12), bd=2)
        self.expense_entry.place(x=220, y=100, width=500, height=30)

        self.due_date_label = tk.Label(self.frame1, text="Due Date:", font=label_font, bg="gray", anchor="w")
        self.due_date_label.place(x=20, y=140, width=200, height=30)
        self.due_date_entry = DateEntry(self.frame1, width=20, background="gray", foreground="white", font=("Arial", 12))
        self.due_date_entry.place(x=220, y=180, width=250, height=30)

        self.price_label = tk.Label(self.frame1, text="Price (PHP):", font=label_font, bg="gray", anchor="w")
        self.price_label.place(x=20, y=220, width=200, height=30)
        self.price_entry = tk.Entry(self.frame1, font=("Arial", 12), bd=2)
        self.price_entry.place(x=220, y=260, width=250, height=30)

        self.category_label = tk.Label(self.frame1, text="Category:", font=label_font, bg="gray", anchor="w")
        self.category_label.place(x=20, y=300, width=200, height=30)
        self.category_var = tk.StringVar()
        self.category_var.set("Food")
        self.category_menu = tk.OptionMenu(self.frame1, self.category_var, "Food", "Utilities", "Entertainment", "Other")
        self.category_menu.config(font=label_font, bg="gray", fg="black")
        self.category_menu.place(x=220, y=340, width=250, height=30)

        self.add_button = tk.Button(self.frame1, text="Add Expense", font=("Arial", 14, "bold"), bg="gray", fg="white", command=self.add_expense, relief="flat", height=2)
        self.add_button.place(x=20, y=400, width=240, height=50)

        self.delete_button = tk.Button(self.frame1, text="Delete Expense", font=("Arial", 14, "bold"), bg="red", fg="white", command=self.delete_expense, relief="flat", height=2)
        self.delete_button.place(x=280, y=400, width=240, height=50)

        self.edit_button = tk.Button(self.frame1, text="Edit Expense", font=("Arial", 14, "bold"), bg="blue", fg="white", command=self.edit_expense, relief="flat", height=2)
        self.edit_button.place(x=540, y=400, width=240, height=50)

        self.clear_all_button = tk.Button(self.frame1, text="Clear All Expenses", font=("Arial", 14, "bold"), bg="darkred", fg="white", command=self.clear_all_expenses, relief="flat", height=2)
        self.clear_all_button.place(x=20, y=470, width=760, height=50)

        self.expense_listbox = tk.Listbox(self.frame1, font=("Courier", 12, "bold"), bd=2, relief="solid", selectbackground="gray")
        self.expense_listbox.place(x=20, y=540, width=760, height=200)

        self.switch_to_screen2_button = tk.Button(self.frame1, text="Go to Reports", font=("Arial", 12, "bold"), bg="green", fg="white", command=self.switch_to_screen2)
        self.switch_to_screen2_button.place(x=650, y=20, width=120, height=40)

        self.populate_expense_listbox()

    def create_screen2_widgets(self):
        self.category_summary_listbox = tk.Listbox(self.frame2, font=("Arial", 12), width=50, height=10)
        self.category_summary_listbox.pack(pady=10)

        self.calculate_button = tk.Button(self.frame2, text="Calculate Total Expenses", font=("Arial", 12, "bold"), bg="blue", fg="white", command=self.calculate_total_expenses)
        self.calculate_button.pack(pady=10)

        self.total_expenses_label = tk.Label(self.frame2, text="Total Expenses: PHP 0.00", font=("Arial", 12, "bold"), bg="gray", fg="white")
        self.total_expenses_label.pack(pady=10)

        self.generate_receipt_button = tk.Button(self.frame2, text="Generate Receipt", font=("Arial", 14, "bold"), bg="green", fg="white", command=self.generate_receipt, relief="flat", height=2)
        self.generate_receipt_button.pack(pady=10)

        self.switch_to_screen1_button = tk.Button(self.frame2, text="Back to Expenses", font=("Arial", 12, "bold"), bg="green", fg="white", command=self.switch_to_screen1)
        self.switch_to_screen1_button.pack(pady=10)

    def add_expense(self):
        expense = self.expense_entry.get()
        due_date = self.due_date_entry.get_date()
        price = self.price_entry.get()
        category = self.category_var.get()

        if not expense or not price:
            messagebox.showerror("Input Error", "Please fill in all fields")
            return

        try:
            price = float(price)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid price")
            return

        due_date_str = due_date.strftime('%Y-%m-%d')

        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO expenses (expense, due_date, price, category) VALUES (?, ?, ?, ?)",
            (expense, due_date_str, price, category)
        )
        conn.commit()
        conn.close()

        self.populate_expense_listbox()

    def delete_expense(self):
        selected_item = self.expense_listbox.curselection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an expense to delete.")
            return

        index = selected_item[0]
        selected_text = self.expense_listbox.get(index)
        expense_description = selected_text.split(" | ")[0]

        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE expense = ?", (expense_description,))
        conn.commit()
        conn.close()

        self.populate_expense_listbox()

    def edit_expense(self):
        selected_item = self.expense_listbox.curselection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an expense to edit.")
            return

        index = selected_item[0]
        selected_text = self.expense_listbox.get(index)
        expense_description = selected_text.split(" | ")[0]

        new_expense = self.expense_entry.get()
        new_due_date = self.due_date_entry.get_date().strftime('%Y-%m-%d')
        new_price = self.price_entry.get()
        new_category = self.category_var.get()

        if not new_expense or not new_price:
            messagebox.showerror("Input Error", "Please fill in all fields to edit.")
            return

        try:
            new_price = float(new_price)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid price")
            return

        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE expenses SET expense = ?, due_date = ?, price = ?, category = ?
            WHERE expense = ?
        """, (new_expense, new_due_date, new_price, new_category, expense_description))
        conn.commit()
        conn.close()

        self.populate_expense_listbox()

    def clear_all_expenses(self):
        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses")
        conn.commit()
        conn.close()

        self.populate_expense_listbox()

    def populate_expense_listbox(self):
        self.expense_listbox.delete(0, tk.END)

        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM expenses")
        expenses = cursor.fetchall()
        conn.close()

        for expense in expenses:
            expense_text = f"{expense[1]} | Due: {expense[2]} | PHP {expense[3]} | {expense[4]}"
            self.expense_listbox.insert(tk.END, expense_text)

    def generate_receipt(self):
        receipt_text = "Receipt\n\n"
        receipt_text += f"Expense: {self.expense_entry.get()}\n"
        receipt_text += f"Due Date: {self.due_date_entry.get_date()}\n"
        receipt_text += f"Price: {self.price_entry.get()}\n"
        receipt_text += f"Category: {self.category_var.get()}\n"

        self.save_receipt(receipt_text)

        messagebox.showinfo("Generated Receipt", receipt_text)

    def save_receipt(self, receipt_text):
        selected_expense = self.expense_listbox.curselection()
        if not selected_expense:
            messagebox.showwarning("Selection Error", "Please select an expense to save receipt")
            return

        expense_id = self.expense_listbox.get(selected_expense[0]).split(" | ")[0]

        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE expenses SET receipt = ? WHERE id = ?", (receipt_text, expense_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Receipt Generated", "Receipt has been saved successfully!")

    def calculate_total_expenses(self):
        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(price) FROM expenses")
        total_expenses = cursor.fetchone()[0] or 0
        conn.close()

        self.total_expenses_label.config(text=f"Total Expenses: PHP {total_expenses:.2f}")

    def switch_to_screen2(self):
        self.frame1.pack_forget()
        self.frame2.pack(fill="both", expand=True)

    def switch_to_screen1(self):
        self.frame2.pack_forget()
        self.frame1.pack(fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseManager(root)
    root.mainloop()
