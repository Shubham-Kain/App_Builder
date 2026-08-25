def planner_prompt(user_prompt: str) -> str:
    return f"""You are the PRINCIPAL SOFTWARE ARCHITECT & PRODUCT DESIGNER for an advanced AI web application builder.

USER REQUEST:
{user_prompt}

YOUR TASK:
Produce an exhaustive, production-grade project plan for a feature-complete, pure HTML/CSS/JS web application.

STRICT DESIGN & ARCHITECTURAL RULES:
1. name        -> Lowercase with underscores only (e.g. "smart_study_planner", "personal_finance_dashboard", "fitness_workout_tracker", "project_crm_hub", "ecommerce_store").
2. title       -> Clean, professional, user-facing title.
3. description -> 2-3 sentences explaining the app's mission, core workflows, and value.
4. complexity  -> Always "complex" for any dashboard, productivity tool, planner, tracker, financial system, CRM, store, or multi-view application.
5. features    -> Break down the user prompt into 14 to 20 concrete, highly specific, and testable features:
   - Identify ALL core data models appropriate for the app's domain:
     * Study/Education: Tasks, Subjects, Topics, Exams, Pomodoro Sessions.
     * Personal Finance: Transactions, Categories, Budgets, Savings Goals, Monthly Summaries.
     * Health/Fitness: Workouts, Exercises, Meals/Calories, Water Intake, Goals, Activity Logs.
     * Project/CRM: Projects, Tasks, Clients/Leads, Milestones, Revenue, Deadlines.
     * E-Commerce/Catalog: Products, Categories, Cart, Wishlist, Order History.
     * Notes/Knowledge: Notes, Notebooks/Folders, Tags, Favorites, Word Count.
   - Plan 4 to 6 distinct navigation tabs/views (e.g. Overview Dashboard, Main Manager/Catalog/Planner, Specialized Interactive Tool/Timer/Calculator, Visual Charts & Analytics, Milestones/History, Settings & CSV Export).
   - Plan live dynamic calculations (e.g. Totals, Scores, Streaks, Progress Bars, Countdowns, Used vs Remaining, Chart Heights).
   - Plan interactive filters & search (live keyword search, category dropdown, priority dropdown, status filters, date range filters).
   - Plan complete CRUD interactions (Add item modal, Edit item modal, Delete item with toast confirmation, Toggle/Complete status).
   - Plan persistent storage in LocalStorage with pre-loaded realistic sample data tailored to the app domain so the app looks alive immediately.
   - Plan dark/light theme switch and CSV data export.
6. files       -> Exactly 3 files: index.html, style.css, script.js.
"""


