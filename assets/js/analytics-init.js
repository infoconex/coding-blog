// Keep Analytics configuration in a first-party file so CSP can block inline JS.
(() => {
  const id = document.currentScript?.dataset.measurementId;
  if (!id || !/^G-[A-Za-z0-9]+$/.test(id)) return;
  window.dataLayer = window.dataLayer || [];
  window.gtag = function () { window.dataLayer.push(arguments); };
  window.gtag('js', new Date());
  window.gtag('config', id);
})();
