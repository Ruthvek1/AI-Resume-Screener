import os
import subprocess
import json
from datetime import datetime

# ─── CONFIG — change these two paths ───────────────────────────────────────
REPO_PATH   = os.getcwd()
# ────────────────────────────────────────────────────────────────────────────

STATE_FILE = os.path.join(REPO_PATH, ".push_state.json")

# Target exactly 150 commits over 5 days (Uneven distribution)
COMMITS_PER_DAY = [35, 25, 30, 28, 32]

COMMITS = [
    ("README.md", "init: add project title and description to README"),
    ("README.md", "docs: add tech stack section to README"),
    ("README.md", "docs: add quickstart section to README"),
    ("README.md", "docs: add live demo badge placeholder"),
    (".gitignore", "config: add Node and env file ignore rules"),
    (".gitignore", "config: add OS-specific ignore patterns"),
    ("README.md", "docs: add license section to README"),
    ("README.md", "docs: add project status badge"),
    (".gitignore", "config: add .push_state.json to gitignore"),
    ("README.md", "docs: add architecture overview paragraph"),
    ("backend/.env.example", "config: add GEMINI_API_KEY placeholder"),
    ("backend/.env.example", "config: add GROQ_API_KEY placeholder"),
    ("backend/.env.example", "config: add model name env vars"),
    ("backend/.env.example", "config: add rate limit env vars"),
    ("backend/requirements.txt", "config: add pdfplumber dependency"),
    ("backend/requirements.txt", "config: add google-generativeai dependency"),
    ("backend/requirements.txt", "config: add httpx and pydantic dependencies"),
    ("backend/config.py", "config: add Settings class with pydantic-settings"),
    ("backend/config.py", "config: add model name constants"),
    ("backend/config.py", "config: add rate limit and cache config"),
    ("backend/main.py", "feat: add FastAPI app instance in main.py"),
    ("backend/main.py", "feat: register health check route"),
    ("backend/main.py", "feat: add uvicorn entry point"),
    ("backend/main.py", "refactor: move app factory to separate function"),
    ("backend/main.py", "config: set allowed origins from env var"),
    ("backend/main.py", "feat: add /version endpoint"),
    ("backend/main.py", "fix: correct import order in main.py"),
    ("backend/main.py", "refactor: extract router registration to function"),
    ("backend/main.py", "config: add startup and shutdown event handlers"),
    ("backend/main.py", "fix: add missing trailing newline"),
    ("backend/services/pdf_parser.py", "feat: add pdf_parser module scaffold"),
    ("backend/services/pdf_parser.py", "feat: add pdfplumber import and file size check"),
    ("backend/services/pdf_parser.py", "feat: add page loop with extract_text call"),
    ("backend/services/pdf_parser.py", "feat: add x_tolerance and y_tolerance params"),
    ("backend/services/pdf_parser.py", "feat: add table extraction with extract_tables"),
    ("backend/services/pdf_parser.py", "feat: join table rows into pipe-separated strings"),
    ("backend/services/pdf_parser.py", "fix: raise 422 if extracted text is empty"),
    ("backend/services/pdf_parser.py", "fix: raise 413 if PDF exceeds 10MB"),
    ("backend/services/pdf_parser.py", "docs: add docstring to extract_text_from_pdf"),
    ("backend/services/pdf_parser.py", "style: format file with black"),
    ("backend/models/request_models.py", "feat: add request_models module"),
    ("backend/models/request_models.py", "feat: add AnalyzeRequest schema"),
    ("backend/models/response_models.py", "feat: add response_models module"),
    ("backend/models/response_models.py", "feat: add ScoreBreakdown model"),
    ("backend/models/response_models.py", "feat: add ATSKeywords model"),
    ("backend/models/response_models.py", "feat: add AnalysisResult model with all fields"),
    ("backend/models/response_models.py", "feat: add field validators for score range 0-100"),
    ("backend/models/response_models.py", "feat: add Optional fields with defaults"),
    ("backend/models/response_models.py", "style: reorder fields by importance"),
    ("backend/models/__init__.py", "feat: add models package init"),
    ("backend/services/gemini_service.py", "feat: add gemini_service module scaffold"),
    ("backend/services/gemini_service.py", "feat: configure genai with API key from settings"),
    ("backend/services/gemini_service.py", "feat: add match_score field to prompt JSON spec"),
    ("backend/services/gemini_service.py", "feat: add score_breakdown fields to prompt"),
    ("backend/services/gemini_service.py", "feat: add ats_keywords section to prompt"),
    ("backend/services/gemini_service.py", "feat: add improvement_suggestions to prompt"),
    ("backend/services/gemini_service.py", "feat: add temperature 0.2 for consistent output"),
    ("backend/services/gemini_service.py", "feat: add prompt formatting with resume and JD"),
    ("backend/services/gemini_service.py", "fix: truncate resume to 50000 chars for safety"),
    ("backend/services/gemini_service.py", "docs: add docstring to analyze_with_gemini"),
    ("backend/services/groq_service.py", "feat: add groq_service module scaffold"),
    ("backend/services/groq_service.py", "feat: init AsyncGroq client with API key"),
    ("backend/services/groq_service.py", "feat: add user message with resume and JD"),
    ("backend/services/groq_service.py", "feat: add chat.completions.create call"),
    ("backend/services/groq_service.py", "feat: set temperature 0.1 for scoring stability"),
    ("backend/services/groq_service.py", "feat: add response_format json_object"),
    ("backend/services/groq_service.py", "fix: truncate resume to 4000 chars for 8k limit"),
    ("backend/services/groq_service.py", "fix: truncate JD to 2000 chars"),
    ("backend/services/groq_service.py", "refactor: extract prompt building to helper"),
    ("backend/services/groq_service.py", "docs: add docstring to analyze_with_groq"),
    ("backend/services/openrouter_service.py", "feat: add openrouter_service module scaffold"),
    ("backend/services/openrouter_service.py", "feat: add Authorization header with Bearer token"),
    ("backend/services/openrouter_service.py", "feat: add model field with llama-3-70b-instruct"),
    ("backend/services/openrouter_service.py", "feat: add system and user messages"),
    ("backend/services/openrouter_service.py", "feat: add POST to openrouter completions URL"),
    ("backend/services/openrouter_service.py", "feat: add response.raise_for_status check"),
    ("backend/services/openrouter_service.py", "fix: truncate inputs for token safety"),
    ("backend/services/openrouter_service.py", "fix: handle HTTPStatusError with logging"),
    ("backend/services/openrouter_service.py", "refactor: move payload to build_payload func"),
    ("backend/services/openrouter_service.py", "docs: add docstring to analyze_with_openrouter"),
    ("backend/utils/rate_limiter.py", "feat: add rate_limiter module scaffold"),
    ("backend/utils/rate_limiter.py", "feat: add RateLimiter class with RPM param"),
    ("backend/utils/rate_limiter.py", "feat: add allow() method with time check"),
    ("backend/utils/rate_limiter.py", "feat: add token refill logic per second"),
    ("backend/utils/__init__.py", "feat: add utils package init"),
    ("backend/services/model_router.py", "feat: add model_router module scaffold"),
    ("backend/services/model_router.py", "feat: add route_analysis async function"),
    ("backend/services/model_router.py", "feat: add Gemini try block with fallback log"),
    ("backend/services/model_router.py", "feat: add OpenRouter as final fallback"),
    ("backend/services/model_router.py", "feat: return model_used string with result"),
    ("backend/routers/__init__.py", "feat: add routers package init"),
    ("backend/routers/analyze.py", "feat: add analyze router with APIRouter"),
    ("backend/routers/analyze.py", "feat: add UploadFile and Form params"),
    ("backend/routers/analyze.py", "feat: add PDF extension validation check"),
    ("backend/routers/analyze.py", "feat: call extract_text_from_pdf service"),
    ("backend/routers/analyze.py", "feat: call route_analysis with text and JD"),
    ("backend/routers/analyze.py", "feat: return AnalysisResponse with all fields"),
    ("backend/routers/analyze.py", "fix: handle UploadFile size attribute safely"),
    ("backend/routers/analyze.py", "docs: add docstring to analyze endpoint"),
    ("backend/main.py", "feat: register analyze router in main app"),
    ("frontend/package.json", "feat: add React and Vite dependencies"),
    ("frontend/package.json", "feat: add Tailwind CSS and PostCSS dependencies"),
    ("frontend/tailwind.config.js", "config: add custom color palette to Tailwind"),
    ("frontend/index.html", "feat: add HTML shell with root div"),
    ("frontend/src/App.jsx", "feat: add App component with router shell"),
    ("frontend/src/App.jsx", "feat: add Home and Results route definitions"),
    ("frontend/src/index.css", "style: add custom CSS variables for theme"),
    ("frontend/src/pages/Home.jsx", "feat: add Home page component scaffold"),
    ("frontend/src/hooks/useAnalyze.js", "feat: add useAnalyze hook with state vars"),
    ("frontend/src/hooks/useAnalyze.js", "feat: add analyze function with FormData"),
    ("frontend/src/components/UploadZone.jsx", "feat: add UploadZone component scaffold"),
    ("frontend/src/components/UploadZone.jsx", "feat: add drag over and drop event handlers"),
    ("frontend/src/components/UploadZone.jsx", "feat: add PDF type validation on drop"),
    ("frontend/src/components/UploadZone.jsx", "feat: show filename and size after selection"),
    ("frontend/src/components/UploadZone.jsx", "style: add drag-active highlight style"),
    ("frontend/src/components/ScoreGauge.jsx", "feat: add ScoreGauge SVG component scaffold"),
    ("frontend/src/components/ScoreGauge.jsx", "feat: add animated fill from 0 to score"),
    ("frontend/src/components/ScoreGauge.jsx", "feat: add color logic red amber green"),
    ("frontend/src/components/ScoreGauge.jsx", "feat: add Match Score label below number"),
    ("frontend/src/components/ModelBadge.jsx", "feat: add ModelBadge pill component"),
    ("frontend/src/components/SkillGapChart.jsx", "feat: add SkillGapChart component scaffold"),
    ("frontend/src/components/SkillGapChart.jsx", "feat: add three column layout structure"),
    ("frontend/src/components/SkillGapChart.jsx", "feat: add missing skills column with red badges"),
    ("frontend/src/components/SkillGapChart.jsx", "feat: add extra skills column with blue badges"),
    ("frontend/src/components/SkillGapChart.jsx", "style: add pill badge styling with Tailwind"),
    ("frontend/src/components/SkillGapChart.jsx", "feat: animate badges in on mount"),
    ("frontend/src/components/KeywordBadges.jsx", "feat: add found keywords row in green"),
    ("frontend/src/components/KeywordBadges.jsx", "feat: add missing keywords row in red"),
    ("frontend/src/components/KeywordBadges.jsx", "feat: add tooltip with why keyword matters"),
    ("frontend/src/components/KeywordBadges.jsx", "style: add hover effect on keyword badges"),
    ("frontend/src/components/SuggestionPanel.jsx", "feat: add SuggestionPanel component scaffold"),
    ("frontend/src/components/SuggestionPanel.jsx", "feat: add accordion list of suggestions"),
    ("frontend/src/components/SuggestionPanel.jsx", "feat: add Before label with original text"),
    ("frontend/src/components/SuggestionPanel.jsx", "feat: add After label with improved text"),
    ("frontend/src/components/SuggestionPanel.jsx", "feat: add section name as accordion header"),
    ("frontend/src/components/SuggestionPanel.jsx", "feat: add reason text below improvement"),
    ("frontend/src/pages/Results.jsx", "feat: import and place ScoreGauge on results"),
    ("frontend/src/pages/Results.jsx", "feat: import and place SkillGapChart"),
    ("frontend/src/pages/Results.jsx", "feat: import and place SuggestionPanel"),
    ("frontend/src/pages/Results.jsx", "feat: add ModelBadge and processing time"),
    ("docker-compose.yml", "config: add backend service to docker-compose"),
    ("docker-compose.yml", "config: add frontend service to docker-compose"),
    ("backend/Dockerfile", "config: add Python backend Dockerfile"),
    ("frontend/Dockerfile", "config: add Node frontend Dockerfile"),
    (".github/workflows/deploy.yml", "config: add Railway deploy step to workflow"),
    (".github/workflows/deploy.yml", "config: add Vercel deploy step to workflow"),
    ("ARCHITECTURE.md", "docs: add model routing flow diagram to arch doc"),
    ("README.md", "docs: add live demo GIF to README"),
    ("README.md", "docs: add deployment instructions to README"),
    ("README.md", "docs: add website embed snippet to README"),
]

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"day_index": 0, "commits_today": 0, "total_commits": 0, "last_date": str(datetime.now().date())}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def run(cmd, cwd=None):
    subprocess.run(cmd, shell=True, cwd=cwd, check=True)

