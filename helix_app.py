import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Mitochondrial Assessment | Helix Media Lab",
    page_icon="🧬",
    layout="centered"
)

# 2. SEU LINK REGISTRADO (CLICKBANK)
AFFILIATE_LINK = "https://47b7dbicrrxvlu7fopsf3l9y5u.hop.clickbank.net/?&campaign=PDF_QUIZ"

# 3. FUNÇÃO DO GERADOR DE PDF
def generate_pdf(name, age, score, status, description, metabolic_age):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Header Branding
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "HELIX MEDIA LAB - MITOCHONDRIAL DIVISION")
    c.setFont("Helvetica", 10)
    c.drawString(100, 735, "Confidential Health Assessment Report | USA")
    c.line(100, 730, 500, 730)

    # Score Section
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 690, "1. Cellular Metabolism Score")
    c.setFont("Helvetica", 12)
    c.drawString(120, 670, f"Score: {score}/100")
    c.drawString(120, 650, f"Status: {status}")

    # Metabolic Age Section
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 610, "2. Estimated Metabolic Age")
    c.setFont("Helvetica", 12)
    c.drawString(120, 590, f"Chronological Age: {age}")
    c.setFont("Helvetica-Bold", 13)
    c.drawString(120, 570, f"Estimated Cellular Age: {metabolic_age} years old")

    # Pattern Analysis
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 530, "3. Mitochondrial Pattern Analysis")
    c.setFont("Helvetica", 11)
    text_object = c.beginText(120, 510)
    text_object.setLeading(14)
    text_object.textLines(description)
    c.drawText(text_object)

    # CTA Footer
    c.line(100, 440, 500, 440)
    c.setFont("Helvetica-Oblique", 11)
    c.drawString(100, 420, "To reactivate your cellular energy, refer to the recommended nutrient protocol.")
    
    c.setFont("Helvetica", 8)
    c.drawCentredString(300, 50, "© 2026 Helix Media Lab. For informational purposes only. This is not medical advice.")
    
    c.save()
    buffer.seek(0)
    return buffer

# 4. INTERFACE DO APP (STREAMLIT)
def main():
    st.title("🧬 Mitochondrial Health Assessment")
    st.write("---")

    if 'step' not in st.session_state:
        st.session_state.step = 1

    # PASSO 1: CAPTURA DE DADOS
    if st.session_state.step == 1:
        st.subheader("Personal Information")
        name = st.text_input("First Name:", placeholder="Enter your name")
        age = st.number_input("Current Age:", min_value=18, max_value=100, value=40)
        
        if st.button("Start Assessment"):
            if name:
                st.session_state.user_name = name
                st.session_state.user_age = age
                st.session_state.step = 2
                st.rerun()
            else:
                st.error("Please provide your name.")

    # PASSO 2: O QUIZ
    elif st.session_state.step == 2:
        st.subheader(f"Analyzing Cellular Energy for {st.session_state.user_name}")
        
        q1 = st.radio("1. How do you usually feel within 30 mins of waking up?", ["Energized", "A little slow", "Tired and unmotivated"], index=None)
        q2 = st.radio("2. Do you often experience an energy crash in the afternoon?", ["Rarely", "Sometimes", "Almost every day"], index=None)
        q3 = st.radio("3. Do you tend to feel colder than other people around you?", ["No", "Sometimes", "Yes, often"], index=None)
        q4 = st.radio("4. Do you struggle to lose weight even when eating less?", ["No", "Sometimes", "Yes, consistently"], index=None)
        q5 = st.radio("5. How often do you experience brain fog?", ["Rarely", "Sometimes", "Frequently"], index=None)

        if st.button("Generate My Report"):
            if all([q1, q2, q3, q4, q5]):
                # Lógica de Pontuação (Peso 1 a 3)
                mapping = {"Energized": 3, "A little slow": 2, "Tired and unmotivated": 1,
                           "Rarely": 3, "Sometimes": 2, "Almost every day": 1, "Frequently": 1,
                           "No": 3, "Yes, often": 1, "Yes, consistently": 1}
                
                total_pts = sum([mapping.get(q, 2) for q in [q1, q2, q3, q4, q5]])
                score = int((total_pts / 15) * 100)
                
                # Classificação e Idade Metabólica
                if score <= 45:
                    status = "Cellular Energy Deficit"
                    metabolic_age = st.session_state.user_age + 10
                    desc = "Your cells indicate a significant slowdown in mitochondrial energy output.\nThis state often forces the body to store fat for survival."
                elif score <= 75:
                    status = "Sluggish Metabolic Function"
                    metabolic_age = st.session_state.user_age + 4
                    desc = "Your results suggest signs of reduced cellular energy efficiency.\nYour metabolism is functioning below its natural potential."
                else:
                    status = "Balanced Cellular Output"
                    metabolic_age = st.session_state.user_age - 1
                    desc = "Your cellular energy levels appear stable.\nOptimization is recommended to maintain peak fat-burning speed."

                st.session_state.final_data = {
                    "score": score, "status": status, "desc": desc, "met_age": metabolic_age
                }
                st.session_state.step = 3
                st.rerun()
            else:
                st.warning("Please answer all questions.")

    # PASSO 3: RESULTADOS E DOWNLOAD
    elif st.session_state.step == 3:
        data = st.session_state.final_data
        st.success("✅ Your Assessment is Complete!")
        
        col1, col2 = st.columns(2)
        col1.metric("Cellular Score", f"{data['score']}/100")
        col2.metric("Metabolic Age", f"{data['met_age']} yrs")

        st.info(f"**Analysis:** {data['desc']}")

        # Download do PDF
        pdf_buf = generate_pdf(
            st.session_state.user_name, st.session_state.user_age,
            data['score'], data['status'], data['desc'], data['met_age']
        )
        
        st.download_button(
            label="📩 DOWNLOAD YOUR DETAILED REPORT (PDF)",
            data=pdf_buf,
            file_name=f"Helix_Metabolic_Report.pdf",
            mime="application/pdf"
        )

        st.write("---")
        st.subheader("💡 Urgent Recommendation")
        st.write("Based on your mitochondrial pattern, you should watch this clinical presentation on how to reactivate your cellular engines.")
        
        st.link_button("WATCH PRESENTATION NOW", AFFILIATE_LINK, type="primary")

if __name__ == "__main__":
    main()