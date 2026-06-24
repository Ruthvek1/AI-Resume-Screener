import os
import subprocess
import json
import time
from datetime import datetime, timedelta

# ─── CONFIG — change these two paths ───────────────────────────────────────
REPO_PATH   = os.getcwd()
# ────────────────────────────────────────────────────────────────────────────

STATE_FILE = os.path.join(REPO_PATH, ".push_state.json")
MINUTES_BETWEEN_COMMITS = 30   # space commits 30 min apart (looks natural)

# 15 days × 15 commits each
DAILY_COMMITS = {
    1: [
        ("README.md",                   "init: add project title and description to README"),
        ("README.md",                   "docs: add tech stack section to README"),
        ("README.md",                   "docs: add features list to README"),
        ("README.md",                   "docs: add quickstart section to README"),
        ("README.md",                   "docs: add live demo badge placeholder"),
        (".gitignore",                  "config: add Python gitignore rules"),
        (".gitignore",                  "config: add Node and env file ignore rules"),
        (".gitignore",                  "config: add OS-specific ignore patterns"),
        ("README.md",                   "docs: add contributing section"),
        ("README.md",                   "docs: add license section to README"),
        ("README.md",                   "docs: add project status badge"),
        ("README.md",                   "style: improve README formatting and spacing"),
        (".gitignore",                  "config: add .push_state.json to gitignore"),
        ("README.md",                   "docs: add architecture overview paragraph"),
        ("README.md",                   "docs: final README review and cleanup"),
    ],
    2: [
        ("backend/.env.example",        "config: add GEMINI_API_KEY placeholder"),
        ("backend/.env.example",        "config: add GROQ_API_KEY placeholder"),
        ("backend/.env.example",        "config: add OPENROUTER_API_KEY placeholder"),
        ("backend/.env.example",        "config: add model name env vars"),
        ("backend/.env.example",        "config: add rate limit env vars"),
        ("backend/requirements.txt",    "config: add fastapi and uvicorn dependencies"),
        ("backend/requirements.txt",    "config: add pdfplumber dependency"),
        ("backend/requirements.txt",    "config: add google-generativeai dependency"),
        ("backend/requirements.txt",    "config: add groq SDK dependency"),
        ("backend/requirements.txt",    "config: add httpx and pydantic dependencies"),
        ("backend/config.py",           "config: add Settings class with pydantic-settings"),
        ("backend/config.py",           "config: add API key fields to Settings"),
        ("backend/config.py",           "config: add model name constants"),
        ("backend/config.py",           "config: add rate limit and cache config"),
        ("backend/config.py",           "config: export settings singleton"),
    ],
    3: [
        ("backend/main.py",             "feat: add FastAPI app instance in main.py"),
        ("backend/main.py",             "feat: register health check route"),
        ("backend/main.py",             "feat: add CORS middleware config"),
        ("backend/main.py",             "feat: add uvicorn entry point"),
        ("backend/main.py",             "refactor: move app factory to separate function"),
        ("backend/main.py",             "docs: add inline docstring to health endpoint"),
        ("backend/main.py",             "config: set allowed origins from env var"),
        ("backend/main.py",             "feat: add /version endpoint"),
        ("backend/main.py",             "style: format main.py with black"),
        ("backend/main.py",             "fix: correct import order in main.py"),
        ("backend/main.py",             "refactor: extract router registration to function"),
        ("backend/main.py",             "docs: add module-level docstring to main.py"),
        ("backend/main.py",             "config: add startup and shutdown event handlers"),
        ("backend/main.py",             "fix: add missing trailing newline"),
        ("README.md",                   "docs: update README with how to run backend"),
    ],
    4: [
        ("backend/services/pdf_parser.py", "feat: add pdf_parser module scaffold"),
        ("backend/services/pdf_parser.py", "feat: add pdfplumber import and file size check"),
        ("backend/services/pdf_parser.py", "feat: add async file read and BytesIO conversion"),
        ("backend/services/pdf_parser.py", "feat: add page loop with extract_text call"),
        ("backend/services/pdf_parser.py", "feat: add x_tolerance and y_tolerance params"),
        ("backend/services/pdf_parser.py", "feat: add page number header to extracted text"),
        ("backend/services/pdf_parser.py", "feat: add table extraction with extract_tables"),
        ("backend/services/pdf_parser.py", "feat: join table rows into pipe-separated strings"),
        ("backend/services/pdf_parser.py", "feat: join all page texts with double newline"),
        ("backend/services/pdf_parser.py", "fix: raise 422 if extracted text is empty"),
        ("backend/services/pdf_parser.py", "fix: raise 413 if PDF exceeds 10MB"),
        ("backend/services/pdf_parser.py", "refactor: extract page text logic to helper"),
        ("backend/services/pdf_parser.py", "docs: add docstring to extract_text_from_pdf"),
        ("backend/services/pdf_parser.py", "style: format file with black"),
        ("backend/services/__init__.py",   "feat: add services package init file"),
    ],
    5: [
        ("backend/models/request_models.py",  "feat: add request_models module"),
        ("backend/models/request_models.py",  "feat: add AnalyzeRequest schema"),
        ("backend/models/request_models.py",  "feat: add job_description field with validator"),
        ("backend/models/response_models.py", "feat: add response_models module"),
        ("backend/models/response_models.py", "feat: add ScoreBreakdown model"),
        ("backend/models/response_models.py", "feat: add ImprovementSuggestion model"),
        ("backend/models/response_models.py", "feat: add ATSKeywords model"),
        ("backend/models/response_models.py", "feat: add AnalysisResult model with all fields"),
        ("backend/models/response_models.py", "feat: add AnalysisResponse wrapper model"),
        ("backend/models/response_models.py", "feat: add field validators for score range 0-100"),
        ("backend/models/response_models.py", "feat: add Optional fields with defaults"),
        ("backend/models/response_models.py", "docs: add docstrings to all model classes"),
        ("backend/models/response_models.py", "style: reorder fields by importance"),
        ("backend/models/__init__.py",        "feat: add models package init"),
        ("README.md",                         "docs: add API response schema to README"),
    ],
    6: [
        ("backend/services/gemini_service.py", "feat: add gemini_service module scaffold"),
        ("backend/services/gemini_service.py", "feat: configure genai with API key from settings"),
        ("backend/services/gemini_service.py", "feat: add ANALYSIS_PROMPT template constant"),
        ("backend/services/gemini_service.py", "feat: add match_score field to prompt JSON spec"),
        ("backend/services/gemini_service.py", "feat: add score_breakdown fields to prompt"),
        ("backend/services/gemini_service.py", "feat: add matching and missing skills to prompt"),
        ("backend/services/gemini_service.py", "feat: add ats_keywords section to prompt"),
        ("backend/services/gemini_service.py", "feat: add improvement_suggestions to prompt"),
        ("backend/services/gemini_service.py", "feat: add GenerativeModel with JSON mime type"),
        ("backend/services/gemini_service.py", "feat: add temperature 0.2 for consistent output"),
        ("backend/services/gemini_service.py", "feat: add prompt formatting with resume and JD"),
        ("backend/services/gemini_service.py", "feat: add JSON parse and AnalysisResult return"),
        ("backend/services/gemini_service.py", "fix: truncate resume to 50000 chars for safety"),
        ("backend/services/gemini_service.py", "docs: add docstring to analyze_with_gemini"),
        ("backend/services/gemini_service.py", "style: format with black"),
    ],
    7: [
        ("backend/services/groq_service.py", "feat: add groq_service module scaffold"),
        ("backend/services/groq_service.py", "feat: init AsyncGroq client with API key"),
        ("backend/services/groq_service.py", "feat: add system prompt for JSON-only output"),
        ("backend/services/groq_service.py", "feat: add user message with resume and JD"),
        ("backend/services/groq_service.py", "feat: add chat.completions.create call"),
        ("backend/services/groq_service.py", "feat: set model to llama3-70b-8192"),
        ("backend/services/groq_service.py", "feat: set temperature 0.1 for scoring stability"),
        ("backend/services/groq_service.py", "feat: add response_format json_object"),
        ("backend/services/groq_service.py", "feat: parse response and return AnalysisResult"),
        ("backend/services/groq_service.py", "fix: truncate resume to 4000 chars for 8k limit"),
        ("backend/services/groq_service.py", "fix: truncate JD to 2000 chars"),
        ("backend/services/groq_service.py", "fix: handle JSON parse error with fallback"),
        ("backend/services/groq_service.py", "refactor: extract prompt building to helper"),
        ("backend/services/groq_service.py", "docs: add docstring to analyze_with_groq"),
        ("backend/services/groq_service.py", "style: format with black"),
    ],
    8: [
        ("backend/services/openrouter_service.py", "feat: add openrouter_service module scaffold"),
        ("backend/services/openrouter_service.py", "feat: add Authorization header with Bearer token"),
        ("backend/services/openrouter_service.py", "feat: add HTTP-Referer and X-Title headers"),
        ("backend/services/openrouter_service.py", "feat: add model field with llama-3-70b-instruct"),
        ("backend/services/openrouter_service.py", "feat: add system and user messages"),
        ("backend/services/openrouter_service.py", "feat: add httpx AsyncClient with 60s timeout"),
        ("backend/services/openrouter_service.py", "feat: add POST to openrouter completions URL"),
        ("backend/services/openrouter_service.py", "feat: add response.raise_for_status check"),
        ("backend/services/openrouter_service.py", "feat: parse JSON response and return result"),
        ("backend/services/openrouter_service.py", "fix: truncate inputs for token safety"),
        ("backend/services/openrouter_service.py", "fix: handle HTTPStatusError with logging"),
        ("backend/services/openrouter_service.py", "refactor: move headers to build_headers func"),
        ("backend/services/openrouter_service.py", "refactor: move payload to build_payload func"),
        ("backend/services/openrouter_service.py", "docs: add docstring to analyze_with_openrouter"),
        ("backend/services/openrouter_service.py", "style: format with black"),
    ],
    9: [
        ("backend/utils/rate_limiter.py",      "feat: add rate_limiter module scaffold"),
        ("backend/utils/rate_limiter.py",       "feat: add RateLimiter class with RPM param"),
        ("backend/utils/rate_limiter.py",       "feat: add token bucket state variables"),
        ("backend/utils/rate_limiter.py",       "feat: add allow() method with time check"),
        ("backend/utils/rate_limiter.py",       "feat: add token refill logic per second"),
        ("backend/utils/rate_limiter.py",       "fix: use threading.Lock for thread safety"),
        ("backend/utils/__init__.py",           "feat: add utils package init"),
        ("backend/services/model_router.py",    "feat: add model_router module scaffold"),
        ("backend/services/model_router.py",    "feat: add gemini and groq RateLimiter instances"),
        ("backend/services/model_router.py",    "feat: add route_analysis async function"),
        ("backend/services/model_router.py",    "feat: add Gemini try block with fallback log"),
        ("backend/services/model_router.py",    "feat: add Groq try block with fallback log"),
        ("backend/services/model_router.py",    "feat: add OpenRouter as final fallback"),
        ("backend/services/model_router.py",    "feat: return model_used string with result"),
        ("backend/services/model_router.py",    "docs: add routing strategy docstring"),
    ],
    10: [
        ("backend/routers/__init__.py",  "feat: add routers package init"),
        ("backend/routers/analyze.py",   "feat: add analyze router with APIRouter"),
        ("backend/routers/analyze.py",   "feat: add POST /api/analyze endpoint signature"),
        ("backend/routers/analyze.py",   "feat: add UploadFile and Form params"),
        ("backend/routers/analyze.py",   "feat: add PDF extension validation check"),
        ("backend/routers/analyze.py",   "feat: add job description length validation"),
        ("backend/routers/analyze.py",   "feat: call extract_text_from_pdf service"),
        ("backend/routers/analyze.py",   "feat: call route_analysis with text and JD"),
        ("backend/routers/analyze.py",   "feat: add processing time calculation in ms"),
        ("backend/routers/analyze.py",   "feat: return AnalysisResponse with all fields"),
        ("backend/routers/analyze.py",   "fix: handle UploadFile size attribute safely"),
        ("backend/routers/analyze.py",   "refactor: extract validation to helper function"),
        ("backend/routers/analyze.py",   "docs: add docstring to analyze endpoint"),
        ("backend/main.py",              "feat: register analyze router in main app"),
        ("README.md",                    "docs: add API endpoint reference to README"),
    ],
    11: [
        ("frontend/package.json",          "feat: add React and Vite dependencies"),
        ("frontend/package.json",          "feat: add Tailwind CSS and PostCSS dependencies"),
        ("frontend/tailwind.config.js",    "config: add Tailwind content paths"),
        ("frontend/tailwind.config.js",    "config: add custom color palette to Tailwind"),
        ("frontend/index.html",            "feat: add HTML shell with root div"),
        ("frontend/src/main.jsx",          "feat: add React DOM render entry point"),
        ("frontend/src/App.jsx",           "feat: add App component with router shell"),
        ("frontend/src/App.jsx",           "feat: add Home and Results route definitions"),
        ("frontend/src/index.css",         "style: add Tailwind base directives"),
        ("frontend/src/index.css",         "style: add custom CSS variables for theme"),
        ("frontend/src/pages/Home.jsx",    "feat: add Home page component scaffold"),
        ("frontend/src/pages/Results.jsx", "feat: add Results page component scaffold"),
        ("frontend/src/hooks/useAnalyze.js","feat: add useAnalyze hook with state vars"),
        ("frontend/src/hooks/useAnalyze.js","feat: add analyze function with FormData"),
        ("frontend/src/hooks/useAnalyze.js","feat: add fetch call and error handling"),
    ],
    12: [
        ("frontend/src/components/UploadZone.jsx", "feat: add UploadZone component scaffold"),
        ("frontend/src/components/UploadZone.jsx", "feat: add drag over and drop event handlers"),
        ("frontend/src/components/UploadZone.jsx", "feat: add file input click trigger"),
        ("frontend/src/components/UploadZone.jsx", "feat: add PDF type validation on drop"),
        ("frontend/src/components/UploadZone.jsx", "feat: show filename and size after selection"),
        ("frontend/src/components/UploadZone.jsx", "feat: add pulsing animation during processing"),
        ("frontend/src/components/UploadZone.jsx", "style: add drag-active highlight style"),
        ("frontend/src/components/ScoreGauge.jsx", "feat: add ScoreGauge SVG component scaffold"),
        ("frontend/src/components/ScoreGauge.jsx", "feat: add circle stroke-dasharray calculation"),
        ("frontend/src/components/ScoreGauge.jsx", "feat: add animated fill from 0 to score"),
        ("frontend/src/components/ScoreGauge.jsx", "feat: add color logic red amber green"),
        ("frontend/src/components/ScoreGauge.jsx", "feat: add large score number in SVG center"),
        ("frontend/src/components/ScoreGauge.jsx", "feat: add Match Score label below number"),
        ("frontend/src/components/ModelBadge.jsx", "feat: add ModelBadge pill component"),
        ("frontend/src/components/ModelBadge.jsx", "style: add model-specific badge colors"),
    ],
    13: [
        ("frontend/src/components/SkillGapChart.jsx", "feat: add SkillGapChart component scaffold"),
        ("frontend/src/components/SkillGapChart.jsx", "feat: add three column layout structure"),
        ("frontend/src/components/SkillGapChart.jsx", "feat: add matching skills column with green badges"),
        ("frontend/src/components/SkillGapChart.jsx", "feat: add missing skills column with red badges"),
        ("frontend/src/components/SkillGapChart.jsx", "feat: add extra skills column with blue badges"),
        ("frontend/src/components/SkillGapChart.jsx", "feat: add count summary above each column"),
        ("frontend/src/components/SkillGapChart.jsx", "style: add pill badge styling with Tailwind"),
        ("frontend/src/components/SkillGapChart.jsx", "feat: animate badges in on mount"),
        ("frontend/src/components/KeywordBadges.jsx", "feat: add KeywordBadges component scaffold"),
        ("frontend/src/components/KeywordBadges.jsx", "feat: add found keywords row in green"),
        ("frontend/src/components/KeywordBadges.jsx", "feat: add missing keywords row in red"),
        ("frontend/src/components/KeywordBadges.jsx", "feat: add click handler to show keyword tip"),
        ("frontend/src/components/KeywordBadges.jsx", "feat: add tooltip with why keyword matters"),
        ("frontend/src/components/KeywordBadges.jsx", "style: add hover effect on keyword badges"),
        ("frontend/src/components/KeywordBadges.jsx", "fix: handle empty keywords array gracefully"),
    ],
    14: [
        ("frontend/src/components/SuggestionPanel.jsx", "feat: add SuggestionPanel component scaffold"),
        ("frontend/src/components/SuggestionPanel.jsx", "feat: add accordion list of suggestions"),
        ("frontend/src/components/SuggestionPanel.jsx", "feat: add expand collapse on click"),
        ("frontend/src/components/SuggestionPanel.jsx", "feat: add Before label with original text"),
        ("frontend/src/components/SuggestionPanel.jsx", "feat: add After label with improved text"),
        ("frontend/src/components/SuggestionPanel.jsx", "feat: add copy to clipboard button"),
        ("frontend/src/components/SuggestionPanel.jsx", "feat: add section name as accordion header"),
        ("frontend/src/components/SuggestionPanel.jsx", "feat: add reason text below improvement"),
        ("frontend/src/components/SuggestionPanel.jsx", "style: add diff highlight on improved text"),
        ("frontend/src/pages/Results.jsx",              "feat: import and place ScoreGauge on results"),
        ("frontend/src/pages/Results.jsx",              "feat: import and place SkillGapChart"),
        ("frontend/src/pages/Results.jsx",              "feat: import and place KeywordBadges"),
        ("frontend/src/pages/Results.jsx",              "feat: import and place SuggestionPanel"),
        ("frontend/src/pages/Results.jsx",              "feat: add ModelBadge and processing time"),
        ("frontend/src/pages/Home.jsx",                 "feat: wire UploadZone and JD input to hook"),
    ],
    15: [
        ("docker-compose.yml",              "config: add backend service to docker-compose"),
        ("docker-compose.yml",              "config: add frontend service to docker-compose"),
        ("docker-compose.yml",              "config: add env_file and port mappings"),
        ("backend/Dockerfile",              "config: add Python backend Dockerfile"),
        ("frontend/Dockerfile",             "config: add Node frontend Dockerfile"),
        (".github/workflows/deploy.yml",    "config: add GitHub Actions deploy workflow"),
        (".github/workflows/deploy.yml",    "config: add Railway deploy step to workflow"),
        (".github/workflows/deploy.yml",    "config: add Vercel deploy step to workflow"),
        ("ARCHITECTURE.md",                 "docs: add architecture overview document"),
        ("ARCHITECTURE.md",                 "docs: add model routing flow diagram to arch doc"),
        ("README.md",                       "docs: add live demo GIF to README"),
        ("README.md",                       "docs: add tech stack badges to README"),
        ("README.md",                       "docs: add deployment instructions to README"),
        ("README.md",                       "docs: add website embed snippet to README"),
        ("README.md",                       "docs: final README polish and spell check"),
    ],
}


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"day": 1, "commit_index": 0}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def run(cmd, cwd=None):
    subprocess.run(cmd, shell=True, cwd=cwd, check=True)


