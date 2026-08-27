#!/usr/bin/env python3
"""Regenerate sitemap.xml from the canonical URL declared on each page.

Truthful <lastmod>: the date of the last git commit that touched the file.
Also validates that every page's rel=canonical matches the URL we emit.
Run from the repository root:  python3 tools/build-sitemap.py
"""
import glob, os, re, subprocess, sys

ORIGIN = "https://lawrenceadjah.com"
SKIP = {"index-previous.html", "404.html"}

def canonical_of(path):
    src = open(path, encoding="utf-8").read()
    m = re.search(r'<link rel="canonical" href="([^"]+)"', src)
    return m.group(1) if m else None

def lastmod_of(path):
    out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", path],
                         capture_output=True, text=True).stdout.strip()
    return out or None

def main():
    files = sorted(glob.glob("*.html")) + sorted(glob.glob("articles/*.html"))
    rows, problems = [], []
    for f in files:
        if os.path.basename(f) in SKIP:
            continue
        loc = canonical_of(f)
        if not loc:
            problems.append(f"{f}: no rel=canonical")
            continue
        if not loc.startswith(ORIGIN):
            problems.append(f"{f}: canonical points off-origin ({loc})")
            continue
        rows.append((loc, lastmod_of(f)))

    # homepage first, then the rest in canonical order
    rows.sort(key=lambda r: (r[0] != ORIGIN + "/", r[0]))

    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, mod in rows:
        out.append(f"  <url><loc>{loc}</loc>" +
                   (f"<lastmod>{mod}</lastmod>" if mod else "") + "</url>")
    out.append("</urlset>")
    open("sitemap.xml", "w", encoding="utf-8").write("\n".join(out) + "\n")

    print(f"sitemap.xml written: {len(rows)} URLs")
    for p in problems:
        print("WARN " + p, file=sys.stderr)
    return 1 if problems else 0

if __name__ == "__main__":
    sys.exit(main())
