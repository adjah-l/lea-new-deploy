# Photography — the one thing the redesign cannot supply

The design brief asks for **six to ten documentary photographs** on the homepage.
Exactly one photograph exists in the repository today: the studio portrait, which is
still in the hero (now visible on mobile at a 4:5 crop).

Every other photographic position on the homepage is a **plate** — a designed slot
that currently holds the table motif and a caption, so it reads as intentional rather
than broken. Drop the real photographs in and the page becomes what the brief describes.

## The shot list

| File | Where it appears | What it should be |
|---|---|---|
| `gathering-01.jpg` | Central conviction, full width (21:9) | An Our Family Dinner gathering mid-meal. Wide, warm, people mid-conversation. Not posed. |
| `pastor-01.jpg` | Chapter I · Pastor (4:3) | Preaching or teaching. Hands, posture, a congregation partly visible. |
| `builder-01.jpg` | Chapter II · Builder (4:3) | Working with a team — whiteboard, screens, an actual working session. |
| `speaker-01.jpg` | Chapter III · Speaker (4:3) | Onstage, mid-talk, with the room in frame. This is the single most valuable missing image. |
| `dinner-01.jpg` | Selected work · the anchor (5:4) | A table photographed from directly above. This is the signature image of the whole brand. |

Two more worth shooting for future use: **counseling / one-to-one conversation**, and a
**quiet portrait** in a library, church, or at a table.

## How to install one

Open `index.html`, find the plate (each is preceded by a `PHOTO SLOT` comment), and put
an `<img>` inside the existing `.plate-fill` div:

```html
<div class="plate-fill">
  <img src="images/gathering-01.jpg" alt="Guests at an Our Family Dinner gathering in Brooklyn">
</div>
```

Leave the surrounding `<figure>`, the `--plate-ratio`, and the `<figcaption>` alone —
the crop, the corner rules, and the caption styling are already handled. The motif
placeholder and its blueprint grid hide themselves automatically once an `<img>` is present.

Update the `<figcaption>` text to describe the actual photograph. Real captions
(place, occasion) are part of the field-guide voice; generic ones undo it.

## Specs

- Long edge **2000px**, JPEG, quality ~80. Keep each file under ~400KB.
- Colour: these sit next to oxblood `#742B38` and brass `#B08A4D` on ink `#101217` or
  parchment `#F2EBDD`. Warm, low-contrast, slightly desaturated frames sit best.
  Avoid anything with a strong cyan or blue cast.
- Every image needs real alt text describing what is happening, not "Lawrence Adjah".
