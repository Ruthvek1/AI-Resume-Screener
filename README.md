# 🚀 AI Resume Screener & Job Match Scorer

![Status](https://img.shields.io/badge/status-active-success.svg)
![Python](https://img.shields.io/badge/python-3670A0?style=flat&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=flat&logo=react&logoColor=%2361DAFB)
![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=flat&logo=tailwind-css&logoColor=white)

An intelligent, multi-model AI application that analyzes your resume against a specific job description. By leveraging cutting-edge LLMs (Gemini 2.5 Flash, Groq Llama-3 70B), the app provides an immediate match score, identifies critical skill gaps, and suggests actionable rewrites for your resume bullet points.

<div align="center">
  <img src="./screenshot.png" alt="Front Page Screenshot" width="100%" style="border-radius: 8px; margin-bottom: 20px;" />
  <br />
  <img src="./demo.gif" alt="Project Demo Video" width="100%" style="border-radius: 8px;" />
</div>

## 🌟 Key Features

### 📊 Deep Analytical Scoring
- **Match Score Gauge**: Instantly calculates a comprehensive 0–100 fit score based on semantic similarity between your resume and the job description.
- **Skill Gap Analysis**: Automatically extracts expected skills from the JD and compares them against your resume. It categorizes them into **Matching Skills**, **Missing Skills**, and **Extra Skills** to help you tailor your application.
- **ATS Keyword Extraction**: Identifies critical Applicant Tracking System (ATS) keywords and highlights which ones are missing from your resume, ensuring you get past automated filters.

### 🤖 Multi-Model AI Routing
- **Primary Engine (Gemini 2.5 Flash)**: Used for its massive context window (ideal for large PDFs and dense resumes) and fast reasoning capabilities.
- **High-Performance Fallback (Groq + Llama 3)**: If rate limits are hit, the system seamlessly routes requests to Groq using Meta's `llama-3.3-70b-versatile` model for lightning-fast inference.
- **Redundancy (OpenRouter)**: A third-layer fallback ensures the application remains highly available even during API outages.

### ✍️ Intelligent Resume Rewriter
- **Actionable Suggestions**: The AI doesn't just tell you what's wrong; it actively rewrites your bullet points. 
- **Before & After**: View side-by-side comparisons of your original text and the AI's improved, impact-driven suggestions tailored to the specific job description.

---

## 🏗️ Architecture & Tech Stack

**Frontend**
- **Framework**: React.js with Vite for lightning-fast HMR.
- **Styling**: Tailwind CSS with a custom dark-mode aesthetic (charcoal & electric violet).
- **Components**: Dynamic SVG animations (Score Gauge) and interactive accordions.

**Backend**
- **Framework**: FastAPI (Python 3.10+) for high-performance async endpoints.
- **PDF Processing**: `pdfplumber` for robust text and table extraction from complex PDF layouts.
- **Validation**: Pydantic models with custom `model_validator` logic to sanitize AI outputs and guarantee perfect JSON responses.

---

## 🏁 Build Order / Roadmap

This project was built iteratively to ensure a stable foundation before adding complex AI logic:

| Phase | Goal |
|------|------|
| **Phase 1** | Backend: Setup FastAPI skeleton, implement `pdfplumber` for robust PDF text extraction. |
| **Phase 2** | AI Integration: Integrate Gemini 2.5 Flash with strict JSON output schemas. |
| **Phase 3** | Resilience: Add Groq (Llama-3 70B) and OpenRouter fallbacks + dynamic rate limiters. |
| **Phase 4** | Frontend: Build React UI, Upload Zone, animated Score Gauge, and Skill Gap charts. |
| **Phase 5** | Polish & Deploy: Refine Tailwind styling, add deployment workflows (Railway & Vercel), and create demo materials. |

---

## 🛠️ Local Installation & Setup

Follow these steps to run the project locally on your machine.

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/ai-resume-screener.git
cd ai-resume-screener
```

### 2. Backend Setup
The backend requires Python 3.10 or higher.
```bash
cd backend

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

# Configure Environment Variables
cp .env.example .env
```
Open the `.env` file and add your API keys:
```env
GEMINI_API_KEY="your_google_ai_studio_key"
GROQ_API_KEY="your_groq_api_key"
OPENROUTER_API_KEY="your_openrouter_key"
```

Start the backend server:
```bash
uvicorn main:app --reload
```
The API will be available at `http://localhost:8000`.

### 3. Frontend Setup
Open a new terminal window and navigate to the frontend directory.
```bash
cd frontend

# Install Node dependencies
npm install

# Start the development server
npm run dev
```
The web app will be available at `http://localhost:5173`.

---

## 🚀 Deployment Guide

This project is configured for seamless deployment to modern cloud platforms.

### Backend (Railway / Render)
1. Connect your GitHub repository to Railway.
2. Railway will automatically detect the `backend/Dockerfile`.
3. Go to Variables and add your API keys (`GEMINI_API_KEY`, etc.).
4. Expose the deployment URL.

### Frontend (Vercel)
1. Import the `frontend/` directory into Vercel.
2. In the Vercel dashboard, add the Environment Variable:
   `VITE_API_URL=https://your-railway-backend-url.up.railway.app`
3. Deploy!

### Embed on your Personal Website
You can easily embed the live tool on your portfolio or blog using an iframe:
```html
<iframe
  src="https://your-frontend-deployment.vercel.app"
  width="100%"
  height="800px"
  style="border: none; border-radius: 12px;"
  title="AI Resume Screener"
/>
```

---

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! 
Feel free to check the [issues page](https://github.com/yourusername/ai-resume-screener/issues).

## 📝 License
This project is [MIT](https://opensource.org/licenses/MIT) licensed.
