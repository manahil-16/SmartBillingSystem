import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class EliteBillingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Nexus AI | Advanced Billing Terminal")
        self.root.geometry("1100x750")
        self.root.configure(bg="#0f172a")

        # Menu Data
        self.menu = {
            "Espresso": {"price": 350, "suggest": "Extra Shot"},
            "Caramel Latte": {"price": 550, "suggest": "Blueberry Muffin"},
            "Club Sandwich": {"price": 650, "suggest": "French Fries"},
            "Zinger Burger": {"price": 750, "suggest": "Cold Drink"},
            "Beef Steak": {"price": 1200, "suggest": "Mashed Potatoes"},
            "Pasta Alfredo": {"price": 850, "suggest": "Garlic Bread"},
            "Fresh Juice": {"price": 400, "suggest": "Fruit Salad"}
        }

        self.setup_ui()

    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#1e293b", pady=15)
        header.pack(fill=tk.X)
        tk.Label(header, text="SMART CAFE", font=("Segoe UI", 20, "bold"), 
                 bg="#1e293b", fg="#10b981").pack()

        main_frame = tk.Frame(self.root, bg="#0f172a", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- LEFT: INPUT PANEL ---
        left_panel = tk.LabelFrame(main_frame, text=" Transaction Console ", font=("Arial", 10, "bold"),
                                   bg="#1e293b", fg="white", padx=20, pady=20)
        left_panel.place(x=0, y=0, width=460, height=620)
        # Customer ID/Number
        self.create_label(left_panel, "Customer ID / Number:")
        self.cust_num_ent = self.create_entry(left_panel)
        # Customer Name
        self.create_label(left_panel, "Customer Name:")
        self.name_ent = self.create_entry(left_panel)
        # Item Selection
        self.create_label(left_panel, "Select Product:")
        self.item_cb = ttk.Combobox(left_panel, values=list(self.menu.keys()), state="readonly", font=("Arial", 11))
        self.item_cb.pack(fill=tk.X, pady=(5, 15))
        self.item_cb.bind("<<ComboboxSelected>>", self.sync_values)
        # Quantity
        self.create_label(left_panel, "Quantity:")
        self.qty_ent = self.create_entry(left_panel)
        self.qty_ent.insert(0, "1")
        self.qty_ent.bind("<KeyRelease>", self.sync_values)
        # Automated Fields (Read-Only)
        self.create_label(left_panel, "Unit Price (Rs.):")
        self.price_ent = self.create_auto_field(left_panel, "#38bdf8")
        self.create_label(left_panel, "AI Automated Discount (Rs.):")
        self.disc_ent = self.create_auto_field(left_panel, "#fbbf24")
        # --- BUTTONS ---
        btn_frame = tk.Frame(left_panel, bg="#1e293b")
        btn_frame.pack(fill=tk.X, pady=20)
        tk.Button(btn_frame, text="Generate Bill", command=self.generate, bg="#10b981", fg="black", 
                  font=("Arial", 10, "bold"), width=14, pady=8).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Reset", command=self.reset, bg="#64748b", fg="white", 
                  font=("Arial", 10, "bold"), width=10, pady=8).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Exit", command=self.root.destroy, bg="#ef4444", fg="white", 
                  font=("Arial", 10, "bold"), width=10, pady=8).grid(row=0, column=2, padx=5)
        # --- RIGHT: RECEIPT ---
        receipt_card = tk.Frame(main_frame, bg="white", padx=2, pady=2)
        receipt_card.place(x=490, y=0, width=500, height=620)
        self.receipt_box = tk.Text(receipt_card, font=("Consolas", 10), bg="#f8fafc", bd=0, padx=20, pady=20)
        self.receipt_box.pack(fill=tk.BOTH, expand=True)
        self.receipt_box.insert(tk.END, "\n\n\n\t   [ SYSTEM READY ]\n\tWaiting for Transaction...")
        self.receipt_box.config(state="disabled")
    def create_label(self, parent, txt):
        tk.Label(parent, text=txt, bg="#1e293b", fg="#94a3b8", font=("Arial", 9, "bold")).pack(anchor="w")
    def create_entry(self, parent):
        e = tk.Entry(parent, font=("Arial", 11), bg="#0f172a", fg="white", insertbackground="white", bd=0)
        e.pack(fill=tk.X, pady=(5, 15), ipady=5)
        return e
    def create_auto_field(self, parent, color):
        e = tk.Entry(parent, font=("Arial", 11, "bold"), bg="#1e293b", fg=color, bd=0)
        e.pack(fill=tk.X, pady=(5, 15))
        e.insert(0, "0.00")
        e.config(state="readonly")
        return e
    def sync_values(self, event=None):
        """Triggers live updates for Price and Automated Discount."""
        item = self.item_cb.get()
        if item in self.menu:
            price = self.menu[item]["price"]
            # Update Price Field
            self.price_ent.config(state="normal")
            self.price_ent.delete(0, tk.END)
            self.price_ent.insert(0, f"{price:.2f}")
            self.price_ent.config(state="readonly")

            # Update Discount Field
            try:
                qty = int(self.qty_ent.get() if self.qty_ent.get() else 0)
                subtotal = price * qty
                discount = 0
                
                if qty >= 5:
                    discount = subtotal * 0.15 # 15% Bulk AI Rule
                elif subtotal > 2500:
                    discount = 250 # Loyalty AI Rule
                
                self.disc_ent.config(state="normal")
                self.disc_ent.delete(0, tk.END)
                self.disc_ent.insert(0, f"{discount:.2f}")
                self.disc_ent.config(state="readonly")
            except ValueError:
                pass

    def generate(self):
        try:
            cid = self.cust_num_ent.get().strip()
            name = self.name_ent.get().strip()
            item = self.item_cb.get()
            qty = int(self.qty_ent.get())
            price = float(self.price_ent.get())
            disc = float(self.disc_ent.get())

            if not cid or not name or not item:
                raise ValueError("Missing Data")

            total = (price * qty) - disc

            self.receipt_box.config(state="normal")
            self.receipt_box.delete(1.0, tk.END)
            
            bill = f"""
{' NEXUS AI CAFE & GRILL ':=^40}
Date: {datetime.now().strftime('%d-%m-%Y %H:%M')}
{'='*40}
CUSTOMER ID:   {cid}
CUSTOMER NAME: {name.upper()}
{'-'*40}
ITEM                QTY      PRICE
{item:<18} {qty:<8} {price:>10.2f}
{'-'*40}
SUBTOTAL:                Rs. {price*qty:>10.2f}
AI AUTO DISCOUNT:        Rs. {disc:>10.2f}
{'-'*40}
GRAND TOTAL:             Rs. {total:>10.2f}
{'-'*40}

[AI RECOMMENDATION]
Since you picked {item},
our system suggests: {self.menu[item]['suggest']}

{' THANK YOU FOR YOUR BUSINESS ':=^40}
            """
            self.receipt_box.insert(tk.END, bill)
            self.receipt_box.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Error", "Please fill all fields with valid information.")

    def reset(self):
        self.cust_num_ent.delete(0, tk.END)
        self.name_ent.delete(0, tk.END)
        self.qty_ent.delete(0, tk.END)
        self.qty_ent.insert(0, "1")
        self.item_cb.set('')
        for ent in [self.price_ent, self.disc_ent]:
            ent.config(state="normal")
            ent.delete(0, tk.END)
            ent.insert(0, "0.00")
            ent.config(state="readonly")
        self.receipt_box.config(state="normal")
        self.receipt_box.delete(1.0, tk.END)
        self.receipt_box.insert(tk.END, "\n\n\n\t   [ SYSTEM READY ]\n\tWaiting for Transaction...")
        self.receipt_box.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = EliteBillingSystem(root)
    root.mainloop()