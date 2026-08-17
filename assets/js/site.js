(() => {
  const root = document.documentElement;
  const key = 'coding-theme';
  const allowed = new Set(['neo-industrial', 'midnight-editorial', 'warm-analog', 'technical-brutalism']);
  const picker = document.querySelector('[data-theme-picker]');
  const trigger = document.querySelector('[data-theme-trigger]');
  const panel = document.querySelector('[data-theme-panel]');
  const closeButton = document.querySelector('[data-theme-close]');
  const options = [...document.querySelectorAll('[data-theme-option]')];

  root.classList.add('js');
  window.CODING_THEME_KEY = key;

  function currentTheme() {
    return allowed.has(root.dataset.theme) ? root.dataset.theme : 'neo-industrial';
  }

  function syncOptions() {
    const current = currentTheme();
    options.forEach((option) => {
      option.setAttribute('aria-checked', String(option.dataset.themeOption === current));
    });
  }

  function setTheme(theme) {
    if (!allowed.has(theme)) return;
    root.dataset.theme = theme;
    try { localStorage.setItem(key, theme); } catch (_) {}
    syncOptions();
  }

  function openPicker() {
    if (!panel || !trigger) return;
    panel.hidden = false;
    trigger.setAttribute('aria-expanded', 'true');
    syncOptions();
    const selected = options.find((option) => option.getAttribute('aria-checked') === 'true');
    (selected || options[0])?.focus();
  }

  function closePicker({ restoreFocus = true } = {}) {
    if (!panel || !trigger) return;
    panel.hidden = true;
    trigger.setAttribute('aria-expanded', 'false');
    if (restoreFocus) trigger.focus();
  }

  trigger?.addEventListener('click', () => panel.hidden ? openPicker() : closePicker());
  closeButton?.addEventListener('click', () => closePicker());

  options.forEach((option) => {
    option.addEventListener('click', () => {
      setTheme(option.dataset.themeOption);
      closePicker();
    });
    option.addEventListener('keydown', (event) => {
      if (!['ArrowDown', 'ArrowRight', 'ArrowUp', 'ArrowLeft'].includes(event.key)) return;
      event.preventDefault();
      const index = options.indexOf(option);
      const delta = ['ArrowDown', 'ArrowRight'].includes(event.key) ? 1 : -1;
      options[(index + delta + options.length) % options.length].focus();
    });
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && panel && !panel.hidden) closePicker();
    if (event.key.toLowerCase() === 't' && !event.metaKey && !event.ctrlKey && !event.altKey && !/input|textarea|select/i.test(document.activeElement?.tagName || '')) {
      event.preventDefault();
      panel?.hidden ? openPicker() : closePicker();
    }
  });

  document.addEventListener('pointerdown', (event) => {
    if (panel && !panel.hidden && picker && !picker.contains(event.target)) closePicker({ restoreFocus: false });
  });

  syncOptions();
})();
