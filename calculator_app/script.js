(function () {
  let expression = '';
  const display = document.getElementById('display');

  function updateDisplay(val) {
    display.textContent = val || '0';
  }

  function handleButton(value) {
    if (value === 'C') {
      expression = '';
      updateDisplay('0');
      return;
    }
    if (value === '←') {
      expression = expression.slice(0, -1);
      updateDisplay(expression || '0');
      return;
    }
    if (value === '=') {
      try {
        const result = Function('"use strict"; return (' + expression + ')')();
        expression = String(parseFloat(result.toFixed(10)));
        updateDisplay(expression);
      } catch (e) {
        updateDisplay('Error');
        expression = '';
      }
      return;
    }
    // Prevent double operators
    const operators = ['+', '-', '*', '/'];
    const lastChar = expression.slice(-1);
    if (operators.includes(value) && operators.includes(lastChar)) {
      expression = expression.slice(0, -1);
    }
    // Prevent multiple decimals in current number
    if (value === '.') {
      const parts = expression.split(/[\+\-\*\/]/);
      if (parts[parts.length - 1].includes('.')) return;
    }
    expression += value;
    updateDisplay(expression);
  }

  document.querySelectorAll('.btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      handleButton(this.dataset.value);
    });
  });

  document.addEventListener('keydown', function (e) {
    const keyMap = { Enter: '=', Escape: 'C', Backspace: '←' };
    const key = keyMap[e.key] || e.key;
    if (key === '←') {
      expression = expression.slice(0, -1);
      updateDisplay(expression || '0');
    } else if ('0123456789+-*/.='.includes(key)) {
      handleButton(key);
    }
  });
})();