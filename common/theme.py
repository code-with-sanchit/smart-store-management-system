"""Shared native Tk styling for a consistent, accessible desktop interface."""

from __future__ import annotations

from tkinter import ttk


APP_BACKGROUND = "#f3f6fb"
PANEL_BACKGROUND = "#ffffff"
INK = "#172033"
MUTED = "#5e6b82"
ACCENT = "#1d4ed8"
ACCENT_HOVER = "#1e40af"


def apply_desktop_theme(root) -> None:
    """Apply the same restrained visual system to every Tk/ttk desktop window."""
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except Exception:
        pass
    root.configure(bg=APP_BACKGROUND)
    style.configure(".", font=("Segoe UI", 9), background=APP_BACKGROUND, foreground=INK)
    style.configure("TFrame", background=APP_BACKGROUND)
    style.configure("TLabelframe", background=APP_BACKGROUND, bordercolor="#d6deea")
    style.configure("TLabelframe.Label", background=APP_BACKGROUND, foreground=INK, font=("Segoe UI", 9, "bold"))
    style.configure("TButton", padding=(10, 6), foreground=INK)
    style.map("TButton", background=[("active", "#e9effa")])
    style.configure("Treeview", background=PANEL_BACKGROUND, fieldbackground=PANEL_BACKGROUND, foreground=INK, rowheight=29, bordercolor="#d6deea")
    style.map("Treeview", background=[("selected", ACCENT)], foreground=[("selected", "#ffffff")])
    style.configure("Treeview.Heading", background="#e8eef8", foreground=INK, font=("Segoe UI", 9, "bold"), relief="flat")
    style.map("Treeview.Heading", background=[("active", "#dce7f7")])
    style.configure("TEntry", fieldbackground=PANEL_BACKGROUND, padding=5)
    style.configure("TCombobox", fieldbackground=PANEL_BACKGROUND, padding=4)
