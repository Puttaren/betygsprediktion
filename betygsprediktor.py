import streamlit as st
import PyPDF2
import re
import urllib.request
from io import BytesIO

st.set_page_config(page_title="ML Betygsprediktor", page_icon="📊")

st.title("🎓 Machine Learning Betygsprediktor")
st.markdown("Ladda upp ditt studieintyg från YH Akademin för att få en prediktion av ditt betyg i Machine Learning-kursen.")

# File upload eller exempelintyg
col1, col2 = st.columns([2, 1])

with col1:
    uploaded_file = st.file_uploader("Välj din PDF-fil", type=['pdf'])

with col2:
    st.write("")  # Spacing
    use_example = st.button("📄 Använd exempelintyg", use_container_width=True)

# URL till exempelintyg på GitHub (du måste uppdatera denna efter du pushat)
EXAMPLE_PDF_URL = "https://raw.githubusercontent.com/Puttaren/betygsprediktion/main/Studieintyg-Exempel.pdf"


def extract_student_name(text):
    """Extraherar studentens namn från studieintyget"""
    # Matchar mönstret: "Härmed intygas att [Namn], [personnummer]"
    match = re.search(r'Härmed intygas att ([A-ZÅÄÖ][a-zåäö]+ [A-ZÅÄÖ][a-zåäö]+),', text)
    if match:
        return match.group(1)

    # Alternativt mönster om namnet kommer före personnummer
    match = re.search(r'intygas att ([A-ZÅÄÖ][\w\s]+?),\s*\d{6,8}[-\s]?\d{4}', text)
    if match:
        return match.group(1).strip()

    return None

def extract_grades_from_pdf(pdf_file):
    """Extraherar kursdata och studentnamn från studieintyget"""
    courses = []
    student_name = None

    # Konvertera till BytesIO om det är bytes
    if isinstance(pdf_file, bytes):
        pdf_file = BytesIO(pdf_file)

    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Läs all text först för att hitta namn
    full_text = ""
    for page in pdf_reader.pages:
        full_text += page.extract_text()

    # Extrahera studentnamn
    student_name = extract_student_name(full_text)

    # Extrahera kurser
    for page in pdf_reader.pages:
        text = page.extract_text()
        lines = text.split('\n')

        for line in lines:
            # Leta efter rader med betyg
            match = re.search(r'^([A-ZÅÄÖ][\w\s,öäåÖÄÅ-]+?)\s+(\d+)\s+(VG|G|IG|-)\s+\d{4}-\d{2}-\d{2}', line)
            if match:
                course_name = match.group(1).strip()
                points = int(match.group(2))
                grade = match.group(3)

                if grade in ['VG', 'G', 'IG']:
                    courses.append({
                        'name': course_name,
                        'points': points,
                        'grade': grade
                    })

    return courses, student_name

def calculate_weighted_stats(courses):
    """Beräknar viktad statistik baserat på kurspoäng"""
    if not courses:
        return None

    total_points = sum(c['points'] for c in courses)
    vg_points = sum(c['points'] for c in courses if c['grade'] == 'VG')
    g_points = sum(c['points'] for c in courses if c['grade'] == 'G')
    ig_points = sum(c['points'] for c in courses if c['grade'] == 'IG')

    vg_percent = (vg_points / total_points * 100) if total_points > 0 else 0
    g_percent = (g_points / total_points * 100) if total_points > 0 else 0
    ig_percent = (ig_points / total_points * 100) if total_points > 0 else 0

    return {
        'total_courses': len(courses),
        'total_points': total_points,
        'vg_points': vg_points,
        'g_points': g_points,
        'ig_points': ig_points,
        'vg_percent': vg_percent,
        'g_percent': g_percent,
        'ig_percent': ig_percent
    }

def predict_grade(stats):
    """Predikterar betyg baserat på historisk prestation"""
    if not stats:
        return "Kunde inte beräkna", "N/A"

    vg_pct = stats['vg_percent']
    g_pct = stats['g_percent']
    ig_pct = stats['ig_percent']

    if ig_pct > 50:
        prediction = "IG"
        reason = f"Över 50% av dina poäng ({ig_pct:.1f}%) är IG, vilket indikerar svårigheter."
    elif ig_pct > 25:
        if vg_pct >= 40:
            prediction = "G"
            reason = f"Du har {ig_pct:.1f}% IG men också {vg_pct:.1f}% VG, vilket balanserar till G."
        else:
            prediction = "G"
            reason = f"Du har {ig_pct:.1f}% IG-poäng, vilket gör VG osannolikt, men G är realistiskt."
    elif ig_pct > 0:
        if vg_pct >= 70:
            prediction = "VG"
            reason = f"Trots {ig_pct:.1f}% IG har du starka {vg_pct:.1f}% VG, vilket tyder på VG."
        else:
            prediction = "G"
            reason = f"Du har {ig_pct:.1f}% IG och {vg_pct:.1f}% VG, vilket balanserar till G."
    else:
        if vg_pct >= 70:
            prediction = "VG"
            reason = f"Du har {vg_pct:.1f}% VG-poäng, vilket starkt indikerar VG."
        elif vg_pct >= 50:
            prediction = "VG"
            reason = f"Du har {vg_pct:.1f}% VG-poäng, vilket gör VG troligt."
        elif vg_pct >= 30:
            prediction = "G"
            reason = f"Du har {vg_pct:.1f}% VG-poäng, vilket indikerar ett stabilt G."
        else:
            prediction = "G"
            reason = f"Du har främst G-betyg ({g_pct:.1f}%), vilket gör G mest sannolikt."

    return prediction, reason

