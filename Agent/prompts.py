def planner_prompt(user_prompt: str) -> str:
    return f"""You are the PRINCIPAL SOFTWARE ARCHITECT & PRODUCT DESIGNER for an advanced web application builder.

USER REQUEST:
{user_prompt}

YOUR TASK:
Produce an exhaustive, production-grade project plan for a feature-complete pure HTML/CSS/JS web application.

STRICT REQUIREMENTS:
1. name        -> Lowercase with underscores only (e.g. "smart_study_planner", "finance_analytics_dashboard").
2. title       -> Clean, user-facing title (e.g. "Smart Study Planner & Productivity Dashboard").
3. description -> 2-3 sentences explaining the app's mission, key features, and user benefits.
4. complexity  -> Always "complex" for dashboards, productivity tools, planners, trackers, or financial apps.
5. features    -> Break down the user prompt into 12 to 20 concrete, highly specific, and testable features:
   - Include all core entities (e.g., Tasks, Subjects, Topics, Exams, Pomodoro Sessions).
   - Include multi-view navigation tabs (e.g., Overview Dashboard, Task Planner, Pomodoro Focus, Subject Analytics, Exam Countdown, Settings/Data Export).
   - Include metric calculation formulas (e.g., Productivity Score 0-100%, Streak Tracking, Progress Bars, Days Remaining).
   - Include multi-criteria Search & Filtering (keyword search, subject filter, priority filter, completion status filter).
   - Include interactive UI elements (modals for adding/editing, dark/light theme switch, toast notifications, CSV data export).
   - Include persistent storage (LocalStorage with pre-loaded realistic sample data).
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
MANDATORY UI ARCHITECTURE (LINEAR / VERCEL / STRIPE SAAS AESTHETICS)
════════════════════════════════════════════════════════════════

Your HTML MUST be rich, semantic, and fully structured. It must include:

1. HEAD SECTION:
   - `<meta charset="UTF-8">` and `<meta name="viewport" content="width=device-width, initial-scale=1.0">`
   - Page `<title>` matching the plan title
   - Google Fonts link for 'Plus Jakarta Sans', 'Inter', or 'Space Grotesk'
   - `<link rel="stylesheet" href="style.css">`

2. APP LAYOUT SHELL (`<div class="app-layout">`):
   A. TOP HEADER (`<header class="topbar">`):
      - Brand logo icon + Application Name + Version badge
      - Quick Search Bar (`<input type="text" id="globalSearch" placeholder="Search tasks, subjects, notes...">`)
      - Quick Action Buttons (e.g. "+ New Task", "+ New Subject")
      - Live Status / Streak Badge (e.g. `<div class="streak-badge" id="streakBadge">🔥 <span>0</span> Day Streak</div>`)
      - Productivity Score Badge (e.g. `<div class="score-badge" id="headerScoreBadge">⚡ <span>0%</span> Score</div>`)
      - Theme Toggle Button (`<button id="themeToggleBtn" class="theme-btn" title="Toggle Theme">🌙</button>`)
      - Mobile Menu Toggle Hamburger Button (`<button id="mobileMenuBtn" class="mobile-menu-btn">☰</button>`)

   B. SIDEBAR NAVIGATION (`<aside class="sidebar" id="sidebar">`):
      - App Brand block
      - Navigation Items with icons and data-tab attributes:
        * `<button class="nav-item active" data-tab="dashboard">📊 Dashboard</button>`
        * `<button class="nav-item" data-tab="planner">📅 Study Planner & Tasks</button>`
        * `<button class="nav-item" data-tab="pomodoro">⏱️ Pomodoro Timer</button>`
        * `<button class="nav-item" data-tab="subjects">📚 Subjects & Topics</button>`
        * `<button class="nav-item" data-tab="analytics">📈 Productivity Analytics</button>`
        * `<button class="nav-item" data-tab="exams">🎯 Exam Countdown</button>`
      - Sidebar Footer with Quick Stats & Data Actions (Export CSV, Clear Data)

   C. MAIN CONTENT AREA (`<main class="main-content">`):
      Every tab below must be present as `<section class="tab-pane active/inactive" id="tab-TABNAME">`:

      1. TAB 1: OVERVIEW DASHBOARD (`id="tab-dashboard"`):
         - Welcome Banner with greeting, current date, and motivational quote
         - Top Metrics Grid (4 Stat Cards):
           * Card 1: Daily Productivity Score (large percentage + progress circle/bar)
           * Card 2: Study Time Today (hours & minutes formatted)
           * Card 3: Tasks Completed (e.g. 5/8 tasks done + mini progress bar)
           * Card 4: Study Streak (consecutive days with flame icon)
         - 2-Column Dashboard Grid:
           * Left: Today's Focus Checklist (priority tasks, quick check, quick add)
           * Right: Mini Pomodoro Widget (quick start) + Upcoming Exam Countdown widget cards
         - Subject Progress Summary section with visual progress bars

      2. TAB 2: STUDY PLANNER & TASKS (`id="tab-planner"`):
         - Toolbar / Filter Bar:
           * Search Input (`id="taskSearchInput"`)
           * Subject Filter Dropdown (`id="taskSubjectFilter"`)
           * Priority Filter Dropdown (`id="taskPriorityFilter"` with All, High, Medium, Low)
           * Status Filter (All / Pending / Completed)
           * "+ Add Task" button (`id="openAddTaskBtn"`)
         - Task List Container (`id="tasksListContainer"`):
           * Displays cards/items with checkbox, title, subject tag, topic tag, priority badge (High/Med/Low), estimated minutes, due date, action buttons (Edit, Delete, Start Timer on Task)
         - Empty state placeholder if no tasks match

      3. TAB 3: POMODORO TIMER (`id="tab-pomodoro"`):
         - Timer Mode Tabs: "Work Focus (25m)", "Short Break (5m)", "Long Break (15m)"
         - Main Timer Display: Huge digital countdown timer (`id="timerDisplay"`, e.g. `25:00`)
         - Circular or horizontal progress indicator showing elapsed percentage
         - Active Task Banner: "Currently Focusing On: [Select a task or General Study]"
         - Timer Controls Bar: Start Button (`id="timerStartBtn"`), Pause Button (`id="timerPauseBtn"`), Reset Button (`id="timerResetBtn"`), Skip Phase (`id="timerSkipBtn"`)
         - Sound toggle & Auto-start break toggles
         - Session Tracker: "Today's Completed Pomodoros: X sessions (Y hrs studied)"
         - Recent Session History Log list

      4. TAB 4: SUBJECTS & TOPICS (`id="tab-subjects"`):
         - Header with "+ Add Subject" button (`id="openAddSubjectBtn"`)
         - Grid of Subject Cards (`id="subjectsGrid"`):
           * Each card has: Subject Title, Color indicator, Target Hours/Week vs Studied Hours, Animated Progress Bar, Topic List with completion checkboxes, "+ Add Topic" inline, Edit & Delete buttons

      5. TAB 5: PRODUCTIVITY ANALYTICS (`id="tab-analytics"`):
         - Header with "Export CSV" button (`id="exportAnalyticsBtn"`)
         - Weekly Study Hours Bar Chart Container (`id="weeklyChartContainer"`)
         - Subject-wise Distribution Bars (`id="subjectDistributionContainer"`)
         - Productivity Score Breakdown (Completed vs Planned, Streak history)
         - Key Insights summary cards

      6. TAB 6: EXAM COUNTDOWN (`id="tab-exams"`):
         - Header with "+ Add Exam" button (`id="openAddExamBtn"`)
         - Grid of Exam Cards (`id="examsGrid"`):
           * Displays Exam Name, Subject, Target Date, Days & Hours Remaining countdown badge with urgency colors (Red for <3 days, Orange for <7 days, Green for 7+ days), Syllabus completion progress bar

3. MODAL DIALOGS:
   - Add/Edit Task Modal (`id="taskModal"` with inputs for title, subject select, topic, priority select, estimated minutes, date)
   - Add/Edit Subject Modal (`id="subjectModal"` with inputs for name, color picker/options, target hours per week)
   - Add/Edit Exam Modal (`id="examModal"` with inputs for name, subject select, exam date, syllabus note)

4. TOAST NOTIFICATION CONTAINER:
   - `<div id="toast" class="toast"></div>`

5. FOOTER & SCRIPTS:
   - `<script src="script.js"></script>` at the bottom of body.

════════════════════════════════════════════════════════════════
OUTPUT RULES
════════════════════════════════════════════════════════════════
- Provide the COMPLETE, 100% finished `index.html` code.
- NEVER use placeholders, ellipses, or "// TODO".
- Every interactive element MUST have descriptive `id`, `class`, and `data-*` attributes so that CSS and JS can style and bind to them flawlessly.
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
   - Root `:root` (Light Theme) and `[data-theme="dark"]` (Dark Theme default):
     * Backgrounds: `--bg-main`, `--bg-card`, `--bg-sidebar`, `--bg-card-hover`, `--bg-input`, `--bg-modal`
     * Text: `--text-main`, `--text-secondary`, `--text-muted`, `--text-inverse`
     * Accents: `--primary` (e.g. vibrant indigo `#6366f1` or violet `#7c3aed`), `--primary-hover`, `--primary-glow`, `--primary-light`
     * Status Colors:
       - `--success` / `--success-light` (Emerald for completed, low priority, good streak)
       - `--warning` / `--warning-light` (Amber for medium priority, upcoming deadlines)
       - `--danger` / `--danger-light` (Rose/Red for high priority, urgent exams, delete buttons)
       - `--info` / `--info-light` (Sky blue for pomodoro, tips)
     * Borders: `--border-color`, `--border-focus`, `--border-subtle`
     * Shadows: `--shadow-sm`, `--shadow-md`, `--shadow-lg`, `--shadow-glow`
     * Radii: `--radius-sm` (6px), `--radius-md` (10px), `--radius-lg` (16px), `--radius-full` (9999px)
     * Transitions: `--transition-fast` (0.15s ease), `--transition-normal` (0.25s ease)

2. CORE STYLES & RESET:
   - `* {{ box-sizing: border-box; margin: 0; padding: 0; }}`
   - `body`: Smooth antialiased font (`'Plus Jakarta Sans', 'Inter', sans-serif`), background transitions, min-height 100vh.

3. APP LAYOUT (FLEX & CSS GRID):
   - `.app-layout`: Flex container with sidebar + main-content
   - `.topbar`: Modern header with glassmorphic blur, 1px border-bottom, flex alignment, gap, search bar, badges, theme toggle button
   - `.sidebar`: Width 260px, fixed or flex-sticky, sleek nav items with active pill highlight, badge counters, hover glow, border-right
   - `.main-content`: Flex 1, padding 28px, max-width 1400px, scrollable, smooth view transitions
   - `.tab-pane`: Display none by default; `.tab-pane.active` displays flex/grid with smooth fade-in animation (`@keyframes fadeIn`)

4. COMPONENT STYLING:
   - Metric / Stat Cards: Glassmorphism effect, subtle border, gradient accent bar, large bold values, trend indicators
   - Buttons: `.btn`, `.btn-primary`, `.btn-secondary`, `.btn-danger`, `.btn-icon` with custom hover elevation, active scale(0.98), focus rings
   - Task Cards: Clean list items with custom styled checkboxes (`accent-color` or custom checkmark), strikethrough animation for completed tasks, priority tags with soft colored backgrounds and text
   - Pomodoro Timer Widget:
     * Mode pills with active highlights
     * Huge crisp digital display with glow effect
     * Large, inviting Start/Pause/Reset action buttons
     * Session dots / streak counter
   - Subject Cards: Colorful top border/accent, progress bar with smooth transition width and gradient fill, topic checkboxes
   - Analytics Charts & Bars:
     * Weekly bar chart using pure CSS Flexbox bars with heights, day labels, tooltips on hover, and value indicators
     * Category distribution bars with percentages
   - Exam Countdown Cards: Urgency-colored badges (urgent pulsating red badge, warning amber badge, safe green badge), days remaining big counter
   - Modals: Fullscreen backdrop blur overlay, centered modal box with smooth scale-up entry animation, clean form groups, styled inputs, close button
   - Toast: Floating notification at bottom-right with slide-up animation, success/error/warning variants

5. RESPONSIVE DESIGN:
   - On screens < 1024px: Adjust grid columns
   - On screens < 768px:
     * Sidebar becomes off-canvas drawer (`transform: translateX(-100%)` / `.sidebar.open { transform: translateX(0) }`)
     * Header adjusts search bar and stacks buttons
     * Metric grid becomes 1-2 columns
     * Touch-friendly button padding

════════════════════════════════════════════════════════════════
OUTPUT RULES
════════════════════════════════════════════════════════════════
- Output the COMPLETE `style.css` code.
- Make sure EVERY class, ID, and tag in `index.html` has gorgeous, finished CSS.
- NO unstyled elements, NO default browser inputs or raw buttons.
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

Your JavaScript code must be modular, robust, and 100% functional. Implement EVERY feature:

1. LOCALSTORAGE STATE MANAGEMENT & DEFAULT SEED DATA:
   - If LocalStorage is empty on first load, populate it with rich, realistic default sample data so the app looks alive and impressive immediately:
     * 3-4 Sample Subjects (e.g., "Mathematics" [color: #6366f1, target: 10 hrs], "Physics" [color: #06b6d4, target: 8 hrs], "Computer Science" [color: #10b981, target: 12 hrs], "Literature" [color: #f59e0b, target: 5 hrs]) with sub-topics
     * 5-6 Sample Tasks with mixed priorities (High, Medium, Low), subjects, estimated minutes, and dates (some completed, some pending)
     * 2 Sample Exams (e.g. "Final Mathematics Exam" 5 days away, "Physics Midterm" 12 days away)
     * Initial Pomodoro stats and a 3-day study streak
   - Helper functions: `loadState(key, fallback)`, `saveState(key, value)`. Always safe with try/catch.

2. TAB NAVIGATION & ROUTING:
   - Handle clicks on all `.nav-item` buttons and switch visible `.tab-pane` smoothly.
   - Update active state on navigation buttons.
   - Mobile sidebar toggle (open/close on mobile hamburger click).

3. TASK PLANNER CRUD & FILTERING:
   - Render tasks dynamically into `#tasksListContainer` and mini-checklist on dashboard.
   - Add new task (via modal or inline form) with validation.
   - Toggle task complete (updates strike-through, completion timestamp, recalculates daily productivity score and streak).
   - Delete task with animation and toast notification.
   - Edit task capability.
   - Multi-Filter & Search Engine:
     * Live search by keyword in title/topic
     * Filter by Subject
     * Filter by Priority (High / Medium / Low)
     * Filter by Status (All / Pending / Completed)
     * Instant re-rendering on any filter change.

4. POMODORO TIMER ENGINE:
   - Timer state: `work` (25m), `shortBreak` (5m), `longBreak` (15m), `timeRemaining`, `isRunning`, `intervalId`, `completedSessions`.
   - Start, Pause, Reset, and Skip phase functions.
   - Smooth countdown updating `#timerDisplay` and document title (e.g. `(24:50) Study Planner`).
   - Web Audio API notification beep when timer ends (using `new (window.AudioContext || window.webkitAudioContext)()` - synthesizes pleasant chime sound without any external audio file!).
   - On work session completion: log study session, increment study minutes for the active subject, update daily total, and trigger toast celebration.

5. STUDY STREAK & DAILY PRODUCTIVITY SCORE ENGINE:
   - Streak tracking: Checks last active study date vs today. If studied yesterday/today, maintains/increments streak; updates `#streakBadge` and dashboard card.
   - Daily Productivity Score Algorithm:
     * Formula combining: Task completion rate (40%), Pomodoro focus hours (40%), Subject goal progress (20%).
     * Outputs 0 - 100%. Updates score badges, progress circles, and visual rating ("Productive", "On Track", "Supercharged").

6. SUBJECTS & TOPICS MANAGEMENT:
   - Render subject cards with progress bars (calculated from studied hours vs weekly target).
   - Add new subject modal and topic checklist toggles.
   - Delete / Edit subject.

7. EXAM COUNTDOWN ENGINE:
   - Calculates exact days and hours remaining for each exam.
   - Sets dynamic badge color (Red <= 3 days, Orange <= 7 days, Green > 7 days).
   - Add exam modal handler and delete exam handler.

8. PRODUCTIVITY ANALYTICS & WEEKLY BAR CHART:
   - Renders weekly study hours bar chart with dynamic heights for Mon-Sun based on logged study sessions.
   - Subject distribution breakdown percentages.
   - CSV Export function: builds CSV string of all tasks & study logs and triggers instant browser file download.

9. THEME TOGGLE (DARK / LIGHT):
   - Toggles `data-theme` attribute on `document.documentElement`.
   - Persists user choice in `localStorage`.
   - Updates icon (`🌙` / `☀️`).

10. MODAL & TOAST MANAGERS:
    - `openModal(modalId)`, `closeModal(modalId)`.
    - Close modals on clicking backdrop or press `Escape` key.
    - `showToast(message, type)`: displays smooth toast notification for 3 seconds.

════════════════════════════════════════════════════════════════
OUTPUT RULES
════════════════════════════════════════════════════════════════
- Output the COMPLETE `script.js` code.
- Write EVERY function in full. NO stubs, NO comments replacing code.
- Attach all event listeners after `DOMContentLoaded`.
"""


def coder_system_prompt() -> str:
    return "You are the Coder Agent. Produce complete, working code."