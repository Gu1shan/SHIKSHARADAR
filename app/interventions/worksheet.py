"""
PDF worksheet generator (ReportLab) for intervention plans.
"""
import os
from datetime import datetime, timedelta

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet


def generate_worksheet_pdf(intervention: dict, output_dir: str = "data/worksheets") -> str:
    """
    Generate a printable intervention worksheet PDF.

    Returns the path of the generated file.
    """
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{intervention['student_id']}_{intervention['concept']}_{intervention['intervention_id']}.pdf"
    path = os.path.join(output_dir, filename.replace(" ", "_").replace(":", "-"))

    styles = getSampleStyleSheet()
    story = []

    # Header
    story.append(Paragraph("Shiksha Radar — Intervention Worksheet", styles["Title"]))
    story.append(Paragraph(
        "Teacher-reviewed remediation plan (suggestion only — adjust as needed)",
        styles["Italic"],
    ))
    story.append(Spacer(1, 0.4 * cm))

    # Summary table
    due_date = (datetime.now() + timedelta(days=14)).strftime("%d %b %Y")
    summary = Table([
        ["Student", intervention["student_id"]],
        ["Concept", intervention["concept"]],
        ["Dominant error pattern", intervention.get("dominant_error", "—")],
        ["Reassessment suggested by", due_date],
    ], colWidths=[6 * cm, 11 * cm])
    summary.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(summary)
    story.append(Spacer(1, 0.6 * cm))

    # Steps
    story.append(Paragraph("Suggested Teaching Steps", styles["Heading2"]))
    for i, step in enumerate(intervention.get("steps", []), 1):
        story.append(Paragraph(f"{i}. {step}", styles["Normal"]))
        story.append(Spacer(1, 0.15 * cm))
    story.append(Spacer(1, 0.5 * cm))

    # Practice questions with answer boxes
    story.append(Paragraph("Practice Questions", styles["Heading2"]))
    for i, q in enumerate(intervention.get("practice_questions", []), 1):
        story.append(Paragraph(f"Q{i}. {q}", styles["Normal"]))
        story.append(Spacer(1, 1.1 * cm))  # space to work
    story.append(Spacer(1, 0.5 * cm))

    # Teacher notes
    story.append(Paragraph("Teacher Notes", styles["Heading2"]))
    notes_table = Table([[""]] * 3, colWidths=[17 * cm], rowHeights=[0.9 * cm] * 3)
    notes_table.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.5, colors.grey)]))
    story.append(notes_table)

    doc = SimpleDocTemplate(path, pagesize=A4,
                            leftMargin=2 * cm, rightMargin=2 * cm,
                            topMargin=1.5 * cm, bottomMargin=1.5 * cm)
    doc.build(story)
    return path


if __name__ == "__main__":
    demo = {
        "intervention_id": "INT-TEST0001",
        "student_id": "Student_001",
        "concept": "Fractions",
        "dominant_error": "denominator_handling",
        "steps": ["Revise common denominators using fraction strips",
                  "Practice 5 problems"],
        "practice_questions": ["3/4 + 1/4 = ?", "2/3 + 1/6 = ?"],
    }
    print(generate_worksheet_pdf(demo, "/tmp/opencode"))
