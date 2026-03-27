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

```bash
# 1. Clone the repository
git clone [https://github.com/fayfayMN/Career-Orchestrator-MultiAgent-Platform.git](https://github.com/fayfayMN/Career-Orchestrator-MultiAgent-Platform.git)

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the Orchestrator
streamlit run app.py
