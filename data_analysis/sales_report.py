import os
import sys
import warnings
from pathlib import Path
from datetime import datetime
import pandas as pd
import numpy as np

# Ensure project root is in sys.path for direct script execution
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from database.db_connection import get_db_connection

# Ignore SQLAlchemy UserWarning from pandas read_sql
warnings.filterwarnings("ignore", category=UserWarning, module="pandas")


from common.logo_utils import get_logo_path

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    Image as RLImage
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def safe_print(*args, **kwargs):
    """Prints text safely without crashing on Windows command prompts with non-UTF8 charmap."""
    text = " ".join(str(a) for a in args)
    try:
        print(text, **kwargs)
    except UnicodeEncodeError:
        # Fallback replacing non-encodable characters (e.g. ₹ -> Rs.)
        fallback = text.replace("₹", "Rs. ")
        try:
            print(fallback, **kwargs)
        except UnicodeEncodeError:
            print(text.encode("ascii", errors="replace").decode("ascii"), **kwargs)


def generate_pdf_business_report(sales_kpis: dict, inv_kpis: dict, reorder_df: pd.DataFrame, export_dir: str) -> str:
    """
    Generates a high-quality PDF Executive Business Report with official SnapKart branding.
    """
    pdf_path = os.path.join(export_dir, "SnapKart_Executive_Business_Report.pdf")
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )

    story = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=20,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=2
    )

    sub_style = ParagraphStyle(
        "ReportSub",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        textColor=colors.HexColor("#475569")
    )

    h2_style = ParagraphStyle(
        "ReportH2",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=10,
        spaceAfter=6
    )

    # 1. Header with Official Logo (with text)
    logo_path = str(get_logo_path(with_text=True))
    logo_element = None
    if os.path.isfile(logo_path):
        try:
            logo_element = RLImage(logo_path, width=70, height=70)
        except Exception:
            pass

    now_str = datetime.now().strftime("%d %B %Y, %I:%M %p")

    if logo_element is not None:
        header_table = Table([
            [
                logo_element,
                [
                    Paragraph("<b>SnapKart Retail Pvt. Ltd.</b>", title_style),
                    Spacer(1, 2),
                    Paragraph("Executive Business Performance & Inventory Intelligence Report", sub_style)
                ],
                Paragraph(
                    f"<b>Report Date:</b><br/>{now_str}<br/><b>Branch:</b> Flagship Hub",
                    ParagraphStyle("MetaStyle", parent=styles["Normal"], fontName="Helvetica", fontSize=8, textColor=colors.HexColor("#334155"), alignment=2, leading=11)
                )
            ]
        ], colWidths=[75, 305, 155])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 2),
            ('RIGHTPADDING', (0, 0), (-1, -1), 2),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
    else:
        header_table = Table([
            [
                Paragraph("<b>SnapKart Retail Pvt. Ltd.</b>", title_style),
                Paragraph(f"<b>Report Date:</b> {now_str}", sub_style)
            ]
        ], colWidths=[360, 175])

    story.append(header_table)
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#16a34a"), spaceAfter=12))

    # 2. Executive KPI Summary Cards / Table
    story.append(Paragraph("<b>1. Key Business Metrics Overview</b>", h2_style))

    rev_str = f"Rs. {sales_kpis.get('total_revenue', 0.0):,.2f}"
    orders_str = f"{sales_kpis.get('total_orders', 0):,}"
    aov_str = f"Rs. {sales_kpis.get('aov', 0.0):,.2f}"
    skus_str = f"{inv_kpis.get('total_skus', 0):,}"
    stock_units_str = f"{inv_kpis.get('total_units', 0):,}"
    val_str = f"Rs. {inv_kpis.get('total_valuation', 0.0):,.2f}"

    kpi_data = [
        [
            Paragraph("<b>Total Revenue Generated</b>", styles["Normal"]),
            Paragraph(f"<b>{rev_str}</b>", styles["Normal"]),
            Paragraph("<b>Total Product SKUs</b>", styles["Normal"]),
            Paragraph(f"<b>{skus_str}</b>", styles["Normal"])
        ],
        [
            Paragraph("<b>Total Orders Completed</b>", styles["Normal"]),
            Paragraph(f"<b>{orders_str}</b>", styles["Normal"]),
            Paragraph("<b>Total Units in Stock</b>", styles["Normal"]),
            Paragraph(f"<b>{stock_units_str}</b>", styles["Normal"])
        ],
        [
            Paragraph("<b>Average Order Value (AOV)</b>", styles["Normal"]),
            Paragraph(f"<b>{aov_str}</b>", styles["Normal"]),
            Paragraph("<b>Total Warehouse Valuation</b>", styles["Normal"]),
            Paragraph(f"<b>{val_str}</b>", styles["Normal"])
        ]
    ]

    kpi_table = Table(kpi_data, colWidths=[160, 105, 160, 110])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 14))

    # 3. Critical Low Stock Restock Priority Table
    story.append(Paragraph("<b>2. Critical Low Stock & Restock Advisory</b>", h2_style))

    if reorder_df is not None and not reorder_df.empty:
        table_rows = [
            [
                Paragraph("<b>Item ID</b>", styles["Normal"]),
                Paragraph("<b>Product Name</b>", styles["Normal"]),
                Paragraph("<b>Category</b>", styles["Normal"]),
                Paragraph("<b>Current Stock</b>", styles["Normal"]),
                Paragraph("<b>Rec. Order</b>", styles["Normal"])
            ]
        ]

        # Top 18 critical items
        sample_reorder = reorder_df.head(18)
        for _, r in sample_reorder.iterrows():
            table_rows.append([
                Paragraph(str(r.get("item_id", "")), styles["Normal"]),
                Paragraph(str(r.get("name", ""))[:28], styles["Normal"]),
                Paragraph(str(r.get("category", ""))[:20], styles["Normal"]),
                Paragraph(f"<font color='#dc2626'><b>{int(r.get('stock_quantity', 0))}</b></font>", styles["Normal"]),
                Paragraph(f"<b>+{int(r.get('recommended_reorder_units', 30))}</b>", styles["Normal"])
            ])

        restock_table = Table(table_rows, colWidths=[55, 205, 135, 70, 70])
        restock_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0f172a")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ]))
        story.append(restock_table)
    else:
        story.append(Paragraph("<i>All product lines currently have sufficient stock levels.</i>", styles["Normal"]))

    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cbd5e1"), spaceAfter=8))
    story.append(Paragraph(
        "<i>Generated by SnapKart Management System. Confidential Internal Business Document.</i>",
        ParagraphStyle("FooterNotice", parent=styles["Normal"], fontName="Helvetica-Oblique", fontSize=8, textColor=colors.HexColor("#94a3b8"), alignment=1)
    ))

    doc.build(story)
    return pdf_path


