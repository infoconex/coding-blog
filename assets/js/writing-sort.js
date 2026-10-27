(() => {
  const list = document.querySelector('[data-topic-filter-list]');
  if (!list) return;

  const allButton = list.querySelector('[data-topic-filter=""]');
  const buttons = [...list.querySelectorAll('[data-topic-filter]')].filter((button) => button !== allButton);
  const unique = new Map();

  buttons.forEach((button) => {
    const key = (button.dataset.topicFilter || '').trim().toLocaleLowerCase();
    if (!key || unique.has(key)) {
      button.remove();
      return;
    }
    unique.set(key, button);
  });

  [...unique.values()]
    .sort((a, b) => a.textContent.trim().localeCompare(b.textContent.trim(), undefined, { sensitivity: 'base' }))
    .forEach((button) => list.appendChild(button));
})();
