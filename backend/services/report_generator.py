"""
backend/services/report_generator.py

Generates a PDF investigation report from a wallet correlation result
(the same shape returned by GET /correlation/wallet/{wallet_address}).

Usage (standalone test):
    python -m backend.services.report_generator

Usage (from other code, e.g. an API route):
    from backend.services.report_generator import generate_report

    pdf_path = generate_report(correlation_data)
"""

import os
from datetime import datetime, timezone

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


REPORTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "generated_reports")


def _build_styles():
    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="ReportTitle",
            fontSize=20,
            leading=24,
            spaceAfter=4,
            textColor=colors.HexColor("#1a1a2e"),
            fontName="Helvetica-Bold",
        )
    )

    styles.add(
        ParagraphStyle(
            name="ReportSubtitle",
            fontSize=11,
            leading=14,
            spaceAfter=20,
            textColor=colors.HexColor("#555555"),
        )
    )

    styles.add(
        ParagraphStyle(
            name="SectionHeading",
            fontSize=13,
            leading=16,
            spaceBefore=16,
            spaceAfter=8,
            textColor=colors.HexColor("#1a1a2e"),
            fontName="Helvetica-Bold",
        )
    )

    styles.add(
        ParagraphStyle(
            name="BodyTextSmall",
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#333333"),
        )
    )

    return styles


def _status_color(has_overlap: bool):
    return colors.HexColor("#c0392b") if has_overlap else colors.HexColor("#27ae60")


def _cases_table(cases, label, styles):
    if not cases:
        return Paragraph(f"No {label.lower()} found.", styles["BodyTextSmall"])

    table_data = [["Case ID", "Case Number", "Fraud Type", "Status"]]

    for case in cases:
        table_data.append(
            [
                str(case.get("id", "N/A")),
                str(case.get("case_number", "N/A")),
                str(case.get("fraud_type", "N/A")),
                str(case.get("status", "N/A")),
            ]
        )

    table = Table(table_data, colWidths=[70, 140, 120, 100])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a1a2e")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f5f5")]),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return table


def generate_report(correlation_data: dict, output_path: str | None = None) -> str:
    wallet_address = correlation_data.get("wallet_address", "UNKNOWN")
    has_overlap = bool(correlation_data.get("has_overlap", False))
    is_known_entity = bool(correlation_data.get("is_known_entity", False))
    active_cases = correlation_data.get("overlapping_active_cases") or []
    past_cases = correlation_data.get("overlapping_past_cases") or []
    known_entity = correlation_data.get("known_entity_details")

    os.makedirs(REPORTS_DIR, exist_ok=True)

    if output_path is None:
        safe_wallet = "".join(c for c in wallet_address if c.isalnum())[:40]
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(
            REPORTS_DIR, f"CHAKRAVYUH_report_{safe_wallet}_{timestamp}.pdf"
        )

    styles = _build_styles()
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        topMargin=25 * mm,
        bottomMargin=20 * mm,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
    )

    story = []

    story.append(Paragraph("CHAKRAVYUH", styles["ReportTitle"]))
    story.append(
        Paragraph(
            "Blockchain Investigation &amp; Cross-Case Correlation Report",
            styles["ReportSubtitle"],
        )
    )

    generated_at = datetime.now(timezone.utc).strftime("%d %b %Y, %H:%M UTC")
    story.append(
        Paragraph(f"Report generated: {generated_at}", styles["BodyTextSmall"])
    )
    story.append(Spacer(1, 12))

    story.append(Paragraph("Investigation Target", styles["SectionHeading"]))
    story.append(
        Paragraph(f"<b>Wallet address:</b> {wallet_address}", styles["BodyTextSmall"])
    )

    status_text = "CONNECTED TO OTHER CASES" if has_overlap else "NO OVERLAP FOUND"
    status_style = ParagraphStyle(
        name="StatusLine",
        parent=styles["BodyTextSmall"],
        textColor=_status_color(has_overlap),
        fontName="Helvetica-Bold",
        fontSize=12,
        spaceBefore=6,
    )
    story.append(Paragraph(f"Status: {status_text}", status_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Known Entity Check", styles["SectionHeading"]))
    if is_known_entity and known_entity:
        story.append(
            Paragraph(
                f"<b>Flagged entity:</b> {known_entity.get('name', 'Unnamed entity')}",
                styles["BodyTextSmall"],
            )
        )
        if known_entity.get("entity_type"):
            story.append(
                Paragraph(
                    f"<b>Entity type:</b> {known_entity.get('entity_type')}",
                    styles["BodyTextSmall"],
                )
            )
        if known_entity.get("risk_level"):
            story.append(
                Paragraph(
                    f"<b>Risk level:</b> {known_entity.get('risk_level')}",
                    styles["BodyTextSmall"],
                )
            )
        if known_entity.get("notes"):
            story.append(
                Paragraph(f"<b>Notes:</b> {known_entity.get('notes')}", styles["BodyTextSmall"])
            )
    else:
        story.append(
            Paragraph(
                "This wallet is not associated with any known flagged entity.",
                styles["BodyTextSmall"],
            )
        )
    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            f"Overlapping Active Cases ({len(active_cases)})", styles["SectionHeading"]
        )
    )
    story.append(_cases_table(active_cases, "active cases", styles))
    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            f"Overlapping Past Cases ({len(past_cases)})", styles["SectionHeading"]
        )
    )
    story.append(_cases_table(past_cases, "past cases", styles))
    story.append(Spacer(1, 16))

    story.append(
        Paragraph(
            "This report was generated automatically by the CHAKRAVYUH system "
            "based on data available in the case database at the time of generation. "
            "It is intended to support, not replace, human investigation.",
            styles["BodyTextSmall"],
        )
    )

    doc.build(story)
    return output_path


if __name__ == "__main__":
    sample_data = {
        "wallet_address": "0xSHARED999",
        "has_overlap": True,
        "is_known_entity": False,
        "overlapping_active_cases": [
            {"id": 1, "case_number": "CHK-2026-0001", "fraud_type": "investment_scam", "status": "investigating"},
            {"id": 2, "case_number": "CHK-2026-0002", "fraud_type": "phishing", "status": "open"},
        ],
        "overlapping_past_cases": [
            {"id": 1, "case_number": "OLD-2024-0099", "fraud_type": "ponzi_scheme", "status": "closed"},
        ],
        "known_entity_details": None,
    }

    path = generate_report(sample_data)
    print(f"Report generated at: {path}")