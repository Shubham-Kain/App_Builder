def planner_prompt(user_prompt: str) -> str:
    return f"""You are the PLANNER agent for a web app builder.

USER REQUEST: {user_prompt}

YOUR JOB: Produce a project plan for a PURE HTML/CSS/JS web app.

STRICT RULES:
1. name        → lowercase, underscores only. e.g. "calculator_app", "todo_app"
2. techstack   → always exactly "HTML, CSS, JavaScript"
3. files       → EXACTLY 3 files, always these paths:
                   index.html  (structure)
                   style.css   (all styles)
                   script.js   (all logic)
4. features    → 3-5 specific, testable features. Be concrete.
                 BAD:  "nice UI"
                 GOOD: "buttons 0-9 plus +,-,*,/ operators, = to compute, C to clear"
5. description → one sentence, plain English

EXAMPLES:
- "build a calculator"  →  name="calculator_app", features=["digit buttons 0-9",
  "operators +,-,*,/", "equals button evaluates expression", "clear button resets",
  "decimal point support"]
- "build a todo app"    →  name="todo_app", features=["text input to add tasks",
  "Add button appends task to list", "checkbox marks task complete with strikethrough",
  "Delete button removes task", "task count shown at bottom"]
"""


def architect_prompt(plan_json: str) -> str:
    return f"""You are the ARCHITECT agent. You receive a project plan and must write
the COMPLETE SOURCE CODE for every file right now — not descriptions, ACTUAL CODE.

PROJECT PLAN:
{plan_json}

YOUR JOB: For each file in the plan, produce an ImplementationTask with:
  • filepath        → exact path from the plan (e.g. "index.html")
  • task_description → one paragraph describing what the file does
  • full_code        → THE COMPLETE FILE CONTENT, ready to save as-is

════════════════════════════════════════════════════════════════
CALCULATOR REFERENCE IMPLEMENTATION (adapt for other apps)
════════════════════════════════════════════════════════════════

── index.html ──
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Calculator</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <div class="calculator">
    <div id="display" class="display">0</div>
    <div class="buttons">
      <button class="btn btn-clear" data-value="C">C</button>
      <button class="btn btn-op"    data-value="%">%</button>
      <button class="btn btn-op"    data-value="/">÷</button>
      <button class="btn btn-op"    data-value="*">×</button>
      <button class="btn btn-num"   data-value="7">7</button>
      <button class="btn btn-num"   data-value="8">8</button>
      <button class="btn btn-num"   data-value="9">9</button>
      <button class="btn btn-op"    data-value="-">−</button>
      <button class="btn btn-num"   data-value="4">4</button>
      <button class="btn btn-num"   data-value="5">5</button>
      <button class="btn btn-num"   data-value="6">6</button>
      <button class="btn btn-op"    data-value="+">+</button>
      <button class="btn btn-num"   data-value="1">1</button>
      <button class="btn btn-num"   data-value="2">2</button>
      <button class="btn btn-num"   data-value="3">3</button>
      <button class="btn btn-eq"    data-value="=" rowspan="2">=</button>
      <button class="btn btn-num btn-zero" data-value="0">0</button>
      <button class="btn btn-num"   data-value=".">.</button>
    </div>
  </div>
  <script src="script.js"></script>
</body>
</html>

── style.css ──
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  display: flex; justify-content: center; align-items: center;
  min-height: 100vh; background: #1a1a2e; font-family: 'Segoe UI', sans-serif;
}}
.calculator {{ background: #16213e; border-radius: 20px; padding: 20px; box-shadow: 0 20px 60px rgba(0,0,0,0.5); width: 320px; }}
.display {{
  background: #0f3460; color: #e0e0e0; font-size: 2.5rem; text-align: right;
  padding: 20px; border-radius: 12px; margin-bottom: 16px;
  min-height: 80px; word-break: break-all; overflow: hidden;
}}
.buttons {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }}
.btn {{
  padding: 18px; font-size: 1.2rem; border: none; border-radius: 10px;
  cursor: pointer; transition: all 0.15s ease; font-weight: 600;
}}
.btn-num  {{ background: #e94560; color: white; }}
.btn-op   {{ background: #0f3460; color: #e94560; }}
.btn-clear{{ background: #533483; color: white; grid-column: span 1; }}
.btn-eq   {{ background: #e94560; color: white; grid-column: span 2; }}
.btn-zero {{ grid-column: span 1; }}
.btn:hover {{ transform: scale(1.05); filter: brightness(1.2); }}
.btn:active{{ transform: scale(0.95); }}

── script.js ──
(function () {{
  let expression = '';
  const display = document.getElementById('display');

  function updateDisplay(val) {{
    display.textContent = val || '0';
  }}

  function handleButton(value) {{
    if (value === 'C') {{
      expression = '';
      updateDisplay('0');
      return;
    }}
    if (value === '=') {{
      try {{
        const result = Function('"use strict"; return (' + expression + ')')();
        expression = String(parseFloat(result.toFixed(10)));
        updateDisplay(expression);
      }} catch (e) {{
        updateDisplay('Error');
        expression = '';
      }}
      return;
    }}
    if (value === '%') {{
      try {{
        expression = String(parseFloat(expression) / 100);
        updateDisplay(expression);
      }} catch (e) {{
        expression = '';
        updateDisplay('0');
      }}
      return;
    }}
    // Prevent double operators
    const operators = ['+', '-', '*', '/'];
    const lastChar = expression.slice(-1);
    if (operators.includes(value) && operators.includes(lastChar)) {{
      expression = expression.slice(0, -1);
    }}
    // Prevent multiple decimals in current number
    if (value === '.') {{
      const parts = expression.split(/[\+\-\*\/]/);
      if (parts[parts.length - 1].includes('.')) return;
    }}
    expression += value;
    updateDisplay(expression);
  }}

  document.querySelectorAll('.btn').forEach(function (btn) {{
    btn.addEventListener('click', function () {{
      handleButton(this.dataset.value);
    }});
  }});

  document.addEventListener('keydown', function (e) {{
    const keyMap = {{ Enter: '=', Escape: 'C', Backspace: 'BACK' }};
    const key = keyMap[e.key] || e.key;
    if (key === 'BACK') {{
      expression = expression.slice(0, -1);
      updateDisplay(expression || '0');
    }} else if ('0123456789+-*/.%=C'.includes(key)) {{
      handleButton(key);
    }}
  }});
}})();

════════════════════════════════════════════════════════════════
TODO APP REFERENCE (adapt if user asked for a todo app)
════════════════════════════════════════════════════════════════

── index.html ──
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Todo App</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <div class="container">
    <h1>My Tasks</h1>
    <div class="input-row">
      <input type="text" id="task-input" placeholder="Add a new task…" maxlength="200">
      <button id="add-btn">Add</button>
    </div>
    <ul id="task-list"></ul>
    <div class="footer">
      <span id="task-count">0 tasks</span>
      <button id="clear-done">Clear completed</button>
    </div>
  </div>
  <script src="script.js"></script>
</body>
</html>

── style.css ──
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  font-family: 'Segoe UI', sans-serif; background: #f0f4f8;
  display: flex; justify-content: center; padding: 40px 16px;
}}
.container {{ background: white; border-radius: 16px; padding: 32px; width: 100%; max-width: 480px; box-shadow: 0 8px 32px rgba(0,0,0,0.1); }}
h1 {{ font-size: 2rem; color: #2d3748; margin-bottom: 24px; }}
.input-row {{ display: flex; gap: 8px; margin-bottom: 24px; }}
#task-input {{
  flex: 1; padding: 12px 16px; border: 2px solid #e2e8f0;
  border-radius: 8px; font-size: 1rem; outline: none;
}}
#task-input:focus {{ border-color: #667eea; }}
#add-btn, #clear-done {{
  padding: 12px 20px; background: #667eea; color: white;
  border: none; border-radius: 8px; font-size: 1rem;
  cursor: pointer; transition: background 0.2s;
}}
#add-btn:hover, #clear-done:hover {{ background: #5a67d8; }}
#task-list {{ list-style: none; display: flex; flex-direction: column; gap: 8px; }}
.task-item {{
  display: flex; align-items: center; gap: 12px; padding: 12px 16px;
  background: #f7fafc; border-radius: 8px; border: 1px solid #e2e8f0;
}}
.task-item input[type="checkbox"] {{ width: 18px; height: 18px; cursor: pointer; accent-color: #667eea; }}
.task-item label {{ flex: 1; font-size: 1rem; color: #2d3748; cursor: pointer; word-break: break-word; }}
.task-item.done label {{ text-decoration: line-through; color: #a0aec0; }}
.task-item .delete-btn {{
  background: none; border: none; color: #fc8181; font-size: 1.2rem;
  cursor: pointer; padding: 0 4px; line-height: 1;
}}
.task-item .delete-btn:hover {{ color: #e53e3e; }}
.footer {{ display: flex; justify-content: space-between; align-items: center; margin-top: 16px; font-size: 0.9rem; color: #718096; }}
#clear-done {{ padding: 8px 14px; font-size: 0.85rem; background: #fc8181; }}
#clear-done:hover {{ background: #e53e3e; }}

── script.js ──
(function () {{
  let tasks = JSON.parse(localStorage.getItem('tasks') || '[]');
  let nextId = tasks.length ? Math.max(...tasks.map(t => t.id)) + 1 : 1;

  const taskList   = document.getElementById('task-list');
  const taskInput  = document.getElementById('task-input');
  const addBtn     = document.getElementById('add-btn');
  const taskCount  = document.getElementById('task-count');
  const clearDone  = document.getElementById('clear-done');

  function saveTasks() {{
    localStorage.setItem('tasks', JSON.stringify(tasks));
  }}

  function updateCount() {{
    const done = tasks.filter(t => t.done).length;
    taskCount.textContent = tasks.length + ' task' + (tasks.length !== 1 ? 's' : '') +
      (done ? ' · ' + done + ' done' : '');
  }}

  function renderTasks() {{
    taskList.innerHTML = '';
    tasks.forEach(function (task) {{
      const li   = document.createElement('li');
      li.className = 'task-item' + (task.done ? ' done' : '');
      li.dataset.id = task.id;
      const cb   = document.createElement('input');
      cb.type    = 'checkbox';
      cb.id      = 'cb-' + task.id;
      cb.checked = task.done;
      const lbl  = document.createElement('label');
      lbl.htmlFor = 'cb-' + task.id;
      lbl.textContent = task.text;
      const del  = document.createElement('button');
      del.className   = 'delete-btn';
      del.textContent = '✕';
      del.title = 'Delete task';
      cb.addEventListener('change', function () {{
        task.done = cb.checked;
        li.classList.toggle('done', task.done);
        saveTasks();
        updateCount();
      }});
      del.addEventListener('click', function () {{
        tasks = tasks.filter(t => t.id !== task.id);
        saveTasks();
        renderTasks();
        updateCount();
      }});
      li.appendChild(cb);
      li.appendChild(lbl);
      li.appendChild(del);
      taskList.appendChild(li);
    }});
    updateCount();
  }}

  function addTask() {{
    const text = taskInput.value.trim();
    if (!text) return;
    tasks.push({{ id: nextId++, text: text, done: false }});
    saveTasks();
    renderTasks();
    taskInput.value = '';
    taskInput.focus();
  }}

  addBtn.addEventListener('click', addTask);
  taskInput.addEventListener('keydown', function (e) {{
    if (e.key === 'Enter') addTask();
  }});
  clearDone.addEventListener('click', function () {{
    tasks = tasks.filter(t => !t.done);
    saveTasks();
    renderTasks();
  }});

  renderTasks();
}})();

════════════════════════════════════════════════════════════════
RULES FOR YOUR OUTPUT
════════════════════════════════════════════════════════════════
1. full_code must be the COMPLETE file — every line, ready to save.
2. Adapt the reference above to match the user's actual request.
3. If it is NOT a calculator or todo app, invent appropriate complete code
   following the same quality standard shown above.
4. filepath must exactly match the path strings from the plan JSON.
5. Order: index.html → style.css → script.js
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