def generate_sales_and_inventory_reports(export_dir=None):
    """
    Analyzes sales and inventory using Pandas and NumPy,
    then exports summary CSV reports to the reports folder.
    """
    if export_dir is None:
        export_dir = os.path.join(PROJECT_ROOT, "reports")
    else:
        export_dir = os.path.abspath(export_dir)

    conn = get_db_connection()
    if not conn:
        safe_print("Database connection failed. Cannot generate reports.")
        return

    # Ensure output folder exists
    os.makedirs(export_dir, exist_ok=True)

    safe_print("\n" + "=" * 50)
    safe_print("      SNAPKART BUSINESS REPORT GENERATOR")
    safe_print("=" * 50)

    try:
        # 1. Load data into Pandas DataFrames
        sales_df = pd.read_sql("SELECT * FROM sales", conn)
        items_df = pd.read_sql("SELECT * FROM sale_items", conn)
        inventory_df = pd.read_sql("SELECT * FROM inventory", conn)

        # ---------------------------------------------------------------------
        # A. SALES PERFORMANCE METRICS (NumPy & Pandas)
        # ---------------------------------------------------------------------
        if not sales_df.empty:
            sales_df["sale_datetime"] = pd.to_datetime(sales_df["sale_datetime"])
            sales_df["total_amount"] = pd.to_numeric(sales_df["total_amount"], errors="coerce").fillna(0.0)
            total_revenue = float(np.sum(sales_df["total_amount"]))
            total_orders = len(sales_df)
            avg_order_val = float(np.mean(sales_df["total_amount"]))
            median_order_val = float(np.median(sales_df["total_amount"]))

            safe_print(f"\n[+] Sales Overview:")
            safe_print(f"    - Total Revenue Generated : Rs. {total_revenue:,.2f}")
            safe_print(f"    - Total Orders Placed     : {total_orders:,}")
            safe_print(f"    - Average Order Value (AOV): Rs. {avg_order_val:,.2f}")
            safe_print(f"    - Median Order Value      : Rs. {median_order_val:,.2f}")

            # Merge items with product names for product breakdown
            if not items_df.empty and not inventory_df.empty:
                items_df["quantity"] = pd.to_numeric(items_df["quantity"], errors="coerce").fillna(0)
                items_df["subtotal"] = pd.to_numeric(items_df["subtotal"], errors="coerce").fillna(0.0)
                merged_items = items_df.merge(inventory_df, on="item_id", how="left")
                top_products = (
                    merged_items.groupby("name")
                    .agg(units_sold=("quantity", "sum"), total_sales=("subtotal", "sum"))
                    .sort_values(by="units_sold", ascending=False)
                    .head(10)
                )

            # Export Daily Sales Summary CSV
            sales_summary_path = os.path.join(export_dir, "daily_sales_summary.csv")
            sales_df.to_csv(sales_summary_path, index=False)
            safe_print(f"    - Saved Sales Report to   : {sales_summary_path}")
        else:
            safe_print("\n[!] Sales Overview: No sales records found yet.")

        # ---------------------------------------------------------------------
        # B. INVENTORY & RESTOCK ANALYSIS
        # ---------------------------------------------------------------------
        if not inventory_df.empty:
            inventory_df["price"] = pd.to_numeric(inventory_df["price"], errors="coerce").fillna(0.0)
            inventory_df["stock_quantity"] = pd.to_numeric(inventory_df["stock_quantity"], errors="coerce").fillna(0)
            total_skus = len(inventory_df)
            total_stock_units = int(np.sum(inventory_df["stock_quantity"]))
            total_stock_value = float(np.sum(inventory_df["price"] * inventory_df["stock_quantity"]))

            # Filter items requiring urgent reorder (stock < 20)
            reorder_df = inventory_df[inventory_df["stock_quantity"] < 20].copy()
            reorder_df["recommended_reorder_units"] = 50 - reorder_df["stock_quantity"]

            safe_print(f"\n[+] Inventory Status:")
            safe_print(f"    - Total Product Catalog   : {total_skus} items")
            safe_print(f"    - Total Warehouse Units   : {total_stock_units:,} units")
            safe_print(f"    - Total Valuation         : Rs. {total_stock_value:,.2f}")
            safe_print(f"    - Critical Reorder Items  : {len(reorder_df)} products")

            # Export Restock Report CSV
            restock_path = os.path.join(export_dir, "inventory_restock_report.csv")
            reorder_df.to_csv(restock_path, index=False)
            safe_print(f"    - Saved Restock Report to : {restock_path}")

        # ---------------------------------------------------------------------
        # C. EXECUTIVE PDF REPORT (WITH OFFICIAL LOGO)
        # ---------------------------------------------------------------------
        sales_kpis = {
            "total_revenue": total_revenue if not sales_df.empty else 0.0,
            "total_orders": total_orders if not sales_df.empty else 0,
            "aov": avg_order_val if not sales_df.empty else 0.0,
        }
        inv_kpis = {
            "total_skus": total_skus if not inventory_df.empty else 0,
            "total_units": total_stock_units if not inventory_df.empty else 0,
            "total_valuation": total_stock_value if not inventory_df.empty else 0.0,
        }
        pdf_path = generate_pdf_business_report(
            sales_kpis=sales_kpis,
            inv_kpis=inv_kpis,
            reorder_df=reorder_df if not inventory_df.empty else None,
            export_dir=export_dir
        )
        safe_print(f"\n[+] Official Business Intelligence PDF Report:")
        safe_print(f"    - Generated SnapKart PDF  : {pdf_path}")

        safe_print("\n" + "=" * 50)
        safe_print("  All CSV & PDF Reports Generated Successfully!")
        safe_print("=" * 50 + "\n")
        return pdf_path

    except Exception as e:
        safe_print(f"Error generating reports: {e}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    generate_sales_and_inventory_reports()