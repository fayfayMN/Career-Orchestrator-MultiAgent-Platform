# 🚀 Career Orchestrator: Multi-Agent AI Strategy Engine
**Bridging the gap between hidden talent and automated hiring filters through high-fidelity agentic reasoning.**

---

### 📌 The Mission
Traditional Applicant Tracking Systems (ATS) often create "blind spots" for high-resilience candidates, such as first-generation scholars. This platform utilizes a **7-Agent Pipeline** to audit job requirements, generate rapid-upskilling syllabi, and preserve a candidate's authentic voice through advanced reflection and multimodal interaction.

---

### 🧠 System Architecture: The "Gatekeeper" Workflow
Unlike standard LLM wrappers, this system utilizes a **Conditional Execution Pipeline** to ensure data integrity and computational efficiency. 

| Agent | Responsibility | Key Technical Feature |
| :--- | :--- | :--- |
| **1. The Auditor** | Semantic Gap Analysis | **The Gatekeeper:** JSON-based scoring; halts pipeline if Match Score < 60%. |
| **2. The Tutor** | Technical Bridging | Generates a custom **48-Hour Learning Syllabus** for identified gaps. |
| **3. The Storyteller** | Narrative Generation | Drafts high-impact **STAR-method** bullets and professional artifacts. |
| **4. The Voice Filter** | Human Authenticity | Strips "AI-sounding" buzzwords to restore a resilient, blunt human tone. |
| **5. The Fact-Checker** | Data Integrity | **Reflection Agent:** Cross-references AI output against Master Resume. |
| **6. The Composer** | Synthesis | Finalizes formal, company-specific Cover Letters. |
| **7. The Coach** | Interview Prep | Provides technical "grills" with a **Professional Hint Layer**. |

---

### 🛠️ Tech Stack & Advanced Patterns
* **Core Logic:** Multi-agent Orchestration (Python / DeepSeek API).
* **Design Patterns:** * **Gatekeeper Logic:** Conditional branching based on real-time audit metrics.
    * **Reflection:** Recursive fact-checking loops to eliminate hallucinations.
    * **Structured Output:** Strict **JSON Parsing** for deterministic UI updates.
* **Multimodal I/O:**
    * **Audio:** Integrated `gTTS` (Text-to-Speech) for interviewer voice-over.
    * **Voice:** Integrated `streamlit-mic-recorder` (Speech-to-Text) for live practice.
* **Output Engine:** Automated `.docx` generation via `python-docx`.

---

### 📈 Project Status: Phase 3 Complete (Production Ready)
- [x] **Phase 1:** Core "Auditor" and "Storyteller" logic with JSON parsing.
- [x] **Phase 2:** "Voice Filter" and "Fact-Checker" reflection loop for 100% accuracy.
- [x] **Phase 3:** Full Multimodal Dashboard with **Voice-to-Text Interviewing** and **Gatekeeper Scoring**.

---

### 📂 Quick Start
```bash
# 1. Clone the repository
git clone [https://github.com/yourusername/career-orchestrator.git](https://github.com/yourusername/career-orchestrator.git)

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the Orchestrator
streamlit run app.py
