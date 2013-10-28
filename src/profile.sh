#!/usr/bin/env sh

python -m cProfile -o $1.prof $1.py

gprof2dot -f pstats -o $1.dot $1.prof

dot -o $1.png -Tpng $1.dot

echo "Open $1.png to view."