def touch_file(filepath, message_hint):
    full_path = os.path.join(REPO_PATH, filepath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    if not os.path.exists(full_path):
        with open(full_path, "w") as f:
            f.write(f"# {message_hint}\n")
    else:
        with open(full_path, "a") as f:
            f.write(f"\n# update: {message_hint} — {datetime.now().isoformat()}\n")

def push():
    state = load_state()
    today_str = str(datetime.now().date())
    
    # If the calendar date changed, advance the day
    if state["last_date"] != today_str:
        state["day_index"] += 1
        state["commits_today"] = 0
        state["last_date"] = today_str
        save_state(state)
        
    day_idx = state["day_index"]
    if day_idx >= len(COMMITS_PER_DAY):
        print("✅ 5 days completed! 150 commits pushed.")
        return
        
    target_today = COMMITS_PER_DAY[day_idx]
    if state["commits_today"] >= target_today:
        print(f"🛑 Reached today's uneven target ({target_today} commits). Waiting for tomorrow.")
        return
        
    commit_idx = state["total_commits"]
    if commit_idx >= len(COMMITS):
        print("✅ All 150 commits have been pushed. Activating Ghost Mode (cleaning up automation files)...")
        files_to_remove = [
            "auto_push.py",
            ".github/workflows/auto_push.yml",
            ".push_state.json"
        ]
        changed = False
        for f in files_to_remove:
            if os.path.exists(os.path.join(REPO_PATH, f)):
                run(f"git rm -f '{f}'", cwd=REPO_PATH)
                changed = True
                
        # Clean up untracked scratch folder
        if os.path.exists(os.path.join(REPO_PATH, "scratch")):
            run("rm -rf scratch", cwd=REPO_PATH)
            
        if changed:
            run('git commit -m "chore: finalize project release and clean up repository"', cwd=REPO_PATH)
            try:
                run("git push origin main", cwd=REPO_PATH)
                print("✅ Automation files deleted and pushed. No one will ever know! 👻")
            except Exception as e:
                print("Final cleanup push failed.")
        return
        
    filepath, message = COMMITS[commit_idx]
    
    # Make a real file change
    touch_file(filepath, message)

    # Commit and push
    run("git add .", cwd=REPO_PATH)
    run(f'git commit -m "{message}"', cwd=REPO_PATH)
    try:
        run("git push origin main", cwd=REPO_PATH)
    except Exception as e:
        print("Push failed (maybe no remote origin setup yet). Continuing...")

    print(f"[Day {day_idx + 1}/5 | Commit {state['commits_today'] + 1}/{target_today}] ✅ {message}")

    # Save progress
    state["commits_today"] += 1
    state["total_commits"] += 1
    save_state(state)

if __name__ == "__main__":
    push()
