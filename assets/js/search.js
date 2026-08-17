(() => {
  const trigger = document.querySelector('[data-search-trigger]');
  const overlay = document.querySelector('[data-search-overlay]');
  const dialog = overlay?.querySelector('.search-dialog');
  const input = overlay?.querySelector('[data-search-input]');
  const close = overlay?.querySelector('[data-search-close]');
  const status = overlay?.querySelector('[data-search-status]');
  const results = overlay?.querySelector('[data-search-results]');
  if (!trigger || !overlay || !input || !results) return;

  let index = null;
  let activeIndex = -1;
  let lastFocus = null;

  const searchUrl = trigger.dataset.searchIndex;

  function normalize(value) {
    return (value || '').toString().toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g, '');
  }

  async function loadIndex() {
    if (index) return index;
    if (status) status.textContent = 'Loading search index…';
    const response = await fetch(searchUrl, { credentials: 'same-origin' });
    if (!response.ok) throw new Error(`Search index request failed: ${response.status}`);
    index = await response.json();
    if (status) status.textContent = `Search ${index.length} archived articles.`;
    return index;
  }

  function scoreArticle(article, tokens) {
    const title = normalize(article.title);
    const description = normalize(article.description);
    const tags = normalize((article.tags || []).join(' '));
    const body = normalize(article.body);
    let score = 0;
    for (const token of tokens) {
      if (!token) continue;
      if (title.includes(token)) score += 20;
      if (tags.includes(token)) score += 12;
      if (description.includes(token)) score += 7;
      if (body.includes(token)) score += 2;
      if (!title.includes(token) && !tags.includes(token) && !description.includes(token) && !body.includes(token)) return 0;
    }
    return score;
  }

  function render(query) {
    const cleaned = normalize(query).trim();
    results.innerHTML = '';
    activeIndex = -1;
    if (!cleaned) {
      if (status) status.textContent = index ? `Search ${index.length} archived articles.` : 'Type to search the full archive.';
      return;
    }

    const tokens = cleaned.split(/\s+/).filter(Boolean);
    const matches = index
      .map((article) => ({ article, score: scoreArticle(article, tokens) }))
      .filter((entry) => entry.score > 0)
      .sort((a, b) => b.score - a.score || String(b.article.date).localeCompare(String(a.article.date)))
      .slice(0, 12);

    if (status) status.textContent = matches.length ? `${matches.length} best matches.` : 'No matching articles.';
    if (!matches.length) {
      results.innerHTML = '<div class="search-empty">No results. Try a technology, concept, title, or phrase.</div>';
      return;
    }

    matches.forEach(({ article }, i) => {
      const link = document.createElement('a');
      link.className = 'search-result';
      link.href = article.url;
      link.setAttribute('role', 'option');
      link.dataset.searchResult = '';
      const tags = Array.isArray(article.tags) ? article.tags.slice(0, 3).join(' · ') : '';
      link.innerHTML = `
        <div>
          <h3></h3>
          <p></p>
          <div class="search-result__meta"></div>
        </div>
        <span class="search-result__arrow" aria-hidden="true">↗</span>`;
      link.querySelector('h3').textContent = article.title || 'Untitled';
      link.querySelector('p').textContent = article.description || 'Archived engineering note.';
      link.querySelector('.search-result__meta').textContent = [article.date, tags].filter(Boolean).join(' · ');
      link.addEventListener('mouseenter', () => setActive(i));
      results.appendChild(link);
    });
  }

  function resultLinks() {
    return [...results.querySelectorAll('[data-search-result]')];
  }

  function setActive(next) {
    const links = resultLinks();
    if (!links.length) return;
    activeIndex = (next + links.length) % links.length;
    links.forEach((link, i) => {
      const active = i === activeIndex;
      link.classList.toggle('is-active', active);
      link.setAttribute('aria-selected', String(active));
    });
    links[activeIndex].scrollIntoView({ block: 'nearest' });
  }

  async function openSearch() {
    lastFocus = document.activeElement;
    overlay.hidden = false;
    trigger.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
    input.focus();
    try {
      await loadIndex();
      render(input.value);
    } catch (_) {
      if (status) status.textContent = 'Search index could not be loaded.';
      results.innerHTML = '<div class="search-empty">Search is temporarily unavailable.</div>';
    }
  }

  function closeSearch() {
    overlay.hidden = true;
    trigger.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
    activeIndex = -1;
    if (lastFocus instanceof HTMLElement) lastFocus.focus();
  }

  trigger.addEventListener('click', openSearch);
  close?.addEventListener('click', closeSearch);
  input.addEventListener('input', () => index && render(input.value));
  overlay.addEventListener('pointerdown', (event) => {
    if (event.target === overlay) closeSearch();
  });

  document.addEventListener('keydown', (event) => {
    const commandK = event.key.toLowerCase() === 'k' && (event.metaKey || event.ctrlKey);
    if (commandK) {
      event.preventDefault();
      overlay.hidden ? openSearch() : closeSearch();
      return;
    }
    if (overlay.hidden) return;
    if (event.key === 'Escape') {
      event.preventDefault();
      closeSearch();
    } else if (event.key === 'ArrowDown') {
      event.preventDefault();
      setActive(activeIndex + 1);
    } else if (event.key === 'ArrowUp') {
      event.preventDefault();
      setActive(activeIndex - 1);
    } else if (event.key === 'Enter' && activeIndex >= 0) {
      event.preventDefault();
      resultLinks()[activeIndex]?.click();
    } else if (event.key === 'Tab' && dialog) {
      const focusable = [...dialog.querySelectorAll('button,input,a[href]')].filter((el) => !el.hidden);
      if (!focusable.length) return;
      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    }
  });
})();