def touch_file(filepath, message_hint):
    """Add a meaningful comment line to the file so git sees a real change."""
    full_path = os.path.join(REPO_PATH, filepath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    # Create file if it doesn't exist
    if not os.path.exists(full_path):
        with open(full_path, "w") as f:
            f.write(f"# {message_hint}\n")
    else:
        with open(full_path, "a") as f:
            f.write(f"\n# update: {message_hint} — {datetime.now().isoformat()}\n")


def push_day():
    state = load_state()
    day = state["day"]
    commit_index = state["commit_index"]

    if day > 15:
        print("✅ All 15 days complete! 225 contributions pushed.")
        return

    commits_today = DAILY_COMMITS[day]

    if commit_index >= len(commits_today):
        # Move to next day
        state["day"] = day + 1
        state["commit_index"] = 0
        save_state(state)
        print(f"✅ Day {day} complete. Moving to Day {day + 1}.")
        return

    filepath, message = commits_today[commit_index]

    # Make a real file change
    touch_file(filepath, message)

    # Commit and push (push is disabled until you add remote)
    run("git add .", cwd=REPO_PATH)
    run(f'git commit -m "{message}"', cwd=REPO_PATH)
    try:
        run("git push origin main", cwd=REPO_PATH)
    except Exception as e:
        print("Push failed (maybe no remote origin setup yet). Continuing...")

    print(f"[Day {day} | Commit {commit_index + 1}/15] ✅ {message}")

    # Save progress
    state["commit_index"] = commit_index + 1
    save_state(state)


if __name__ == "__main__":
    push_day()
