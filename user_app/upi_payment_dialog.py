import tkinter as tk
import re
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

from common.logo_utils import get_logo_image, set_window_icon

try:
    import qrcode
    HAS_QRCODE = True
except ImportError:
    HAS_QRCODE = False


def is_valid_upi_id(value: str) -> bool:
    """Perform a small local format check; this does not verify a bank account."""
    return bool(re.fullmatch(r"[A-Za-z0-9._-]{2,}@[A-Za-z0-9._-]{2,}", value.strip()))


class UPIPaymentDialog(tk.Toplevel):
    def __init__(self, parent, total_amount, customer_name, on_payment_success):
        super().__init__(parent)

        self.title("SnapKart - UPI Payment Confirmation")
        self.geometry("420x580")
        self.resizable(False, False)
        self.configure(bg="#ffffff")

        # Set official window icon
        set_window_icon(self)

        # Keep on top of main window
        self.transient(parent)
        self.grab_set()

        self.total_amount = total_amount
        self.customer_name = customer_name
        self.on_payment_success = on_payment_success
        self.qr_image_tk = None

        self.create_ui()

    def create_ui(self):
        # Header Banner
        header = tk.Frame(self, bg="#16a34a", height=74)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        top_title_row = tk.Frame(header, bg="#16a34a")
        top_title_row.pack(pady=(10, 2))

        self.upi_logo = get_logo_image(with_text=False, size=(30, 30))
        if self.upi_logo:
            tk.Label(top_title_row, image=self.upi_logo, bg="#16a34a").pack(side=tk.LEFT, padx=(0, 6))

        tk.Label(
            top_title_row,
            text="SnapKart UPI Payment",
            font=("Segoe UI", 14, "bold"),
            fg="#ffffff",
            bg="#16a34a"
        ).pack(side=tk.LEFT)

        tk.Label(
            header,
            text="Use your UPI app, then confirm the payment in this demo",
            font=("Segoe UI", 8),
            fg="#dcfce7",
            bg="#16a34a"
        ).pack()

        # Amount Box
        amt_box = tk.Frame(self, bg="#f8fafc", bd=1, relief=tk.SOLID)
        amt_box.pack(fill=tk.X, padx=25, pady=12, ipady=6)

        tk.Label(amt_box, text="Amount to Pay", font=("Segoe UI", 8), fg="#64748b", bg="#f8fafc").pack()
        tk.Label(
            amt_box,
            text=f"₹ {self.total_amount:,.2f}",
            font=("Segoe UI", 18, "bold"),
            fg="#0f172a",
            bg="#f8fafc"
        ).pack()

        # QR Code Display
        qr_frame = tk.Frame(self, bg="#ffffff", bd=1, relief=tk.SOLID)
        qr_frame.pack(pady=5)

        self.generate_qr_code(qr_frame)

        tk.Label(
            self,
            text="Demo UPI ID: snapkart@upi  |  Payment is not bank-verified",
            font=("Segoe UI", 8, "bold"),
            fg="#334155",
            bg="#ffffff"
        ).pack(pady=(4, 8))

        # Divider
        divider = tk.Frame(self, bg="#e2e8f0", height=1)
        divider.pack(fill=tk.X, padx=25, pady=6)

        # UPI ID Entry
        form_frame = tk.Frame(self, bg="#ffffff")
        form_frame.pack(fill=tk.X, padx=25, pady=4)

        tk.Label(form_frame, text="Or Pay using UPI ID:", font=("Segoe UI", 8, "bold"), fg="#0f172a", bg="#ffffff").pack(anchor="w")

        self.upi_entry = tk.Entry(form_frame, font=("Segoe UI", 9), bg="#f8fafc", relief=tk.SOLID, bd=1)
        self.upi_entry.insert(0, "")
        self.upi_entry.pack(fill=tk.X, ipady=4, pady=(3, 8))

        # Status Label (Shows "Processing...")
        self.lbl_status = tk.Label(
            self,
            text="",
            font=("Segoe UI", 9, "bold"),
            fg="#16a34a",
            bg="#ffffff"
        )
        self.lbl_status.pack(pady=2)

        # Pay Button
        self.btn_pay = tk.Button(
            self,
            text=f"Confirm ₹ {self.total_amount:,.2f} paid",
            font=("Segoe UI", 10, "bold"),
            bg="#16a34a",
            fg="#ffffff",
            activebackground="#15803d",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.confirm_payment
        )
        self.btn_pay.pack(fill=tk.X, padx=25, pady=(4, 6), ipady=5)

        # Cancel Button
        tk.Button(
            self,
            text="Cancel Transaction",
            font=("Segoe UI", 8),
            fg="#dc2626",
            bg="#ffffff",
            bd=0,
            cursor="hand2",
            command=self.destroy
        ).pack(pady=(0, 10))

    def generate_qr_code(self, parent_frame):
        """Generates dynamic UPI QR Code image or placeholder."""
        upi_string = f"upi://pay?pa=snapkart@upi&pn=SnapKart&am={self.total_amount}&cu=INR"

        if HAS_QRCODE:
            qr = qrcode.QRCode(box_size=4, border=2)
            qr.add_data(upi_string)
            qr.make(fit=True)
            pil_img = qr.make_image(fill_color="#0f172a", back_color="#ffffff").convert("RGBA")
            self.qr_image_tk = ImageTk.PhotoImage(pil_img)
            lbl = tk.Label(parent_frame, image=self.qr_image_tk, bg="#ffffff")
            lbl.pack(padx=8, pady=8)
        else:
            # Fallback simple card if qrcode library is not installed
            lbl = tk.Label(
                parent_frame,
                text="[ QR CODE ]\nScan with GPay / PhonePe / Paytm",
                font=("Segoe UI", 9),
                bg="#f1f5f9",
                fg="#334155",
                width=24,
                height=7
            )
            lbl.pack(padx=8, pady=8)

    def confirm_payment(self):
        """Record the user's confirmation without claiming bank verification."""
        upi_id = self.upi_entry.get().strip()
        if upi_id and not is_valid_upi_id(upi_id):
            self.lbl_status.config(text="Enter a valid UPI ID or leave the field blank after scanning.", fg="#dc2626")
            return
        if not messagebox.askyesno(
            "Confirm payment",
            "This desktop demo cannot verify a payment with a bank.\n\n"
            "Only continue if the customer has completed payment in their UPI app.",
            parent=self,
        ):
            return
        self.btn_pay.config(state=tk.DISABLED, bg="#94a3b8", text="Payment confirmed")
        self.lbl_status.config(text="Payment marked as confirmed by cashier/customer.", fg="#16a34a")
        self.after(250, self.finish_flow)

    def finish_flow(self):
        self.destroy()
        # Call the checkout success callback
        self.on_payment_success()
