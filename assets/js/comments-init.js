// Giscus is normally disabled; if enabled, its origin must also be in CSP.
(() => {
  const current = document.currentScript;
  const container = current?.previousElementSibling;
  if (!current || !container?.classList.contains('giscus')) return;
  const root = document.documentElement;
  const giscusOrigin = 'https://giscus.app';
  const theme = () => root.dataset.theme === 'technical-brutalism' ? 'light' : 'dark';
  function syncTheme() {
    const frame = container.querySelector('iframe.giscus-frame');
    frame?.contentWindow?.postMessage({ giscus: { setConfig: { theme: theme() } } }, giscusOrigin);
  }
  const script = document.createElement('script');
  script.src = giscusOrigin + '/client.js';
  script.async = true;
  script.crossOrigin = 'anonymous';
  const config = current.dataset;
  for (const [name, value] of Object.entries({
    repo: config.repo, 'repo-id': config.repoId, category: config.category,
    'category-id': config.categoryId, mapping: config.mapping,
    strict: '0', 'reactions-enabled': '1', 'emit-metadata': '0',
    'input-position': 'bottom', theme: theme(), lang: 'en', loading: 'lazy'
  })) script.setAttribute('data-' + name, value);
  container.appendChild(script);
  window.addEventListener('coding:themechange', syncTheme);
})();
