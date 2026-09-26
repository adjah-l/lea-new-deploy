# Additional books

Published books currently available through the Books page:

- `interpreting-his-word.pdf` — the gated 72-page digital edition
- `interpreting-his-word-cover.png` — the website cover image
- `interpreting-his-word-cover-3d.png` — the dimensional website mockup

The Books page currently treats this title as a free digital book. It collects
a visitor's full name, email address, phone number, and selected book through
the Netlify form named `resource-access`. After a successful submission, the
page requests the matching file through a Netlify Function. Direct website
requests to the PDF are blocked by `_redirects`.

When `RESEND_API_KEY` and `RESOURCE_FROM_EMAIL` are configured in Netlify, the
function also emails the book immediately, adds the reader to Resend Contacts,
and schedules a seven-day follow-up. `RESEND_SEGMENT_ID` is optional and can be
used to group these readers for future campaigns.

Each book record has an `access` setting currently set to `free`. This preserves
a clear place to add code redemption or a purchase link later, once the sales
and Kindle paths are ready.

To add another book, copy one book card and add its title and file path
to the `resources` object near the bottom of `books.html`.