def html_prompt(plan_json: str, user_prompt: str) -> str:
    return f"""You are the LEAD UI/UX & FRONTEND ARCHITECT.
You are generating the COMPLETE `index.html` file for a world-class, modern, feature-rich web application.

USER PROMPT:
{user_prompt}

PROJECT PLAN:
{plan_json}

════════════════════════════════════════════════════════════════
MANDATORY UI ARCHITECTURE (LINEAR / VERCEL / STRIPE SAAS DESIGN)
════════════════════════════════════════════════════════════════

Your HTML MUST be rich, semantic, beautifully structured, and fully customized to the specific app requested in the user prompt and plan.

1. HEAD SECTION:
   - `<meta charset="UTF-8">` and `<meta name="viewport" content="width=device-width, initial-scale=1.0">`
   - Page `<title>` matching the plan title
   - Google Fonts link for 'Plus Jakarta Sans', 'Inter', or 'Space Grotesk'
   - `<link rel="stylesheet" href="style.css">`

2. APP LAYOUT SHELL (`<div class="app-layout">`):

   A. TOPBAR HEADER (`<header class="topbar">`):
      - Brand logo icon + Application Name
      - Global Search Bar (`<input type="text" id="globalSearch" placeholder="Search...">`)
      - Key live status indicators/badges tailored to the app (e.g., Streak Badge, Productivity/Balance Badge, Metric Counter)
      - Quick Action CTA Button (e.g., "+ New Task", "+ New Transaction", "+ Add Item") with `type="button"`
      - Theme Toggle Button (`<button type="button" id="themeToggleBtn" class="theme-btn" title="Toggle Theme">🌙</button>`)
      - Mobile Menu Hamburger Toggle (`<button type="button" id="mobileMenuBtn" class="mobile-menu-btn">☰</button>`)

   B. SIDEBAR NAVIGATION (`<aside class="sidebar" id="sidebar">`):
      - Brand Logo block with app title and subtitle
      - Navigation Items tailored to the app's views with icons and `data-tab` attributes:
        * 4 to 6 `<button type="button" class="nav-item" data-tab="tab-id">` buttons (the first marked `class="nav-item active"`).
        * Examples for Study App: Dashboard Overview, Study Planner & Tasks, Pomodoro Focus, Subjects & Topics, Analytics & Progress, Exam Countdown.
        * Examples for Finance App: Overview Dashboard, Transactions Manager, Category Budgets, Spending Analytics, Goals & Savings, Reports & Export.
        * Examples for Fitness App: Dashboard Overview, Workout Planner, Exercise Library, Meal & Calorie Log, Progress Analytics, Goals.
        * Examples for CRM App: Dashboard, Leads & Pipeline, Client Contacts, Deals & Revenue, Task Milestones, Reports.
      - Sidebar Footer with quick stats, "Export CSV" button (`id="sidebarExportCsvBtn"`), and "Reset Sample Data" button (`id="resetDataBtn"`).

   C. MAIN CONTENT CONTAINER (`<main class="main-content">`):
      Include ALL planned views as `<section class="tab-pane" id="tab-TABID">` (first tab has `class="tab-pane active"`, others are inactive):

      - VIEW 1: OVERVIEW DASHBOARD:
        * Welcome greeting banner with date & inspirational summary
        * 4 Top Metric Cards with big bold values, trend indicators, and progress bars/circles (e.g. Score/Balance, Focus/Income, Tasks/Expenses, Streak/Savings)
        * 2-Column Dashboard Grid with primary quick-action widget (e.g. today's checklist or recent items) on the left, and secondary tool widget (e.g. Timer, Budget bars, Countdown) on the right
        * Quick summaries for categories, subjects, or accounts

      - VIEW 2: MAIN MANAGEMENT / PLANNER / CATALOG VIEW:
        * Toolbar with search input, category filter dropdown, priority/type filter, status filter, and "+ Add New" button
        * Dynamic list/table/grid container for items (with checkboxes, badges, edit buttons, delete buttons, action triggers)
        * Empty state placeholder for when filters return no items

      - VIEW 3: SPECIALIZED TOOL / TIMER / BUDGET / CALCULATOR VIEW:
        * Full interactive component (e.g. Pomodoro timer with phase pills 25/5/15, big digital display, start/pause/reset buttons; OR Category Budget manager with set budget forms, used vs remaining meters, and warning highlights)

      - VIEW 4: CATEGORIES / SUBJECTS / GOALS / TRACKING VIEW:
        * Grid of cards representing entities (e.g. Subjects with topic checklists and weekly hour progress; or Financial Goals with target amount and savings progress; or Workout routines)

      - VIEW 5: ANALYTICS & VISUAL CHARTS VIEW:
        * Weekly Bar Chart container (using pure CSS/HTML flex bars with dynamic heights and day labels)
        * Category/Subject distribution breakdown with colored progress bars and percentages
        * Summary insights and performance metrics

      - VIEW 6: COUNTDOWN / REPORTS / LOGS VIEW:
        * Specialized countdown cards (e.g. Exam dates with urgent/warning badges; or Monthly Financial Statement breakdown; or Milestone timeline)
        * "Export to CSV" button (`id="exportCsvBtn"`)

3. MODAL DIALOGS (Include all modals needed for creating and editing data):
   - Every modal has `<div class="modal-overlay" id="MODAL_ID">` containing `<div class="modal">`
   - Modal Header with title and close button (`<button type="button" class="modal-close">×</button>`)
   - Modal Form with labeled inputs, selects, validation error spans, and submit button
   - Modals for: Add/Edit Main Item, Add/Edit Category or Subject, Add/Edit Goal or Exam

4. TOAST NOTIFICATION CONTAINER:
   - `<div id="toast" class="toast"></div>`

5. SCRIPTS:
   - `<script src="script.js"></script>` at the bottom of `<body>`.

════════════════════════════════════════════════════════════════
CRITICAL RULES FOR INTERACTIVE HTML
════════════════════════════════════════════════════════════════
- All `<button>` tags MUST have `type="button"` (unless explicitly inside a `<form>` as submit button).
- Every interactive element (inputs, buttons, tabs, select dropdowns, modals, containers) MUST have unique, descriptive `id` and `class` attributes so JavaScript and CSS can hook into them.
- Provide 100% COMPLETE HTML. NEVER use ellipses, placeholders, or "// TODO".
"""


