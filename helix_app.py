import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import time

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Cellular Metabolism Assessment | Helix Media Lab",
    page_icon="🧬",
    layout="centered"
)

# 2. LINK DE AFILIADO
AFFILIATE_LINK = "https://47b7dbicrrxvlu7fopsf3l9y5u.hop.clickbank.net/?&campaign=PDF_QUIZ"

# 3. GERADOR DE PDF
def generate_pdf(name, age, score, status, description, metabolic_age, answers):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Header Branding
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "HELIX MEDIA LAB - MITOCHONDRIAL DIVISION")
    c.setFont("Helvetica", 10)
    c.drawString(100, 735, "Confidential Health Assessment Report | USA")
    c.line(100, 730, 500, 730)

    # Conteúdo Principal
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 690, "1. Cellular Metabolism Score")
    c.setFont("Helvetica", 12)
    c.drawString(120, 670, f"Score: {score}/100")
    c.drawString(120, 650, f"Status: {status}")

    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 610, "2. Estimated Metabolic Age")
    c.setFont("Helvetica", 12)
    c.drawString(120, 590, f"Chronological Age: {age}")
    c.drawString(120, 570, f"Estimated Cellular Age: {metabolic_age} years old")

    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 530, "3. Mitochondrial Pattern Analysis")
    c.setFont("Helvetica", 11)
    text_object = c.beginText(120, 510)
    text_object.setLeading(14)
    text_object.textLines(description)
    c.drawText(text_object)

    # Key Indicators
    energy_marker = "Stable" if answers["q1"] == "Energized" else "Reduced Output"
    weight_marker = "Optimal" if answers["q4"] == "No" else "Elevated Resistance"
    brain_marker = "Clear" if answers["q5"] == "Rarely" else "Reduced Clarity"

    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 440, "4. Key Indicators")
    c.setFont("Helvetica", 11)
    c.drawString(120, 420, f"Morning Energy Stability: {energy_marker}")
    c.drawString(120, 405, f"Weight Resistance Marker: {weight_marker}")
    c.drawString(120, 390, f"Cognitive Clarity Marker: {brain_marker}")

    # Footer
    c.line(100, 340, 500, 340)
    c.setFont("Helvetica", 8)
    c.drawCentredString(300, 50, "© 2026 Helix Media Lab. For informational purposes only. This is not medical advice.")
    
    c.save()
    buffer.seek(0)
    return buffer

# 4. TRACKING LOG
def log_event(event_name, detail=""):
    print(f"[TRACKING] {event_name.upper()} | {detail}")

