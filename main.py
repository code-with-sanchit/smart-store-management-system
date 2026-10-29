import os
import subprocess
import sys
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from common.store_status import check_store_status
from common.logo_utils import get_logo_image, set_window_icon


class SnapKartLauncher(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("SnapKart - Retail Application Launcher")
        self.geometry("680x540")
        self.resizable(False, False)
        self.configure(bg="#0f172a")

        # Set window icon to official logo
        set_window_icon(self)

        self.create_ui()
        self.update_live_badge()

    def create_ui(self):
        # 1. Header & Branding
        header_frame = tk.Frame(self, bg="#0f172a")
        header_frame.pack(fill=tk.X, pady=(25, 8))

        brand_row = tk.Frame(header_frame, bg="#0f172a")
        brand_row.pack()

        self.logo_img = get_logo_image(with_text=False, size=(48, 48))
        if self.logo_img:
            tk.Label(brand_row, image=self.logo_img, bg="#0f172a").pack(side=tk.LEFT, padx=(0, 10))

        tk.Label(
            brand_row,
            text="SnapKart",
            font=("Segoe UI", 25, "bold"),
            fg="#38bdf8",
            bg="#0f172a"
        ).pack(side=tk.LEFT)

        tk.Label(
            header_frame,
            text="Business Hours Aware Billing & Inventory Management System",
            font=("Segoe UI", 10),
            fg="#94a3b8",
            bg="#0f172a"
        ).pack(pady=(4, 0))

        # 2. Live Store Status Badge
        self.status_badge = tk.Label(
            self,
            text="Checking Store Hours...",
            font=("Segoe UI", 10, "bold"),
            bg="#1e293b",
            fg="#cbd5e1",
            padx=14,
            pady=6,
            relief=tk.SOLID,
            bd=1
        )
        self.status_badge.pack(pady=15)

        # 3. Action Cards Frame
        card_container = tk.Frame(self, bg="#0f172a")
        card_container.pack(fill=tk.BOTH, expand=True, padx=40, pady=10)

        # Button 1: Launch Customer App
        self.create_launch_button(
            parent=card_container,
            icon="🛍️",
            title="Launch Customer Storefront",
            subtitle="Shop products, manage cart, and real-time checkout",
            btn_color="#16a34a",
            command=self.open_customer_app
        )

        # Button 2: Launch Admin Dashboard
        self.create_launch_button(
            parent=card_container,
            icon="📊",
            title="Launch Admin Portal",
            subtitle="Inventory tracking, operating hours control, and sales charts",
            btn_color="#2563eb",
            command=self.open_admin_app
        )

        # Button 3: Generate Business & PDF Reports
        self.create_launch_button(
            parent=card_container,
            icon="📈",
            title="Generate Business & PDF Reports",
            subtitle="Export executive branded PDF report & analytical spreadsheets",
            btn_color="#7c3aed",
            command=self.run_reports_script
        )

        # 4. Footer
        footer = tk.Label(
            self,
            text="Sanjay Place, Agra - 282002 • Python + Tkinter + MySQL",
            font=("Segoe UI", 8),
            fg="#64748b",
            bg="#0f172a"
        )
        footer.pack(side=tk.BOTTOM, pady=15)

    def create_launch_button(self, parent, icon, title, subtitle, btn_color, command):
        frame = tk.Frame(parent, bg="#1e293b", bd=1, relief=tk.SOLID)
        frame.pack(fill=tk.X, pady=6, ipady=4)

        text_box = tk.Frame(frame, bg="#1e293b")
        text_box.pack(side=tk.LEFT, padx=15, pady=8)

        tk.Label(
            text_box,
            text=f"{icon}  {title}",
            font=("Segoe UI", 11, "bold"),
            fg="#ffffff",
            bg="#1e293b"
        ).pack(anchor="w")

        tk.Label(
            text_box,
            text=subtitle,
            font=("Segoe UI", 8),
            fg="#94a3b8",
            bg="#1e293b"
        ).pack(anchor="w")

        launch_btn = tk.Button(
            frame,
            text="Open ➔",
            font=("Segoe UI", 9, "bold"),
            bg=btn_color,
            fg="#ffffff",
            activebackground="#ffffff",
            relief=tk.FLAT,
            padx=16,
            pady=4,
            cursor="hand2",
            command=command
        )
        launch_btn.pack(side=tk.RIGHT, padx=15)

    def update_live_badge(self):
        is_open, msg = check_store_status()
        if is_open:
            self.status_badge.config(
                text="● STORE STATUS: OPEN (Accepting Orders)",
                bg="#064e3b",
                fg="#6ee7b7"
            )
        else:
            self.status_badge.config(
                text="● STORE STATUS: CLOSED (Transactions Locked)",
                bg="#7f1d1d",
                fg="#fca5a5"
            )

    def open_customer_app(self):
        subprocess.Popen([sys.executable, "-m", "user_app.user_main"], cwd=str(PROJECT_ROOT))

    def open_admin_app(self):
        subprocess.Popen([sys.executable, "-m", "admin_app.admin_main"], cwd=str(PROJECT_ROOT))

    def run_reports_script(self):
        from data_analysis.sales_report import generate_sales_and_inventory_reports
        from common.pdf_generator import open_pdf_file
        try:
            pdf_path = generate_sales_and_inventory_reports()
            if pdf_path and os.path.isfile(pdf_path):
                if messagebox.askyesno(
                    "Executive Reports Ready",
                    f"Official SnapKart Business Reports generated successfully!\n\n"
                    f"• Executive Branded PDF: {os.path.basename(pdf_path)}\n"
                    f"• CSV Spreadsheets in 'reports/' folder\n\n"
                    f"Open official PDF report now?"
                ):
                    open_pdf_file(pdf_path)
            else:
                messagebox.showinfo("Reports Generated", "Successfully exported reports to the 'reports/' folder!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate reports: {e}")


if __name__ == "__main__":
    app = SnapKartLauncher()
    app.mainloop()