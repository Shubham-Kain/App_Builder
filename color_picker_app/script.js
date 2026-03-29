(function () {
  const preview   = document.getElementById('color-preview');
  const hexInput  = document.getElementById('hex-input');
  const copyBtn   = document.getElementById('copy-btn');
  const resetBtn  = document.getElementById('reset-btn');
  const redSlider = document.getElementById('red');
  const greenSlider = document.getElementById('green');
  const blueSlider = document.getElementById('blue');
  const redVal   = document.getElementById('red-val');
  const greenVal = document.getElementById('green-val');
  const blueVal  = document.getElementById('blue-val');
  const presetPanel = document.getElementById('preset-panel');

  // 12 preset colors
  const presets = [
    '#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF',
    '#FFA500', '#800080', '#A52A2A', '#000000', '#FFFFFF', '#C0C0C0'
  ];

  // Utility: convert 0‑255 to two‑digit hex
  function componentToHex(c) {
    const hex = c.toString(16);
    return hex.length === 1 ? '0' + hex : hex;
  }

  // RGB → Hex
  function rgbToHex(r, g, b) {
    return '#' + componentToHex(r) + componentToHex(g) + componentToHex(b);
  }

  // Hex → RGB object {r,g,b}
  function hexToRgb(hex) {
    // Strip leading # if present
    hex = hex.replace(/^#/, '');
    if (hex.length === 3) {
      // expand shorthand form (e.g. #FFF)
      hex = hex.split('').map(ch => ch + ch).join('');
    }
    const num = parseInt(hex, 16);
    return {
      r: (num >> 16) & 0xFF,
      g: (num >> 8) & 0xFF,
      b: num & 0xFF
    };
  }

  // Update UI from RGB slider values
  function updateFromRGB() {
    const r = parseInt(redSlider.value, 10);
    const g = parseInt(greenSlider.value, 10);
    const b = parseInt(blueSlider.value, 10);
    redVal.textContent   = r;
    greenVal.textContent = g;
    blueVal.textContent  = b;
    const hex = rgbToHex(r, g, b);
    preview.style.backgroundColor = hex;
    hexInput.value = hex;
    // Update active preset highlight
    updatePresetActive(hex);
  }

  // Update UI from a hex string
  function updateFromHex(hex) {
    if (!/^#?[0-9a-fA-F]{3}$|^#?[0-9a-fA-F]{6}$/.test(hex)) return;
    const rgb = hexToRgb(hex);
    redSlider.value   = rgb.r;
    greenSlider.value = rgb.g;
    blueSlider.value  = rgb.b;
    redVal.textContent   = rgb.r;
    greenVal.textContent = rgb.g;
    blueVal.textContent  = rgb.b;
    preview.style.backgroundColor = hex;
    hexInput.value = hex;
    updatePresetActive(hex);
  }

  // Highlight the preset swatch that matches the current color
  function updatePresetActive(currentHex) {
    const swatches = presetPanel.querySelectorAll('.preset-swatch');
    swatches.forEach(sw => {
      sw.classList.toggle('active', sw.dataset.hex.toUpperCase() === currentHex.toUpperCase());
    });
  }

  // Build preset swatches
  function buildPresets() {
    presetPanel.innerHTML = '';
    presets.forEach(col => {
      const sw = document.createElement('div');
      sw.className = 'preset-swatch';
      sw.style.backgroundColor = col;
      sw.dataset.hex = col;
      sw.title = col;
      sw.addEventListener('click', () => updateFromHex(col));
      presetPanel.appendChild(sw);
    });
    // Initially none active (white is in presets, will be highlighted)
    updatePresetActive('#FFFFFF');
  }

  // Event listeners
  redSlider.addEventListener('input', updateFromRGB);
  greenSlider.addEventListener('input', updateFromRGB);
  blueSlider.addEventListener('input', updateFromRGB);

  hexInput.addEventListener('input', (e) => {
    const val = e.target.value.trim();
    if (val === '') return;
    updateFromHex(val);
  });

  copyBtn.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(hexInput.value);
      copyBtn.textContent = 'Copied!';
      setTimeout(() => { copyBtn.textContent = 'Copy'; }, 1500);
    } catch (err) {
      console.error('Clipboard write failed', err);
      copyBtn.textContent = 'Failed';
      setTimeout(() => { copyBtn.textContent = 'Copy'; }, 1500);
    }
  });

  resetBtn.addEventListener('click', () => {
    redSlider.value   = 255;
    greenSlider.value = 255;
    blueSlider.value  = 255;
    updateFromRGB();
  });

  // Initialise
  buildPresets();
  updateFromRGB(); // set initial state (white)
})();