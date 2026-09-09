# TFM Overleaf Project

LaTeX thesis and development workspace for a RAG-based LLM assistant for web
application log analysis under Prompt Injection attacks.

The repository contains the thesis source, bibliography, figures, and the
planned implementation structure. Generated LaTeX files and local datasets are
excluded through `.gitignore`.

## Main file
`main.tex`

## Compiler
Use **pdfLaTeX**. Bibliography uses **Biber** through `biblatex`.

From the repository root:

```bash
pdflatex -interaction=nonstopmode -file-line-error main.tex
biber main
pdflatex -interaction=nonstopmode -file-line-error main.tex
pdflatex -interaction=nonstopmode -file-line-error main.tex
```

Alternatively, use `latexmk` after Biber is available:

```bash
latexmk -pdf -f -interaction=nonstopmode -file-line-error main.tex
```

## Included
- Complete cleaned thesis draft
- 8 separate chapter files
- 4 appendix files
- bibliography folder
- figures folder
- title page, abstract, TOC, list of figures/tables
- Overleaf-compatible code blocks and tables

## Scope

- Web application logs only
- Synthetic clean/adversarial dataset with explicit ground truth
- RAG knowledge base with OWASP, MITRE ATT&CK, playbooks, and Prompt Injection policy
- C1-C4 experimental configurations
- Detector outputs evaluated with precision, recall, F1-score, and error rates

## Before final submission
- Adapt the cover to the official UPC/MERIT template if required.
- Add supervisor/programme information.
- Add and verify the complete literature bibliography.
- Replace `TBD` experimental results after running the experiments.
- Replace text diagrams with final figures where appropriate.
