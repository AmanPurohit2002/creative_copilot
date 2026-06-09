import io
import base64
from PIL import Image as PILImage
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle

def generate_storyboard_pdf(brief: dict, panels: list[dict]) -> bytes:
    """
    Generate a high-quality PDF storyboard using ReportLab.
    Returns the PDF as a byte string.
    """
    buffer = io.BytesIO()
    
    # Use landscape letter size for better storyboard layout
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=landscape(letter),
        rightMargin=0.5*inch, leftMargin=0.5*inch,
        topMargin=0.5*inch, bottomMargin=0.5*inch
    )
    
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor("#1e1e1e"),
        spaceAfter=6,
    )
    
    meta_style = ParagraphStyle(
        'MetaStyle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor("#555555"),
        spaceAfter=20,
    )

    label_style = ParagraphStyle(
        'LabelStyle',
        parent=styles['Normal'],
        fontSize=10,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#555555"),
        spaceAfter=2,
    )
    
    text_style = ParagraphStyle(
        'TextStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor("#111111"),
        spaceAfter=12,
    )
    
    # Header
    title = brief.get("title", "Storyboard")
    story.append(Paragraph(title, title_style))
    
    meta_text = f"<b>Format:</b> {brief.get('format', 'N/A')} &nbsp;&nbsp;|&nbsp;&nbsp; <b>Duration:</b> {brief.get('duration', 'N/A')} &nbsp;&nbsp;|&nbsp;&nbsp; <b>Platform:</b> {brief.get('platform', 'N/A')}"
    story.append(Paragraph(meta_text, meta_style))
    
    # Process Panels
    for idx, panel in enumerate(panels):
        shot_num = panel.get("shot_number", idx + 1)
        
        # Process Image
        img_platypus = None
        img_b64 = panel.get("image_base64")
        if img_b64:
            try:
                img_data = base64.b64decode(img_b64)
                img_stream = io.BytesIO(img_data)
                # Ensure valid image
                pil_img = PILImage.open(img_stream)
                img_width, img_height = pil_img.size
                
                # Resize for PDF (target width: 4.5 inches)
                target_w = 4.5 * inch
                aspect = img_height / float(img_width)
                target_h = target_w * aspect
                
                # Create ReportLab Image
                img_stream.seek(0)
                img_platypus = Image(img_stream, width=target_w, height=target_h)
            except Exception as e:
                print(f"Error loading image for shot {shot_num}: {e}")
                
        if not img_platypus:
            img_platypus = Paragraph("[Image Generation Failed or Missing]", text_style)
            
        # Left column content (Image + Shot info)
        shot_info = Paragraph(f"<b>SHOT {shot_num}</b>  ({panel.get('duration', '')})", label_style)
        left_col = [shot_info, Spacer(1, 6), img_platypus]
        
        # Right column content (Annotations)
        right_col = []
        
        visual = panel.get("visual", "")
        if visual:
            right_col.append(Paragraph("VISUAL:", label_style))
            right_col.append(Paragraph(visual, text_style))
            
        camera = panel.get("camera", "")
        if camera:
            right_col.append(Paragraph("CAMERA:", label_style))
            right_col.append(Paragraph(camera, text_style))
            
        vo = panel.get("voiceover", "")
        if vo:
            right_col.append(Paragraph("AUDIO / VO:", label_style))
            right_col.append(Paragraph(vo, text_style))
            
        text_overlay = panel.get("text_overlay", "")
        if text_overlay:
            right_col.append(Paragraph("ON-SCREEN TEXT:", label_style))
            right_col.append(Paragraph(text_overlay, text_style))
            
        # Create Table for the Shot
        # Layout: Left column = 5 inches, Right column = remaining space (~4.5 inches)
        table = Table([[left_col, right_col]], colWidths=[5.2*inch, 4.3*inch])
        
        table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
        ]))
        
        # Keep table together on same page to avoid splitting shots
        table.keepWithNext = False
        
        story.append(table)
        
    # Build PDF
    doc.build(story)
    
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes
