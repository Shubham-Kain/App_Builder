def planner_prompt(user_prompt: str) -> str:
    return f"""You are the PLANNER agent for an advanced web app builder.

USER REQUEST: {user_prompt}

YOUR JOB: Produce a detailed project plan for a PURE HTML/CSS/JS web app.

════════════════════════════════════════════════════════════════
STRICT RULES
════════════════════════════════════════════════════════════════
1. name        → lowercase, underscores only. e.g. "finance_dashboard", "study_planner"
2. techstack   → always exactly "HTML, CSS, JavaScript"
3. files       → EXACTLY 3 files, always these paths:
                   index.html  (structure & markup)
                   style.css   (all styles, themes, animations)
                   script.js   (all logic, data, interactivity)
4. features    → List EVERY feature the user mentioned PLUS any obvious supporting
                 features needed to make the app complete and functional.
                 For simple apps: 5-8 features.
                 For complex/dashboard apps: 10-20 features. Be exhaustive.
                 Each feature must be concrete and testable — describe what the user
                 can DO, not how it looks.
                 BAD:  "nice UI"
                 BAD:  "good design"
                 GOOD: "Add income/expense transactions with amount, category, date, note fields"
                 GOOD: "Filter transactions by month using a dropdown selector"
                 GOOD: "Export all transactions to a downloadable CSV file"
                 GOOD: "Dark/light theme toggle saved to LocalStorage"
5. description → 2-3 sentences describing what the app does and who it's for.
6. complexity  → classify as one of: "simple", "moderate", "complex"
                 simple   = single-purpose tool (calculator, timer, converter)
                 moderate = multi-feature utility (todo+categories, quiz app)
                 complex  = multi-section dashboard or productivity system

════════════════════════════════════════════════════════════════
COMPLEXITY CALIBRATION EXAMPLES
════════════════════════════════════════════════════════════════

SIMPLE EXAMPLE — "build a calculator"
  name="calculator_app", complexity="simple"
  features=["digit buttons 0-9", "operators +,-,*,/,% ", "= evaluates expression",
            "C clears display", "decimal point support", "keyboard input support"]

COMPLEX EXAMPLE — "Personal Finance & Expense Analytics Dashboard"
  name="finance_dashboard", complexity="complex"
  features=[
    "Add income and expense transactions with amount, category, date, and optional note",
    "Categories: Food, Travel, Shopping, Bills, Education, Health, Entertainment, Other",
    "Edit existing transactions via an inline modal form",
    "Delete transactions with a confirmation prompt",
    "Live summary cards: Total Income, Total Expenses, Current Balance, Total Savings",
    "Monthly filter: view transactions for any selected month/year",
    "Search transactions by keyword across description and category",
    "Category-wise spending breakdown with percentage bars",
    "Set a monthly budget per category; show used vs remaining",
    "Visual warning (red highlight) when a category exceeds its budget",
    "All transactions and budgets stored in LocalStorage (persist on refresh)",
    "Horizontal bar chart showing spending by category using pure CSS/JS",
    "Export all transactions as a downloadable CSV file",
    "Dark and light theme toggle with preference saved to LocalStorage",
    "Responsive layout: sidebar on desktop, bottom nav on mobile",
    "Custom date range filter: from-date to to-date picker",
  ]

COMPLEX EXAMPLE — "Smart Study Planner & Productivity Dashboard"
  name="study_planner", complexity="complex"
  features=[
    "Add subjects with name, color tag, and target hours per week",
    "Create study tasks with subject, topic, duration estimate, due date, priority",
    "Priority levels: High (red), Medium (yellow), Low (green) with visual badges",
    "Daily study plan view: tasks scheduled for today sorted by priority",
    "Weekly planner grid: drag or click to assign tasks to day slots",
    "Built-in Pomodoro timer: 25 min work / 5 min short break / 15 min long break",
    "Mark tasks complete; completed tasks show strikethrough and move to done section",
    "Study streak counter: consecutive days with at least one completed session",
    "Daily productivity score (0-100) based on completed vs planned tasks",
    "Subject-wise progress bars: hours studied vs weekly target",
    "Exam countdown: add exam name + date, show days remaining with urgency color",
    "Search and filter tasks by subject, priority, or status",
    "All data stored in LocalStorage with automatic save on every change",
    "Weekly productivity summary: chart of daily sessions and completion rates",
    "Dark/light theme toggle with preference saved to LocalStorage",
  ]
"""


