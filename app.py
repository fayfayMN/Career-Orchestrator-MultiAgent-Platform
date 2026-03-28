import streamlit as st
import pdfplumber
import sys
import os
from io import BytesIO
from docx import Document
from gtts import gTTS
from streamlit_mic_recorder import mic_recorder

# --- 1. PATH RESILIENCE ---
root_path = os.path.dirname(os.path.abspath(__file__))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

# --- 2. PAGE CONFIGURATION ---
st.set_page_config(page_title="Job-Ready v2.0", layout="wide")

# --- 3. IMPORT GENERALIZED AGENTS ---
try:
    from agents.strategy_arch import run_strategy_architect
    from agents.ats_architect import run_ats_architect
    from agents.human_narrator import run_human_narrator
    from agents.integrity import run_integrity_guardian, evaluate_and_reorg_answer 
except Exception as e:
    st.error(f"🛑 Critical Load Failure: {e}")
    st.stop()

# --- 4. SESSION STATE ---
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = ""
if 'final_results' not in st.session_state:
    st.session_state.final_results = None

# --- 5. HELPERS: DOWNLOAD ENGINE ---
def generate_docx_report(company, level, jd, results):
    doc = Document()
    doc.add_heading(f"Strategy Report: {company}", 0)
    
    doc.add_heading("Target Role Context", level=1)
    doc.add_paragraph(f"**Target Company:** {company}")
    doc.add_paragraph(f"**Target Role:** {level}")
    
    strat = results.get('strategy', {})
    doc.add_heading("Layer 1: Strategic Audit", level=1)
    doc.add_paragraph(f"Match Score: {strat.get('match_score', 'N/A')}%")
    doc.add_paragraph(f"Persona: {strat.get('persona_assessment', 'N/A')}")
    doc.add_paragraph(strat.get('learning_syllabus', ''))
    
    ats = results.get('ats', {})
    doc.add_heading("Layer 2: Optimized ATS Bullets", level=1)
    doc.add_paragraph(f"Recruiter Verdict: {ats.get('recruiter_scan_verdict', 'N/A')}")
    for exp in ats.get('optimized_experience', []):
        role_text = f"{exp.get('Role', 'Experience')} | {exp.get('Tech_Stack', '')}"
        doc.add_heading(role_text, level=2)
        for bullet in exp.get('Bullets', []):
            doc.add_paragraph(bullet, style='List Bullet')
    
    doc.add_heading("Layer 3: Formal Cover Letter", level=1)
    doc.add_paragraph(results.get('narrative', {}).get('cover_letter_narrative', ''))
    
    doc.add_heading("Layer 4: Interview Drills", level=1)
    drills = results.get('integrity', {}).get('interview_drills', [])
    for d in drills:
        doc.add_heading("Dynamic Drill", level=2)
        doc.add_paragraph(f"Q: {d.get('question', '')}")
        doc.add_paragraph(f"Hint: {d.get('strategic_hint', '')}")

    bio = BytesIO()
    doc.save(bio)
    return bio.getvalue()

# --- 6. SIDEBAR: PERSONA & DNA ---
with st.sidebar:
    st.header("👤 Persona Discovery")
    api_key = st.text_input("DeepSeek API Key", type="password")
    user_strengths = st.text_area("Your Top 3 Strengths", placeholder="e.g., Reliability, Python, Grit")
    user_weaknesses = st.text_area("Gaps/Weaknesses", placeholder="e.g., Impatience")
    writing_dna_choice = st.selectbox("Base Writing Style", ["Blunt & Gritty", "Professional", "Academic"])
    
    st.header("🧬 Linguistic DNA")
    style_file = st.file_uploader("Upload a Writing Sample", type=["pdf", "docx"], key="style_upload")
    style_text = ""
    if style_file:
        try:
            if style_file.type == "application/pdf":
                with pdfplumber.open(style_file) as pdf:
                    style_text = "\n".join([p.extract_text() for p in pdf.pages if p.extract_text()])
            else:
                doc_style = Document(style_file)
                style_text = "\n".join([p.text for p in doc_style.paragraphs])
            st.success("✅ DNA Captured")
        except: st.error("Style parsing failed.")

    st.header("📂 Ingestion")
    uploaded_file = st.file_uploader("Upload Master Resume", type=["pdf", "docx"])
    if uploaded_file:
        if uploaded_file.type == "application/pdf":
            with pdfplumber.open(uploaded_file) as pdf:
                st.session_state.resume_text = "\n".join([p.extract_text() for p in pdf.pages if p.extract_text()])
        else:
            doc_res = Document(uploaded_file)
            st.session_state.resume_text = "\n".join([p.text for p in doc_res.paragraphs])
        st.success("✅ Resume Memory Locked")

# --- 7. MAIN UI ---
st.title("🚀 Job-Ready: The No-Fluff Career Engine")
c1, c2 = st.columns(2)
with c1:
    company_name = st.text_input("Target Company", value="Johnson Brothers")
    job_level = st.selectbox("Job Level", ["Intern", "Junior", "Senior", "Lead"]) 
with c2:
    jd_input = st.text_area("Target Job Description", height=150)

