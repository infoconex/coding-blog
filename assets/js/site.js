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

  function slugifyHeading(text) {
    return text
      .toLowerCase()
      .trim()
      .replace(/[^a-z0-9\s-]/g, '')
      .replace(/\s+/g, '-')
      .replace(/-+/g, '-');
  }

  function enhanceArticle() {
    const article = document.querySelector('[data-article-content]');
    if (!article) return;

    const usedIds = new Set([...document.querySelectorAll('[id]')].map((element) => element.id));
    article.querySelectorAll('h2, h3').forEach((heading, index) => {
      if (!heading.id) {
        const base = slugifyHeading(heading.textContent) || `section-${index + 1}`;
        let candidate = base;
        let suffix = 2;
        while (usedIds.has(candidate)) candidate = `${base}-${suffix++}`;
        heading.id = candidate;
        usedIds.add(candidate);
      }
      if (heading.querySelector('.heading-anchor')) return;
      const anchor = document.createElement('a');
      anchor.className = 'heading-anchor';
      anchor.href = `#${heading.id}`;
      anchor.setAttribute('aria-label', `Link to ${heading.textContent.trim()}`);
      anchor.textContent = '#';
      heading.prepend(anchor);
    });

    article.querySelectorAll('pre').forEach((pre) => {
      if (pre.closest('.code-block')?.querySelector('.code-copy') || pre.parentElement?.querySelector(':scope > .code-copy')) return;

      let container = pre.parentElement?.classList.contains('highlight') ? pre.parentElement : null;
      if (!container) {
        container = document.createElement('div');
        container.className = 'code-block';
        pre.before(container);
        container.appendChild(pre);
      }

      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'code-copy';
      button.textContent = 'Copy';
      button.setAttribute('aria-label', 'Copy code to clipboard');
      button.addEventListener('click', async () => {
        try {
          await navigator.clipboard.writeText(pre.innerText);
          button.textContent = 'Copied';
          window.setTimeout(() => { button.textContent = 'Copy'; }, 1400);
        } catch (_) {
          button.textContent = 'Select';
          const selection = window.getSelection();
          const range = document.createRange();
          range.selectNodeContents(pre);
          selection.removeAllRanges();
          selection.addRange(range);
        }
      });
      container.appendChild(button);
    });
  }

  function enhanceWritingBrowser() {
    const browser = document.querySelector('[data-writing-browser]');
    if (!browser) return;

    const cards = [...browser.querySelectorAll('[data-writing-card]')];
    const filters = [...browser.querySelectorAll('[data-topic-filter]')];
    const status = browser.querySelector('[data-writing-status]');
    const moreWrap = browser.querySelector('[data-writing-more-wrap]');
    const moreButton = browser.querySelector('[data-writing-more]');
    const pageSize = 18;
    let visibleLimit = pageSize;
    let activeTopic = new URLSearchParams(window.location.search).get('topic')?.toLowerCase().trim() || '';

    function matchingCards() {
      return cards.filter((card) => {
        if (!activeTopic) return true;
        return (card.dataset.tags || '').split('|').map((tag) => tag.trim()).includes(activeTopic);
      });
    }

    function render({ updateUrl = false } = {}) {
      const matching = matchingCards();
      cards.forEach((card) => { card.hidden = true; });
      matching.slice(0, visibleLimit).forEach((card) => { card.hidden = false; });

      filters.forEach((button) => {
        const selected = (button.dataset.topicFilter || '') === activeTopic;
        button.classList.toggle('is-active', selected);
        button.setAttribute('aria-pressed', String(selected));
      });

      if (status) {
        const label = activeTopic ? ` in “${activeTopic}”` : '';
        status.textContent = `Showing ${Math.min(visibleLimit, matching.length)} of ${matching.length} articles${label}.`;
      }

      if (moreWrap) moreWrap.hidden = matching.length <= visibleLimit;

      if (updateUrl) {
        const url = new URL(window.location.href);
        if (activeTopic) url.searchParams.set('topic', activeTopic);
        else url.searchParams.delete('topic');
        window.history.replaceState({}, '', url);
      }
    }

    filters.forEach((button) => {
      button.addEventListener('click', () => {
        activeTopic = button.dataset.topicFilter || '';
        visibleLimit = pageSize;
        render({ updateUrl: true });
      });
    });

    moreButton?.addEventListener('click', () => {
      visibleLimit += pageSize;
      render();
    });

    if (!filters.some((button) => (button.dataset.topicFilter || '') === activeTopic)) activeTopic = '';
    render();
  }

  syncOptions();
  enhanceArticle();
  enhanceWritingBrowser();
})();
