# Custom domain cutover: coding.infoconex.com

This site currently publishes from the `main` branch with GitHub Pages' native Jekyll build at `https://infoconex.github.io/coding-blog/`.

Do not perform the steps below until the production site is ready to move to the historical domain.

## Before changing DNS

1. Run the source-only preflight:
   ```bash
   python scripts/custom_domain_preflight.py
   ```
   It must report no hard-coded `/coding-blog/` production links.
2. In GitHub account Pages settings, verify `infoconex.com` using GitHub's TXT-record workflow and keep the verification TXT record in DNS.
3. In this repository, open **Settings → Pages** and set the custom domain to `coding.infoconex.com` **before** pointing DNS at GitHub Pages. Because this site publishes from a branch, GitHub will create/update the root `CNAME` file.
4. Pull/retain the `CNAME` commit; do not overwrite it.

## Jekyll cutover patch

Change `_config.yml` from:

```yaml
url: "https://infoconex.github.io"
baseurl: "/coding-blog"
```

to:

```yaml
url: "https://coding.infoconex.com"
baseurl: ""
```

No post front matter or historical `permalink` value should change.

The root `CNAME` file must contain exactly:

```text
coding.infoconex.com
```

Then run:

```bash
python scripts/custom_domain_preflight.py --cutover-ready
python scripts/validate.py
```

## DNS

At the DNS provider, configure:

```text
Type: CNAME
Name/Host: coding
Target: infoconex.github.io
```

The target must not include `/coding-blog` or any repository path.

Avoid wildcard DNS records for the Pages domain.

Verify with:

```bash
dig coding.infoconex.com +nostats +nocomments +nocmd
```

DNS changes may take time to propagate.

## Post-cutover verification

After GitHub Pages reports the domain as configured:

1. Confirm `https://coding.infoconex.com/` loads the homepage.
2. Confirm representative historical URLs load unchanged, including:
   - `/post/2008/06/01/BlueQuartz-add-virus-scanning-to-sendmail`
   - `/post/2025/06/28/single-responsibility-principle-srp`
3. Confirm page canonical/OG URLs use `https://coding.infoconex.com`.
4. Confirm `/feed.xml`, `/sitemap.xml`, `/robots.txt`, `/writing/`, `/archive/`, and search all work without `/coding-blog` in generated URLs.
5. Enable **Enforce HTTPS** in Pages once GitHub makes it available.
6. Re-run the validator and custom-domain preflight.

## Rollback

If DNS or HTTPS cannot be stabilized, remove the custom domain in Settings → Pages, restore the project Pages `_config.yml` values, remove/revert `CNAME`, and restore the previous DNS record. Historical post source files do not require any rollback because their permalinks are domain-independent.
