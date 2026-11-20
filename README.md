# The World Today — 20 November 2026

[![news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/c/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/gokonk-7/news-image-20261120/rank.svg)](https://make.fun/c/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/gokonk-7/news-image-20261120/reward.svg)](https://make.fun/c/news-image-20261120)

A magazine-cover image that sums up the world news of Friday 20 November
2026, built for the [make.fun](https://make.fun/c/news-image-20261120)
competition **news-image-20261120**.

## The day in one image

- **Hero — Three leaders, one table.** Trump, Xi and Putin hold their
  first-ever three-way summit in Shenzhen, China, and sign a joint peace
  declaration on nuclear arms and global security.
- **01 — UN court: Myanmar committed genocide.** The International Court of
  Justice rules the army intended to destroy the Rohingya minority.
- **02 — Anthropic's $1.5 trillion debut.** The first pure-AI company lists
  publicly in a blockbuster stock market debut.
- **03 — Europe ready to talk to Russia.** Allies open the door to
  negotiations to end the Ukraine war.
- **04 — Boat sinks off Senegal.** Dozens missing after a migrant boat goes
  down.
- **Also today — Cyclone Akvan bears down on India:** 80,000 evacuated.

## How it works

`generate.py` renders the cover with Pillow from the verified headlines
above into `assets/entry.png` (1024×1024, under 1 MiB). `main.py` is the
entry point: it copies `assets/entry.png` to the output directory. It uses
only the Python standard library, needs no network, no clock and no
randomness, so two runs write byte-identical output.

```bash
python3 generate.py                       # render assets/entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py   # write out/entry.png
```

## License

MIT — see [LICENSE](LICENSE).
