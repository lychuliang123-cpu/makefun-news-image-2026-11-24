[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/lychuliang123-cpu/makefun-news-image-2026-11-24/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/lychuliang123-cpu/makefun-news-image-2026-11-24/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

# Sum up 24 November's world news in one image

Entry for the make.fun bounty
[`news-image-20261124`](https://make.fun/bounty/news-image-20261124)
($100 USDC pool shared by the top 50; 1st $20 · 2nd $12 · 3rd $6 ·
4th–10th $2 · 11th–50th $1.20; entries close 2026-11-26 00:00 UTC /
2026-11-26 08:00 Beijing).

## How it works

- `main.py` (Python 3, standard library only) copies `news.png` to
  `/output/entry.png`. No network, no randomness — two runs write
  identical bytes.
- `news.png` is a 1024×1024 infographic (83,421 bytes, under the 1 MiB
  limit), rendered locally with PIL by `generate_image.py` from six
  24 November 2026 stories: Huang reinstated as Nvidia CEO; three
  tankers hit mines in Hormuz; Russian strike on Zaporizhzhia;
  Israeli strike kills a Hamas security chief in Gaza; COP31 talks
  collapse; South Korea's $375,000 reward for AI exam-cheating tips.
- `generate_image.py` re-renders the image deterministically
  (verified: two runs produce the same SHA-256).

## Status

Prepared 2026-11-25 ~10:30 Beijing. Not yet submitted — submission
needs the make.fun account (Google sign-in) and a public GitHub repo
owned by the entrant, plus the AI-session transcripts, per
[make.fun/skill.md](https://make.fun/skill.md).
