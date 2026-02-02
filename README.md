# PyRetail POS System 🛍️

A desktop-based Point of Sale (POS) application designed for small retail environments. This system manages inventory, processes sales transactions, and provides real-time stock updates using a persistent CSV database.

## 🚀 Features
- **Inventory Management:** Add, update, and track items with details like size, colour, and stock level.
- **Robust Validation:** Prevents data corruption by validating user inputs (e.g., rejecting numeric values for names, ensuring unique IDs).
- **Persistent Storage:** Custom file-handling logic to save/load data from CSV, ensuring no data loss between sessions.
- **Modern UI:** A responsive, grid-based interface built with Tkinter using custom rounded elements and dynamic scrolling.
- **Shopping Cart Logic:** Real-time total calculation with VAT support.

## 🛠️ Technical Stack
- **Language:** Python 3.x
- **GUI:** Tkinter (Custom implementations for modern widgets)
- **Database:** CSV (File I/O)
- **Image Processing:** PIL (Pillow) for dynamic product rendering.

## 📦 How to Run
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/mohamed67-source/Retail-POS-System.git](https://github.com/mohamed67-source/Retail-POS-System.git)