# --- 8. ORCHESTRATION ---
if st.button("🔥 Run Full Optimization"):
    if not st.session_state.resume_text or not api_key:
        st.error("❌ Missing Resume or API Key.")
    else:
        try:
            with st.status("Orchestrating Agents...") as status:
                st.write("🕵️ Phase 1: Strategy Architect...")
                strat = run_strategy_architect(st.session_state.resume_text, jd_input, job_level, company_name, api_key, user_strengths, user_weaknesses, writing_dna_choice)
                
                st.write("🤖 Phase 2: ATS Architect...")
                ats = run_ats_architect(st.session_state.resume_text, jd_input, job_level, company_name, strat.get('missing_gaps', []), api_key, writing_dna_choice)
                
                st.write("✍️ Phase 3: Human Narrator...")
                narrative = run_human_narrator(st.session_state.resume_text, jd_input, strat.get('persona_assessment', ''), writing_dna_choice, company_name, job_level, api_key, style_text)
                
                st.write("🛡️ Phase 4: Integrity Guardian...")
                integrity = run_integrity_guardian(st.session_state.resume_text, ats, narrative, strat.get('missing_gaps', []), api_key, job_level)
                
                st.session_state.final_results = {"strategy": strat, "ats": ats, "narrative": narrative, "integrity": integrity}
                status.update(label="✅ Optimization Complete!", state="complete")
            st.rerun() 
        except Exception as e:
            st.error(f"❌ Orchestration Error: {e}")
            
# --- 9. RESULTS DISPLAY ---
if st.session_state.final_results:
    res = st.session_state.final_results
    st.divider()
    
    st.subheader("👤 Candidate Persona & Management Roadmap")
    col_narr, col_risk = st.columns(2)
    with col_narr:
        st.info(f"**Persona Fit:** {res['strategy'].get('persona_assessment', 'Standard Grit Pattern')}")
    with col_risk:
        # FIXED KEY: Changed from 'internal_placement_strategy' to 'value_anchor' to match your Narrator Agent
        st.warning(f"**Strategy:** {res['narrative'].get('value_anchor', 'Transferable Logic Bridge Enabled')}")

    t1, t2, t3, t4 = st.tabs(["📊 Strategy", "📄 ATS Bullets", "✉️ Formal Cover Letter", "🎙️ Voice Practice"])
    
    with t1:
        st.metric("Match Score", f"{res['strategy'].get('match_score', 0)}%")
        st.markdown(res['strategy'].get('learning_syllabus', ''))
    
    with t2:
        st.subheader("📄 Tailored Technical Resume")
        ats_data = res.get('ats', {})
        if ats_data:
            st.markdown("### Feifei Li") # Anchored to your identity
            st.caption("Data Science | Operational Excellence | Data Integrity Specialist")
            st.divider()

            for item in ats_data.get('optimized_experience', []):
                role = item.get('Role', 'Project')
                stack = item.get('Tech_Stack', 'Technical Stack')
                st.markdown(f"#### {role} | {stack}")
                for bullet in item.get('Bullets', []):
                    clean_bullet = bullet.lstrip('• ').lstrip('✅ ')
                    st.write(f"• {clean_bullet}")
                st.write("") 
        else:
            st.error("No experience data generated.")

    with t3:
        st.subheader("✉️ Formal Persona-Driven Cover Letter")
        letter = res['narrative'].get('cover_letter_narrative', "")
        st.text_area("Review your Letter:", letter, height=400)
        st.download_button("📥 Download Report (.docx)", generate_docx_report(company_name, job_level, jd_input, res), file_name=f"{company_name}_Career_Pack.docx")

    with t4:
        st.subheader("🎙️ Interactive Technical Drill")
        drills = res.get('integrity', {}).get('interview_drills', [])
        
        if drills:
            # 1. State Persistence for Audio
            if 'last_recording' not in st.session_state:
                st.session_state.last_recording = None
    
            drill_map = {d['question']: d['strategic_hint'] for d in drills}
            q_selected = st.selectbox("Select Drill:", list(drill_map.keys()))
            
            st.info(f"**Challenge:** {q_selected}")
            with st.expander("💡 View Strategic Hint (Tailored STAR)"):
                st.write(drill_map[q_selected])
    
            if st.button("📢 Hear Question"):
                tts = gTTS(text=q_selected, lang='en')
                audio_fp = BytesIO()
                tts.write_to_fp(audio_fp)
                st.audio(audio_fp.getvalue(), format='audio/mp3')
    
            st.divider()
            st.write("Record your answer:")
            
            # 2. Capture and store audio immediately
            audio_data = mic_recorder(start_prompt="🎤 Start Recording", stop_prompt="🛑 Stop", key=f'mic_{q_selected}')
            
            if audio_data:
                st.session_state.last_recording = audio_data['bytes']
    
            # 3. Display the persistent audio player
            if st.session_state.last_recording:
                st.audio(st.session_state.last_recording)
                
            # --- Inside Tab 4 (Voice Practice) ---
            if st.button("⚖️ Get Blunt Feedback & STAR Reorg"):
                with st.spinner("Analyzing your grit..."):
                    # MANDATORY: Pass the 'q_selected' variable so the AI knows the context
                    feedback = evaluate_and_reorg_answer(
                        question=q_selected, 
                        user_transcript=user_answer_text, # Ensure this is your recorded text
                        api_key=api_key
                    )
                    st.markdown("### 📝 Coach's Blunt Feedback")
                    st.warning(feedback)
        else:
            st.warning("No drills generated.")
