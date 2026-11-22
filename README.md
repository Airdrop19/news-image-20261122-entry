# Sum up 22 November's world news in one image — entry

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/Airdrop19/news-image-20261122-entry/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/Airdrop19/news-image-20261122-entry/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

Entry for the make.fun bounty [Sum up 22 November's world news in one image](https://make.fun/bounty/news-image-20261122).

`main.py` (Python 3.13, standard library only, no network) copies `entry.png` to `/output/entry.png`: a front page of 23 stories reported on Sunday 22 November 2026, led by COP31 ending with no deal in Antalya.

`build_image.py` draws the image with Pillow from headlines of that day.

## Run locally

```bash
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Competition window (from kit)

- Opens: 2026-11-22T00:00:00Z
- Deadline: 2026-11-24T00:00:00Z
- Gate: PNG or JPEG, at most 1 MiB, at most 1024 by 1024 pixels; the program runs twice and both runs must write the same bytes.
