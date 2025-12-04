from fpdf import FPDF
import os

def generate(name):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 24)
    pdf.cell(0, 50, "Certificate of Participation", 0, 1, 'C')
    pdf.set_font("Arial", '', 20)
    pdf.cell(0, 20, f"Presented to {name}", 0, 1, 'C')
    pdf_file = os.path.join(os.path.dirname(__file__), '../database', f"{name.replace(' ','_')}.pdf")
    pdf.output(pdf_file)
    return pdf_file
