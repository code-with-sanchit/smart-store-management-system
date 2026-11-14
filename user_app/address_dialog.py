"""
SnapKart - Delivery Address Confirmation & Update Dialog.
Prompts the user to review, edit, or enter their full delivery address every time an order is placed.
No default silent bypass.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox
from common.logo_utils import set_window_icon

# Standard localities supported by SnapKart delivery
DEFAULT_LOCALITIES = [
    "Sanjay Place Commercial Hub",
    "Civil Lines",
    "Fatehabad Road",
    "Kamla Nagar",
    "Tajganj Tourist Zone",
    "Dayalbagh Educational Enclave",
    "Shahganj Market",
    "Bodla Crossing",
    "Sikandra Industrial Belt",
    "Khandari",
    "Belanganj Wholesale Mandi",
    "Vasant Vihar Enclave"
]


def format_delivery_address(house: str, locality: str, city: str = "Agra", pincode: str = "282002") -> str:
    """Format structured address components into a clean single string for bills."""
    parts = [p.strip() for p in [house, locality, city] if p and p.strip()]
    addr = ", ".join(parts)
    if pincode and pincode.strip():
        addr += f" - {pincode.strip()}"
    return addr


def validate_address_fields(house: str, locality: str, pincode: str, phone: str) -> tuple[bool, str]:
    """Validate mandatory delivery address and contact fields."""
    if not house or not house.strip():
        return False, "Please enter your Flat / House number and street details."
    if not locality or not locality.strip():
        return False, "Please select or specify your delivery locality."
    clean_pin = pincode.strip()
    if not clean_pin or len(clean_pin) < 4:
        return False, "Please enter a valid PIN Code."
    clean_phone = phone.replace("+", "").replace(" ", "").replace("-", "")
    if not clean_phone or len(clean_phone) < 10:
        return False, "Please enter a valid 10-digit mobile number for delivery coordination."
    return True, ""


class AddressConfirmationDialog(tk.Toplevel):
    """
    Mandatory Address Confirmation Dialog for SnapKart Checkout.
    Requires user confirmation and allows editing address on every order placement.
    """

    def __init__(
        self,
        parent: tk.Widget,
        initial_house: str = "",
        initial_locality: str = "",
        initial_phone: str = "",
        on_confirmed = None
    ):
        super().__init__(parent)
        self.on_confirmed = on_confirmed
        self.confirmed_address = None

        set_window_icon(self)
        self.title("SnapKart - Confirm Delivery Address")
        self.geometry("540x580")
        self.minsize(480, 520)
        self.configure(bg="#f8fafc")
        self.transient(parent)
        self.grab_set()

        # Center on parent
        self.update_idletasks()
        try:
            px = parent.winfo_rootx() + (parent.winfo_width() - 540) // 2
            py = parent.winfo_rooty() + (parent.winfo_height() - 580) // 2
            self.geometry(f"+{max(10, px)}+{max(10, py)}")
        except Exception:
            pass

        self.create_ui(initial_house, initial_locality, initial_phone)

    def create_ui(self, initial_house: str, initial_locality: str, initial_phone: str):
        # 1. Header with SnapKart Branding
        head = tk.Frame(self, bg="#0f172a", height=60)
        head.pack(fill=tk.X)
        head.pack_propagate(False)

        h_inner = tk.Frame(head, bg="#0f172a")
        h_inner.pack(side=tk.LEFT, padx=18, pady=10)

        tk.Label(
            h_inner,
            text="📍 Confirm Delivery Address",
            font=("Segoe UI", 13, "bold"),
            fg="#38bdf8",
            bg="#0f172a"
        ).pack(anchor="w")

        tk.Label(
            h_inner,
            text="Verify or update your delivery destination before payment",
            font=("Segoe UI", 8),
            fg="#94a3b8",
            bg="#0f172a"
        ).pack(anchor="w")

        # 2. Main Form Container
        card = tk.Frame(self, bg="#ffffff", bd=1, relief=tk.SOLID)
        card.pack(fill=tk.BOTH, expand=True, padx=20, pady=16)

        pad_f = tk.Frame(card, bg="#ffffff")
        pad_f.pack(fill=tk.BOTH, expand=True, padx=20, pady=16)

        # Field: Flat / House / Building / Street
        tk.Label(
            pad_f,
            text="Flat / House No. / Building / Street: *",
            font=("Segoe UI", 9, "bold"),
            fg="#0f172a",
            bg="#ffffff"
        ).pack(anchor="w", pady=(2, 3))

        self.entry_house = tk.Entry(
            pad_f,
            font=("Segoe UI", 10),
            bg="#f8fafc",
            relief=tk.SOLID,
            bd=1
        )
        self.entry_house.pack(fill=tk.X, ipady=4, pady=(0, 10))
        if initial_house:
            self.entry_house.insert(0, initial_house)

        # Field: Locality / Area
        tk.Label(
            pad_f,
            text="Locality / Area: *",
            font=("Segoe UI", 9, "bold"),
            fg="#0f172a",
            bg="#ffffff"
        ).pack(anchor="w", pady=(2, 3))

        self.cb_locality = ttk.Combobox(
            pad_f,
            values=DEFAULT_LOCALITIES,
            font=("Segoe UI", 9)
        )
        self.cb_locality.pack(fill=tk.X, pady=(0, 10))
        if initial_locality and initial_locality in DEFAULT_LOCALITIES:
            self.cb_locality.set(initial_locality)
        elif initial_locality:
            self.cb_locality.set(initial_locality)
        else:
            self.cb_locality.current(0)

        # Row with City & PIN Code
        row_city = tk.Frame(pad_f, bg="#ffffff")
        row_city.pack(fill=tk.X, pady=(0, 10))

        col_city = tk.Frame(row_city, bg="#ffffff")
        col_city.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))

        tk.Label(
            col_city,
            text="City:",
            font=("Segoe UI", 9, "bold"),
            fg="#0f172a",
            bg="#ffffff"
        ).pack(anchor="w", pady=(0, 3))

        self.entry_city = tk.Entry(
            col_city,
            font=("Segoe UI", 10),
            bg="#f8fafc",
            relief=tk.SOLID,
            bd=1
        )
        self.entry_city.insert(0, "Agra")
        self.entry_city.pack(fill=tk.X, ipady=4)

        col_pin = tk.Frame(row_city, bg="#ffffff")
        col_pin.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(6, 0))

        tk.Label(
            col_pin,
            text="PIN Code: *",
            font=("Segoe UI", 9, "bold"),
            fg="#0f172a",
            bg="#ffffff"
        ).pack(anchor="w", pady=(0, 3))

        self.entry_pin = tk.Entry(
            col_pin,
            font=("Segoe UI", 10),
            bg="#f8fafc",
            relief=tk.SOLID,
            bd=1
        )
        self.entry_pin.insert(0, "282002")
        self.entry_pin.pack(fill=tk.X, ipady=4)

        # Field: Contact Mobile Number
        tk.Label(
            pad_f,
            text="Contact Mobile Number (for delivery executive): *",
            font=("Segoe UI", 9, "bold"),
            fg="#0f172a",
            bg="#ffffff"
        ).pack(anchor="w", pady=(2, 3))

        self.entry_phone = tk.Entry(
            pad_f,
            font=("Segoe UI", 10),
            bg="#f8fafc",
            relief=tk.SOLID,
            bd=1
        )
        self.entry_phone.pack(fill=tk.X, ipady=4, pady=(0, 12))
        if initial_phone:
            self.entry_phone.insert(0, initial_phone)
        else:
            self.entry_phone.insert(0, "+91 98")

        # Delivery Guarantee Notice
        notice_box = tk.Frame(pad_f, bg="#ecfdf5", bd=1, relief=tk.SOLID)
        notice_box.pack(fill=tk.X, pady=(2, 6), ipady=6)

        tk.Label(
            notice_box,
            text="⚡ SnapKart Express: Delivery within 30-45 minutes to this location.",
            font=("Segoe UI", 8, "bold"),
            fg="#065f46",
            bg="#ecfdf5"
        ).pack(anchor="w", padx=10)

        # 3. Action Buttons
        btn_box = tk.Frame(self, bg="#f8fafc")
        btn_box.pack(fill=tk.X, padx=20, pady=(0, 16))

        tk.Button(
            btn_box,
            text="Cancel Order",
            font=("Segoe UI", 9),
            fg="#64748b",
            bg="#f1f5f9",
            relief=tk.FLAT,
            padx=14,
            pady=6,
            cursor="hand2",
            command=self.on_cancel
        ).pack(side=tk.LEFT)

        tk.Button(
            btn_box,
            text="✅ Confirm Address & Proceed to Pay ➔",
            font=("Segoe UI", 10, "bold"),
            fg="#ffffff",
            bg="#16a34a",
            activebackground="#15803d",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=18,
            pady=7,
            cursor="hand2",
            command=self.on_submit
        ).pack(side=tk.RIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_cancel)

    def on_submit(self):
        house = self.entry_house.get().strip()
        locality = self.cb_locality.get().strip()
        city = self.entry_city.get().strip() or "Agra"
        pin = self.entry_pin.get().strip()
        phone = self.entry_phone.get().strip()

        is_valid, err_msg = validate_address_fields(house, locality, pin, phone)
        if not is_valid:
            messagebox.showwarning("Validation Error", err_msg, parent=self)
            return

        full_address = format_delivery_address(house, locality, city, pin)
        self.confirmed_address = {
            "house": house,
            "locality": locality,
            "city": city,
            "pincode": pin,
            "phone": phone,
            "full_address": full_address
        }

        self.destroy()
        if self.on_confirmed:
            self.on_confirmed(self.confirmed_address)

    def on_cancel(self):
        self.destroy()
