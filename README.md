# Evidence-Closure RAG Artifact

This is the public, metric-only artifact accompanying
`paper/paper.tex`. It contains the anonymized manuscript, bibliography,
frozen result tables, metric-only JSON, the public PrivacyQA v1.4 adapter
data, a deterministic table generator, and license notices.

## Build the paper

```bash
cd paper
pdflatex paper.tex
bibtex paper
pdflatex paper.tex
pdflatex paper.tex
```

## Regenerate the frozen-result tables

```bash
python3 scripts/generate_paper_tables_v1.py \
  --input metrics/public-paper-metrics-v1.json \
  --output paper/paper_v1_tables.md
```

## Boundary

The artifact intentionally excludes controlled standard text, private
knowledge-base archives, raw traces, internal extraction implementations,
model weights, credentials, logs, and machine-local paths. Source hashes in
the metric file identify private evaluation inputs only by generic,
anonymized names.
