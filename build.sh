#!/bin/sh
# Full site build: calculators/home/sitemap (gen.py) then guides + post-processing (guides_gen.py). Safe to re-run.
set -e
cd "$(dirname "$0")"
python3 gen.py
python3 guides_gen.py
node validation/rq_check.js
