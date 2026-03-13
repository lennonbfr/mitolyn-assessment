from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph

def generate_pdf(name, age, score, status, description, metabolic_age, answers):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Estilo customizado para o corpo do texto com quebra automática
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=14,
        alignment=0,
    )
    
    # Header Branding
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "HELIX MEDIA LAB - MITOCHONDRIAL DIVISION")
    c.setFont("Helvetica", 10)
    c.drawString(100, 735, "Confidential Health Assessment Report | USA")
    c.line(100, 730, 500, 730)

    # 1. Score
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 690, "1. Cellular Metabolism Score")
    c.setFont("Helvetica", 12)
    c.drawString(120, 670, f"Score: {score}/100")
    c.drawString(120, 650, f"Status: {status}")

    # 2. Metabolic Age
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 610, "2. Estimated Metabolic Age")
    c.setFont("Helvetica", 12)
    c.drawString(120, 590, f"Chronological Age: {age}")
    c.drawString(120, 570, f"Estimated Cellular Age: {metabolic_age} years old")

    # 3. Mitochondrial Pattern Analysis (DINÂMICO)
    c.setFont("Helvetica-Bold", 14)
    start_y_analysis = 530
    c.drawString(100, start_y_analysis, "3. Mitochondrial Pattern Analysis")
    
    p = Paragraph(description, body_style)
    # wrap(largura_disponivel, altura_maxima)
    w, h = p.wrap(400, 200) 
    
    # Desenhamos o parágrafo logo abaixo do título da seção
    # O ReportLab desenha de baixo para cima, então subtraímos a altura (h)
    p.drawOn(c, 120, start_y_analysis - h - 10)

    # 4. Key Indicators (POSIÇÃO CALCULADA)
    # Calculamos o próximo Y com base na altura real do texto anterior + margem
    next_y = start_y_analysis - h - 50 

    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, next_y, "4. Key Indicators")
    
    energy_marker = "Stable" if answers["q1"] == "Energized" else "Reduced Output"
    weight_marker = "Optimal" if answers["q4"] == "No" else "Elevated Resistance"
    brain_marker = "Clear" if answers["q5"] == "Rarely" else "Reduced Clarity"

    c.setFont("Helvetica", 11)
    c.drawString(120, next_y - 20, f"Morning Energy Stability: {energy_marker}")
    c.drawString(120, next_y - 35, f"Weight Resistance Marker: {weight_marker}")
    c.drawString(120, next_y - 50, f"Cognitive Clarity Marker: {brain_marker}")

    # CTA Footer (Também relativo para não ser atropelado)
    footer_y = next_y - 100
    c.line(100, footer_y, 500, footer_y)
    c.setFont("Helvetica", 8)
    c.drawCentredString(300, 50, "© 2026 Helix Media Lab. For informational purposes only. This is not medical advice.")
    
    c.save()
    buffer.seek(0)
    return buffer