# Hantera exempelintyg
if use_example:
    try:
        # Ladda exempelintyget från GitHub
        with urllib.request.urlopen(EXAMPLE_PDF_URL) as response:
            uploaded_file = response.read()
            st.info("📄 Exempelintyg laddat från GitHub")
    except Exception as e:
        st.error(f"❌ Kunde inte ladda exempelintyget: {str(e)}")
        st.write("Kontrollera att filen finns på GitHub: Studieintyg-Exempel.pdf")
        uploaded_file = None

if uploaded_file is not None:
    try:
        # Extrahera betyg och namn från PDF
        courses, student_name = extract_grades_from_pdf(uploaded_file)

        if not courses:
            st.error("❌ Ladda upp en korrekt PDF eller använd exempelintyget.")
        else:
            # Visa studentnamn om det hittades
            if student_name:
                st.success(f"👤 Student: **{student_name}**")

            # Visa extraherade kurser
            st.subheader("📚 Extraherade kurser")
            st.write(f"Totalt {len(courses)} betygsatta kurser hittades:")

            for course in courses:
                st.write(f"- **{course['name']}**: {course['points']} poäng - {course['grade']}")

            # Beräkna statistik
            stats = calculate_weighted_stats(courses)

            st.divider()

            # Visa statistik
            st.subheader("📊 Viktad statistik")
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("VG-poäng", f"{stats['vg_points']}/{stats['total_points']}")
                st.caption(f"{stats['vg_percent']:.1f}%")

            with col2:
                st.metric("G-poäng", f"{stats['g_points']}/{stats['total_points']}")
                st.caption(f"{stats['g_percent']:.1f}%")

            with col3:
                st.metric("IG-poäng", f"{stats['ig_points']}/{stats['total_points']}")
                st.caption(f"{stats['ig_percent']:.1f}%")

            st.divider()

            # Prediktion med namn
            prediction, reason = predict_grade(stats)

            # Anpassa header baserat på om vi har namn
            if student_name:
                st.subheader(f"🎯 Betygsprediktion för {student_name}")
            else:
                st.subheader("🎯 Betygsprediktion för Machine Learning")

            # Visa prediktion med färgkodning
            if prediction == "VG":
                st.success(f"### Predikterat betyg: **{prediction}** 🌟")
            elif prediction == "G":
                st.info(f"### Predikterat betyg: **{prediction}** ✅")
            else:
                st.warning(f"### Predikterat betyg: **{prediction}** ⚠️")

            st.write(f"**Motivering:** {reason}")

            # Tips
            st.divider()
            st.subheader("💡 Tips för Machine Learning-kursen")
            if prediction == "VG":
                st.write("Du har visat utmärkt prestation hittills! Fortsätt med samma dedikation och fokus på:")
                st.write("- Djup förståelse av algoritmer och koncept")
                st.write("- Väldokumenterad kod och analys")
                st.write("- Självständigt tänkande och problemlösning")
            elif prediction == "G":
                st.write("Du ligger på god väg! För att nå VG, fokusera på:")
                st.write("- Extra djupdykning i komplexa koncept")
                st.write("- Utforska användningsfall utanför kursmaterialet")
                st.write("- Visa djupare analys i dina inlämningar")
            else:
                st.write("Fokusera på att klara grunderna först:")
                st.write("- Se till att du förstår fundamentala koncept")
                st.write("- Använd alla tillgängliga resurser och fråga om hjälp")
                st.write("- Övning och repetition är nyckeln")

    except Exception as e:
        st.error("❌ Ladda upp en korrekt PDF eller använd exempelintyget.")
        st.write(f"Teknisk information: {str(e)}")

else:
    st.info("👆 Ladda upp ditt studieintyg eller använd exempelintyget för att komma igång!")

    # Instruktioner
    with st.expander("ℹ️ Hur fungerar det?"):
        st.write("""
        1. **Ladda upp** ditt studieintyg från YH Akademin (PDF-format)
        2. Eller klicka på **"Använd exempelintyg"** för att se hur det fungerar
        3. Appen **extraherar** automatiskt ditt namn, dina kurser och betyg
        4. **Viktad statistik** beräknas baserat på kurspoäng
        5. En **prediktion** görs för Machine Learning-kursen

        **Prediktionslogik:**
        - **VG**: ≥70% VG-poäng (starkt) eller ≥50% (med få/inga IG)
        - **G**: 30-70% VG-poäng, eller balanserat mellan VG/IG
        - **IG**: >50% IG-poäng

        Systemet tar hänsyn till både procent VG och procent IG för en mer nyanserad prediktion.
        Enstaka IG-kurser ger inte automatiskt IG om övriga prestationer är starka.
        """)
