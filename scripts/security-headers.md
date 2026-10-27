# Browser security on GitHub Pages

The production site is served directly by GitHub Pages. GitHub Pages cannot
configure arbitrary HTTP response headers through repository files, so this
project deliberately does **not** create a pretend _headers file.

## Implemented (HTML-level)
- CSP in _includes/security-policy.html, loaded before any scripts.
- No executable inline scripts; configuration moved to same-origin assets/js/.
- Restrictive script/connect origins covering Google Analytics without Google
  Ads features and Microsoft Clarity; comments/Giscus only if explicitly enabled.
- Referrer policy: strict-origin-when-cross-origin.
- Built-site tests block missing/late CSP, inline JS, and inline event handlers.

The legacy archive uses inline styles, so style-src temporarily permits
'unsafe-inline'. Some historical images are remote, so img-src permits https:.
Neither permission applies to executable JavaScript.

## GitHub Pages setting to verify manually

Repository Settings -> Pages -> **Enforce HTTPS** should be selected.
This enables GitHub Pages' HTTP-to-HTTPS redirect. Check with:
  curl.exe -I http://coding.infoconex.com/
  curl.exe -I https://coding.infoconex.com/

Inspect the actual response headers for Strict-Transport-Security (HSTS).
HSTS can only be sent via HTTP response headers, not HTML meta tags. Do not
add preload or includeSubDomains at the parent domain without confirming that
*all* infoconex.com subdomains support HTTPS.

## Headers that cannot be configured here

- Strict-Transport-Security (HSTS): controlled by hosting provider.
- X-Frame-Options and CSP frame-ancestors: header-only anti-framing controls.
- X-Content-Type-Options: nosniff: header-only.
- Permissions-Policy: header-only.
- Content-Security-Policy-Report-Only: header-only.

Enforcement of these independently requires a provider/proxy able to set
HTTP response headers. They are not emulated with unsupported meta tags.

## Functional regression checks

After deployment, confirm homepage, search, theme selection, writing filter,
an archived post, and both Analytics/Clarity beacon delivery in browser DevTools.
In the console, look for CSP violations. Comments are currently disabled;
enabling them requires reassessing CSP permissions for Giscus.
