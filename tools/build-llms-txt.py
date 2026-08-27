#!/usr/bin/env python3
"""Regenerate llms.txt from each page's own <title>, description and canonical.

Keeps the curated directory truthful and in sync with the pages themselves.
Run from the repository root:  python3 tools/build-llms-txt.py
"""
import glob, html, re, sys

ORDER = ['index.html', 'about.html', 'books.html', 'the100marriagebook.html',
         'the-100-marriage-arranged.html', 'audiobook.html', 'speaking.html',
         'request.html', 'sermons.html', 'articles.html', 'projects.html',
         'partner.html', 'press.html', 'media.html']

def meta(f):
    s = open(f, encoding='utf-8').read()
    t = html.unescape(re.sub(r'\s*(&mdash;|—)\s*Lawrence E\. Adjah\s*$', '',
                             re.search(r'<title>(.*?)</title>', s, re.S).group(1)).strip())
    d = html.unescape(re.search(r'<meta name="description" content="([^"]*)"', s).group(1))
    c = re.search(r'<link rel="canonical" href="([^"]+)"', s).group(1)
    return t, d, c

L = ["# Lawrence E. Adjah", "",
     "> Pastor, social entrepreneur, author and speaker based in Dallas, Texas. Founder and "
     "CEO of the Family Dinner Foundation. Author of The 100 Marriage and narrator of "
     "Lawrence E. Adjah Reads the Bible: NIV. This file lists the canonical pages of "
     "lawrenceadjah.com so they can be read directly rather than inferred.", "",
     "All URLs below are canonical and extensionless. The machine-readable index is "
     "https://lawrenceadjah.com/sitemap.xml.", "",
     "## Core pages", ""]
for f in ORDER:
    t, d, c = meta(f)
    L.append(f"- [{t}]({c}): {d}")

L += ["", "## Articles", ""]
for f in sorted(glob.glob('articles/*.html')):
    t, d, c = meta(f)
    L.append(f"- [{t}]({c}): {d}")

L += ["", "## Related organizations", "",
      "- [Family Dinner Foundation](https://ourfamilydinner.org/): the organization Lawrence "
      "founded and leads as Founder and CEO; canonical source for its programs and impact.",
      "- [5C Mutual Care Framework](https://ourfamilydinner.org/5c-mutual-care-framework/): the "
      "definitive description of the framework. lawrenceadjah.com summarizes it and links here "
      "rather than duplicating it.",
      "- [The 100 Marriage Assessment](https://the100marriage.lawrenceadjah.com/): the "
      "compatibility assessment underneath the book and the arranged marriage process.", "",
      "## Independent coverage", "",
      "- [‘Our Family Dinner’ Unites Young Professionals For Social Gathering and Family-Style "
      "Dinners](https://www.blackenterprise.com/our-family-dinner-unites-young-professionals-for-social-gathering-and-family-style-dinners/) "
      "— Black Enterprise, 21 August 2015",
      "- [BE Modern Man: Lawrence Adjah](https://www.blackenterprise.com/be-modern-man-lawrence-adjah/) "
      "— Black Enterprise",
      "- [‘We’re not built to do life alone,’ says Our Family Dinner founder]"
      "(https://www.chicagotribune.com/2016/03/01/were-not-built-to-do-life-alone-says-our-family-dinner-founder/) "
      "— Chicago Tribune, 1 March 2016",
      "- [Mental health event at Wayne State to focus on issues facing Black men]"
      "(https://www.freep.com/story/news/health/2023/10/27/mental-health-event-at-wayne-state-to-focus-on-issues-facing-black-men/71333723007/) "
      "— Detroit Free Press, 27 October 2023",
      "- [Building Bridges in the Divided States of America]"
      "(https://www.bushcenter.org/catalyst/profiles-in-pluralism/building-bridges-in-the-divided-states-of-america) "
      "— George W. Bush Presidential Center", ""]

open('llms.txt', 'w', encoding='utf-8').write("\n".join(L) + "\n")
print(f"llms.txt written: {len(ORDER)} core pages, {len(glob.glob('articles/*.html'))} articles")
