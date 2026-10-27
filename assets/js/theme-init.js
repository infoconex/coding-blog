// Apply a known theme before the body paints; never trust arbitrary stored values.
(() => {
  try {
    const allowed = ['neo-industrial','midnight-editorial','warm-analog','technical-brutalism','swiss-engineering','terminal-modern','technical-paper','digital-garden'];
    const saved = localStorage.getItem('coding-theme');
    if (allowed.includes(saved)) document.documentElement.dataset.theme = saved;
  } catch (_) {}
})();
