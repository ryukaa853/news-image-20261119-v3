# news-image-20261119-v3

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/ryukaa853/news-image-20261119-v3/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/ryukaa853/news-image-20261119-v3/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

A one-image summary of Thursday 19 November 2026's world news, drawn as
a 1024×1024 PNG broadsheet front page: the first-ever Trump–Xi–Putin
trilateral in Shenzhen, the ICJ's genocide verdict against Myanmar,
GTA VI's record launch, Anthropic's $81.3bn IPO, a missile strike on
Riyadh's PIF Tower, and the Gaza raid ending as Ukraine hit the Crimean
Bridge again.

This is v3: a fresh design drawn from scratch, not a reskin of v2. The
hero now shows the three leaders seated at the round table under their
flags; every one of the six stories carries its own drawn scene (the
court with its 9–6 verdict badge, the GTA VI sunset skyline, the IPO
chart, the tower under a missile arc, the tank past the Yellow Line
beside the bridge under fire); headlines are larger and decks shorter,
so the page still reads when shrunk to ~300 pixels. The facts were
re-verified against live reporting on 20 November 2026 and corrected
where v2 hedged: the leaders themselves called their statement a
"Peace Declaration", the GTA VI figures are Sensor Tower estimates, and
the Gaza raid began on 18 November and was concluded on 19 November.

## Stories in the image

1. **Trump, Xi and Putin meet for the first time** — 90 minutes at a
   round table in Kylin Villa, Shenzhen; a joint statement the leaders
   called a "Peace Declaration": a nuclear war "cannot be won and must
   never be fought". (USA Today, The Times, Reuters)
2. **Myanmar guilty of genocide** — the ICJ ruled 9–6 that Myanmar
   committed genocide against the Rohingya in 2017, the first time the
   court has ever held a state responsible. (Human Rights Watch, CNN,
   Le Monde)
3. **GTA VI smashes every record** — launched at midnight; an estimated
   $2.36bn and 24.6m copies on day one, the biggest entertainment
   launch ever. (Sensor Tower estimates via NotebookCheck, CNN)
4. **The biggest IPO ever** — Anthropic raised a record $81.3bn at $83
   a share; "ANT" opened at $111.50 and closed up 17% at $97.17.
   (WSJ, Reuters)
5. **Missile hits Riyadh tower** — a Houthi missile struck the
   80-storey PIF Tower, blowing out windows on 7–8 floors. No
   injuries. (Reuters, WSJ)
6. **Raid ends; bridge hit again** — Israel concluded its first tank
   raid past Gaza's Yellow Line since the October 2025 truce; Ukraine
   struck the Crimean Bridge again. (Reuters, BBC)

## How it is built

`draw.py` draws the whole page with Pillow (Noto Serif / Noto Sans),
deterministically: no network, no clock, no randomness — two runs
write byte-identical PNGs. `main.py` copies the shipped `entry.png`
to `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR`).

    python3 draw.py            # regenerate entry.png
    MAKEFUN_OUTPUT_DIR=out python3 main.py   # copy it to out/entry.png
