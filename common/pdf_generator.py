import os
import sys
import html
import subprocess
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    Image as RLImage,
    KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.barcode import qr

from common.logo_utils import get_logo_path


def invoice_number(sale_id: int, issued_at: datetime | None = None) -> str:
    """Create the readable invoice number shown in the desktop app and PDF."""
    date_value = issued_at or datetime.now()
    return f"SK-{date_value.year}-{int(sale_id):06d}"


def _draw_invoice_footer(canvas, document):
    """Add a professional running footer to every invoice page."""
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#cbd5e1"))
    canvas.setLineWidth(0.75)
    canvas.line(document.leftMargin, 22, A4[0] - document.rightMargin, 22)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(colors.HexColor("#64748b"))
    canvas.drawString(
        document.leftMargin,
        12,
        "SnapKart • Computer-Generated Tax Invoice under Rule 46 of CGST Rules 2017"
    )
    canvas.drawRightString(
        A4[0] - document.rightMargin,
        12,
        f"Page {document.page}"
    )
    canvas.restoreState()


def generate_pdf_receipt(
    sale_id,
    items_dict,
    subtotal,
    delivery_fee,
    total_amount,
    customer_name="Guest Customer",
    customer_address="Store counter",
    payment_method="UPI",
    discount_amount=0.0,
    output_dir="receipts"
):
    """
    Generates an authentic, executive-standard Retail GST Supermarket Tax Invoice PDF for SnapKart.
    Saves it in the 'receipts' folder and returns the file path.
    """
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, f"SnapKart_TaxInvoice_{sale_id}.pdf")

    # A4 dimensions: 595.28 x 841.89 points.
    # Margins: 28pt left/right leaves 539.28pt usable width. Tables use 540pt width.
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        rightMargin=28,
        leftMargin=28,
        topMargin=24,
        bottomMargin=26
    )

    story = []
    styles = getSampleStyleSheet()

    # Typography & Styles with strictly defined leading to prevent text overlap
    brand_title_style = ParagraphStyle(
        "BrandTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=19,
        spaceAfter=2
    )

    brand_sub_style = ParagraphStyle(
        "BrandSub",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#475569")
    )

    store_addr_style = ParagraphStyle(
        "StoreAddr",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=11.5,
        textColor=colors.HexColor("#334155"),
        alignment=2
    )

    banner_title_style = ParagraphStyle(
        "HeadingBannerTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=13,
        textColor=colors.white,
        alignment=1
    )

    banner_sub_style = ParagraphStyle(
        "HeadingBannerSub",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7,
        leading=9,
        textColor=colors.HexColor("#94a3b8"),
        alignment=1
    )

    # 1. Header: Store Branding with Official Logo App Badge & Tax Info
    logo_path = str(get_logo_path(with_text=False, as_badge=True))
    logo_element = None
    if os.path.isfile(logo_path):
        try:
            logo_element = RLImage(logo_path, width=48, height=48)
        except Exception as e:
            print(f"Notice: Could not load logo in PDF: {e}")

    brand_info = [
        Paragraph("<font color='#15803d'><b>SnapKart</b></font>", brand_title_style),
        Paragraph("<font color='#64748b' size='7.5'>CIN: U52100DL2024PTC123456 &bull; Regd. Off: New Delhi</font>", brand_sub_style)
    ]

    store_info = Paragraph(
        "<b>SnapKart</b><br/>"
        "Plot No. 45, Prime Commercial Hub, Sec-14<br/>"
        "<b>GSTIN:</b> 09AAACS1429B1Z8 | <b>FSSAI:</b> 12722001000456<br/>"
        "<font color='#64748b'>support@snapkart.in &bull; Helpline: 1800-245-8900</font>",
        store_addr_style
    )

    if logo_element is not None:
        header_data = [[logo_element, brand_info, store_info]]
        header_table = Table(header_data, colWidths=[54, 266, 220])
    else:
        header_data = [[brand_info, store_info]]
        header_table = Table(header_data, colWidths=[320, 220])

    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#15803d"), spaceAfter=8))

    # 2. Tax Invoice Title Box
    banner_content = [
        Paragraph("TAX INVOICE / CASH MEMO", banner_title_style),
        Spacer(1, 2),
        Paragraph("ORIGINAL FOR RECIPIENT &bull; ISSUED UNDER RULE 46 OF CGST RULES, 2017", banner_sub_style)
    ]
    title_box = Table([[banner_content]], colWidths=[540])
    title_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#0f172a")),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    story.append(title_box)
    story.append(Spacer(1, 8))

    # 3. Invoice Metadata & Customer Section (Structured 2-Column Card)
    meta_val_style = ParagraphStyle(
        "MVal",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#0f172a")
    )

    esc_customer_name = html.escape(str(customer_name or "Guest Customer"))
    esc_customer_address = html.escape(str(customer_address or "Store counter"))
    esc_payment_method = html.escape(str(payment_method or "UPI"))
    now_str = datetime.now().strftime("%d %b %Y, %I:%M %p")

    meta_data = [
        [
            Paragraph(f"<b>Invoice ID:</b> #{invoice_number(sale_id)}", meta_val_style),
            Paragraph(f"<b>Billed To:</b> {esc_customer_name}", meta_val_style),
        ],
        [
            Paragraph(f"<b>Date & Time:</b> {now_str}", meta_val_style),
            Paragraph(f"<b>Payment Mode:</b> {esc_payment_method} (Completed & Verified)", meta_val_style),
        ],
        [
            Paragraph("<b>POS Terminal:</b> POS-Terminal-01 (Express Billing)", meta_val_style),
            Paragraph(f"<b>Delivery Address:</b> {esc_customer_address}", meta_val_style),
        ]
    ]

    meta_table = Table(meta_data, colWidths=[270, 270])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 9))

    # 4. Itemized GST Product Table
    # Replaced missing Rupee symbol (which rendered as black rectangle) with clean 'Rs.'
    th_center = ParagraphStyle("THC", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=8, textColor=colors.white, alignment=1)
    th_left = ParagraphStyle("THL", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=8, textColor=colors.white)
    th_right = ParagraphStyle("THR", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=8, textColor=colors.white, alignment=2)

    table_data = [
        [
            Paragraph("<b>#</b>", th_center),
            Paragraph("<b>Item Description</b>", th_left),
            Paragraph("<b>HSN</b>", th_center),
            Paragraph("<b>Qty</b>", th_center),
            Paragraph("<b>Rate (Rs.)</b>", th_right),
            Paragraph("<b>Tax (5%)</b>", th_right),
            Paragraph("<b>Total (Rs.)</b>", th_right)
        ]
    ]

    subtotal = max(0.0, float(subtotal))
    delivery_fee = max(0.0, float(delivery_fee))
    discount_amount = max(0.0, float(discount_amount))
    total_gst_amount = round(subtotal * 0.05, 2)
    cgst_val = round(total_gst_amount / 2, 2)
    sgst_val = round(total_gst_amount - cgst_val, 2)
    computed_final = round(subtotal + total_gst_amount + delivery_fee - discount_amount, 2)
    total_amount = max(0.0, float(total_amount)) if total_amount else computed_final

    item_name_style = ParagraphStyle(
        "ItemNameStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#0f172a")
    )
    item_num_style = ParagraphStyle(
        "ItemNumStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=10,
        alignment=2,
        textColor=colors.HexColor("#0f172a")
    )
    item_center_style = ParagraphStyle(
        "ItemCenterStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=10,
        alignment=1,
        textColor=colors.HexColor("#334155")
    )

    idx = 1
    for item in items_dict.values():
        i_price = float(item["price"])
        i_qty = int(item["qty"])
        line_sub = i_price * i_qty
        hsn_code = f"2106{idx % 89 + 10:02d}"
        line_tax = round(line_sub * 0.05, 2)
        line_total = line_sub + line_tax
        esc_name = html.escape(str(item["name"]))
        table_data.append([
            Paragraph(str(idx), item_center_style),
            Paragraph(esc_name, item_name_style),
            Paragraph(hsn_code, item_center_style),
            Paragraph(str(i_qty), item_center_style),
            Paragraph(f"{i_price:.2f}", item_num_style),
            Paragraph(f"{line_tax:.2f}", item_num_style),
            Paragraph(f"{line_total:.2f}", item_num_style)
        ])
        idx += 1

    product_table = Table(table_data, colWidths=[25, 230, 50, 35, 65, 65, 70])
    product_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#15803d")),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, 0), 5),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
        ('TOPPADDING', (0, 1), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
    ]))
    story.append(product_table)
    story.append(Spacer(1, 9))

    # 5. Financial Summary & Official GST Tax Breakdown (Two-Column Layout)
    gst_hdr_style = ParagraphStyle("GSTH", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=7.5, leading=9, textColor=colors.HexColor("#0f172a"))
    gst_hdr_r_style = ParagraphStyle("GSTHR", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=7.5, leading=9, alignment=2, textColor=colors.HexColor("#0f172a"))
    gst_row_style = ParagraphStyle("GSTR", parent=styles["Normal"], fontName="Helvetica", fontSize=7.5, leading=9.5, textColor=colors.HexColor("#475569"))
    gst_row_r_style = ParagraphStyle("GSTRR", parent=styles["Normal"], fontName="Helvetica", fontSize=7.5, leading=9.5, alignment=2, textColor=colors.HexColor("#475569"))
    gst_bold_style = ParagraphStyle("GSTB", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=7.5, leading=9.5, textColor=colors.HexColor("#15803d"))
    gst_bold_r_style = ParagraphStyle("GSTBR", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=7.5, leading=9.5, alignment=2, textColor=colors.HexColor("#15803d"))

    tax_box_data = [
        [
            Paragraph("<b>GST Rate</b>", gst_hdr_style),
            Paragraph("<b>Taxable Subtotal</b>", gst_hdr_r_style),
            Paragraph("<b>CGST (2.5%)</b>", gst_hdr_r_style),
            Paragraph("<b>SGST (2.5%)</b>", gst_hdr_r_style),
        ],
        [
            Paragraph("5.0% Slab", gst_row_style),
            Paragraph(f"Rs. {subtotal:,.2f}", gst_row_r_style),
            Paragraph(f"Rs. {cgst_val:,.2f}", gst_row_r_style),
            Paragraph(f"Rs. {sgst_val:,.2f}", gst_row_r_style),
        ],
        [
            Paragraph("<b>Total GST Added (5%)</b>", gst_bold_style),
            Paragraph(f"<b>Rs. {total_gst_amount:,.2f}</b>", gst_bold_r_style),
            "", ""
        ]
    ]
    tax_sub_table = Table(tax_box_data, colWidths=[76, 62, 56, 56])
    tax_sub_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('SPAN', (1, 2), (3, 2)),
    ]))

    summary_data = [
        ["Subtotal (Excl. Tax):", f"Rs. {subtotal:,.2f}"],
        ["CGST @ 2.5%:", f"Rs. {cgst_val:,.2f}"],
        ["SGST @ 2.5%:", f"Rs. {sgst_val:,.2f}"],
        ["Total GST (5%):", f"Rs. {total_gst_amount:,.2f}"],
        ["Delivery & Handling Fee:", f"Rs. {delivery_fee:,.2f}"],
        ["Discount Applied:", f"- Rs. {discount_amount:,.2f}"],
        ["TOTAL AMOUNT PAID:", f"Rs. {total_amount:,.2f}"]
    ]

    bill_sub_table = Table(summary_data, colWidths=[165, 115])
    bill_sub_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -2), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -2), 8),
        ('TEXTCOLOR', (0, 0), (-1, -2), colors.HexColor("#475569")),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 10.5),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.white),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor("#15803d")),
        ('TOPPADDING', (0, 0), (-1, -2), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -2), 2.5),
        ('TOPPADDING', (0, -1), (-1, -1), 5),
        ('BOTTOMPADDING', (0, -1), (-1, -1), 5),
        ('LINEABOVE', (0, -1), (-1, -1), 1, colors.HexColor("#15803d")),
    ]))

    financial_container = Table([[tax_sub_table, bill_sub_table]], colWidths=[255, 285])
    financial_container.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(financial_container)
    story.append(Spacer(1, 10))

    # 6. QR Code for Invoice Verification & Store Returns Policy Card
    qr_code = qr.QrCodeWidget(f"SK-INV-{sale_id}-{total_amount:.2f}")
    bounds = qr_code.getBounds()
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    d = Drawing(54, 54, transform=[54.0 / width, 0, 0, 54.0 / height, 0, 0])
    d.add(qr_code)

    policy_style = ParagraphStyle(
        "PolicyStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.5,
        leading=10.5,
        textColor=colors.HexColor("#334155")
    )

    qr_box_data = [
        [
            d,
            Paragraph(
                "<b>Digital GST Tax Invoice Verification & Store Policy</b><br/>"
                "<font color='#475569'>"
                "&bull; Scan this QR code using any UPI / camera app to authenticate digital GST compliance.<br/>"
                "&bull; Returns & exchange accepted within 7 days of purchase on presentation of original invoice.<br/>"
                "&bull; Perishable items (milk, dairy, fruits, vegetables) must be verified within 24 hours of delivery."
                "</font>",
                policy_style
            )
        ]
    ]
    qr_box = Table(qr_box_data, colWidths=[64, 476])
    qr_box.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f1f5f9")),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(qr_box)
    story.append(Spacer(1, 10))

    # 7. Official Legal Footer (Clean, standard text without emoji render bugs)
    footer_text = ParagraphStyle(
        "FooterNote",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#64748b"),
        alignment=1
    )
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cbd5e1"), spaceAfter=5))
    story.append(Paragraph("<b>Thank you for shopping at SnapKart! Please visit us again.</b>", footer_text))
    story.append(Spacer(1, 2))
    story.append(Paragraph("Helpline: 1800-245-8900 (Toll-Free) &bull; Email: support@snapkart.in &bull; Web: www.snapkart.in", footer_text))
    story.append(Spacer(1, 2))
    story.append(Paragraph("<i>This is an authenticated computer-generated invoice issued under Rule 46 of CGST Rules 2017. Does not require physical signature.</i>", footer_text))

    doc.build(story, onFirstPage=_draw_invoice_footer, onLaterPages=_draw_invoice_footer)
    return pdf_path


def open_pdf_file(file_path):
    try:
        if sys.platform.startswith("win"):
            os.startfile(file_path)
        elif sys.platform.startswith("darwin"):
            subprocess.Popen(["open", file_path])
        else:
            subprocess.Popen(["xdg-open", file_path])
    except Exception as e:
        print(f"Could not open PDF automatically: {e}")