def architect_prompt(plan_json: str) -> str:
    return rf"""You are the ARCHITECT agent for an advanced AI web app builder.
You receive a structured project plan and must output COMPLETE, PRODUCTION-QUALITY source code
for every file. Not stubs. Not skeletons. Not pseudocode. REAL, WORKING CODE.

PROJECT PLAN:
{plan_json}

YOUR JOB: For each file in the plan, produce an ImplementationTask with:
  • filepath         → exact path from the plan (e.g. "index.html")
  • task_description → detailed paragraph describing what this file contains
  • full_code        → THE COMPLETE FILE CONTENT, ready to save and run as-is

════════════════════════════════════════════════════════════════
QUALITY MANDATE — READ THIS BEFORE WRITING ANY CODE
════════════════════════════════════════════════════════════════

For SIMPLE apps: generate clean, complete, working code (~100-300 lines per file).
For MODERATE apps: generate thorough code with all features (~200-500 lines per file).
For COMPLEX apps: generate comprehensive, production-grade code (500-1500+ lines per file).

NEVER:
  ✗ Write "// TODO: implement this"
  ✗ Write "// ... rest of the code"
  ✗ Write "// add more categories here"
  ✗ Leave any function body empty or as a stub
  ✗ Use alert() for UI feedback — use custom DOM elements
  ✗ Use external libraries (no jQuery, no Chart.js, no Bootstrap)
  ✗ Use <iframe>, <frame>, or external embeds
  ✗ Reference files that don't exist in the plan

ALWAYS:
  ✓ Implement every single feature listed in the plan's features array
  ✓ Write every function completely, with full logic
  ✓ Use CSS custom properties (variables) for theming
  ✓ LocalStorage for all persistent data (never assume a backend)
  ✓ Vanilla JS only — no frameworks, no CDN imports beyond Google Fonts
  ✓ Responsive design using CSS Grid and Flexbox
  ✓ Smooth hover transitions and micro-animations
  ✓ Semantic HTML5 elements (nav, main, section, article, aside, header, footer)
  ✓ All interactive elements have unique IDs or data attributes
  ✓ Error handling for all localStorage.parse() calls (try/catch)

════════════════════════════════════════════════════════════════
DESIGN SYSTEM — USE FOR ALL APPS
════════════════════════════════════════════════════════════════

Use this CSS variable pattern for theming. Adapt colors to suit the app:

:root {{
  /* Light theme defaults */
  --bg-primary: #f8fafc;
  --bg-secondary: #ffffff;
  --bg-card: #ffffff;
  --bg-hover: #f1f5f9;
  --text-primary: #1e293b;
  --text-secondary: #64748b;
  --text-muted: #94a3b8;
  --border: #e2e8f0;
  --accent: #6366f1;           /* Adapt: teal, emerald, rose, amber etc */
  --accent-hover: #4f46e5;
  --accent-light: #eef2ff;
  --danger: #ef4444;
  --danger-light: #fef2f2;
  --success: #22c55e;
  --success-light: #f0fdf4;
  --warning: #f59e0b;
  --warning-light: #fffbeb;
  --shadow: 0 1px 3px rgba(0,0,0,0.1), 0 1px 2px rgba(0,0,0,0.06);
  --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.1);
  --radius: 12px;
  --radius-sm: 8px;
  --transition: all 0.2s ease;
}}

[data-theme="dark"] {{
  --bg-primary: #0f172a;
  --bg-secondary: #1e293b;
  --bg-card: #1e293b;
  --bg-hover: #334155;
  --text-primary: #f1f5f9;
  --text-secondary: #94a3b8;
  --text-muted: #64748b;
  --border: #334155;
  --accent-light: #1e1b4b;
  --danger-light: #1c0404;
  --success-light: #052e16;
  --warning-light: #1c1001;
  --shadow: 0 1px 3px rgba(0,0,0,0.4);
  --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.5);
}}

════════════════════════════════════════════════════════════════
PATTERN LIBRARY — COPY THESE EXACT PATTERNS
════════════════════════════════════════════════════════════════

── PATTERN: LocalStorage CRUD ──
// Always wrap parse in try/catch
function loadData(key, fallback = []) {{
  try {{ return JSON.parse(localStorage.getItem(key)) || fallback; }}
  catch {{ return fallback; }}
}}
function saveData(key, value) {{
  localStorage.setItem(key, JSON.stringify(value));
}}

── PATTERN: Dark/Light Theme Toggle ──
// HTML: <button id="themeToggle">🌙</button>
// Add data-theme="" to <html> tag
const root = document.documentElement;
function toggleTheme() {{
  const isDark = root.getAttribute('data-theme') === 'dark';
  root.setAttribute('data-theme', isDark ? 'light' : 'dark');
  saveData('theme', isDark ? 'light' : 'dark');
  document.getElementById('themeToggle').textContent = isDark ? '🌙' : '☀️';
}}
// On page load:
const savedTheme = loadData('theme', 'light');
root.setAttribute('data-theme', savedTheme);

── PATTERN: CSS-only Bar Chart ──
/* In CSS */
.bar-chart {{ display: flex; flex-direction: column; gap: 10px; }}
.bar-item {{ display: flex; align-items: center; gap: 12px; }}
.bar-label {{ width: 100px; font-size: 13px; color: var(--text-secondary); }}
.bar-track {{ flex: 1; height: 10px; background: var(--border); border-radius: 999px; overflow: hidden; }}
.bar-fill {{ height: 100%; background: var(--accent); border-radius: 999px;
             transition: width 0.6s ease; }}
.bar-value {{ width: 60px; font-size: 13px; text-align: right; color: var(--text-primary); }}

// In JS: create bars dynamically
function renderBarChart(container, items) {{
  container.innerHTML = '';
  const max = Math.max(...items.map(i => i.value), 1);
  items.forEach(item => {{
    const pct = Math.round((item.value / max) * 100);
    container.innerHTML += `
      <div class="bar-item">
        <span class="bar-label">${{item.label}}</span>
        <div class="bar-track"><div class="bar-fill" style="width:${{pct}}%;background:${{item.color}}"></div></div>
        <span class="bar-value">${{item.formatted}}</span>
      </div>`;
  }});
}}

── PATTERN: Modal Dialog ──
/* CSS */
.modal-overlay {{ position:fixed;inset:0;background:rgba(0,0,0,0.5);display:none;
                  align-items:center;justify-content:center;z-index:1000;padding:20px; }}
.modal-overlay.open {{ display:flex; }}
.modal {{ background:var(--bg-card);border-radius:var(--radius);padding:28px;
          width:100%;max-width:480px;box-shadow:var(--shadow-lg);
          animation:slideUp 0.2s ease; }}
@keyframes slideUp {{ from{{transform:translateY(20px);opacity:0}} to{{transform:translateY(0);opacity:1}} }}
.modal-header {{ display:flex;justify-content:space-between;align-items:center;margin-bottom:20px; }}
.modal-close {{ background:none;border:none;font-size:20px;cursor:pointer;color:var(--text-muted); }}

// JS
function openModal(id) {{ document.getElementById(id).classList.add('open'); }}
function closeModal(id) {{ document.getElementById(id).classList.remove('open'); }}
// Close on overlay click:
document.querySelectorAll('.modal-overlay').forEach(m => {{
  m.addEventListener('click', e => {{ if(e.target === m) m.classList.remove('open'); }});
}});

── PATTERN: CSV Export ──
function exportCSV(data, filename) {{
  if (!data.length) return;
  const headers = Object.keys(data[0]);
  const rows = data.map(row => headers.map(h => `"${{String(row[h]).replace(/"/g,'""')}}"`).join(','));
  const csv = [headers.join(','), ...rows].join('\n');
  const blob = new Blob([csv], {{ type: 'text/csv' }});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a'); a.href = url; a.download = filename;
  document.body.appendChild(a); a.click(); a.remove(); URL.revokeObjectURL(url);
}}

── PATTERN: Search/Filter ──
function filterItems(items, query, fields) {{
  if (!query.trim()) return items;
  const q = query.toLowerCase();
  return items.filter(item => fields.some(f => String(item[f] || '').toLowerCase().includes(q)));
}}

── PATTERN: Toast Notification ──
/* CSS */
.toast {{ position:fixed;bottom:24px;right:24px;padding:12px 20px;
          border-radius:var(--radius-sm);color:white;font-size:14px;
          transform:translateY(80px);opacity:0;transition:all 0.3s ease;
          z-index:9999;max-width:300px;box-shadow:var(--shadow-lg); }}
.toast.show {{ transform:translateY(0);opacity:1; }}
.toast.success {{ background:var(--success); }}
.toast.error   {{ background:var(--danger);   }}
.toast.warning {{ background:var(--warning);  }}

// JS
function showToast(message, type='success', duration=3000) {{
  const t = document.getElementById('toast');
  t.textContent = message; t.className = `toast ${{type}} show`;
  setTimeout(() => t.classList.remove('show'), duration);
}}

── PATTERN: Responsive Dashboard Layout ──
/* CSS */
.app-layout {{ display:flex;min-height:100vh; }}
.sidebar {{ width:260px;background:var(--bg-secondary);border-right:1px solid var(--border);
            padding:24px 0;flex-shrink:0;transition:var(--transition); }}
.main-content {{ flex:1;overflow-y:auto;padding:24px; }}
.stats-grid {{ display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px;margin-bottom:24px; }}
.stat-card {{ background:var(--bg-card);border-radius:var(--radius);padding:20px;box-shadow:var(--shadow); }}
.content-grid {{ display:grid;grid-template-columns:1fr 380px;gap:20px; }}
@media(max-width:1024px) {{ .content-grid {{ grid-template-columns:1fr; }} }}
@media(max-width:768px) {{
  .sidebar {{ position:fixed;left:-260px;top:0;height:100%;z-index:100; }}
  .sidebar.open {{ left:0;box-shadow:var(--shadow-lg); }}
  .main-content {{ padding:16px; }}
}}

── PATTERN: Tabs/Sections ──
// HTML: <div class="tab-btn active" data-tab="overview">Overview</div>
// Sections: <section id="tab-overview" class="tab-content active">...</section>
function initTabs() {{
  document.querySelectorAll('.tab-btn').forEach(btn => {{
    btn.addEventListener('click', () => {{
      const target = btn.dataset.tab;
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(s => s.classList.remove('active'));
      btn.classList.add('active');
      document.getElementById('tab-' + target).classList.add('active');
    }});
  }});
}}

── PATTERN: Form Validation ──
function validateForm(fields) {{
  let valid = true;
  fields.forEach({{ id, message }}) => {{
    const el = document.getElementById(id);
    const err = document.getElementById(id + '-err');
    if (!el.value.trim()) {{
      if(err) {{ err.textContent = message; err.style.display = 'block'; }}
      el.style.borderColor = 'var(--danger)';
      valid = false;
    }} else {{
      if(err) err.style.display = 'none';
      el.style.borderColor = '';
    }}
  }});
  return valid;
}}

── PATTERN: Pomodoro Timer ──
let timerInterval = null, secondsLeft = 25 * 60, phase = 'work';
const PHASES = {{ work: 25*60, short: 5*60, long: 15*60 }};
function startTimer() {{
  if (timerInterval) return;
  timerInterval = setInterval(() => {{
    secondsLeft--;
    updateTimerDisplay();
    if (secondsLeft <= 0) {{ clearInterval(timerInterval); timerInterval = null; onTimerEnd(); }}
  }}, 1000);
}}
function pauseTimer() {{ clearInterval(timerInterval); timerInterval = null; }}
function resetTimer(p = 'work') {{
  clearInterval(timerInterval); timerInterval = null;
  phase = p; secondsLeft = PHASES[p]; updateTimerDisplay();
}}
function updateTimerDisplay() {{
  const m = String(Math.floor(secondsLeft/60)).padStart(2,'0');
  const s = String(secondsLeft%60).padStart(2,'0');
  document.getElementById('timerDisplay').textContent = `${{m}}:${{s}}`;
}}

── PATTERN: Streak Counter ──
function updateStreak(key) {{
  const data = loadData(key, {{ streak: 0, lastDate: null }});
  const today = new Date().toDateString();
  const yesterday = new Date(Date.now() - 86400000).toDateString();
  if (data.lastDate === today) return data.streak;
  if (data.lastDate === yesterday) data.streak++;
  else data.streak = 1;
  data.lastDate = today;
  saveData(key, data);
  return data.streak;
}}

════════════════════════════════════════════════════════════════
RULES FOR YOUR OUTPUT
════════════════════════════════════════════════════════════════
1. full_code must be the COMPLETE file — every line, ready to save and run.
2. Implement EVERY feature listed in the plan's features array. Do not skip any.
3. Order: index.html → style.css → script.js
4. index.html must link style.css via <link> and script.js via <script src> at end of body.
5. For complex apps, script.js will naturally be 500-1500+ lines. That is expected and correct.
6. Always include a <div id="toast" class="toast"></div> and toast JS for user feedback.
7. All data must persist via LocalStorage — never assume a backend or server.
8. The app must work perfectly when opened as a local HTML file or via iframe srcdoc.
9. DO NOT use any external JS libraries. Pure vanilla JS only.
10. FONTS: You may use one Google Fonts import in index.html (Inter or similar).
"""


def coder_system_prompt() -> str:
    return """You are the CODER agent. Your only job is to save a file using write_file.

WORKFLOW — follow this EXACTLY:
1. Call read_file(filepath) to see any existing content.
2. Call write_file(filepath, full_code) with the COMPLETE file content.
   - full_code comes from your task description's 'full_code' field.
   - Do NOT truncate it. Write every single line.
3. Verify: call read_file(filepath) again to confirm it was saved.
4. If read_file returns empty, call write_file again.

CRITICAL:
- You MUST call write_file. Responding with text only is a failure.
- The content argument must be the COMPLETE file — not a summary, not pseudocode.
- HTML files must have <!DOCTYPE html> and working <link>/<script> tags.
- JS files must have all functions implemented and all event listeners attached.
"""