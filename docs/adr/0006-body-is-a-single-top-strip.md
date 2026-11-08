# The Body is a single Top strip

The v1 test print showed that the Body flexing sideways doesn't matter in use: the tea holds it. What still matters is Bowing under the Springs' own push. That push enters the Body only through the Top bars, at the top, so all the Body needs is one strip along the top that can carry it. Everything below the strip is open down to the floor. The Wall went from 21 g (v1) to about 10 g. The Top strip is 21 mm tall, which keeps a margin of about 1.5x against Bowing: it bows somewhere between about 3.4 N (ends free to pivot) and 13.7 N (ends held), against a maximum push of about 2.2 N. Its height scales with the Spring force; make the Springs stronger and it has to grow.

This partly supersedes ADR 0003: thickness stays 1.2 mm, but the Body is no longer a plain sheet.

## Considered Options

- **A thin border (2-3 mm) all round:** the top edge alone would bow at about 0.5 N.
- **A frame with a Window (top strip, 6 mm bottom strip, 3 mm side posts):** the bottom strip carried almost none of the push, because the posts were too flexible to pass it down, so it was dropped.

## Consequences

The middle is open from the floor up to 39 mm, so anything shorter than that, such as a tea bag lying flat, can slide under to the other side. If v2 bows, make TOP_STRIP taller or weaken the Springs. If it holds with margin, TOP_STRIP is the first thing to trim.

**v2 test:** the Top strip bows just under the most the user will accept. The margin is real but thin, which fits the estimate: the maximum push is about 0.65 of the ends-pivoting bowing load.
Kept as is after the v2 test (2026-11-08), knowing PLA creep could slowly add to the bend. If the bend grows past what's acceptable, make TOP_STRIP taller (25 mm cuts the bend by about 20% at the same Spring force).

**v3:** the Top strip went to 25 mm, at the user's request after v2. It now bows somewhere between about 4.1 N (ends pivoting) and 16.4 N (ends held), against the same 2.2 N maximum push. The gap under it is now 35 mm, and the Wall weighs 11.2 g.
