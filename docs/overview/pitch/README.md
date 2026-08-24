# Investor Deck

`investor-deck.html` — 18 slides assembled from the [overview](../README.md).
It opens in a browser, is navigated by scrolling, prints to PDF (`Ctrl+P`) and
works in both light and dark themes.

## What has to be filled in before showing it

Slide 17 contains a frame marked in the text: **round size, valuation, equity,
runway to the next round, team composition**. That is the founder's decision and
is deliberately left blank, so that no invented figures end up in the deck.

## Where the numbers come from

Every figure is taken from the overview and was reconciled against the code and
production at build time (`scripts/overview_snapshot.py`). The deck is a
**snapshot**: unlike the overview itself, it is not recalculated automatically.

So before each showing:

1. run `python3 scripts/overview_snapshot.py` and confirm the overview still
   adds up;
2. carry any changed figures into the deck by hand.

Snapshot date: **14 August 2026**.