def css_prompt(plan_json: str, html_code: str) -> str:
    return f"""You are the LEAD DESIGN SYSTEM ARCHITECT & CSS ENGINEER.
You are generating the COMPLETE `style.css` for a world-class, premium SaaS web application.

PROJECT PLAN:
{plan_json}

HTML MARKUP BEING STYLED:
{html_code}

════════════════════════════════════════════════════════════════
DESIGN SPECIFICATIONS (PREMIUM MODERN SAAS / DARK & LIGHT MODE)
════════════════════════════════════════════════════════════════

Your CSS must provide an ultra-clean, modern, polished design (similar to Linear.app, Vercel, Stripe).

1. CSS DESIGN TOKENS & THEMING:
   - `:root` (Light Theme) and `[data-theme="dark"]` (Dark Theme by default):
     * Backgrounds:
       - `--bg-base`: #0B0F17 (dark) / #F8FAFC (light)
       - `--bg-card`: #131B2A (dark) / #FFFFFF (light)
       - `--bg-card-hover`: #1B2538 (dark) / #F1F5F9 (light)
       - `--bg-sidebar`: #0F1622 (dark) / #FFFFFF (light)
       - `--bg-input`: #172235 (dark) / #F1F5F9 (light)
       - `--bg-modal`: #131B2A (dark) / #FFFFFF (light)
     * Text:
       - `--text-primary`: #F1F5F9 (dark) / #0F172A (light)
       - `--text-secondary`: #94A3B8 (dark) / #475569 (light)
       - `--text-muted`: #64748B (dark) / #94A3B8 (light)
     * Accents & Brand:
       - `--primary`: #6366F1 (vibrant indigo)
       - `--primary-hover`: #4F46E5
       - `--primary-glow`: rgba(99, 102, 241, 0.3)
       - `--primary-light`: rgba(99, 102, 241, 0.15)
     * Status Colors:
       - `--success`: #10B981 / `--success-light`: rgba(16, 185, 129, 0.15)
       - `--warning`: #F59E0B / `--warning-light`: rgba(245, 158, 11, 0.15)
       - `--danger`: #EF4444 / `--danger-light`: rgba(239, 68, 68, 0.15)
       - `--info`: #06B6D4 / `--info-light`: rgba(6, 182, 212, 0.15)
     * Borders & Shadows:
       - `--border`: rgba(255, 255, 255, 0.08) (dark) / #E2E8F0 (light)
       - `--border-focus`: #6366F1
       - `--shadow-sm`: 0 1px 2px rgba(0,0,0,0.3)
       - `--shadow-md`: 0 4px 12px rgba(0,0,0,0.3)
       - `--shadow-lg`: 0 12px 32px rgba(0,0,0,0.4)
       - `--radius-sm`: 6px; `--radius-md`: 10px; `--radius-lg`: 16px; `--radius-full`: 9999px;
       - `--transition`: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);

2. CORE RESET & BASE STYLES:
   - `* {{ box-sizing: border-box; margin: 0; padding: 0; }}`
   - `body`: `font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif; background-color: var(--bg-base); color: var(--text-primary); line-height: 1.5; min-height: 100vh;`

3. APP LAYOUT STRUCTURE:
   - `.app-layout`: `display: flex; min-height: 100vh; width: 100%;`
   - `.sidebar`: `width: 260px; background: var(--bg-sidebar); border-right: 1px solid var(--border); display: flex; flex-direction: column; flex-shrink: 0; position: sticky; top: 0; height: 100vh; padding: 20px 16px; transition: var(--transition);`
   - `.nav-item`: `display: flex; align-items: center; gap: 12px; padding: 12px 14px; width: 100%; border: none; background: transparent; color: var(--text-secondary); border-radius: var(--radius-md); font-size: 14px; font-weight: 500; cursor: pointer; transition: var(--transition); text-align: left; margin-bottom: 4px;`
   - `.nav-item:hover`: `background: var(--bg-card-hover); color: var(--text-primary); transform: translateX(3px);`
   - `.nav-item.active`: `background: var(--primary-light); color: var(--primary); font-weight: 600; box-shadow: inset 0 0 0 1px var(--primary);`
   - `.main-content`: `flex: 1; min-width: 0; display: flex; flex-direction: column; overflow-y: auto;`
   - `.topbar`: `display: flex; align-items: center; justify-content: space-between; padding: 16px 28px; background: var(--bg-card); border-bottom: 1px solid var(--border); position: sticky; top: 0; z-index: 50; backdrop-filter: blur(12px);`
   - `.tab-pane`: `display: none; padding: 28px; animation: fadeIn 0.25s ease-out;`
   - `.tab-pane.active`: `display: block;`
   - `@keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: translateY(0); }} }}`

4. COMPONENT STYLING:
   - **Metric / Stat Cards**: `background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 22px; box-shadow: var(--shadow-sm); transition: var(--transition);`
     * Hover: `transform: translateY(-3px); box-shadow: var(--shadow-md); border-color: var(--primary-glow);`
     * Number: `font-size: 28px; font-weight: 700; color: var(--text-primary); margin: 8px 0;`
   - **Buttons**:
     * `.btn`: `display: inline-flex; align-items: center; justify-content: center; gap: 8px; padding: 10px 18px; border-radius: var(--radius-md); font-size: 14px; font-weight: 600; cursor: pointer; border: 1px solid transparent; transition: var(--transition);`
     * `.btn-primary`: `background: var(--primary); color: #FFF; box-shadow: 0 4px 14px var(--primary-glow);`
     * `.btn-primary:hover`: `background: var(--primary-hover); transform: translateY(-1px);`
     * `.btn-secondary`: `background: var(--bg-input); color: var(--text-primary); border-color: var(--border);`
     * `.btn-danger`: `background: var(--danger); color: #FFF;`
     * `.btn-icon`: `padding: 8px; border-radius: var(--radius-md); background: transparent; border: 1px solid var(--border); color: var(--text-secondary); cursor: pointer;`
   - **Badges & Tags**:
     * `.badge`: `display: inline-flex; align-items: center; gap: 6px; padding: 4px 10px; border-radius: var(--radius-full); font-size: 12px; font-weight: 600;`
     * `.badge-success`, `.priority-low`: `background: var(--success-light); color: var(--success);`
     * `.badge-warning`, `.priority-medium`: `background: var(--warning-light); color: var(--warning);`
     * `.badge-danger`, `.priority-high`: `background: var(--danger-light); color: var(--danger);`
   - **Forms & Inputs**:
     * `input[type="text"]`, `input[type="number"]`, `input[type="date"]`, `select`, `textarea`: `width: 100%; padding: 10px 14px; background: var(--bg-input); border: 1px solid var(--border); border-radius: var(--radius-md); color: var(--text-primary); font-size: 14px; outline: none; transition: var(--transition);`
     * `:focus`: `border-color: var(--border-focus); box-shadow: 0 0 0 3px var(--primary-glow);`
   - **Progress Bars**:
     * `.progress-track`: `height: 8px; background: var(--bg-input); border-radius: var(--radius-full); overflow: hidden; margin: 8px 0;`
     * `.progress-fill`: `height: 100%; background: linear-gradient(90deg, var(--primary), #8B5CF6); border-radius: var(--radius-full); transition: width 0.5s ease;`
   - **Interactive Charts & Weekly Bars**:
     * `.chart-container`: `display: flex; align-items: flex-end; justify-content: space-between; gap: 12px; height: 180px; padding: 16px 0; border-bottom: 1px solid var(--border);`
     * `.chart-col`: `flex: 1; display: flex; flex-direction: column; align-items: center; gap: 8px; height: 100%; justify-content: flex-end;`
     * `.chart-bar`: `width: 100%; max-width: 36px; background: var(--primary); border-radius: 6px 6px 0 0; transition: height 0.6s cubic-bezier(0.34, 1.56, 0.64, 1); min-height: 4px;`
     * `.chart-label`: `font-size: 12px; color: var(--text-secondary);`
   - **Digital Timer Widget** (if present):
     * `.timer-display`: `font-size: 64px; font-weight: 800; font-family: 'Space Grotesk', monospace; color: var(--primary); text-align: center; margin: 24px 0; letter-spacing: 2px; text-shadow: 0 0 24px var(--primary-glow);`
   - **Modals**:
     * `.modal-overlay`: `position: fixed; inset: 0; background: rgba(0,0,0,0.65); backdrop-filter: blur(6px); display: none; align-items: center; justify-content: center; z-index: 1000; padding: 20px;`
     * `.modal-overlay.open`: `display: flex;`
     * `.modal`: `background: var(--bg-modal); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 28px; width: 100%; max-width: 520px; box-shadow: var(--shadow-lg); animation: modalPop 0.2s ease-out;`
     * `@keyframes modalPop {{ from {{ transform: scale(0.95); opacity: 0; }} to {{ transform: scale(1); opacity: 1; }} }}`
   - **Toast Notifications**:
     * `.toast`: `position: fixed; bottom: 24px; right: 24px; padding: 14px 22px; border-radius: var(--radius-md); background: var(--bg-card); color: var(--text-primary); border: 1px solid var(--border); box-shadow: var(--shadow-lg); font-size: 14px; font-weight: 500; display: flex; align-items: center; gap: 10px; transform: translateY(100px); opacity: 0; transition: var(--transition); z-index: 9999;`
     * `.toast.show`: `transform: translateY(0); opacity: 1;`
     * `.toast.success`: `border-left: 4px solid var(--success);`
     * `.toast.error`: `border-left: 4px solid var(--danger);`

5. RESPONSIVE MEDIA QUERIES:
   - `@media (max-width: 1024px) {{ .dashboard-grid {{ grid-template-columns: 1fr; }} }}`
   - `@media (max-width: 768px) {{`
     * `.sidebar {{ position: fixed; left: -260px; z-index: 100; box-shadow: var(--shadow-lg); }}`
     * `.sidebar.open {{ left: 0; }}`
     * `.mobile-menu-btn {{ display: flex; }}`
     * `.topbar {{ padding: 12px 16px; }}`
     * `.tab-pane {{ padding: 16px; }}`
     * `}}`

════════════════════════════════════════════════════════════════
OUTPUT RULES
════════════════════════════════════════════════════════════════
- Output the COMPLETE `style.css` code.
- Ensure EVERY single element, tag, ID, and class in `index.html` has gorgeous styling.
- NO unstyled elements, NO raw browser defaults.
"""


