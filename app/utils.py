import io
import random
import time
from datetime import datetime
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


def simulate_validation_row(provider):
    delay = random.uniform(0.05, 0.25)
    time.sleep(delay)

    confidence = random.randint(60, 100)
    if confidence >= 80:
        status = 'Valid'
    elif confidence >= 60:
        status = 'Review'
    else:
        status = 'Invalid'

    return {
        'name': provider.get('name', ''),
        'phone': provider.get('phone', ''),
        'address': provider.get('address', ''),
        'specialty': provider.get('specialty', ''),
        'confidence': confidence,
        'status': status,
        'timestamp': datetime.utcnow().isoformat() + 'Z',
    }


def compute_aggregates(providers):
    total = len(providers)
    counts = {'Valid': 0, 'Review': 0, 'Invalid': 0}
    total_conf = 0

    for p in providers:
        st = p.get('status')
        if st in counts:
            counts[st] += 1
        total_conf += float(p.get('confidence', 0))

    avg_conf = round(total_conf / total, 2) if total > 0 else 0
    return {'total': total, 'counts': counts, 'average_confidence': avg_conf}


def generate_pdf_report(providers, aggregates):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=LETTER)
    width, height = LETTER

    c.setFont('Helvetica-Bold', 16)
    c.drawString(1 * inch, height - 1 * inch, 'Provider Data Validator Report')
    c.setFont('Helvetica', 10)
    c.drawString(1 * inch, height - 1.25 * inch, f'Generated: {datetime.utcnow().isoformat()}Z')

    y = height - 1.75 * inch
    c.setFont('Helvetica-Bold', 12)
    c.drawString(1 * inch, y, 'Summary')
    y -= 0.25 * inch

    c.setFont('Helvetica', 10)
    c.drawString(1 * inch, y, f"Total providers: {aggregates.get('total')}")
    y -= 0.18 * inch
    counts = aggregates.get('counts', {})
    c.drawString(1 * inch, y, f"Valid: {counts.get('Valid', 0)}  Review: {counts.get('Review', 0)}  Invalid: {counts.get('Invalid', 0)}")
    y -= 0.18 * inch
    c.drawString(1 * inch, y, f"Average confidence: {aggregates.get('average_confidence')}")

    y -= 0.4 * inch
    c.setFont('Helvetica-Bold', 10)
    c.drawString(1 * inch, y, 'Name')
    c.drawString(3.5 * inch, y, 'Phone')
    c.drawString(5 * inch, y, 'Confidence')
    c.drawString(6 * inch, y, 'Status')
    y -= 0.14 * inch
    c.line(1 * inch, y, 7.5 * inch, y)
    y -= 0.12 * inch

    c.setFont('Helvetica', 9)
    for p in providers:
        if y < 1 * inch:
            c.showPage()
            y = height - 1 * inch
        c.drawString(1 * inch, y, str(p.get('name', ''))[:30])
        c.drawString(3.5 * inch, y, str(p.get('phone', ''))[:18])
        c.drawString(5 * inch, y, str(p.get('confidence', '')))
        c.drawString(6 * inch, y, str(p.get('status', '')))
        y -= 0.18 * inch

    c.save()
    buffer.seek(0)
    return buffer