# 5. APP INTERFACE
def main():
    st.title("🧬 Cellular Metabolism Assessment")
    st.write("---")

    if 'step' not in st.session_state:
        st.session_state.step = 1

    # STEP 1: IDADE (Com Limpeza de Sessão Sugerida pela Eva)
    if st.session_state.step == 1:
        st.subheader("Start your assessment")
        age = st.number_input("Current Age:", min_value=18, max_value=100, value=40)
        
        if st.button("Start Assessment"):
            # Limpeza cirúrgica para evitar vazamento de dados de sessões anteriores
            for key in ["lead_logged", "user_name", "user_email", "final_data", "answers"]:
                st.session_state.pop(key, None)
            
            st.session_state.user_age = age
            log_event("quiz_started", f"age={age}")
            st.session_state.step = 2
            st.rerun()

    # STEP 2: QUIZ
    elif st.session_state.step == 2:
        st.subheader("Mitochondrial Pattern Screening")
        q1 = st.radio("1. How do you usually feel within 30 mins of waking up?", ["Energized", "A little slow", "Tired and unmotivated"], index=None)
        q2 = st.radio("2. Do you often experience an energy crash in the afternoon?", ["Rarely", "Sometimes", "Almost every day"], index=None)
        q3 = st.radio("3. Do you tend to feel colder than other people around you?", ["No", "Sometimes", "Yes, often"], index=None)
        q4 = st.radio("4. Do you struggle to lose weight even when eating less?", ["No", "Sometimes", "Yes, consistently"], index=None)
        q5 = st.radio("5. How often do you experience brain fog?", ["Rarely", "Sometimes", "Frequently"], index=None)

        if st.button("Generate My Report"):
            if all([q1, q2, q3, q4, q5]):
                mapping = {"Energized": 3, "A little slow": 2, "Tired and unmotivated": 0, "Rarely": 3, "Sometimes": 1, "Almost every day": 0, "Frequently": 0, "No": 3, "Yes, often": 0, "Yes, consistently": 0}
                total_pts = sum([mapping.get(q, 1) for q in [q1, q2, q3, q4, q5]])
                score = int((total_pts / 15) * 90)
                
                st.session_state.answers = {"q1": q1, "q2": q2, "q3": q3, "q4": q4, "q5": q5}
                
                if score <= 40:
                    status, age_plus = "Cellular Energy Deficit", 12
                    desc = "Your results suggest a pronounced reduction in cellular energy efficiency. This pattern is often associated with slower metabolic activity and reduced fat-burning responsiveness."
                elif score <= 70:
                    status, age_plus = "Sluggish Metabolic Function", 6
                    desc = "Your answers indicate signs of reduced mitochondrial output. Your metabolism may currently be working below its ideal cellular potential."
                else:
                    status, age_plus = "Balanced Cellular Output", 2
                    desc = "Your cellular energy profile appears relatively stable, although there may still be room to improve metabolic efficiency and long-term energy balance."

                st.session_state.final_data = {"score": score, "status": status, "desc": desc, "met_age": st.session_state.user_age + age_plus}
                log_event("quiz_completed", f"score={score}|status={status}") # Log melhorado
                st.session_state.step = 3
                st.rerun()
            else:
                st.warning("Please answer all questions.")

    # STEP 3: ANALYZING
    elif st.session_state.step == 3:
        st.subheader("Analyzing your cellular metabolism...")
        with st.status("Scanning mitochondrial markers...", expanded=True) as s:
            time.sleep(1.2)
            s.update(label="Matching age-related energy patterns...", state="running")
            time.sleep(1.2)
            s.update(label="Assessment complete.", state="complete")
        st.session_state.step = 4
        st.rerun()

    # STEP 4: RESULTADO + LEAD + CTA
    elif st.session_state.step == 4:
        data = st.session_state.final_data
        st.warning("Your results suggest that reduced cellular energy may be affecting how efficiently your body burns fuel.")
        
        col1, col2 = st.columns(2)
        col1.metric("Cellular Score", f"{data['score']}/100")
        col2.metric("Metabolic Age", f"{data['met_age']} yrs")
        st.info(f"**Summary:** {data['desc']}")

        st.write("---")
        st.subheader("📩 Unlock your full PDF report")
        st.caption("Enter your details to unlock your personalized PDF report instantly.") # UX Caption
        name = st.text_input("First Name:")
        email = st.text_input("Email Address:")

        if name and "@" in email:
            st.session_state.user_name, st.session_state.user_email = name, email
            if "lead_logged" not in st.session_state:
                log_event("lead_captured", f"email={email}")
                st.session_state.lead_logged = True
            
            pdf_buf = generate_pdf(name, st.session_state.user_age, data['score'], data['status'], data['desc'], data['met_age'], st.session_state.answers)
            st.download_button(label=f"📩 DOWNLOAD {name.upper()}'S REPORT (PDF)", data=pdf_buf, file_name=f"{name}_Helix_Report.pdf", mime="application/pdf", on_click=lambda: log_event("pdf_downloaded", email))

        st.write("---")
        st.subheader("💡 Urgent Recommendation")
        st.write("Based on your cellular profile, you should watch this short presentation to understand the nutrient protocol many are using to support metabolic function.")
        if st.link_button("WATCH PRESENTATION NOW", AFFILIATE_LINK, type="primary"):
            log_event("affiliate_click", "mitolyn_cta")

if __name__ == "__main__":
    main()
