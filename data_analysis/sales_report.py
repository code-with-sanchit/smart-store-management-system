import os
import sys
import html
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
warnings.filterwarnings("ignore", category=UserWarning)


from common.logo_utils import get_logo_path


def _draw_report_footer(canvas, document):
    """Keep page context on printed or multi-page management reports."""
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#cbd5e1"))
    canvas.setLineWidth(0.75)
    canvas.line(document.leftMargin, 22, A4[0] - document.rightMargin, 22)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(colors.HexColor("#64748b"))
    canvas.drawString(document.leftMargin, 12, "SnapKart Management Information System • Strictly Confidential Internal Business Document")
    canvas.drawRightString(A4[0] - document.rightMargin, 12, f"Page {document.page}")
    canvas.restoreState()

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


def summarize_sales_by_day(sales_df: pd.DataFrame) -> pd.DataFrame:
    """Return one manager-friendly row per sale date instead of exporting raw orders."""
    columns = ["sale_date", "orders", "revenue", "average_order_value"]
    if sales_df.empty:
        return pd.DataFrame(columns=columns)
    normalized = sales_df.copy()
    normalized["sale_datetime"] = pd.to_datetime(normalized["sale_datetime"], errors="coerce")
    normalized["total_amount"] = pd.to_numeric(normalized["total_amount"], errors="coerce").fillna(0.0)
    normalized = normalized.dropna(subset=["sale_datetime"])
    normalized["sale_date"] = normalized["sale_datetime"].dt.date
    return (
        normalized.groupby("sale_date", as_index=False)["total_amount"]
        .agg(orders="count", revenue="sum", average_order_value="mean")
        .sort_values("sale_date", ascending=False)
        .round(2)
    )


