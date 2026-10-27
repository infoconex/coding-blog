// Clarity bootstrap in a first-party file to avoid allowing inline JavaScript.
(() => {
  const id = document.currentScript?.dataset.clarityId;
  if (!id || !/^[A-Za-z0-9]+$/.test(id)) return;
  (function (c, l, a, r, i, t, y) {
    c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); };
    t = l.createElement(r); t.async = true; t.src = 'https://www.clarity.ms/tag/' + i;
    y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y);
  })(window, document, 'clarity', 'script', id);
})();