def js_prompt(plan_json: str, html_code: str, css_code: str) -> str:
    return f"""You are the PRINCIPAL FULL-STACK JAVASCRIPT ENGINEER.
You are generating the COMPLETE `script.js` file for a world-class, production-ready web application.

PROJECT PLAN:
{plan_json}

HTML STRUCTURE:
{html_code}

CSS STYLING REFERENCE:
{css_code}

════════════════════════════════════════════════════════════════
MANDATORY JAVASCRIPT ARCHITECTURE & LOGIC
════════════════════════════════════════════════════════════════

Your JavaScript code must be modular, robust, comprehensive, and 100% bug-free.

1. LOCALSTORAGE STATE ENGINE & PRE-LOADED SEED DATA:
   - Maintain a single centralized state object or typed repositories.
   - If LocalStorage is empty on first load, AUTOMATICALLY populate it with rich, realistic default sample data tailored to the app domain (e.g. 4-5 sample items, categories, metrics, and logs) so the dashboard looks alive and functional immediately!
   - Provide safe persistence:
     ```javascript
     function getStorage(key, fallback) {{{{
       try {{{{ const v = localStorage.getItem(key); return v ? JSON.parse(v) : fallback; }}}}
       catch (e) {{{{ return fallback; }}}}
     }}}}
     function setStorage(key, value) {{{{
       try {{{{ localStorage.setItem(key, JSON.stringify(value)); }}}}
       catch (e) {{{{ console.error(e); }}}}
     }}}}
     ```

2. TAB NAVIGATION & ROUTING:
   - Attach click listeners to ALL `.nav-item` buttons:
     ```javascript
     document.querySelectorAll('.nav-item').forEach(btn => {{{{
       btn.addEventListener('click', () => {{{{
         const targetTab = btn.dataset.tab;
         document.querySelectorAll('.nav-item').forEach(b => b.classList.remove('active'));
         document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
         btn.classList.add('active');
         const targetPane = document.getElementById('tab-' + targetTab);
         if (targetPane) targetPane.classList.add('active');
         // Close mobile sidebar if open
         const sb = document.getElementById('sidebar');
         if (sb) sb.classList.remove('open');
       }}}});
     }}}});
     ```
   - Handle mobile hamburger menu button toggle (`#mobileMenuBtn`).

3. FULL CRUD LOGIC FOR MAIN ENTITIES:
   - Implement complete Create, Read, Update, Delete for all core models.
   - Render functions that dynamically build DOM elements with checkboxes, edit buttons, delete buttons, action triggers, and badges.
   - Attach event delegation or dynamic event listeners to every action button.
   - Deletion must show confirmation or instant remove with toast undo/notification.

4. MULTI-CRITERIA SEARCH & FILTER ENGINE:
   - Wire up live keyword search input (`#globalSearch`, `#taskSearchInput`, etc.) to filter items in real time.
   - Wire up category/subject filter dropdowns, priority dropdowns, and status filter buttons.
   - Re-render the active view instantly on any input/change event.

5. SPECIALIZED DOMAIN ENGINES (Implement fully based on the app domain):
   - **If Timer/Pomodoro present**:
     * Implement accurate `setInterval` timer with start, pause, reset, skip phase.
     * Use Web Audio API `AudioContext` to play a pleasant chime sound on completion without external files!
     * Log completed focus sessions and update daily stats.
   - **If Streaks / Productivity / Score calculations present**:
     * Compute actual consecutive day streaks using date comparisons.
     * Calculate live scores/balances and update all summary badges and gauge bars in the DOM.
   - **If Budget / Finance present**:
     * Calculate Total Income, Total Expenses, Balance, Category totals.
     * Trigger warning badges when expenses exceed category budget.
   - **If Exam / Milestone / Deadline Countdown present**:
     * Calculate real remaining days and hours and apply urgency classes.

6. CHARTS & VISUAL ANALYTICS RENDERING:
   - Dynamically compute and set heights/percentages on CSS bar charts and progress bars.
   - Update labels, values, and tooltips.

7. CSV EXPORT ENGINE:
   - Provide working CSV file download function:
     ```javascript
     function exportToCsv(filename, rows) {{{{
       if (!rows || !rows.length) return;
       const headers = Object.keys(rows[0]);
       const csvContent = [
         headers.join(','),
         ...rows.map(r => headers.map(h => `"${{{{String(r[h] ?? '').replace(/"/g, '""')}}}}"`).join(','))
       ].join('\\n');
       const blob = new Blob([csvContent], {{{{ type: 'text/csv;charset=utf-8;' }}}});
       const url = URL.createObjectURL(blob);
       const link = document.createElement('a');
       link.setAttribute('href', url);
       link.setAttribute('download', filename);
       document.body.appendChild(link);
       link.click();
       document.body.removeChild(link);
       URL.revokeObjectURL(url);
     }}}}
     ```

8. DARK / LIGHT THEME TOGGLE:
   - Wire up `#themeToggleBtn`:
     ```javascript
     function initTheme() {{{{
       const saved = getStorage('app_theme', 'dark');
       document.documentElement.setAttribute('data-theme', saved);
       const btn = document.getElementById('themeToggleBtn');
       if (btn) btn.textContent = saved === 'dark' ? '☀️' : '🌙';
     }}}}
     function toggleTheme() {{{{
       const current = document.documentElement.getAttribute('data-theme') || 'dark';
       const next = current === 'dark' ? 'light' : 'dark';
       document.documentElement.setAttribute('data-theme', next);
       setStorage('app_theme', next);
       const btn = document.getElementById('themeToggleBtn');
       if (btn) btn.textContent = next === 'dark' ? '☀️' : '🌙';
       showToast(`Switched to ${{next}} mode`, 'info');
     }}}}
     ```

9. MODAL & TOAST MANAGERS:
   - Safe modal open/close functions with backdrop click handling and `Escape` key handler.
   - Safe form submissions: ALWAYS call `e.preventDefault()` on form submit events!
   - Toast notification helper:
     ```javascript
     function showToast(message, type = 'success') {{{{
       const toast = document.getElementById('toast');
       if (!toast) return;
       toast.textContent = message;
       toast.className = `toast ${{type}} show`;
       setTimeout(() => {{{{ toast.classList.remove('show'); }}}}, 3000);
     }}}}
     ```

10. INITIALIZATION:
    - Wrap all event listener attachments and initial renders in `document.addEventListener('DOMContentLoaded', () => {{{{ ... }}}})`.

════════════════════════════════════════════════════════════════
CRITICAL OUTPUT RULES
════════════════════════════════════════════════════════════════
- Output the COMPLETE, 100% working `script.js` code.
- NEVER write placeholders, stubs, or comments replacing logic.
- Ensure EVERY button, form, filter, tab, and modal in `index.html` has its active event handler.
"""


def coder_system_prompt() -> str:
    return "You are the Coder Agent. Produce complete, working code."