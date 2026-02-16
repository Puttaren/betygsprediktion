# Installera först: pip install fpdf2

from fpdf import FPDF

class StudieintygsGenerator(FPDF):
    def header(self):
        # Logo/Header
        self.set_font('Arial', 'B', 24)
        self.set_text_color(155, 159, 204)
        self.cell(20, 10, 'YH', 0, 0, 'L')
        self.set_text_color(244, 197, 66)
        self.cell(10, 10, 'o', 0, 0, 'L')
        self.set_text_color(51, 51, 51)
        self.cell(0, 10, 'Akademin', 0, 1, 'L')
        self.ln(5)

    def footer(self):
        self.set_y(-20)
        # Blå bakgrund för footer
        self.set_fill_color(91, 127, 204)
        self.rect(0, self.get_y(), 210, 20, 'F')

        self.set_text_color(255, 255, 255)
        self.set_font('Arial', '', 8)
        self.cell(0, 10, 'YH Akademin · Box 127· 791 23 Falun · yh.se · Servicecenter: 023-584 00 · hej@yh.se', 0, 0, 'C')

# Skapa PDF
pdf = StudieintygsGenerator()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=25)

# Rubrik
pdf.set_font('Arial', 'B', 20)
pdf.set_text_color(51, 51, 51)
pdf.cell(0, 10, 'Studieintyg', 0, 1, 'L')
# Blå linje
pdf.set_draw_color(91, 127, 204)
pdf.set_line_width(0.8)
pdf.line(10, pdf.get_y(), 110, pdf.get_y())
pdf.ln(10)

# Intygstext
pdf.set_font('Arial', '', 11)
pdf.multi_cell(0, 5, 'Härmed intygas att Exempel Exempelsson, 000000-0000, studerar YH-utbildningen BI-Analyst med AI-kompetens vid YH Akademin. Utbildningen startade 2025-01-07 och pågår till 2026-12-11 med studietakten 100%.')
pdf.ln(5)

# Tabell headers
pdf.set_font('Arial', 'B', 10)
pdf.cell(80, 7, 'Kurs', 1, 0, 'L')
pdf.cell(25, 7, 'Yh-poäng', 1, 0, 'C')
pdf.cell(25, 7, 'Betyg', 1, 0, 'C')
pdf.cell(30, 7, 'Startdatum', 1, 1, 'C')

# Tabell data
pdf.set_font('Arial', '', 9)
courses = [
    ("Business Intelligence introduktion", "10", "VG", "2025-01-07"),
    ("BI verktyg, verksamhetsprocesser", "40", "VG", "2025-01-20"),
    ("SQL", "20", "VG", "2025-03-17"),
    ("Datautvinning och förädling", "30", "VG", "2025-04-14"),
    ("Dataanalys och statistik", "20", "VG", "2025-05-26"),
    ("Python och verksamhetsstödjande visualisering", "30", "VG", "2025-08-25"),
    ("Ledarskap och projektmetodik", "30", "VG", "2025-10-06"),
    ("Molnbaserade lösningar", "20", "VG", "2025-11-17"),
    ("Machine Learning", "40", "-", "2026-01-05"),
    ("AI och IOT", "40", "-", "2026-03-02"),
    ("Lärande i Arbete", "100", "-", "2026-04-27"),
    ("Examensarbete", "20", "-", "2026-11-16"),
]

for course, points, grade, date in courses:
    pdf.cell(80, 6, course.encode('latin-1', 'replace').decode('latin-1'), 1, 0, 'L')
    pdf.cell(25, 6, points, 1, 0, 'C')
    pdf.cell(25, 6, grade, 1, 0, 'C')
    pdf.cell(30, 6, date, 1, 1, 'C')

pdf.ln(5)

# Utfärdat datum
pdf.set_font('Arial', '', 11)
pdf.cell(0, 5, 'Utfärdat: 2026-02-06', 0, 1, 'L')
pdf.ln(10)

# Signatur
pdf.set_font('Arial', '', 11)
pdf.cell(0, 5, 'Ella Lilja', 0, 1, 'L')
pdf.set_font('Arial', '', 9)
pdf.cell(0, 4, 'Utbildningsledare', 0, 1, 'L')
pdf.cell(0, 4, 'Växel: +46 23 585 00', 0, 1, 'L')
pdf.cell(0, 4, 'E-post: ella.lilja@yh.se', 0, 1, 'L')
pdf.cell(0, 4, 'YH Akademin', 0, 1, 'L')

# Spara PDF
filename = 'Studieintyg-Exempel.pdf'
pdf.output(filename)

print(f"✅ Skapade {filename}")
print("📄 Exempel-studieintyg skapat med:")
print("   - Namn: Exempel Exempelsson")
print("   - Personnummer: 000000-0000")
