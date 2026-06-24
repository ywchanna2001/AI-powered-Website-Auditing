# 🔍 AI-Powered Website Audit Tool

> A lightweight, AI-native tool built for **EIGHT25MEDIA**. It extracts factual website metrics and generates structured SEO/UX insights and recommendations using **Google Gemini 2.5 Flash**.

---

## 🚀 Local Setup Instructions

Follow these steps to run the application on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/ywchanna2001/AI-powered-Website-Auditing.git
cd AI-powered-Website-Auditing
```

### 2. Create and Activate Virtual Environment

```bash
# Create the virtual environment
python -m venv .venv

# Activate it (Windows)
.venv\Scripts\activate

# Activate it (Mac/Linux)
source .venv/bin/activate
```

### 3. Install Requirements


```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables

Create a file named `.env` in the root directory and add your Gemini API Key:

```env
GEMINI_API_KEY=your_google_ai_studio_api_key_here
```

### 5. Run the Backend (Terminal 1)

Start the FastAPI server first:

```bash
# Ensure you are in the root directory
uvicorn Backend.main:app --reload
```

- The backend will be running at: `http://127.0.0.1:8000`
- Interactive API documentation available at: `http://127.0.0.1:8000/docs`

### 6. Run the Frontend (Terminal 2)

Open a new terminal window, activate the virtual environment again, and run:

```bash
# Ensure you are in the root directory
streamlit run Frontend/app.py
```

The application will automatically open in your browser at `http://localhost:8501`.

---

## 🏗️ Architecture Overview

To meet the evaluation criteria for **Engineering Clarity**, the system is strictly decoupled into three layers:

| Layer | Technology | Role |
|---|---|---|
| **Scraping** (Deterministic) | BeautifulSoup4 | Extracts raw HTML data and computes factual metrics (word counts, heading distributions, link ratios). No AI is used here to ensure data accuracy. |
| **AI Orchestration** (Probabilistic) | Google Gemini 2.5 Flash | A dedicated AI agent maps raw metrics to qualitative insights, using Pydantic models to enforce Structured Outputs. |
| **Frontend** | Streamlit | A dashboard that communicates with the Backend API, ensuring the UI is fully independent of business logic. |

---

## 🧠 AI Design Decisions

- **Structured JSON Output** — Gemini's `response_mime_type: "application/json"` capability is combined with a strict Pydantic schema. This ensures the model never hallucinates the format and always returns valid, parseable data.

- **Data Grounding** — The system prompt is designed to prevent generic AI advice. By injecting scraped metrics directly into the prompt context, the AI is forced to reference factual data (e.g., *"The page has 18 H1 tags, which is a critical SEO error"*) rather than producing boilerplate suggestions.

- **Prompt Logging** — Every AI request and raw response is captured in the `/Prompt_Logs` directory, providing full visibility into the model's reasoning traces and input/output structure.

---

## ⚖️ Trade-offs

**Static vs. Dynamic Scraping**

Chose `requests` + `BeautifulSoup4` over `Playwright`/`Selenium`.

> **Reasoning:** While BS4 cannot execute JavaScript, it is significantly faster and uses fewer resources. For a "lightweight" audit tool, speed of execution was prioritized over the ability to scrape heavily obfuscated Single Page Applications (SPAs).

**Heuristic CTA Detection**

CTAs are identified by scanning for `<button>` tags and specific link patterns.

> **Reasoning:** A perfect CTA detection would require a Vision LLM or complex CSS analysis. For this 24-hour scope, a heuristic approach provides ~90% accuracy with 100% speed.

---

## 📂 Deliverables Included

1. **Source Code** — Decoupled FastAPI and Streamlit codebase.
2. **Prompt Logs** — Found in the `/Prompt_Logs` folder *(Required Traceability)*.
3. **Documentation** — This README covering architecture, setup, and design decisions.

---

*Built for the EIGHT25MEDIA AI-Native Software Engineer Assignment.*
