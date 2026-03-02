from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def build_report_pdf(report: dict) -> bytes:
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    width, height = letter

    y = height - 60
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Resume Match Report")
    y -= 30

    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Report ID: {report['id']}")
    y -= 18
    c.drawString(50, y, f"Score: {report['score']} / 100")
    y -= 18
    c.drawString(50, y, f"Created at: {report['created_at']}")
    y -= 24

    breakdown = report.get("breakdown", {}) or {}
    preset = breakdown.get("preset", "swe")
    c.drawString(50, y, f"Preset: {preset}")
    y -= 18
    c.drawString(50, y, f"Similarity: {breakdown.get('similarity', 0)}%")
    y -= 18
    c.drawString(50, y, f"Skill overlap: {breakdown.get('skill_overlap', 0)}%")
    y -= 24

    missing = report.get("missing_skills", []) or []
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Missing / Gap Skills:")
    y -= 18

    c.setFont("Helvetica", 11)
    if not missing:
        c.drawString(60, y, "- None 🎉")
        y -= 16
    else:
        for s in missing[:25]:
            c.drawString(60, y, f"- {s}")
            y -= 16
            if y < 80:
                c.showPage()
                y = height - 60
                c.setFont("Helvetica", 11)

    c.showPage()
    c.save()
    return buf.getvalue()