def generate_pdf_business_report(sales_kpis: dict, inv_kpis: dict, reorder_df: pd.DataFrame, export_dir: str) -> str:
    """
    Generates an executive-grade PDF Business Performance & Restock Report with official SnapKart branding.
    """
    pdf_path = os.path.join(export_dir, "SnapKart_Executive_Business_Report.pdf")
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=26,
        bottomMargin=26
    )

    story = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=17,
        leading=21,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=2
    )

    sub_style = ParagraphStyle(
        "ReportSub",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#475569")
    )

    meta_style = ParagraphStyle(
        "MetaStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=11.5,
        textColor=colors.HexColor("#334155"),
        alignment=2
    )

    h2_style = ParagraphStyle(
        "ReportH2",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=8,
        spaceAfter=5
    )

    # 1. Header with Official SnapKart App Badge Logo
    logo_path = str(get_logo_path(with_text=False, as_badge=True))
    logo_element = None
    if os.path.isfile(logo_path):
        try:
            logo_element = RLImage(logo_path, width=48, height=48)
        except Exception:
            pass

    brand_info = [
        Paragraph("<font color='#15803d'><b>SnapKart</b></font>", title_style),
        Paragraph("Executive Business Performance & Inventory Intelligence Report<br/><font color='#94a3b8' size='7'>Management Information System (MIS) &bull; Analytics & Forecasting Division</font>", sub_style)
    ]

    now_str = datetime.now().strftime("%d %B %Y, %I:%M %p")
    store_info = Paragraph(
        f"<b>Report Date:</b> {now_str}<br/>"
        "<b>Store:</b> SnapKart<br/>"
        "<b>Prepared For:</b> Executive Management<br/>"
        "<font color='#dc2626'><b>CONFIDENTIAL &bull; INTERNAL USE ONLY</b></font>",
        meta_style
    )

    if logo_element is not None:
        header_data = [[logo_element, brand_info, store_info]]
        header_table = Table(header_data, colWidths=[54, 280, 201])
    else:
        header_data = [[brand_info, store_info]]
        header_table = Table(header_data, colWidths=[334, 201])

    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#15803d"), spaceAfter=10))

    # 2. Executive KPI Summary Cards
    story.append(Paragraph("<b>1. Key Business Performance Metrics Overview</b>", h2_style))

    rev_val = float(sales_kpis.get('total_revenue', 0.0))
    orders_val = int(sales_kpis.get('total_orders', 0))
    aov_val = float(sales_kpis.get('aov', 0.0))
    skus_val = int(inv_kpis.get('total_skus', 0))
    stock_units_val = int(inv_kpis.get('total_units', 0))
    stock_val = float(inv_kpis.get('total_valuation', 0.0))

    def make_kpi_card(title, value, subtitle, accent_color):
        p_title = Paragraph(f"<font color='{accent_color}'><b>{title.upper()}</b></font>", ParagraphStyle("KT", fontName="Helvetica-Bold", fontSize=7, leading=9))
        p_val = Paragraph(f"<font color='#0f172a'><b>{value}</b></font>", ParagraphStyle("KV", fontName="Helvetica-Bold", fontSize=13, leading=16))
        p_sub = Paragraph(f"<font color='#64748b'>{subtitle}</font>", ParagraphStyle("KS", fontName="Helvetica", fontSize=7, leading=9))
        tbl = Table([[p_title], [p_val], [p_sub]], colWidths=[170])
        tbl.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ('LINEBEFORE', (0, 0), (0, -1), 3, colors.HexColor(accent_color)),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))
        return tbl

    c1 = make_kpi_card("Total Revenue", f"Rs. {rev_val:,.2f}", "Gross Sales Realized", "#15803d")
    c2 = make_kpi_card("Total Orders", f"{orders_val:,} Orders", "Fulfilled Transactions", "#2563eb")
    c3 = make_kpi_card("Average Order Value", f"Rs. {aov_val:,.2f}", "Basket Size Average", "#7c3aed")

    c4 = make_kpi_card("Product Catalog", f"{skus_val:,} SKUs", "Active Inventory Lines", "#0f172a")
    c5 = make_kpi_card("Stock on Hand", f"{stock_units_val:,} Units", "Physical Warehouse Count", "#0891b2")
    c6 = make_kpi_card("Warehouse Valuation", f"Rs. {stock_val:,.2f}", "Total Inventory Asset Value", "#b45309")

    kpi_grid = Table([
        [c1, c2, c3],
        [c4, c5, c6]
    ], colWidths=[178, 178, 178])
    kpi_grid.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(kpi_grid)
    story.append(Spacer(1, 10))

    # 3. Critical Low Stock Restock Priority Table
    story.append(Paragraph("<b>2. Critical Low Stock & Priority Restock Advisory</b>", h2_style))
    story.append(Paragraph(
        "<font color='#64748b' size='7.5'>Products with warehouse stock below safety threshold (&lt; 20 units). Immediate replenishment recommended.</font>",
        styles["Normal"]
    ))
    story.append(Spacer(1, 4))

    th_c = ParagraphStyle("THC", fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=colors.white, alignment=1)
    th_l = ParagraphStyle("THL", fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=colors.white)
    tb_c = ParagraphStyle("TBC", fontName="Helvetica", fontSize=7.5, leading=9.5, textColor=colors.HexColor("#334155"), alignment=1)
    tb_l = ParagraphStyle("TBL", fontName="Helvetica", fontSize=7.5, leading=9.5, textColor=colors.HexColor("#0f172a"))

    crit_count = 0
    if reorder_df is not None and not reorder_df.empty:
        crit_count = len(reorder_df)
        table_rows = [
            [
                Paragraph("<b>SKU ID</b>", th_c),
                Paragraph("<b>Product Description</b>", th_l),
                Paragraph("<b>Category</b>", th_l),
                Paragraph("<b>Stock on Hand</b>", th_c),
                Paragraph("<b>Rec. Order</b>", th_c),
            ]
        ]

        # Top 12 critical items to fit comfortably with clean aesthetics
        sample_reorder = reorder_df.head(12)
        for _, r in sample_reorder.iterrows():
            item_id_str = html.escape(str(r.get("item_id", "")))
            item_name_str = html.escape(str(r.get("name", "")))
            item_cat_str = html.escape(str(r.get("category", "")))
            stock_qty = int(r.get("stock_quantity", 0))
            reorder_units = int(r.get("recommended_reorder_units", 30))
            table_rows.append([
                Paragraph(item_id_str, tb_c),
                Paragraph(item_name_str, tb_l),
                Paragraph(item_cat_str, tb_l),
                Paragraph(f"<font color='#dc2626'><b>{stock_qty} units</b></font>", tb_c),
                Paragraph(f"<font color='#15803d'><b>+{reorder_units} units</b></font>", tb_c),
            ])

        restock_table = Table(table_rows, colWidths=[48, 216, 140, 65, 65])
        restock_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0f172a")),
            ('TOPPADDING', (0, 0), (-1, 0), 5),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
            ('TOPPADDING', (0, 1), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 3),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ]))
        story.append(restock_table)
    else:
        story.append(Paragraph("<i>All product lines currently have sufficient stock levels. Zero critical items.</i>", styles["Normal"]))

    story.append(Spacer(1, 10))

    # 4. Strategic Executive Summary Callout Box
    insights_html = (
        "<b>Strategic Inventory & Performance Summary:</b><br/>"
        f"&bull; <b>Replenishment Priority:</b> <b>{crit_count} critical SKUs</b> have fallen below safety threshold (&lt; 20 units). Immediate purchase orders recommended.<br/>"
        f"&bull; <b>Capital Efficiency:</b> Total warehouse stock valuation is <b>Rs. {stock_val:,.2f}</b> across <b>{stock_units_val:,} physical units</b> in catalog.<br/>"
        f"&bull; <b>Sales Health:</b> Total generated revenue of <b>Rs. {rev_val:,.2f}</b> across <b>{orders_val} completed transactions</b> with Average Order Value of <b>Rs. {aov_val:,.2f}</b>."
    )
    callout_p = Paragraph(insights_html, ParagraphStyle("Callout", fontName="Helvetica", fontSize=7.5, leading=10.5, textColor=colors.HexColor("#334155")))
    callout_box = Table([[callout_p]], colWidths=[534])
    callout_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f1f5f9")),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('LINEBEFORE', (0, 0), (0, -1), 3, colors.HexColor("#15803d")),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(callout_box)
    story.append(Spacer(1, 8))

    # 5. Footer
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cbd5e1"), spaceAfter=4))
    story.append(Paragraph(
        "<i>Generated automatically by SnapKart Management System. Strictly Confidential Internal Business Document &bull; Not for Public Circulation.</i>",
        ParagraphStyle("FooterNotice", parent=styles["Normal"], fontName="Helvetica-Oblique", fontSize=7, leading=9, textColor=colors.HexColor("#94a3b8"), alignment=1)
    ))

    doc.build(story, onFirstPage=_draw_report_footer, onLaterPages=_draw_report_footer)
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

        total_revenue = 0.0
        total_orders = 0
        avg_order_val = 0.0
        median_order_val = 0.0

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
                top_products_path = os.path.join(export_dir, "top_selling_products.csv")
                top_products.to_csv(top_products_path)
                safe_print(f"    - Saved Top Products to   : {top_products_path}")

            # Export an actual daily summary rather than a raw sales dump.
            sales_summary_path = os.path.join(export_dir, "daily_sales_summary.csv")
            summarize_sales_by_day(sales_df).to_csv(sales_summary_path, index=False)
            safe_print(f"    - Saved Sales Report to   : {sales_summary_path}")
        else:
            safe_print("\n[!] Sales Overview: No sales records found yet.")

        total_skus = 0
        total_stock_units = 0
        total_stock_value = 0.0
        reorder_df = None

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
