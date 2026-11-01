# Refaire la notice

1. `python3 caps.py fr` (puis en, es, pt, de, it) : prend les captures d'écran du logiciel dans `img/<langue>/`.
2. `PDFDUO_ROOT=../.. python3 gen.py` : produit `docs/notice/notice-<langue>.html` et `.pdf`, et copie les PDF dans `pdfduo/notices/`.

Textes : `texts.py` (sections) et `figs.py` (légendes des captures et repères numérotés).
Il faut PySide6, PyMuPDF et Playwright (`pip install playwright && playwright install chromium`).
