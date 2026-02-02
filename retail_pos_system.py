import csv
import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk, ImageDraw


def load_inventory(filename='inventory_text.csv'):
    inventory_data = []

    try:
        with open(filename, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for parts in reader:
                if len(parts) < 6:
                    continue
                inventory_data.append({
                    "id": int(parts[0]),
                    "name": parts[1],
                    "price": float(parts[2]),
                    "size": parts[3],
                    "quantity": int(parts[4]),
                    "color": parts[5]
                })
    except (FileNotFoundError, ValueError):
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            pass
    return inventory_data


def save_inventory(inventory_data, filename='inventory_text.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for item in inventory_data:
            writer.writerow([
                item['id'], item['name'], item['price'],
                item['size'], item['quantity'], item['color']
            ])


class ModernButton(tk.Button):
    def __init__(self, master, text, command, bg_color="#34495e", hover_color="#2c3e50", **kwargs):
        super().__init__(master, text=text, command=command, bg=bg_color, fg="white",
                         font=("Segoe UI", 11), relief="flat", activebackground=hover_color,
                         activeforeground="white", cursor="hand2", **kwargs)
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, _event):
        self['background'] = self.hover_color

    def on_leave(self, _event):
        self['background'] = self.bg_color


class ScrollableFrame(tk.Frame):
    def __init__(self, container, bg_color):
        super().__init__(container, bg=bg_color)
        canvas = tk.Canvas(self, bg=bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_window = tk.Frame(canvas, bg=bg_color)

        self.scrollable_window.bind(
            "<Configure>",
            lambda _e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.scrollable_window, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.canvas = canvas


class InventoryApp:
    def __init__(self, root_window):
        self.root = root_window
        self.root.title("Modern Store POS")
        self.root.geometry("1200x800")
        self.img_folder = "product_images"

        try:
            self.root.state('zoomed')
        except tk.TclError:
            self.root.attributes('-zoomed', True)

        self.col_sidebar = "#1e272e"
        self.col_bg = "#ecf0f1"
        self.col_card = "#ffffff"

        self.root.configure(bg=self.col_bg)

        self.inventory = load_inventory("inventory_text.csv")
        self.cart = []
        self.photo_cache = []

        self.sidebar = tk.Frame(self.root, bg=self.col_sidebar, width=280)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(self.sidebar, text="🛍️ MY SHOP", bg=self.col_sidebar, fg="white",
                 font=("Segoe UI", 22, "bold")).pack(pady=(40, 40))

        self.create_sidebar_btn("View All Products", self.buy_items)
        self.create_sidebar_btn("Search by Category", self.browse_category)
        self.create_sidebar_btn("Search by Size", self.search_by_size)
        self.create_sidebar_btn("Admin: Add Item", self.admin_add_item)

        tk.Frame(self.sidebar, bg=self.col_sidebar, height=50).pack()

        self.btn_cart = ModernButton(self.sidebar, text="🛒 View Cart (0)",
                                     command=self.checkout, bg_color="#00b894", hover_color="#00a884")
        self.btn_cart.pack(fill="x", padx=20, pady=10)

        self.create_sidebar_btn("Exit", self.root.quit, bg="#d63031", hover="#c0392b")

        self.content = tk.Frame(self.root, bg=self.col_bg)
        self.content.pack(side="right", fill="both", expand=True)

        self.header_label = tk.Label(self.content, text="Product Catalog", bg=self.col_bg,
                                     fg="#2d3436", font=("Segoe UI", 24))
        self.header_label.pack(pady=20, padx=30, anchor="w")

        self.scroll_frame = ScrollableFrame(self.content, self.col_bg)
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.grid_area = self.scroll_frame.scrollable_window

        self.buy_items()

    def create_sidebar_btn(self, text, command, bg="#1e272e", hover="#34495e"):
        btn = ModernButton(self.sidebar, text=text, command=command, bg_color=bg, hover_color=hover)
        btn.pack(fill="x", pady=5, padx=20)

    def get_image(self, item_id):
        path = f"{self.img_folder}/{item_id}"
        found_path = None

        for ext in [".jpg", ".png", ".jpeg"]:
            if os.path.exists(path + ext):
                found_path = path + ext
                break

        if found_path:
            try:
                img = Image.open(found_path)
                img = img.resize((180, 180), Image.Resampling.LANCZOS)
                return ImageTk.PhotoImage(img)
            except Exception:
                pass

        img = Image.new('RGB', (180, 180), color="#b2bec3")
        draw = ImageDraw.Draw(img)
        draw.text((70, 80), "No Image", fill="white")
        return ImageTk.PhotoImage(img)

    def display_items(self, items, title_text):
        self.header_label.config(text=title_text)

        for widget in self.grid_area.winfo_children():
            widget.destroy()
        self.photo_cache = []

        if not items:
            tk.Label(self.grid_area, text="No items found.", bg=self.col_bg,
                     font=("Segoe UI", 14)).pack()
            return

        columns = 4
        row = 0
        col = 0

        for item in items:
            card = tk.Frame(self.grid_area, bg="white",
                            highlightbackground="#dfe6e9", highlightthickness=1)
            card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")

            photo = self.get_image(item['id'])
            self.photo_cache.append(photo)
            tk.Label(card, image=photo, bg="white").pack(pady=10)

            tk.Label(card, text=item['name'], font=("Segoe UI", 12, "bold"),
                     bg="white", fg="#2d3436").pack()
            tk.Label(card, text=f"Size: {item['size']} | {item['color']}",
                     font=("Segoe UI", 9), bg="white", fg="#636e72").pack()
            tk.Label(card, text=f"${item['price']}", font=("Segoe UI", 14, "bold"),
                     bg="white", fg="#d63031").pack(pady=5)

            if item['quantity'] > 0:
                stock_txt = f"In Stock: {item['quantity']}"
                state = "normal"
                btn_bg = "#0984e3"
                stock_fg = "#00b894"
            else:
                stock_txt = "Out of Stock"
                state = "disabled"
                btn_bg = "#b2bec3"
                stock_fg = "#d63031"

            tk.Label(card, text=stock_txt, font=("Segoe UI", 9, "bold"),
                     bg="white", fg=stock_fg).pack()

            tk.Button(card, text="ADD TO CART", bg=btn_bg, fg="white",
                      font=("Segoe UI", 9, "bold"), relief="flat", pady=5, state=state,
                      command=lambda x=item: self.add_to_cart_action(x)).pack(fill="x", padx=15, pady=15)

            col += 1
            if col >= columns:
                col = 0
                row += 1

    def add_to_cart_action(self, item_data):
        real_item = next((i for i in self.inventory if i['id'] == item_data['id']), None)
        if real_item and real_item['quantity'] > 0:
            self.cart.append(real_item.copy())
            self.update_cart_btn()
            messagebox.showinfo("Success", f"Added {real_item['name']} to cart")
        else:
            messagebox.showwarning("Error", "Item is out of stock")

    def update_cart_btn(self):
        count = len(self.cart)
        self.btn_cart.config(text=f"🛒 View Cart ({count})")

    def buy_items(self):
        self.display_items(self.inventory, "All Products")

    def search_by_size(self):
        size = simpledialog.askstring("Search", "Enter size (S/M/L):")
        if size:
            res = [i for i in self.inventory if i['size'].lower() == size.lower()]
            self.display_items(res, f"Results for Size: {size}")

    def browse_category(self):
        prompt_text = "Select Category:\n1. Hoodie\n2. Crewneck\n\nEnter number (1 or 2):"
        choice = simpledialog.askinteger("Category", prompt_text)

        if choice is None:
            return

        categories = {1: "Hoodie", 2: "Crewneck"}

        if choice in categories:
            term = categories[choice]
            results = [i for i in self.inventory if term.lower() in i['name'].lower()]

            if results:
                self.display_items(results, f"Category: {term}")
            else:
                messagebox.showinfo("No Results", f"No items found matching '{term}'.")
        else:
            messagebox.showwarning("Invalid", "Please enter 1 or 2.")

    def admin_add_item(self):
        try:
            id_item = simpledialog.askinteger("Admin", "Item ID:")
            if id_item is None:
                return
            if any(item['id'] == id_item for item in self.inventory):
                messagebox.showerror("Error", "This Item ID already exists!")
                return

            name_item = simpledialog.askstring("Admin", "Name:")
            if not name_item or name_item.strip().isdigit():
                messagebox.showerror("Invalid", "Name cannot be empty or numbers.")
                return

            price_item = simpledialog.askfloat("Admin", "Price:")
            if price_item is None or price_item < 0:
                messagebox.showerror("Invalid", "Price must be positive.")
                return

            size_item = simpledialog.askstring("Admin", "Size:")
            if not size_item or size_item.strip().isdigit():
                messagebox.showerror("Invalid", "Size cannot be just numbers.")
                return

            qty_item = simpledialog.askinteger("Admin", "Qty:")
            if qty_item is None or qty_item < 0:
                messagebox.showerror("Invalid", "Quantity cannot be negative.")
                return

            color_item = simpledialog.askstring("Admin", "Color:")
            if not color_item or color_item.strip().isdigit():
                messagebox.showerror("Invalid", "Color cannot be just numbers.")
                return

            new_item = {
                "id": id_item, "name": name_item, "price": price_item,
                "size": size_item, "quantity": qty_item, "color": color_item
            }
            self.inventory.append(new_item)
            save_inventory(self.inventory, "inventory_text.csv")
            messagebox.showinfo("Done", "Item added successfully!")
            self.buy_items()

        except Exception as error:
            messagebox.showerror("Error", f"An error occurred: {error}")

    def checkout(self):
        if not self.cart:
            messagebox.showinfo("Empty", "Cart is empty")
            return

        total = sum(i['price'] for i in self.cart)
        vat_total = round(total * 1.14, 2)

        txt = ("-------------------------------\n"
               "        OFFICIAL RECEIPT       \n"
               "-------------------------------\n")
        for i in self.cart:
            txt += f"{i['name']:<20} ${i['price']}\n"
        txt += "-------------------------------\n"
        txt += f"TOTAL (incl. VAT):   ${vat_total}\n"
        txt += "-------------------------------"

        messagebox.showinfo("Checkout", txt)

        for c_item in self.cart:
            real_item = next((i for i in self.inventory if i['id'] == c_item['id']), None)
            if real_item:
                real_item['quantity'] -= 1

        save_inventory(self.inventory, "inventory_text.csv")
        self.cart = []
        self.update_cart_btn()
        self.buy_items()


if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()