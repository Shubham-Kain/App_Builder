(function () {
  // Load tasks from localStorage or initialize empty array
  let tasks = JSON.parse(localStorage.getItem('tasks') || '[]');
  let nextId = tasks.length ? Math.max(...tasks.map(t => t.id)) + 1 : 1;

  const taskList   = document.getElementById('task-list');
  const taskInput  = document.getElementById('task-input');
  const addBtn     = document.getElementById('add-btn');
  const taskCount  = document.getElementById('task-count');

  // Save tasks to localStorage
  function saveTasks() {
    localStorage.setItem('tasks', JSON.stringify(tasks));
  }

  // Update the counter showing number of incomplete tasks
  function updateCount() {
    const incomplete = tasks.filter(t => !t.done).length;
    taskCount.textContent = incomplete + ' task' + (incomplete !== 1 ? 's' : '') + ' remaining';
  }

  // Render the task list from the tasks array
  function renderTasks() {
    taskList.innerHTML = '';
    tasks.forEach(function (task) {
      const li   = document.createElement('li');
      li.className = 'task-item' + (task.done ? ' done' : '');
      li.dataset.id = task.id;

      const cb = document.createElement('input');
      cb.type    = 'checkbox';
      cb.id      = 'cb-' + task.id;
      cb.checked = task.done;

      const lbl = document.createElement('label');
      lbl.htmlFor = 'cb-' + task.id;
      lbl.textContent = task.text;

      const del = document.createElement('button');
      del.className   = 'delete-btn';
      del.textContent = '🗑️'; // trash icon
      del.title = 'Delete task';

      // Toggle completion
      cb.addEventListener('change', function () {
        task.done = cb.checked;
        li.classList.toggle('done', task.done);
        saveTasks();
        updateCount();
      });

      // Delete task
      del.addEventListener('click', function () {
        tasks = tasks.filter(t => t.id !== task.id);
        saveTasks();
        renderTasks();
        updateCount();
      });

      li.appendChild(cb);
      li.appendChild(lbl);
      li.appendChild(del);
      taskList.appendChild(li);
    });
    updateCount();
  }

  // Add a new task
  function addTask() {
    const text = taskInput.value.trim();
    if (!text) return;
    tasks.push({ id: nextId++, text: text, done: false });
    saveTasks();
    renderTasks();
    taskInput.value = '';
    taskInput.focus();
  }

  // Event listeners
  addBtn.addEventListener('click', addTask);
  taskInput.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') addTask();
  });

  // Initial render
  renderTasks();
})();