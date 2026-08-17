(() => {
  document.documentElement.classList.add('js');

  // Theme switching is implemented in issue #3. The persisted key is established
  // here so the production shell and the later picker share one contract.
  window.CODING_THEME_KEY = 'coding-theme';
})();
