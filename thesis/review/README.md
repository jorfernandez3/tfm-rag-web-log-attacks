# Chapter review PDFs

This folder contains separate PDF files and the corresponding LaTeX source references for reviewing the thesis chapters individually.

| Chapter | PDF version | LaTeX source |
| --- | --- | --- |
| Chapter 1 - Introduction | [Open PDF](chapter_01.pdf) | [Open LaTeX](../chapters/01_introduction.tex) |
| Chapter 2 - Background and Related Work | [Open PDF](chapter_02.pdf) | [Open LaTeX](../chapters/02_background_and_related_work.tex) |
| Chapter 3 - Research Methodology | [Open PDF](chapter_03.pdf) | [Open LaTeX](../chapters/03_research_methodology.tex) |
| Chapter 4 - System Design | [Open PDF](chapter_04.pdf) | [Open LaTeX](../chapters/04_system_design.tex) |
| Chapter 5 - Dataset and Implementation | [Open PDF](chapter_05.pdf) | [Open LaTeX](../chapters/05_dataset_and_implementation.tex) |

The PDFs can be regenerated from the `thesis/` directory with:

```bash
bash build_review_chapters.sh
```

The complete thesis remains available as [`main.pdf`](../main.pdf), with its main source in [`main.tex`](../main.tex). Chapters 6-8 are not included in this review package yet because they are still being written and reviewed.
