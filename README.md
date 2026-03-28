# 🚀 Career Orchestrator: 8-Agent "Seniority-Aware" Engine

**Bridging the gap between high-grit talent and automated hiring filters through dual-track agentic reasoning.**


---

### 📌 The Mission
Traditional Applicant Tracking Systems (ATS) often create "blind spots" for high-resilience candidates. This platform utilizes an **8-Agent Pipeline** to audit job requirements, generate seniority-tuned upskilling syllabi, and preserve a candidate's authentic voice through advanced semantic sanitization.

---

### 🧠 System Architecture: The "Context-Aware" Workflow
Unlike standard LLM wrappers, this system utilizes **Semantic Intent Filtering** to distinguish between **Analytical** (Data Science) and **Engineering** (Software) roles.

| Agent | Responsibility | Key Technical Feature |
| :--- | :--- | :--- |
| **1. The Auditor** | Semantic Gap Analysis | **The Gatekeeper:** JSON-based scoring; halts pipeline if Match Score < 50%. |
| **2. The Tutor** | Seniority-Tuned Bridging | **Smart-Pivot:** Detects role type (e.g., Software vs. Analyst) to generate level-appropriate 48-hour syllabi. |
| **3. The Storyteller** | ATS Optimization | **ATS Engine:** Converts resume facts into professional, third-person bullets. |
| **4. The Voice Filter** | Human Authenticity | **Semantic Sanitizer:** Restores a blunt, resilient human tone for cover letters. |
| **5. The Fact-Checker** | Data Integrity | **Reflection Agent:** Cross-references outputs against Master Resume facts. |
| **6. The Composer** | Synthesis | Fuses "Human Grit" stories with company-specific objectives. |
| **7. The Resume Pro** | ATS Re-Architecting | **Keyword Injection:** Rebuilds the resume based on JD keyword frequency. |
| **8. The Coach** | Interview Simulation | Technical "grills" with **gTTS (Text-to-Speech)** voice-over and grading. |

---

### 🛠️ Advanced Engineering Features
* **Multimodal Ingestion Layer:** Supports binary file streams (**PDF/DOCX**) for automated resume parsing via `pdfplumber` and `python-docx`.
* **Context-Aware Reporting:** Automated `.docx` generation that anchors all AI output to the specific **Target Company Name** and **Job Description Metadata**.
* **Dual-Track Optimization:** Simultaneously optimizes for **Machine Algorithms** (ATS) and **Human Empathy** (Hiring Manager).
* **Network Resilience:** Custom `APIConnectionError` handling for stable high-traffic LLM cycles.

---

### 📈 Project Status: Phase 5 Complete (Professional Ingestion)
* **Phase 1-3:** Core logic, Reflection loops, and Multimodal (TTS) features.
* **Phase 4:** **Seniority-Aware Logic** and **ATS Resume Re-Architecting**.
* **Phase 5:** **Binary File Parsing** and **Contextual Report Generation**.

---

### 📂 Quick Start

[https://career-orchestrator-multiagent-platformgit-nyoayktbvkpcsbgamg7.streamlit.app/](url)

```bash
# 1. Clone the repository
git clone [https://github.com/fayfayMN/Career-Orchestrator-MultiAgent-Platform.git](https://github.com/fayfayMN/Career-Orchestrator-MultiAgent-Platform.git)

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the Orchestrator
streamlit run app.py

## 🛠️ Development Log & Optimization Journal

This section tracks the architectural evolution of the Career Orchestrator, highlighting key technical challenges and engineering pivots.

### **Log 01: From Sequential to Parallel (The Latency Sprint)**
* **Problem:** The initial 8-agent pipeline ran sequentially, causing a 45+ second wait time that degraded user experience.
* **Solution:** Refactored the orchestration layer using Python's `asyncio`. By implementing `asyncio.gather`, independent agents (e.g., **Tutor** and **Storyteller**) now fire simultaneously.
* **Result:** Reduced end-to-end execution time by **~60%**, achieving sub-15-second response times for the full analysis package.

### **Log 02: Binary Stream Ingestion (The "No-Paste" Pivot)**
* **Problem:** Manual "Copy-Paste" of resumes introduced data truncation and formatting errors, weakening the **Auditor's** accuracy.
* **Solution:** Integrated `pdfplumber` and `python-docx` to handle raw binary file streams. The system now programmatically parses uploaded files to ensure 100% data fidelity.
* **Technical Win:** Implemented error-handling for non-standard PDF encodings, ensuring a robust ingestion layer for diverse user inputs.

### **Log 03: Context-Aware Persistence & Data Provenance**
* **Problem:** AI-generated artifacts lacked traceability; users couldn't see the specific JD constraints that triggered certain resume keywords.
* **Solution:** Re-engineered the `.docx` export function to inject **Company Name** and **Target JD Metadata** as a "Reference Layer" at the top of every report.
* **Benefit:** Achieved **Data Provenance**, allowing candidates to audit why the **Resume Pro** agent chose specific engineering keywords (like FastAPI or Azure) for a given role.

### **Log 04: Handling API Connection Instability**
* **Problem:** High-traffic periods on the DeepSeek API caused frequent `APIConnectionError` crashes during the Audit phase. 
* **Solution:** Implemented custom **Exception Handling** and **Exponential Backoff** logic. The app now provides clear user feedback and retries the connection rather than crashing.
