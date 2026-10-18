# Paper v1 frozen-result tables

Generated from committed evaluation artifacts; no evaluation is rerun by this script.

## Table 1: Mechanical held-out v2

| Method | N | Behavior | False answer | False refusal | Citation P | Citation R | Closure | Certificate |
|---|---|---|---|---|---|---|---|---|
| ordinary RAG deterministic | 250 | 0.840 | 0.160 | 0.000 | 0.306 | 0.919 | 0.000 | 0.000 |
| hybrid RAG deterministic | 250 | 0.840 | 0.160 | 0.000 | 0.298 | 0.895 | 0.000 | 0.000 |
| Self-RAG-style deterministic | 250 | 0.840 | 0.160 | 0.000 | 0.298 | 0.895 | 0.000 | 0.000 |
| rule-only | 250 | 0.316 | 0.000 | 0.684 | 1.000 | 0.186 | 1.000 | 0.000 |
| v10-full | 250 | 1.000 | 0.000 | 0.000 | 0.990 | 0.990 | 0.992 | 1.000 |
| concept-closure-v1 | 250 | 1.000 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 | 1.000 |

Claim: mechanism-level support only; labels and baselines are deterministic/mechanical.

Source: `metrics/public-paper-metrics-v1.json`; SHA-256 `aefc715a30312ffffbfb1da4379f6e7dddb9ef7206af5155933512bc328237b5`.

## Table 2: PrivacyQA v1.4 v7 one-pass gate

| Method | Behavior | False answer | False refusal | Citation micro-P |
|---|---|---|---|---|
| v4 reference | 91/147 | 16/47 | 40/100 | 0.2368 |
| v7 candidate | 72/147 | 4/47 | 71/100 | 0.1515 |

Decision: `candidate_rejected_no_v14_tuning`; the false-answer gain is offset by a false-refusal collapse.

Source: `metrics/public-paper-metrics-v1.json`; SHA-256 `aefc715a30312ffffbfb1da4379f6e7dddb9ef7206af5155933512bc328237b5`.

## Table 3: PrivacyQA relation closure P5 held-out 20

| Metric | Value |
|---|---|
| Items | 20 |
| Grounded answers | 3 |
| Answerable grounded | 3/15 |
| False grounded on no-relevant | 0 |
| No-relevant empty selected evidence | 5 |
| Selected citation precision | 1.000 |
| Grounded citations in gold | 3/3 |
| Gap certificates valid | 17/17 |
| Runtime LLM calls | 0 |
| Runtime human confirmations | 0 |

Claim: safety and certificate transfer only; coverage is a weak signal.

Source: `metrics/public-paper-metrics-v1.json`; SHA-256 `aefc715a30312ffffbfb1da4379f6e7dddb9ef7206af5155933512bc328237b5`.

## Table 4: Real standard extraction held-out negative results

| Method | Items | Exact/action match | Precision | Recall | F1 |
|---|---|---|---|---|---|
| structured relation v1 | 30 | 7/30 | 0.388889 | 0.233333 | n/a |
| scope extraction v6 | 11 | 1 action match | 0.166667 | 0.030303 | 0.051282 |

Claim: these failures justify Closure-Ready gating; they do not prove all extraction is impossible.

Source: `metrics/public-paper-metrics-v1.json`; SHA-256 `aefc715a30312ffffbfb1da4379f6e7dddb9ef7206af5155933512bc328237b5`.

## Table 5: Closure-Ready routing dev smoke v0

| Layer | N | Behavior correct | False answer | False refusal | Citation P | Unauthorized frame |
|---|---|---|---|---|---|---|
| structured_frames | 8 | 8 | 0 | 0 | 1.000 | 0 |
| passage_only | 4 | 4 | 0 | 0 | 0.750 | 0 |
| out_of_domain | 1 | 1 | 0 | 0 | 1.000 | 0 |
| overall | 13 | 13 | 0 | 0 | 0.9167 | 0 |

Claim: 13-item development smoke; mechanism viability only, not held-out or product effectiveness.

Source: `metrics/public-paper-metrics-v1.json`; SHA-256 `aefc715a30312ffffbfb1da4379f6e7dddb9ef7206af5155933512bc328237b5`.

## Claim boundary

These tables are evidence layers, not one composite leaderboard. Mechanical, public-gold, real-standard, and development-smoke results must not be mixed into a single SOTA claim.
