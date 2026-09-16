import tkinter as tk
from tkinter import ttk, messagebox

import settings
import products
import customers
import orders
import payments
import inventory
import reports
import calculator
import validator
import logger

class ShopSystem:
    def __init__(self, root):
        self.root = root
        self.root.title(settings.APP_TITLE)
        self.root.geometry(settings.WINDOW_SIZE)
        self.root.configure(bg=settings.BG)
        self.root.resizable(False, False)

        self.cart = []
        self.current_customer = "Walk-in Customer"

        self.setup_style()
        self.build_layout()
        self.show_dashboard()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background=settings.PANEL,
            foreground=settings.TEXT,
            fieldbackground=settings.PANEL,
            rowheight=30,
            font=("Arial", 10)
        )
        style.configure(
            "Treeview.Heading",
            background=settings.ACCENT,
            foreground="white",
            font=("Arial", 10, "bold")
        )

    def build_layout(self):
        self.sidebar = tk.Frame(self.root, bg=settings.SIDEBAR, width=210)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar, text="🛍 JIN SHOP",
            bg=settings.SIDEBAR, fg=settings.TEXT,
            font=("Arial", 20, "bold")
        ).pack(pady=(25, 5))

        tk.Label(
            self.sidebar, text="SHOP MANAGEMENT",
            bg=settings.SIDEBAR, fg="#9AA1B2",
            font=("Arial", 9)
        ).pack(pady=(0, 25))

        buttons = [
            ("🏠 Dashboard", self.show_dashboard),
            ("📦 Products", self.show_products),
            ("👤 Customers", self.show_customers),
            ("🛒 New Order", self.show_order),
            ("📊 Reports", self.show_reports),
        ]

        for text, command in buttons:
            tk.Button(
                self.sidebar, text=text, command=command,
                bg=settings.SIDEBAR, fg=settings.TEXT,
                activebackground=settings.ACCENT,
                activeforeground="white", relief="flat",
                anchor="w", padx=25, pady=12,
                font=("Arial", 11, "bold"), cursor="hand2"
            ).pack(fill="x")

        tk.Button(
            self.sidebar, text="✕ Exit", command=self.exit_app,
            bg=settings.SIDEBAR, fg=settings.DANGER,
            activebackground=settings.DANGER,
            activeforeground="white", relief="flat",
            anchor="w", padx=25, pady=12,
            font=("Arial", 11, "bold"), cursor="hand2"
        ).pack(side="bottom", fill="x", pady=15)

        self.content = tk.Frame(self.root, bg=settings.BG)
        self.content.pack(side="right", fill="both", expand=True)

    def clear(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def title(self, text, subtitle=""):
        tk.Label(
            self.content, text=text, bg=settings.BG, fg=settings.TEXT,
            font=("Arial", 23, "bold")
        ).pack(anchor="w", padx=30, pady=(25, 3))
        if subtitle:
            tk.Label(
                self.content, text=subtitle, bg=settings.BG, fg="#9AA1B2",
                font=("Arial", 10)
            ).pack(anchor="w", padx=30, pady=(0, 18))

    def card(self, parent, label, value, color):
        frame = tk.Frame(parent, bg=settings.PANEL, width=190, height=105)
        frame.pack(side="left", padx=7)
        frame.pack_propagate(False)
        tk.Label(frame, text=label, bg=settings.PANEL, fg="#9AA1B2",
                 font=("Arial", 10)).pack(anchor="w", padx=15, pady=(15, 4))
        tk.Label(frame, text=value, bg=settings.PANEL, fg=color,
                 font=("Arial", 20, "bold")).pack(anchor="w", padx=15)

    def show_dashboard(self):
        self.clear()
        self.title("Dashboard", "ภาพรวมระบบร้านค้า")

        row = tk.Frame(self.content, bg=settings.BG)
        row.pack(fill="x", padx=22)

        sale = reports.total_sales(orders.get_all())
        count = reports.total_orders(orders.get_all())
        stock_count = sum(p["stock"] for p in products.get_all())
        low = len(reports.low_stock(products.get_all()))

        self.card(row, "ยอดขายทั้งหมด", f"{sale:,.2f}", settings.SUCCESS)
        self.card(row, "จำนวนออเดอร์", str(count), settings.ACCENT)
        self.card(row, "สินค้าในสต็อก", str(stock_count), settings.WARNING)
        self.card(row, "สินค้าใกล้หมด", str(low), settings.DANGER)

        tk.Label(
            self.content, text="สินค้า", bg=settings.BG, fg=settings.TEXT,
            font=("Arial", 16, "bold")
        ).pack(anchor="w", padx=30, pady=(30, 10))

        tree = self.product_tree(self.content)
        for p in products.get_all():
            tree.insert("", "end", values=(
                p["id"], p["name"], f"{p['price']:,.2f}", p["stock"]
            ))

    def product_tree(self, parent):
        frame = tk.Frame(parent, bg=settings.BG)
        frame.pack(fill="both", expand=True, padx=30, pady=5)

        tree = ttk.Treeview(
            frame, columns=("id", "name", "price", "stock"),
            show="headings", height=13
        )
        for col, text, width in [
            ("id", "ID", 60), ("name", "สินค้า", 300),
            ("price", "ราคา", 160), ("stock", "สต็อก", 140)
        ]:
            tree.heading(col, text=text)
            tree.column(col, width=width, anchor="center")
        tree.pack(fill="both", expand=True)
        return tree

    def show_products(self):
        self.clear()
        self.title("Products", "จัดการสินค้าและสต็อก")

        form = tk.Frame(self.content, bg=settings.PANEL)
        form.pack(fill="x", padx=30, pady=5)

        entries = {}
        for i, (label, key) in enumerate([
            ("ชื่อสินค้า", "name"), ("ราคา", "price"), ("จำนวน", "stock")
        ]):
            tk.Label(form, text=label, bg=settings.PANEL, fg=settings.TEXT).grid(
                row=0, column=i*2, padx=10, pady=15
            )
            e = tk.Entry(form, width=18)
            e.grid(row=0, column=i*2+1, padx=5)
            entries[key] = e

        def add():
            name = entries["name"].get()
            price = entries["price"].get()
            stock = entries["stock"].get()

            if not validator.valid_text(name) or not validator.valid_positive_number(price) or not validator.valid_positive_int(stock):
                messagebox.showerror("Error", "กรุณากรอกข้อมูลให้ถูกต้อง")
                return

            p = products.add_product(name, price, stock)
            logger.log(f"เพิ่มสินค้า {p['name']}")
            messagebox.showinfo("สำเร็จ", "เพิ่มสินค้าเรียบร้อย")
            self.show_products()

        tk.Button(
            form, text="+ เพิ่มสินค้า", command=add,
            bg=settings.SUCCESS, fg="white", relief="flat",
            font=("Arial", 10, "bold"), padx=15, pady=7
        ).grid(row=0, column=6, padx=15)

        tree = self.product_tree(self.content)
        for p in products.get_all():
            tree.insert("", "end", values=(
                p["id"], p["name"], f"{p['price']:,.2f}", p["stock"]
            ))

    def show_customers(self):
        self.clear()
        self.title("Customers", "จัดการข้อมูลลูกค้า")

        form = tk.Frame(self.content, bg=settings.PANEL)
        form.pack(fill="x", padx=30, pady=5)

        tk.Label(form, text="ชื่อลูกค้า", bg=settings.PANEL, fg=settings.TEXT).grid(row=0, column=0, padx=10, pady=15)
        name = tk.Entry(form, width=25)
        name.grid(row=0, column=1)

        tk.Label(form, text="เบอร์โทร", bg=settings.PANEL, fg=settings.TEXT).grid(row=0, column=2, padx=10)
        phone = tk.Entry(form, width=20)
        phone.grid(row=0, column=3)

        def add():
            if not validator.valid_text(name.get()):
                messagebox.showerror("Error", "กรุณาใส่ชื่อลูกค้า")
                return
            customers.add_customer(name.get(), phone.get())
            logger.log(f"เพิ่มลูกค้า {name.get()}")
            self.show_customers()

        tk.Button(form, text="+ เพิ่มลูกค้า", command=add,
                  bg=settings.SUCCESS, fg="white", relief="flat",
                  font=("Arial", 10, "bold"), padx=15, pady=7).grid(row=0, column=4, padx=15)

        tree = ttk.Treeview(self.content, columns=("id", "name", "phone"), show="headings", height=17)
        for col, text, width in [("id","ID",80),("name","ชื่อ",300),("phone","เบอร์โทร",250)]:
            tree.heading(col, text=text)
            tree.column(col, width=width, anchor="center")
        tree.pack(fill="both", expand=True, padx=30, pady=15)

        for c in customers.get_all():
            tree.insert("", "end", values=(c["id"], c["name"], c["phone"]))

    def show_order(self):
        self.clear()
        self.title("New Order", "สร้างรายการสั่งซื้อ")

        top = tk.Frame(self.content, bg=settings.PANEL)
        top.pack(fill="x", padx=30)

        tk.Label(top, text="ลูกค้า:", bg=settings.PANEL, fg=settings.TEXT).pack(side="left", padx=10, pady=15)
        customer = tk.Entry(top, width=25)
        customer.insert(0, self.current_customer)
        customer.pack(side="left")

        self.cart = []

        tree = ttk.Treeview(
            self.content,
            columns=("id", "name", "price", "qty", "total"),
            show="headings", height=10
        )
        for col, text, width in [
            ("id","ID",60),("name","สินค้า",240),("price","ราคา",120),
            ("qty","จำนวน",100),("total","รวม",140)
        ]:
            tree.heading(col, text=text)
            tree.column(col, width=width, anchor="center")
        tree.pack(fill="both", expand=True, padx=30, pady=15)

        controls = tk.Frame(self.content, bg=settings.BG)
        controls.pack(fill="x", padx=30)

        tk.Label(controls, text="Product ID", bg=settings.BG, fg=settings.TEXT).pack(side="left")
        pid = tk.Entry(controls, width=8)
        pid.pack(side="left", padx=5)
        tk.Label(controls, text="จำนวน", bg=settings.BG, fg=settings.TEXT).pack(side="left")
        qty = tk.Entry(controls, width=8)
        qty.insert(0, "1")
        qty.pack(side="left", padx=5)

        total_label = tk.Label(
            controls, text="Total: 0.00 บาท",
            bg=settings.BG, fg=settings.SUCCESS,
            font=("Arial", 15, "bold")
        )
        total_label.pack(side="right")

        def refresh_cart():
            tree.delete(*tree.get_children())
            subtotal = payments.calculate_subtotal(self.cart)
            tax = payments.calculate_tax(subtotal, settings.TAX_RATE)
            total = payments.calculate_total(subtotal, tax)
            for item in self.cart:
                tree.insert("", "end", values=(
                    item["id"], item["name"], f"{item['price']:,.2f}",
                    item["quantity"], f"{item['price']*item['quantity']:,.2f}"
                ))
            total_label.config(text=f"Total: {total:,.2f} บาท")

        def add():
            try:
                product = products.find(int(pid.get()))
                amount = int(qty.get())
            except ValueError:
                product, amount = None, 0

            if not product or amount <= 0:
                messagebox.showerror("Error", "Product ID หรือจำนวนไม่ถูกต้อง")
                return

            already = sum(x["quantity"] for x in self.cart if x["id"] == product["id"])
            if product["stock"] - already < amount:
                messagebox.showerror("Error", "สินค้าในสต็อกไม่เพียงพอ")
                return

            existing = next((x for x in self.cart if x["id"] == product["id"]), None)
            if existing:
                existing["quantity"] += amount
            else:
                self.cart.append({
                    "id": product["id"], "name": product["name"],
                    "price": product["price"], "quantity": amount
                })
            refresh_cart()

        def checkout():
            if not self.cart:
                messagebox.showerror("Error", "ยังไม่มีสินค้าในตะกร้า")
                return

            customer_name = customer.get().strip() or "Walk-in Customer"
            subtotal = payments.calculate_subtotal(self.cart)
            tax = payments.calculate_tax(subtotal, settings.TAX_RATE)
            total = payments.calculate_total(subtotal, tax)

            for item in self.cart:
                p = products.find(item["id"])
                inventory.reduce_stock(p, item["quantity"])

            order = orders.create_order(customer_name, self.cart.copy(), total)
            logger.log(f"สร้างออเดอร์ #{order['id']} ยอด {total:.2f}")
            messagebox.showinfo("ชำระเงินสำเร็จ", f"ยอดสุทธิ {total:,.2f} บาท")
            self.cart = []
            self.show_dashboard()

        tk.Button(controls, text="เพิ่มลงตะกร้า", command=add,
                  bg=settings.ACCENT, fg="white", relief="flat",
                  font=("Arial", 10, "bold"), padx=15, pady=7).pack(side="left", padx=10)
        tk.Button(controls, text="✓ ชำระเงิน", command=checkout,
                  bg=settings.SUCCESS, fg="white", relief="flat",
                  font=("Arial", 10, "bold"), padx=15, pady=7).pack(side="left")

    def show_reports(self):
        self.clear()
        self.title("Reports", "รายงานยอดขายและสินค้าใกล้หมด")

        sale = reports.total_sales(orders.get_all())
        count = reports.total_orders(orders.get_all())
        low = reports.low_stock(products.get_all())

        row = tk.Frame(self.content, bg=settings.BG)
        row.pack(fill="x", padx=22)
        self.card(row, "ยอดขาย", f"{sale:,.2f} บาท", settings.SUCCESS)
        self.card(row, "ออเดอร์", str(count), settings.ACCENT)
        self.card(row, "ใกล้หมด", str(len(low)), settings.DANGER)

        tk.Label(self.content, text="สินค้าใกล้หมด",
                 bg=settings.BG, fg=settings.TEXT,
                 font=("Arial", 16, "bold")).pack(anchor="w", padx=30, pady=25)

        tree = self.product_tree(self.content)
        for p in low:
            tree.insert("", "end", values=(
                p["id"], p["name"], f"{p['price']:,.2f}", p["stock"]
            ))

    def exit_app(self):
        if messagebox.askyesno("Exit", "ต้องการออกจากโปรแกรมหรือไม่?"):
            logger.log("ปิดโปรแกรม")
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ShopSystem(root)
    root.mainloop()
