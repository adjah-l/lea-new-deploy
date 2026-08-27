# lawrenceadjah.com

Source for the canonical website of Lawrence E. Adjah — pastor, social entrepreneur,
author and speaker, founder of the [Family Dinner Foundation](https://ourfamilydinner.org/).

**Live site:** <https://lawrenceadjah.com>

This repository is the single source of truth for the site. Any other host serving
this content (including the legacy Squarespace property) is a legacy version being
retired, not an alternate canonical.

## Architecture

A static site deployed on Netlify. There is no build step — the HTML in this
repository is what ships.

| Path | Role |
|---|---|
| `index.html`, `about.html`, … | The 13 top-level pages. Each is a Design Component page: an `<x-dc>` template hydrated at runtime by `support.js`. |
| `articles/*.html` | The 13 essays. Plain static HTML with no runtime dependency. |
| `support.js`, `image-slot.js` | Generated runtime. **Do not hand-edit** — see the header comment in each file. |
| `assets/` | Images, logos, and the canonical bio PDF. |
| `_redirects` | Netlify routing: clean-URL rewrites, `.html` consolidation, legacy aliases. |
| `sitemap.xml` | Generated. Run `python3 tools/build-sitemap.py`. |
| `llms.txt` | Curated directory of canonical URLs for answer engines. |
| `404.html` | Branded not-found page. |
| `index-previous.html` | Archived prior homepage. `noindex`; not linked. |

### Runtime and progressive enhancement

`support.js` loads React from a public CDN and mounts the `<x-dc>` template. Because
that is an external dependency, every hydrated page also ships a static
`#la-fallback` block containing the page's identity text and its links. It is hidden
the moment JavaScript runs and restored if the runtime has not mounted within six
seconds, so the page never renders empty and its links stay in the served HTML.

## URL rules

One canonical, extensionless URL per resource.

- Link internally to `/about`, never `/about.html` or `about.html`.
- Article links are `/articles/<slug>`.
- Every page carries a self-referencing `rel="canonical"`.
- Aliases resolve in a single hop; no chains, and no `.html` final URLs.

## Local validation

```sh
python3 -m http.server 8899          # serve; open http://localhost:8899/index.html
python3 tools/build-sitemap.py       # regenerate sitemap.xml, verify canonicals
```

After deploying, confirm redirects at the edge:

```sh
curl -sI https://lawrenceadjah.com/about.html | head -2   # expect 301 -> /about
curl -sI https://lawrenceadjah.com/about      | head -1   # expect 200
```

## Content ownership

Copyright © 2026 Lawrence E. Adjah. All rights reserved.

Content, images, design and copy are his. This repository is public so the
deployed site can be read, audited and referenced — that is not a grant of any
licence or reuse right. See [LICENSE](LICENSE).

Contact: <la@lawrenceadjah.com>
