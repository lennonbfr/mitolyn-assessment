import io
import time

import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph


# 1. PAGE CONFIG
st.set_page_config(
    page_title="Cellular Metabolism Assessment | Helix Media Lab",
    page_icon="🧬",
    layout="centered"
)

# 2. AFFILIATE LINK
AFFILIATE_LINK = "https://47b7dbicrrxvlu7fopsf3l9y5u.hop.clickbank.net/?&campaign=PDF_QUIZ"


# 3. TRACKING
def log_event(event_name: str, detail: str = "") -> None:
    print(f"[TRACKING] {event_name.upper()} | {detail}")


# 4. PDF GENERATOR
def generate_pdf(
    name: str,
    age: int,
    score: int,
    status: str,
    description: str,
    metabolic_age: int,
    answers: dict
) -> io.BytesIO:
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    body_style = ParagraphStyle(
        "BodyStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=11,
        leading=14,
        alignment=0,
    )

    # Header
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

    # 3. Mitochondrial Pattern Analysis
    c.setFont("Helvetica-Bold", 14)
    start_y_analysis = 530
    c.drawString(100, start_y_analysis, "3. Mitochondrial Pattern Analysis")

    p = Paragraph(description, body_style)
    _, h = p.wrap(400, 200)
    p.drawOn(c, 120, start_y_analysis - h - 10)

    # 4. Key Indicators
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

    # Footer line
    footer_y = next_y - 100
    c.line(100, footer_y, 500, footer_y)

    # Footer text
    c.setFont("Helvetica", 8)
    c.drawCentredString(
        300,
        50,
        "© 2026 Helix Media Lab. For informational purposes only. This is not medical advice."
    )

    c.save()
    buffer.seek(0)
    return buffer


# 5. MAIN APP
def main() -> None:
    st.title("🧬 Cellular Metabolism Assessment")
    st.write("---")

    if "step" not in st.session_state:
        st.session_state.step = 1

    # STEP 1: AGE ONLY
    if st.session_state.step == 1:
        st.subheader("Start your assessment")
        age = st.number_input("Current Age:", min_value=18, max_value=100, value=40)

        if st.button("Start Assessment"):
            # Reset session data to avoid leaking previous run info
            for key in [
                "lead_logged",
                "user_name",
                "user_email",
                "final_data",
                "answers",
                "pdf_unlocked",
            ]:
                st.session_state.pop(key, None)

            st.session_state.user_age = age
            log_event("quiz_started", f"age={age}")
            st.session_state.step = 2
            st.rerun()

    # STEP 2: QUIZ
    elif st.session_state.step == 2:
        st.subheader("Mitochondrial Pattern Screening")

        q1 = st.radio(
            "1. How do you usually feel within 30 mins of waking up?",
            ["Energized", "A little slow", "Tired and unmotivated"],
            index=None
        )
        q2 = st.radio(
            "2. Do you often experience an energy crash in the afternoon?",
            ["Rarely", "Sometimes", "Almost every day"],
            index=None
        )
        q3 = st.radio(
            "3. Do you tend to feel colder than other people around you?",
            ["No", "Sometimes", "Yes, often"],
            index=None
        )
        q4 = st.radio(
            "4. Do you struggle to lose weight even when eating less?",
            ["No", "Sometimes", "Yes, consistently"],
            index=None
        )
        q5 = st.radio(
            "5. How often do you experience brain fog?",
            ["Rarely", "Sometimes", "Frequently"],
            index=None
        )

        if st.button("Generate My Report"):
            if all([q1, q2, q3, q4, q5]):
                mapping = {
                    "Energized": 3,
                    "A little slow": 2,
                    "Tired and unmotivated": 0,
                    "Rarely": 3,
                    "Sometimes": 1,
                    "Almost every day": 0,
                    "Frequently": 0,
                    "No": 3,
                    "Yes, often": 0,
                    "Yes, consistently": 0,
                }

                total_pts = sum(mapping.get(q, 1) for q in [q1, q2, q3, q4, q5])
                score = int((total_pts / 15) * 90)

                st.session_state.answers = {
                    "q1": q1,
                    "q2": q2,
                    "q3": q3,
                    "q4": q4,
                    "q5": q5,
                }

                if score <= 40:
                    status = "Cellular Energy Deficit"
                    age_plus = 12
                    desc = (
                        "Your results suggest a pronounced reduction in cellular energy "
                        "efficiency. This pattern is often associated with slower metabolic "
                        "activity and reduced fat-burning responsiveness."
                    )
                elif score <= 70:
                    status = "Sluggish Metabolic Function"
                    age_plus = 6
                    desc = (
                        "Your answers indicate signs of reduced mitochondrial output. "
                        "Your metabolism may currently be working below its ideal "
                        "cellular potential."
                    )
                else:
                    status = "Balanced Cellular Output"
                    age_plus = 2
                    desc = (
                        "Your cellular energy profile appears relatively stable, although "
                        "there may still be room to improve metabolic efficiency and "
                        "long-term energy balance."
                    )

                st.session_state.final_data = {
                    "score": score,
                    "status": status,
                    "desc": desc,
                    "met_age": st.session_state.user_age + age_plus,
                }

                log_event("quiz_completed", f"score={score}|status={status}")
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

    # STEP 4: RESULT + LEAD + PDF + CTA
    elif st.session_state.step == 4:
        data = st.session_state.final_data

        st.warning(
            "Your results suggest that reduced cellular energy may be affecting "
            "how efficiently your body burns fuel."
        )

        col1, col2 = st.columns(2)
        col1.metric("Cellular Score", f"{data['score']}/100")
        col2.metric("Metabolic Age", f"{data['met_age']} yrs")

        st.info(f"**Summary:** {data['desc']}")

        st.write("---")
        st.subheader("📩 Unlock your full PDF report")
        st.caption("Enter your details to unlock your personalized PDF report instantly.")

        name = st.text_input("First Name:")
        email = st.text_input("Email Address:")

        if name and "@" in email:
            st.session_state.user_name = name
            st.session_state.user_email = email

            if "lead_logged" not in st.session_state:
                log_event("lead_captured", f"email={email}")
                st.session_state.lead_logged = True

            pdf_buf = generate_pdf(
                name=name,
                age=st.session_state.user_age,
                score=data["score"],
                status=data["status"],
                description=data["desc"],
                metabolic_age=data["met_age"],
                answers=st.session_state.answers,
            )

            downloaded = st.download_button(
                label=f"📩 DOWNLOAD {name.upper()}'S REPORT (PDF)",
                data=pdf_buf,
                file_name=f"{name}_Helix_Report.pdf",
                mime="application/pdf",
            )

            if downloaded:
                log_event("pdf_downloaded", email)
                st.session_state.pdf_unlocked = True
                st.success("Your report is ready. You can now continue to the presentation.")

            if st.session_state.get("pdf_unlocked"):
                st.write("---")
                st.subheader("💡 Urgent Recommendation")
                st.write(
                    "Based on your cellular profile, you should watch this short presentation "
                    "to understand the nutrient protocol many are using to support metabolic function."
                )

                if st.button("WATCH PRESENTATION NOW", type="primary"):
                    log_event("affiliate_click", "mitolyn_cta")
                    st.markdown(
                        f'<meta http-equiv="refresh" content="0;URL={AFFILIATE_LINK}">',
                        unsafe_allow_html=True
                    )
        else:
            st.caption("Enter your name and a valid email to unlock the PDF.")


if __name__ == "__main__":
    main()
