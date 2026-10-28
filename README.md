# 🛒 SnapKart - Business Hours Aware Billing and Inventory System

SnapKart is a desktop retail management system built with Python, Tkinter, and MySQL[cite: 1]. It includes two separate interfaces: an **Admin Dashboard** for store owners and a **Customer Storefront** for shoppers[cite: 2, 3].

A key feature of SnapKart is **Business Hours Control**: customers can only place orders when the store is open[cite: 1, 3]. If the store is closed, checkout locks automatically[cite: 1].

---

## 🌟 Key Features

### 1. Customer Shopping Application (`user_app`)
* **Category Browsing:** Browse products by departments like Groceries, Dairy, Snacks, and Tech[cite: 3].
* **Live Search:** Search items instantly by name[cite: 3].
* **Interactive Cart:** Add items, change quantities, and see live bill updates[cite: 3].
* **Time-Aware Checkout:** Real-time check to confirm the store is open before processing any sale[cite: 1].
* **Digital Receipts:** Automatically creates and saves order receipts to a text file.

### 2. Admin & Store Manager Portal (`admin_app`)
* **Live Analytics Dashboard:** View total sales today, items sold, low stock alerts, and real sales charts powered by Matplotlib[cite: 2].
* **Product Management:** Add new items, edit prices, update stock, and delete products.
* **Store Hours Control:** Set opening and closing times for each day of the week, or close the store with one click[cite: 2].
* **Low Stock Alerts:** Highlights items when warehouse stock drops below 20 units[cite: 2].

### 3. Automated Business Reports (`data_analysis`)
* Uses **Pandas** and **NumPy** to read sales and inventory data from MySQL[cite: 1].
* Exports two CSV reports to the `reports/` folder[cite: 1]:
  * `daily_sales_summary.csv`
  * `inventory_restock_report.csv`

---

## 🛠️ Tech Stack

* **Programming Language:** Python[cite: 1]
* **User Interface (GUI):** Tkinter[cite: 1]
* **Database:** MySQL (connected via `mysql-connector-python`)[cite: 1]
* **Data Analytics:** Pandas, NumPy[cite: 1]
* **Data Visualization:** Matplotlib[cite: 1]
* **Version Control:** Git & GitHub[cite: 1]

---

## 📁 Project Structure

```text
smart_store_project/
│
├── common/                     # Shared tools and status checks
│   ├── __init__.py
│   ├── store_status.py         # Business hours checking logic
│   └── utils.py                # Digital receipt generator
│
├── database/                   # MySQL configuration and setup
│   ├── __init__.py
│   ├── db_connection.py        # MySQL connection function
│   ├── setup_db.py             # Database and table creation script
│   ├── populate_inventory.py   # Populates products into MySQL
│   └── schema.sql              # MySQL DDL table schema
│
├── admin_app/                  # Admin portal desktop files
│   ├── __init__.py
│   ├── admin_main.py           # Modern admin dashboard (Smart POS)
│   ├── billing_pos_ui.py       # POS Billing Terminal
│   ├── inventory_ui.py         # Product management table & restock
│   ├── store_settings_ui.py    # Business hours settings
│   ├── transactions_ui.py      # Transaction logs & PDF reprint
│   └── analytics_ui.py         # Matplotlib chart view
│
├── user_app/                   # Customer storefront desktop files
│   ├── __init__.py
│   ├── user_main.py            # Customer shopping window and cart
│   ├── auth_ui.py              # Customer login/register dialog
│   └── upi_payment_dialog.py   # Simulated UPI payment gateway
│
├── data_analysis/              # Data reports
│   ├── __init__.py
│   └── sales_report.py         # Pandas/NumPy CSV report generator
│
├── logo/                       # Official application branding logos
│   ├── Neon Blue Futuristic Shopping Cart.png  # Emblem without text (icons & navbars)
│   └── SnapKart Smart Store Logo.png          # Full logo with text (PDFs & banners)
├── receipts/                   # Auto-generated GST Tax Invoices (.pdf)
├── reports/                    # Auto-generated PDF & CSV executive reports
├── main.py                     # Central app launcher (Tkinter)
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation

---

## 🚀 Running the Project

### Virtual Environment Setup
Ensure the project's virtual environment is activated before running commands:
```powershell
.\venv\Scripts\Activate.ps1
```
*(Or invoke directly using `.\venv\Scripts\python.exe <script>`)*

### 1. Run via Central Desktop Launcher
Launch the central application launcher:
```powershell
python main.py
```
From the launcher, you can:
* Open the **Customer Storefront** (`user_app.user_main`)
* Open the **Admin Portal & POS Terminal** (`admin_app.admin_main`)
* Generate **Executive PDF & CSV Reports** with 1 click (`data_analysis.sales_report`)

### 2. Run Standalone Desktop Modules
* **Customer Shopping Storefront:**
  ```powershell
  python -m user_app.user_main
  ```
* **Admin Dashboard & POS Control:**
  ```powershell
  python -m admin_app.admin_main
  ```
* **Automated Executive PDF & CSV Reports (Pandas & ReportLab):**
  ```powershell
  python -m data_analysis.sales_report
  ```
## Configuration and first run

1. Create the MySQL database and tables with `python database/setup_db.py`.
2. Set the database environment variables shown in `.env.example` before opening the app.
3. Run `python database/populate_inventory.py` once to add the starter catalogue to an empty database.
4. Start the desktop launcher with `python main.py`.

The starter catalogue is intentionally modest and varied. It does not replace existing products or sales. To deliberately reset demo data, run `python database/populate_inventory.py --replace`.

