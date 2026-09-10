#!/usr/bin/env bash

set -euo pipefail

thesis_dir="$(cd "$(dirname "$0")" && pwd)"
review_dir="$thesis_dir/review"
cd "$thesis_dir"

mkdir -p "$review_dir"
rm -f "$review_dir"/chapter_0{1,2,3}.{aux,bbl,bcf,blg,fls,log,out,pdf,run.xml,toc,lof,lot,synctex.gz}

for chapter in 01 02 03; do
  pdflatex \
    -interaction=nonstopmode \
    -halt-on-error \
    -output-directory="$review_dir" \
    -jobname="chapter_$chapter" \
    "$review_dir/chapter_$chapter.tex"
  biber "$review_dir/chapter_$chapter"
  pdflatex \
    -interaction=nonstopmode \
    -halt-on-error \
    -output-directory="$review_dir" \
    -jobname="chapter_$chapter" \
    "$review_dir/chapter_$chapter.tex"
  pdflatex \
    -interaction=nonstopmode \
    -halt-on-error \
    -output-directory="$review_dir" \
    -jobname="chapter_$chapter" \
    "$review_dir/chapter_$chapter.tex"
done

rm -f "$review_dir"/chapter_0{1,2,3}.{aux,bbl,bcf,blg,fls,log,out,run.xml,toc,lof,lot,synctex.gz}

printf 'Review PDFs created in %s\n' "$review_dir"
ls -lh "$review_dir"/chapter_0{1,2,3}.pdf
